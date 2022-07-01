# =============================================================================
# Bokeh app focusing on record efficiencies
# 
# By Jesper Jacobsson
# 2019 06
# =============================================================================

#%% Imports
from dateutil.relativedelta import relativedelta
import datetime
import os
import pathlib
import time

from bokeh.events import ButtonClick
from bokeh.layouts import column, row
from bokeh.models import BooleanFilter
from bokeh.models import Button
from bokeh.models import CDSView
from bokeh.models import CheckboxButtonGroup
from bokeh.models import ColumnDataSource
from bokeh.models import CustomJS
from bokeh.models import Div
from bokeh.models import IndexFilter
from bokeh.models import Legend, LegendItem
from bokeh.models import LinearColorMapper
from bokeh.models import MultiSelect
from bokeh.models import OpenURL
from bokeh.models import Panel
from bokeh.models import RangeSlider
from bokeh.models import Range1d
from bokeh.models import Select
from bokeh.models import Slider
from bokeh.models import TapTool
from bokeh.models import TextInput
from bokeh.models import DataTable, TableColumn, NumberFormatter
from bokeh.models.widgets import Paragraph
from bokeh.plotting import figure
from bokeh.transform import factor_cmap, factor_mark
import numpy as np
import pandas as pd

from UtilityFunctions.categoricalColors import categoricalColors
from UtilityFunctions.utilityFunctions import (conectToDatabase,
    convertNumerListToFloats,
    databaseCategoriesMostCommon,
    databaseCatagoriesUnique,
    database_details,
    dataManipulation,
    integerList,
    is_number,
    loadData,
    toolTipsDict,
    toolTipsMap)


#%% helper functions
def getAppInstructions(fileName = 'Instructions.txt'):
    '''Read in text file with instructions'''

    #The file shoud be placed in the same folder as the main script
    path = pathlib.Path(__file__).parent.absolute()

    # Read file
    filePath = os.path.join(path, fileName)
    with open(filePath, 'r') as f:
        appInstructions = f.read()

    return appInstructions

def dataColumnsToUse():
    ''' Returns a list of the data columns the app will use'''
    return    ['Backcontact_stack_sequence',
               'Cell_architecture',
               'Cell_area_measured',
               'Cell_stack_sequence',
               'Cell_flexible',
               'Cell_semitransparent',
               'Encapsulation',
               'ETL_additives_compounds',
               'ETL_deposition_procedure',
               'ETL_stack_sequence',
               'HTL_additives_compounds',
               'HTL_deposition_procedure',
               'HTL_stack_sequence',
               'JV_certified_values',
               'JV_default_FF',
               'JV_default_FF_scan_direction',
               'JV_default_Jsc',
               'JV_default_Jsc_scan_direction',
               'JV_default_PCE',
               'JV_default_PCE_scan_direction',
               'JV_default_Voc',
               'JV_default_Voc_scan_direction',
               'JV_light_intensity',
               'Module',
               'Module_number_of_cells_in_module',
               'Module_area_effective',
               'Module_area_total',
               'Perovskite_additives_compounds',
               'Perovskite_band_gap',
               'Perovskite_composition_a_ions',                                       
               'Perovskite_composition_b_ions',                                           
               'Perovskite_composition_c_ions', 
               'Perovskite_composition_inorganic',
               'Perovskite_composition_leadfree',
               'Perovskite_composition_long_form',
               'Perovskite_composition_short_form',
               'Perovskite_composition_perovskite_ABC3_structure',          
               'Perovskite_composition_perovskite_inspired_structure', 
               'Perovskite_deposition_aggregation_state_of_reactants',
               'Perovskite_deposition_number_of_deposition_steps',
               'Perovskite_deposition_quenching_induced_crystallisation',
               'Perovskite_deposition_quenching_media',
               'Perovskite_deposition_quenching_media_additives_compounds',
               'Perovskite_deposition_procedure',
               'Perovskite_deposition_solvents',
               'Perovskite_deposition_solvent_annealing',
               'Perovskite_deposition_synthesis_atmosphere',
               'Perovskite_dimension_0D',
               'Perovskite_dimension_2D',
               'Perovskite_dimension_2D3D_mixture',
               'Perovskite_dimension_3D',
               'Perovskite_dimension_3D_with_2D_capping_layer',
               'Perovskite_single_crystal',
               'Ref_DOI_number',
               'Ref_ID',
               'Ref_lead_author',
               'Ref_publication_date',
               'Stabilised_performance_measured',
               'Substrate_stack_sequence']

def dataColumnsToUseFromTheStart():
    '''Defines the initial set of data columns'''
    return   ['JV_default_PCE',
              'Ref_ID',
              'Ref_DOI_number',
              'Ref_publication_date',
              ]

def make_plot(source, data, view, alphaValue, booleanCategory, colorLabels, legendCategory, legendFontSize, markerSize, newPlotWidth, tooltips, useColorMarkers, yAxisLogStart, y_axis, y_scale_select):
    ''' Generat the plot'''

    TOOLS = "box_select, box_zoom, hover, lasso_select, pan, reset, save, tap, wheel_zoom"    
    TOOLTIPS = tooltips

    # Initiate figure
    p = figure(plot_width   = newPlotWidth, 
                plot_height  = 800,
                tools        = TOOLS,
                tooltips     = TOOLTIPS,
                toolbar_location = 'above',
                x_axis_type = 'datetime',
                y_axis_type= y_scale_select,
                output_backend = "webgl")

    # List of posible marker types
    markerSet = []
    if useColorMarkers: 
        markerSet = ['hex_dot', 'circle', 'diamond', 'square', 'triangle', 'circle_cross', 'diamond_cross', 'square_cross', 'triangle_dot', 'circle_dot', 'diamond_dot', 'square_dot', 'circle_x', 'square_pin', 'inverted_triangle', 'plus', 'circle_y', 'square_x', 'triangle_pin']
    else:
        markerSet = ['hex_dot']

    #%% Generate the figure
    # If there is a legend category
    if legendCategory != 'none':
        # Import a colormap for categorical ploting in the form of a list of 61 hex values
        colorSet = categoricalColors('Dark')

        # Ensure that the color palet is large enough by cycling it
        if len(colorLabels) > len(colorSet):
            n = int(len(colorLabels)/len(colorSet)) + 1
            colorSet = colorSet*(n)

        # Ensure that the marker palet is large enough by cycling it
        if len(colorLabels) > len(markerSet):
            n = int(len(colorLabels)/len(markerSet)) + 1
            markerSet = markerSet*(n)   
        
        GlyphRenderer = p.scatter(x = 'Ref_publication_date', y = y_axis[1], source = source, view = view,
                size = markerSize, alpha = alphaValue, line_alpha = 1,
                marker = factor_mark(legendCategory, markers=markerSet, factors=colorLabels),
                color = factor_cmap(legendCategory, palette=colorSet, factors=colorLabels),
                hover_color="red")
        
        # Add an emty legend
        p.add_layout(Legend())


    # If data should be coloured by boolean category
    elif booleanCategory != 'none':
        # Import a colormap for categorical ploting in the form of a list of 61 hex values
        color_mapper = LinearColorMapper(palette=['darkgrey', "slateblue"], low=0, high=1)

        GlyphRenderer = p.scatter(x = 'Ref_publication_date', y = y_axis[1], source = source, view = view,
                size = markerSize, alpha = alphaValue, line_alpha = 1,
                marker = 'hex_dot',
                color={'field': booleanCategory, 'transform': color_mapper},
                hover_color="red")

        # Add an emty legend
        p.add_layout(Legend())

    # If no category to color by
    else:
        GlyphRenderer = p.scatter(x = 'Ref_publication_date', y = y_axis[1], source = source, view = view,
                    marker = 'hex_dot', size = markerSize, 
                    alpha = alphaValue, line_alpha = 1,
                    color = "slateblue", hover_color="red")
 
    # Title and axis labels
    p.yaxis.axis_label = y_axis[0]
    p.xaxis.axis_label = 'Publication date'
        
    if y_scale_select == 'log':
        p.y_range=Range1d(10**yAxisLogStart, 1.02*max(data[y_axis[1]]))
    else:
        p.y_range=Range1d(0, 1.02*max(data[y_axis[1]]))

    p.x_range=Range1d(pd.to_datetime('2009-01-01'), max(source.data['Ref_publication_date']) + relativedelta(months=3))

    # Enable that a tap on a point links to the article's URL (based on the DOI number)
    url = "https://doi.org/@Ref_DOI_number"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    return p, GlyphRenderer

def style(p, fontSize = 14):
    ''' Provide basic styling '''

    # Convert given font sizes to strings
    size1 = str(fontSize) + 'pt'
    size2 = str(fontSize + 4) + 'pt'

    # Title and axis labels
    p.title.text = "The Perovskite Database Project. " + datetime.datetime.today().strftime('%Y-%m-%d')
    #p.title_location = "right"
    p.title.align = "left"
    p.title.text_font_size = "8pt"
    p.title.text_font_style = 'italic'

    # Axis titles
    p.xaxis.axis_label_text_font_size = size1
    p.xaxis.axis_label_text_font_style = 'bold'
    p.yaxis.axis_label_text_font_size = size1
    p.yaxis.axis_label_text_font_style = 'bold'

    # Tick labels
    p.xaxis.major_label_text_font_size = size1
    p.yaxis.major_label_text_font_size = size1
        
    # The outer box
    p.outline_line_width = 1
    p.outline_line_color = "black"

    return p   

def tableColumnsForSelectedData():
    '''Defines and returns structure for a data table'''
    tableColumns = [
        TableColumn(field='Ref_ID', title='Database ID', width = 70),
        TableColumn(field='Ref_DOI_number', title='DOI', width = 250),
        TableColumn(field='Ref_lead_author', title='Lead author', width = 120),
        TableColumn(field='JV_default_Voc', title='Voc [V]', formatter=NumberFormatter(format="0.00"), width = 50),
        TableColumn(field='JV_default_Jsc', title='Jsc [mA/cm^2]', formatter=NumberFormatter(format="0.00"), width = 75),
        TableColumn(field='JV_default_FF', title='FF', formatter=NumberFormatter(format="0.00"), width = 50),
        TableColumn(field='JV_default_PCE', title='PCE [%]', formatter=NumberFormatter(format="0.00"), width = 50),
        TableColumn(field='Cell_architecture', title='Architecture', width = 70),
        TableColumn(field="Cell_stack_sequence", title="Stack", width = 700),
        TableColumn(field='Cell_area_measured', title='Area [cm^2]', width = 60),
        TableColumn(field='Perovskite_composition_long_form', title='Perovskite', width = 400),
        TableColumn(field="Perovskite_band_gap", title="Band gap [eV]", formatter=NumberFormatter(format="0.00"), width = 90),
        TableColumn(field='Perovskite_additives_compounds', title='Perovskite additives', width = 150),  
        TableColumn(field="Perovskite_deposition_procedure", title="Perovskite deposition", width = 400)]

    return tableColumns

#%% The interactive engine
def interactiveEngine():
    '''The main function that generates the the plot, the controlls, the callbacks, and specifies the layout '''
    # Internal helper functions
    def download_Data_via_Json():
        '''Activate the dummy glyph that trigers java script for downloading data '''
        download_trigger.text = str(int(download_trigger.text) + 1)    
 
    def downloadDataTable(event):
        '''Download selected data in table as .csv-file '''

        # Fetch table and scheema names of the database
        bd_details = database_details()
        table = bd_details['table']
        schema = bd_details['schema']
        ID = bd_details['bd_key']

        # The Ref_ID for all selected cells
        #Cell_ID_numbers = source.data['Ref_ID']

        Cell_ID_numbers = list(mainDataFrame.loc[global_selectedRows]['Ref_ID'])

        # Format the Cell_ID_numbers for the SQL query
        IDnumbersString = [str(x) for x in Cell_ID_numbers]
        IDnumbersString = '(' + ','.join(IDnumbersString) + ')'

        # Query the database for all data for the selected cells
        query = f'''select * from {schema}.{table} where {table}."{ID}" in {IDnumbersString}'''
        query_results = pd.read_sql_query(sql = query, con = engine)

        # Download results
        if len(query_results) != 0:

            # Make the data accesible to download
            callback.args['userFilename'] = 'Perovsite database query.csv' 
            callback.args['data'] = query_results.to_csv(header=True, index=False)

            # Activate the dummy glyph that trigers java script for downloading data 
            download_Data_via_Json()
 
    def downloadFigureAndMetadata(event):
        '''Download figure metadata '''
        # Generate the metadata
        text = generateFigureMataData()

        # Make the data accesible to download
        callback.args['userFilename'] = 'Figure metadata.csv' 
        callback.args['data'] = text

        # Activate the dummy glyph that trigers java script for downloading data 
        download_Data_via_Json()

    def generateFigureMataData():
        '''Generate metadata for the figure and stor it in a text string'''

        # Values for all input controlls and filters
        filters1 = dict(zip([checkBoxButtons[item].labels[0] for item in list(checkBoxButtons.keys())],
                                    [checkBoxButtons[item].active for item in list(checkBoxButtons.keys())]))

        filters2 = dict(zip([checkBoxButtonsPlotProperties[item].labels[0] for item in list(checkBoxButtonsPlotProperties.keys())],
                                    [checkBoxButtonsPlotProperties[item].active for item in list(checkBoxButtonsPlotProperties.keys())]))    

        filters3 = dict(zip([multiselects[item].title for item in list(multiselects.keys())],
                                    [multiselects[item].value for item in list(multiselects.keys())]))

        filters4 = dict(zip([multiselectsShort[item].title for item in list(multiselectsShort.keys())],
                                    [multiselectsShort[item].value for item in list(multiselectsShort.keys())]))

        filters5 = dict(zip([selects[item].title for item in list(selects.keys())],
                                    [selects[item].value for item in list(selects.keys())]))

        filters6 = dict(zip([rangeSliders[item].title for item in list(rangeSliders.keys())],
                                    [rangeSliders[item].value for item in list(rangeSliders.keys())]))

        filters7 = dict(zip([sliders[item].title for item in list(sliders.keys())],
                                    [sliders[item].value for item in list(sliders.keys())]))

        #filters8 = dict(zip([daterangeSliders[item].title for item in list(daterangeSliders.keys())],
        #                            [daterangeSliders[item].value for item in list(daterangeSliders.keys())]))

        filters9 = dict(zip([textInputControlls[item].title for item in list(textInputControlls.keys())],
                                    [textInputControlls[item].value for item in list(textInputControlls.keys())]))

        # Put everything together in a dictionary
        figureMetadata = {'checkBoxButtons' : filters1,
                          'checkBoxButtonsPlotProperties' : filters2,
                          'multiselects' : filters3,
                          'multiselectsShort' : filters4,
                          'selects' : filters5,
                          'rangeSliders' : filters6,
                          'sliders' : filters7,
                          #'daterangeSliders' : filters8,
                          'textInputControlls' : filters9,
                          }

        # Return a strin greprecentation of the dicttionary
        return str(figureMetadata)
 
    def getNewDataColumnsToDownload():
        '''Returns a list of datacolumns that should be downloaded'''        
        # List of datacolumns
        activeDataColumns = []

        #%% Extract all filters selected that require data
        # Active Checkboxbutton grups
        activeDataColumns += [item for item in checkBoxButtons if checkBoxButtons[item].active != []]

        # Multiselects
        activeDataColumns += [item for item in multiselects if multiselects[item].value != ['All']]
        activeDataColumns += [item for item in multiselectsShort if multiselectsShort[item].value != ['All']]

        # Selects
        if booleanCategory_map[selects['booleanCategory'].value] != 'none':
            activeDataColumns += [booleanCategory_map[selects['booleanCategory'].value]]

        if legendCategory_map[selects['legendCategory'].value] != 'none':
            activeDataColumns += [legendCategory_map[selects['legendCategory'].value]]

        #activeDataColumns += [x_axis_map[selects['x_axis'].value]]
        activeDataColumns += [y_axis_map[selects['y_axis'].value]]

        # Range sliders
        activeDataColumns += [item for item in rangeSliders if rangeSliders[item].value != sliderLimits[item]]

        # Hoover tools
        hovertools = toolTipsDict()
        activeDataColumns += [hovertools[item] for item in hoverToolSelect.value]

        # Generate list of new categories
        newCategories = [item for item in activeDataColumns if item not in list(mainDataFrame.columns)]

        return newCategories
 
    def select_data(data):
        '''Start by selecting all data and succesivly narrow it down'''

        # Categories in dataset so far fetched from the database
        presentDataCategories = list(data.columns)

        # Filter out nan values in the categories that should be plotted (nan values have previously been set to -1)
        data = data[data[y_axis_map[selects['y_axis'].value]] != -1]
        #data = data[data[x_axis_map[selects['x_axis'].value]] != -1]

       #%% Checkboxbuttongroups
        # For each active filter, sucessivly sort out entries where those values are True
        for category in checkBoxButtons:
            if category in presentDataCategories:
                if 0 in checkBoxButtons[category].active:
                    data = data[data[category] == True]

        #%% Multiselects long
        for category in multiselects:
            if category in presentDataCategories:
                if 'All' not in multiselects[category].value:
                    data = data[data[category].isin(multiselects[category].value)]

        #%% Multiselects short
        for category in multiselectsShort:
            if category in presentDataCategories:
                if 'All' not in multiselectsShort[category].value:
                    data = data[data[category].isin(multiselectsShort[category].value)]

        #%% Sliders
        for category in rangeSliders:
            if category in presentDataCategories:
                if rangeSliders[category].value[0] > sliderLimits[category][0] or rangeSliders[category].value[1] < sliderLimits[category][1]:
                    data = data[(data[category] > rangeSliders[category].value[0]) & (data[category] < rangeSliders[category].value[1])]

        #%% Text input
        if 'Ref_ID' in presentDataCategories: 
            if textInputControlls['excludeCellID'].value != '':
                ID_to_drop = integerList(textInputControlls['excludeCellID'].value)
                data = data[~data['Ref_ID'].isin(ID_to_drop)]

        #%% Filtering out the records
        # Add a temporary column with the cumulative max of the PCE (or other category)
        # Requires that the the dataframe is sorted
        # To prevent that values are set on a slize of the dataframe a copy is made
        data = data.copy() 

        # Resort the data
        data.sort_values(by=['Ref_publication_date', y_axis_map[selects['y_axis'].value]], inplace=True)

        data['cummax'] = data[y_axis_map[selects['y_axis'].value]].cummax()

        # Only keep the records
        data = data.drop_duplicates('cummax', keep = 'first')

        # Remove the temporay column
        data = data.drop(columns = ['cummax'])

        # Only keep one record per publication date (the last one which will be the highest)
        data = data.drop_duplicates('Ref_publication_date', keep = 'last')

        return data

    def update():
        ''' Uppdate the data selection'''   
        # Read in more data from the database if nessesary
        columnsToDownload = getNewDataColumnsToDownload()
        updateMainDataFrame(columnsToDownload)

        # Uppdate the selection of data to plot based on the filters selected by the user
        newSelectionOfData = select_data(mainDataFrame)
 
        # Uppdate the column data source with the new data selection (older solution. takes a lot of time)
        updateSource(categories = list(newSelectionOfData.columns))

        #updateSourceNew(data = newSelectionOfData)
        #source.data = newSelectionOfData.to_dict('series')

        # Update the list of indicies for the selected data so that it can be accessed by remaining internal functions
        global_selectedRows.clear()
        global_selectedRows.extend(list(newSelectionOfData.index))

        ## Uppdate the view of the columnDataSource
        ID_list = list(newSelectionOfData['Ref_ID'])
        booleans = [True if ID in ID_list else False for ID in source.data['Ref_ID']]
        view.filters = [BooleanFilter(booleans)]

        # Update and add the legend (if the figure is defined and if it has a legend)
        if global_figure != []:
            if len(global_figure[0].legend) != 0: 
                updateLegend()
 
    def updateDataTable(event):
        '''Uppdate the column data source feeding data to the datatable'''

        # START WAINTING SPINNER

        # Columns that should be in the table
        tableColumns = [item.field for item in tableColumnsForSelectedData()]

        # Columns already downloaded
        downloadedColumns = list(mainDataFrame.columns)

        # Columns to download
        newColmns = list(set(tableColumns).difference(downloadedColumns))

        # Update the mainDataFram with the catagorise that should be in the table
        if len(newColmns) > 0:
            updateMainDataFrame(newColmns)

        # Generte a dataframe with the currenlty selected data 
        dataSelection = mainDataFrame.loc[global_selectedRows]

        # Uppdate the columnDataSource responsible for the datatabel with the currently selected data
        sourceDataTable.data = dataSelection.to_dict('series')

    def updateLegend():
        '''Update the legend '''
        # Fetch the desired state of the legend
        booleanCategory = booleanCategory_map[selects['booleanCategory'].value]
        legendCategory = legendCategory_map[selects['legendCategory'].value]
        legendFontSize = sliders['legendFontSize'].value

        # Fetch handels to the current figure
        p = global_figure[0]
        GlyphRenderer = global_GlyphRenderer[0]

        # If there is a legend category
        if legendCategory != 'none':
            # Define the complete set of legend lables and sort those based on how common they are. That is, all unique entries in the legendCategory
            legendLabelsComplete = global_legendLabelsComplete

            # The current selection of data in the plot         
            dataSelection = mainDataFrame.loc[global_selectedRows,[legendCategory]]

            # Define the set of legend labels in the reduced dataset in the current figure where there is data 
            categoriesWithData = list(dataSelection[legendCategory].unique())

            # Sort legendLabels based on frequence in the total dataset
            legendLabels = [x for x in legendLabelsComplete if x in categoriesWithData]

            # Find the index in the data source for the first occurance of each legendLabel
            LegendIndex = dict.fromkeys(legendLabels)
            dataSelectionList = dataSelection[legendCategory].tolist()
            for item in legendLabels:
                LegendIndex[item] = dataSelectionList.index(item)

            # Define the LegendItems for each category in the current figure
            legendEntries = []
            for item in legendLabels:
                legendEntries.append(LegendItem(label=item, index=LegendIndex[item], renderers=[GlyphRenderer]))

            # Add an emty legend if no legend already excist
            if len(p.legend) == 0:
                p.add_layout(Legend())

            # Add the legend to the figure p 
            p.add_layout(p.legend[0], 'right')    
            p.legend.items =  legendEntries  
            p.legend.label_text_font_size = str(legendFontSize) + 'pt'
            p.legend.spacing = 0
            p.legend.label_width = 250
            
        # If there is a bolean category but no legend category
        elif booleanCategory != 'none':
            # The current selection of data in the plot         
            dataSelection = mainDataFrame.loc[global_selectedRows,[booleanCategory]]

            #selected_ID = source.data['Ref_ID']
            #dataSelection = mainDataFrame.loc[selected_ID,[booleanCategory]]

            # Define the set of legend labels in the reduced dataset in the current figure where there is data 
            legendLabels = list(dataSelection[booleanCategory].unique())

            # Find the index in the data source of the first occurance of each legendLabel
            LegendIndex = dict.fromkeys(legendLabels)
            dataSelectionList = dataSelection[booleanCategory].tolist()
            for item in legendLabels:
                LegendIndex[item] = dataSelectionList.index(item)

            # Define the LegendItems for each category in the current figure
            legendEntries = []
            for item in legendLabels:
                legendEntries.append(LegendItem(label=str(item), index=LegendIndex[item], renderers=[GlyphRenderer]))

            # Add an emty legend if no one legend already excist
            if len(p.legend) == 0:
                p.add_layout(Legend())

            # Add the legend to the figure p
            p.add_layout(p.legend[0], 'right')    
            p.legend.items =  legendEntries  
            p.legend.label_text_font_size = str(legendFontSize) + 'pt'
            p.legend.spacing = 0
            p.legend.label_width = 50

    def updateMainDataFrame(newCategories):
        '''Reads in more data from the database if a filter has been selected that needs that data for filtering'''

        #%% Get new data from the database and add to the mainDataFrame
        if len(newCategories) > 0:
        # Add the ID column and remove dublets
            newCategories.append('Ref_ID')
            newCategories = set(newCategories)
     
            # Read in new data
            newData = loadData(dataColumns = newCategories, engine = engine)

            # Do data cleaning
            newData = dataManipulation(newData)

            # Merge data to mainDataFrame's index column
            mergedDataFrame = pd.DataFrame(mainDataFrame['Ref_ID']).join(newData.set_index('Ref_ID'), on='Ref_ID')

            # Add all new columns to the mainDataFrame. The reson that this not is done in the previous line is that we must add to the old datafram and not create a new one if we should be able to directly use it in subfunctions
            newCategories.remove('Ref_ID')

            for category in newCategories:
                mainDataFrame[category] = newData[category]
     
    def updatePlot():
        '''Generated the plots'''
        # Check which color markers that should be used
        useColorMarkers = False
        if 0 in checkBoxButtonsPlotProperties['MarkerSymbols'].active:
            useColorMarkers = True
        else:
            useColorMarkers = False

        # determin the desired width of the figure depending if there is a legend or not
        booleanCategory = booleanCategory_map[selects['booleanCategory'].value]
        legendCategory = legendCategory_map[selects['legendCategory'].value]
 
        # determin the desired widht of the figure depending if there is a legend or not
        if legendCategory == 'none' and booleanCategory == 'none':            
            newPlotWidth = 800
        elif legendCategory == 'none':
            newPlotWidth = 950
        else:
            newPlotWidth = 1000         

        # Tool tips
        hoverTools_map = toolTipsMap()
        tooltips = [hoverTools_map[tips] for tips in hoverToolSelect.value]
 
        
        # Define the complete set of legend lables and sort those based on how common they are. That is, all unique entries in the legendCategory
        if legendCategory != 'none':
            #selected_ID = source.data['Ref_ID']
            #dataSelection = mainDataFrame.loc[selected_ID,[legendCategory]]
            global_legendLabelsComplete.clear()
            global_legendLabelsComplete.extend(list(mainDataFrame[legendCategory].value_counts().index))
        elif booleanCategory != 'none':
            global_legendLabelsComplete.clear()
            global_legendLabelsComplete.extend(['True', 'False'])
        else:
            global_legendLabelsComplete.clear()

        # Initiate the figure
        p, GlyphRenderer = make_plot(source = source, data = mainDataFrame.loc[global_selectedRows], 
                  view = view,
                  alphaValue = sliders['plotAlpha'].value,
                  booleanCategory = booleanCategory,
                  colorLabels = global_legendLabelsComplete,
                  legendCategory = legendCategory,
                  legendFontSize = sliders['legendFontSize'].value,
                  markerSize = sliders['markerSize'].value,
                  newPlotWidth = newPlotWidth,
                  tooltips = tooltips,
                  useColorMarkers = useColorMarkers,
                  yAxisLogStart = sliders['yAxisLogStart'].value,
                  y_axis = (selects['y_axis'].value, y_axis_map[selects['y_axis'].value]),
                  y_scale_select = y_scale_select_map[selects['y_scale_select'].value],
                  )

        # Set the styling for the plot
        p = style(p, fontSize = sliders['fontSize'].value,)

        # Update the global list of figures and glyphrenderes
        global_figure.clear()
        global_figure.append(p)
        global_GlyphRenderer.clear()
        global_GlyphRenderer.append(GlyphRenderer)

        # Update the legend (if there should be a legend)
        updateLegend()

        return global_figure[0]

    def updatePlotCategories():
        '''Uppdate the categories to plot, i.e. PCE, Voc, Jsc, FF '''
        # Resort the data 
        #mainDataFrame.sort_values(by=['Ref_publication_date', y_axis_map[selects['y_axis'].value]], inplace=True)

        # Update the data
        update()

        # Uppdate the plot
        p_new = updatePlot()

        # Insert the updated plot in the layout
        layout_tab1.children[1] = p_new
    
    def updateSource(categories):
        '''Update the column data source if needed'''
        # If the x-axis, or the y-axis or the hover tools are change, more data may need to be added to the source

        excistingCategories = source.column_names

        # The x-axis
        #x_axis = x_axis_map[selects['x_axis'].value] 
        #if x_axis not in excistingCategories:
        #    source.data[x_axis] = mainDataFrame[x_axis]

        # The y-axis
        y_axis = y_axis_map[selects['y_axis'].value] 
        if y_axis not in excistingCategories:
            source.data[y_axis] = mainDataFrame[y_axis]

        # The booleanCategory
        booleanCategory = booleanCategory_map[selects['booleanCategory'].value]
        if booleanCategory != 'none':
            if booleanCategory not in excistingCategories:
                source.data[booleanCategory] = mainDataFrame[booleanCategory]

        # The legendCategory
        legendCategory = legendCategory_map[selects['legendCategory'].value]
        if legendCategory != 'none':
            if legendCategory not in excistingCategories:
                source.data[legendCategory] = mainDataFrame[legendCategory]

        # Hoover tool tips
        hovertools = toolTipsDict()
        for category in [hovertools[item] for item in hoverToolSelect.value]:
            if category not in excistingCategories:
                source.data[category] = mainDataFrame[category]

    def updateSourceNew(data):
        '''Update the column data source '''
        categories_to_source = []

        # Database ID
        categories_to_source.append('Ref_ID')

        # The x-axis
        categories_to_source.append('Ref_publication_date') 
        #source.data['Ref_publication_date'] = data['Ref_publication_date']

        # The y-axis
        y_axis = y_axis_map[selects['y_axis'].value]
        categories_to_source.append(y_axis)
        #source.data[y_axis] = data[y_axis]

        # The booleanCategory
        booleanCategory = booleanCategory_map[selects['booleanCategory'].value]
        if booleanCategory != 'none':
            #source.data[booleanCategory] = data[booleanCategory]
            categories_to_source.append(booleanCategory)

        # The legendCategory
        legendCategory = legendCategory_map[selects['legendCategory'].value]
        if legendCategory != 'none':
            categories_to_source.append(legendCategory)
            #source.data[legendCategory] = data[legendCategory]

        # Hoover tool tips
        hovertools = toolTipsDict()
        for category in [hovertools[item] for item in hoverToolSelect.value]:
            categories_to_source.append(category)
            #source.data[category] = data[category]

        # Remove dublicates
        categories_to_source = list(set(categories_to_source))

        newData = data[categories_to_source]

        source.data = { name : [] for name in list(newData.columns) }
        source.data = newData.to_dict('series')


    #%% Main function #######################################################
    #%% Initial setup
    # Set up a conection to the database
    engine = conectToDatabase()

    # Read in data needed for the initial plot
    mainDataFrame = loadData(dataColumns = dataColumnsToUseFromTheStart(), engine = engine)

    # Ensure proper formating of the data
    mainDataFrame = dataManipulation(mainDataFrame)

    # Sort data by publication date, and by PCE for each date
    mainDataFrame.sort_values(by=['Ref_publication_date', 'JV_default_PCE'], inplace = True)

    # Main ColumnDataSource. 
    source = ColumnDataSource(data=dict())
    source.data = mainDataFrame.to_dict('series')

    # Set up a view conected to the main column data source
    view = CDSView(source=source)
    
    # Set up ColumnDataSources for tables
    sourceDataTable = ColumnDataSource()
    #sourceLassoSelect = ColumnDataSource()
    
    # Global lists to keep track of selected data, current figures, and legend, and to provide access to those in sub functions
    global_selectedRows = []
    global_figure = []
    global_GlyphRenderer = []
    global_legendLabelsComplete = []

    #%% Read in text instructions about the app to be shown in a separate tab
    appInstructions = getAppInstructions(fileName = 'Instructions.html')

    #%% Input controlls ####################################################
    #%% Buttons
    buttons = {
        'donwload_data_button' : Button(label="Download data in table as a .csv file", button_type="success"),
        'update_data_table_button' : Button(label="Update data in tabel", button_type="success"),
        'donwload_figure_button' : Button(label="Download figure metadata"),
    }

    #%% checkBoxButtons
    checkBoxButtons = {    
        'Cell_flexible' : CheckboxButtonGroup(labels = ['Flexible cell'], active = []),
        'Cell_semitransparent' : CheckboxButtonGroup(labels = ['Transparent cell'], active = []),
        'Encapsulation' : CheckboxButtonGroup(labels = ['Encapsulated cell'], active = []),
        'JV_certified_values' : CheckboxButtonGroup(labels = ['Externaly certified JV data'], active = []), 
        'Module' : CheckboxButtonGroup(labels = ['Modules'], active = []),
        'Perovskite_composition_inorganic' : CheckboxButtonGroup(labels = ['Inorganic perovskite'], active = []),
        'Perovskite_composition_leadfree' : CheckboxButtonGroup(labels = ['Lead free perovskite'], active = []),
        'Perovskite_composition_perovskite_ABC3_structure' : CheckboxButtonGroup(labels = ['Perovskite crystal structure'], active = []),
        'Perovskite_composition_perovskite_inspired_structure' : CheckboxButtonGroup(labels = ['Perovskite inspired structure'], active = []),
        'Perovskite_deposition_solvent_annealing' : CheckboxButtonGroup(labels = ['Solvent annealing of the Perovskite'], active = []),
        'Perovskite_deposition_quenching_induced_crystallisation' : CheckboxButtonGroup(labels = ['Antisolvent method'], active = []),
        'Perovskite_dimension_0D' : CheckboxButtonGroup(labels = ['Perovskite. 0D (QDs)'], active = []),
        'Perovskite_dimension_2D' : CheckboxButtonGroup(labels = ['Perovskite. 2D'], active = []),
        'Perovskite_dimension_2D3D_mixture' : CheckboxButtonGroup(labels = ['Perovskite. 2D/3D mixture'], active = []),
        'Perovskite_dimension_3D' : CheckboxButtonGroup(labels = ['Perovskite. 3D'], active = []),
        'Perovskite_dimension_3D_with_2D_capping_layer' : CheckboxButtonGroup(labels = ['Perovskite. 3D with 2D capping layer'], active = []),
        'Perovskite_single_crystal' : CheckboxButtonGroup(labels = ['Perovskite. Single crystal'], active = []),
        'Stabilised_performance_measured' : CheckboxButtonGroup(labels = ['Stabilised performance measured'], active = []),
    }
    checkBoxButtonsPlotProperties = {
        'MarkerSymbols' : CheckboxButtonGroup(labels = ['Separate color by marker type'], active = []),
        }

    #%% Data table
    data_table = DataTable(source=sourceDataTable, columns=tableColumnsForSelectedData(), width=2500, height=800, scroll_to_selection=True, editable=True)

    #%% Multiselects    
    multiselectCategories = [
        'Backcontact_stack_sequence',
        'ETL_additives_compounds',
        'ETL_deposition_procedure',
        'ETL_stack_sequence',
        'HTL_additives_compounds',
        'HTL_deposition_procedure',
        'HTL_stack_sequence',
        'Perovskite_additives_compounds',
        'Perovskite_composition_short_form',
        'Perovskite_deposition_aggregation_state_of_reactants',
        'Perovskite_deposition_procedure',
        'Perovskite_deposition_quenching_media',
        'Perovskite_deposition_quenching_media_additives_compounds',
        'Perovskite_deposition_solvents',
        'Perovskite_deposition_synthesis_atmosphere',
        'Substrate_stack_sequence',
        ]

    multiselectCategories_short =  [
        'Backcontact_stack_sequence',
        'Cell_architecture',
        'ETL_stack_sequence',
        'HTL_stack_sequence',
        'Perovskite_additives_compounds',
        'Perovskite_composition_short_form',
        'Perovskite_deposition_procedure',
        'Substrate_stack_sequence',
        ]

    # Generate alphabetic lists of all alternatives in the database for each multiselect category 
    multiselectDict = {}
    for i, item in enumerate(multiselectCategories):
        multiselectDict[item] = databaseCatagoriesUnique(column = item, engine = engine)
        multiselectDict[item] = [str(i) for i in multiselectDict[item]]
        multiselectDict[item].insert(0, 'All') 

    # Generate alphabetic lists of the {number} most common alternatives in the database for each multiselect category 
    multiselectDictShort = {}
    numberOfMostComonAlternatives = 30
    for i, item in enumerate(multiselectCategories_short):
        multiselectDictShort[item] = databaseCategoriesMostCommon(column = item, number = numberOfMostComonAlternatives, engine = engine)
        multiselectDictShort[item] = [str(i) for i in multiselectDictShort[item]]
        multiselectDictShort[item].insert(0, 'All') 

    # Multiselects
    multiselects = {
        'Backcontact_stack_sequence' : MultiSelect(title="Back contact", value=['All'], options = multiselectDict['Backcontact_stack_sequence'], size = 50),
        'ETL_additives_compounds' : MultiSelect(title="ETL additives/doping", value=['All'], options = multiselectDict['ETL_additives_compounds'], size = 22),
        'ETL_deposition_procedure' : MultiSelect(title="ETL deposition procedure", value=['All'], options = multiselectDict['ETL_deposition_procedure'], size = 22),
        'ETL_stack_sequence' : MultiSelect(title="ETL stack", value=['All'], options = multiselectDict['ETL_stack_sequence'], size = 50, width = 450),
        'HTL_additives_compounds' : MultiSelect(title="HTL additives/doping", value=['All'], options = multiselectDict['HTL_additives_compounds'], size = 22),
        'HTL_deposition_procedure' : MultiSelect(title="HTL deposition procedure", value=['All'], options = multiselectDict['HTL_deposition_procedure'], size = 22),
        'HTL_stack_sequence' : MultiSelect(title="HTL stack", value=['All'], options = multiselectDict['HTL_stack_sequence'], size = 50, width=1100),
        'Perovskite_additives_compounds' : MultiSelect(title="Perovskite additives", value=['All'], options = multiselectDict['Perovskite_additives_compounds'], size = 50, width = 450),
        'Perovskite_composition_short_form' : MultiSelect(title="Perovskite", value=['All'], options = multiselectDict['Perovskite_composition_short_form'], size = 50),
        'Perovskite_deposition_aggregation_state_of_reactants' : MultiSelect(title="Perovskite. Aggregation state of reactants", value=['All'], options = multiselectDict['Perovskite_deposition_aggregation_state_of_reactants'], size = 22),
        'Perovskite_deposition_procedure' : MultiSelect(title="Perovskite deposition procedure", value=['All'], options = multiselectDict['Perovskite_deposition_procedure'], size = 50, width = 500),
        'Perovskite_deposition_quenching_media' : MultiSelect(title="Perovskite. Quenching media", value=['All'], options = multiselectDict['Perovskite_deposition_quenching_media'], size = 22),
        'Perovskite_deposition_quenching_media_additives_compounds' : MultiSelect(title="Quenching media additives", value=['All'], options = multiselectDict['Perovskite_deposition_quenching_media_additives_compounds'], size = 22),
        'Perovskite_deposition_solvents' : MultiSelect(title="Perovskite. Solvent", value=['All'], options = multiselectDict['Perovskite_deposition_solvents'], size = 50),
        'Perovskite_deposition_synthesis_atmosphere' : MultiSelect(title="Perovskite. Syntesis atmosphere", value=['All'], options = multiselectDict['Perovskite_deposition_synthesis_atmosphere'], size = 22),
        'Substrate_stack_sequence' : MultiSelect(title="Substrate", value=['All'], options = multiselectDict['Substrate_stack_sequence'], size = 50, width = 300),
    }

    multiselectsShort = {
        'Backcontact_stack_sequence' : MultiSelect(title="Back contact", value=['All'], options = multiselectDictShort['Backcontact_stack_sequence'], size = 6),
        'Cell_architecture' : MultiSelect(title="Cell_architecture", value=['All'], options = multiselectDictShort['Cell_architecture'], size = 3),       
        'ETL_stack_sequence' : MultiSelect(title="ETL stack", value=['All'], options = multiselectDictShort['ETL_stack_sequence'], size = 6),
        'HTL_stack_sequence' : MultiSelect(title="HTL stack", value=['All'], options = multiselectDictShort['HTL_stack_sequence'], size = 6),
        'Perovskite_additives_compounds' : MultiSelect(title="Perovskite additives", value=['All'], options = multiselectDictShort['Perovskite_additives_compounds'], size = 6),
        'Perovskite_composition_short_form' : MultiSelect(title="Perovskite", value=['All'], options = multiselectDictShort['Perovskite_composition_short_form'], size = 6),
        'Perovskite_deposition_procedure' : MultiSelect(title="Perovskite deposition procedure", value=['All'], options = multiselectDictShort['Perovskite_deposition_procedure'], size = 6),
        'Substrate_stack_sequence' : MultiSelect(title="Substrate", value=['All'], options = multiselectDictShort['Substrate_stack_sequence'], size = 6),      
        }

    # Multiselec list of catgories of information given when hovering over a point
    hoverToolSelect =  MultiSelect(title="Data when hover over a point", value=['DOI', 'Database ID', 'PCE'], options = list(toolTipsDict()), size = 6, width = 300)

    #%% Selects
    # Options
    booleanCategory_map = {'none': 'none'}
    booleanCategory_map.update(dict(zip([checkBoxButtons[item].labels[0] for item in list(checkBoxButtons.keys())], list(checkBoxButtons.keys()))))
    
    legendCategory_map = {
        'none': 'none',
        'Back contact': 'Backcontact_stack_sequence',
        'Cell architecture': 'Cell_architecture', 
        'ETL additives/dopands': 'ETL_additives_compounds',
        'ETL deposition procedure': 'ETL_deposition_procedure',
        'ETL stack': 'ETL_stack_sequence',
        'HTL additives/dopands': 'HTL_additives_compounds',
        'HTL deposition procedure': 'HTL_deposition_procedure',
        'HTL stack': 'HTL_stack_sequence',
        'Perovskite': 'Perovskite_composition_short_form',
        'Perovskite additives/dopands': 'Perovskite_additives_compounds',
        'Perovskite deposition aggeregation state': 'Perovskite_deposition_aggregation_state_of_reactants',
        'Perovskite deposition antisolvent': 'Perovskite_deposition_quenching_media',
        'Perovskite deposition antisolvent additives': 'Perovskite_deposition_quenching_media_additives_compounds',
        'Perovskite deposition procedure': 'Perovskite_deposition_procedure',
        'Perovskite deposition synthesis atmpsphere': 'Perovskite_deposition_synthesis_atmosphere',
        'Perovskite solvent': 'Perovskite_deposition_solvents',    
        'Substrate': 'Substrate_stack_sequence',
        }
    y_axis_map = {
        "PCE [%]": "JV_default_PCE",
        "Voc [V]": "JV_default_Voc",
        "Jsc [mA/cm^2]": "JV_default_Jsc",
        "FF": "JV_default_FF",
        'Active cell area [cm^2]' : 'Cell_area_measured',
        'Total cell area [cm^2]' : 'Cell_area_total',
        'Total module area [cm^2]' : 'Module_area_total', 
        'Active module area [cm^2]' : 'Module_area_effective',             
        }
    y_scale_select_map = {
        "Linear": 'linear',
        "log": 'log'
        }

    selects = {
        'booleanCategory' : Select(title="Color by True/False filters", options=list(booleanCategory_map.keys()), value="none"),
        'legendCategory' : Select(title="Color by category", options=list(legendCategory_map.keys()), value="none"),
        'y_axis' : Select(title="Y-Axis", options=list(y_axis_map.keys()), value="PCE [%]"),
        'y_scale_select' : Select(title="Y-Axis scale", options=list(y_scale_select_map.keys()), value="Linear"),
        }

    #%% Sliders
    sliderLimits ={
        'Cell_area_measured' : (0, 100),
        'JV_light_intensity' : (0, 1000),
        'Module_area_effective' : (0, 150),
        'Module_area_total' : (0, 500),
        'Module_number_of_cells_in_module' : (1, 35),
        'Perovskite_band_gap' : (1, 3.5),
        'Ref_publication_date' : (min(mainDataFrame['Ref_publication_date']) - relativedelta(months=1), max(mainDataFrame['Ref_publication_date']) + relativedelta(months=1)),
         }

    rangeSliders = {
        'Cell_area_measured' : RangeSlider(start=sliderLimits['Cell_area_measured'][0], end=sliderLimits['Cell_area_measured'][1], value=(sliderLimits['Cell_area_measured'][0], sliderLimits['Cell_area_measured'][1]), step=0.1, title="Active cell area [cm^2]"),
        'JV_light_intensity' : RangeSlider(start=sliderLimits['JV_light_intensity'][0], end=sliderLimits['JV_light_intensity'][1], value=(90, 110), step=0.1, title="Light intensity [mW/cm^2]"),
        'Module_number_of_cells_in_module' : RangeSlider(start=sliderLimits['Module_number_of_cells_in_module'][0], end=sliderLimits['Module_number_of_cells_in_module'][1], value=(sliderLimits['Module_number_of_cells_in_module'][0], sliderLimits['Module_number_of_cells_in_module'][1]), step=1, title="Number of cells in module"),
        'Module_area_effective' : RangeSlider(start=sliderLimits['Module_area_effective'][0], end=sliderLimits['Module_area_effective'][1], value=(sliderLimits['Module_area_effective'][0], sliderLimits['Module_area_effective'][1]), step=1, title="Active Module area [cm^2]"),
        'Module_area_total' : RangeSlider(start=sliderLimits['Module_area_total'][0], end=sliderLimits['Module_area_total'][1], value=(sliderLimits['Module_area_total'][0], sliderLimits['Module_area_total'][1]), step=1, title="Total Module area [cm^2]"),
        'Perovskite_band_gap' : RangeSlider(start=sliderLimits['Perovskite_band_gap'][0], end=sliderLimits['Perovskite_band_gap'][1], value=(sliderLimits['Perovskite_band_gap'][0], sliderLimits['Perovskite_band_gap'][1]), step=0.01, title="Band gap [eV]"),
        }

    sliders = {
        'legendFontSize' : Slider(start=4, end=30, value=8, step=1, title="Legend font size"),
        'plotAlpha' : Slider(start=0, end=1, value=0.8, step=0.05, title="Marker alpha"),
        'markerSize' : Slider(start=2, end=40, value=20, step=1, title="Marker size"),
        'yAxisLogStart' : Slider(start=-5, end=5, value=-1, step=1, title="Y-axis. log scale lower limit"),
        'fontSize' : Slider(start=5, end=50, value=16, step=1, title="Font size"),
        }

    #%% TextInput
    textInputControlls = {
        'excludeCellID' : TextInput(title = 'Exclude Cell ID (ID1; ID2; ID3; ...)'),
        }

    #%% Setting up callbacks ###############################################
    # Buttons
    buttons['update_data_table_button'].on_event(ButtonClick, updateDataTable)
    buttons['donwload_data_button'].on_event(ButtonClick, downloadDataTable)
   
    buttons['donwload_figure_button'].on_event(ButtonClick, downloadFigureAndMetadata)

    # Checkboxbuttons
    for item in checkBoxButtons:
        checkBoxButtons[item].on_change('active', lambda attr, old, new: update())

    for item in checkBoxButtonsPlotProperties:
        checkBoxButtonsPlotProperties[item].on_change('active', lambda attr, old, new: updatePlotCategories())

    # Multiselects long
    for item in multiselects:
        multiselects[item].on_change('value', lambda attr, old, new: update())

    # Multiselects short
    for item in multiselectsShort:
        multiselectsShort[item].on_change('value', lambda attr, old, new: update())

    # Hoover tool tips
    hoverToolSelect.on_change('value', lambda attr, old, new: updatePlotCategories())

    # Selects
    for item in selects:
        selects[item].on_change('value', lambda attr, old, new: updatePlotCategories())

    # Sliders   
    for item in sliders:
        sliders[item].on_change('value_throttled', lambda attr, old, new: updatePlotCategories())

    for item in rangeSliders:
        rangeSliders[item].on_change('value_throttled', lambda attr, old, new: update())

    # TextInput
    for item in textInputControlls:
        textInputControlls[item].on_change('value', lambda attr, old, new: update())

    #%% Set up a dummy glyph which when triggered runs a javascript based function for downloading selected data
    filename = 'Perovskite_database_content.csv'
    download_trigger = Div(text="1", visible=False)
    callback = CustomJS(args=dict(data={}, userFilename=filename),
                        code=open(os.path.join(os.path.dirname(__file__), "download.js")).read())
    download_trigger.js_on_change('text', callback)

    #%% Text fields
    settingUpFigure =  Div(text = "<b>Figure properties</b>")
    concernignTheMeasurement = Div(text = "<b>Measurement properties</b>")
    concerningTheCell = Div(text = "<b>Sample properties</b>")
    comonAlternatives = Div(text = "<b>Most common alternatives</b>")
    instruction_1 = Paragraph(text="""Filter out all non-True values""")
    blankColumnShort = Div(text = "              ", width=200, height=100)
    aboutTheApp = Div(text = appInstructions, width=700, height=1000)

    #%% Initial update
    # Initial data update
    update()

    # Initiate the figure
    p = updatePlot()

    #%% Group the input controlls
    controls1 = column(settingUpFigure,
        selects['y_axis'],
        selects['y_scale_select'],
        selects['legendCategory'],
        selects['booleanCategory'],
        checkBoxButtonsPlotProperties['MarkerSymbols'],
        textInputControlls['excludeCellID'],
        sliders['plotAlpha'],
        sliders['markerSize'],
        sliders['yAxisLogStart'],
        sliders['fontSize'],
        sliders['legendFontSize'],
        hoverToolSelect,
        buttons['donwload_figure_button'],
        concernignTheMeasurement,
        rangeSliders['JV_light_intensity'],
        checkBoxButtons['JV_certified_values'],
        checkBoxButtons['Stabilised_performance_measured'],     
        )

    controls3 = column(concerningTheCell,
        rangeSliders['Module_number_of_cells_in_module'],
        rangeSliders['Module_area_total'],
        rangeSliders['Module_area_effective'],   
        rangeSliders['Cell_area_measured'],
        rangeSliders['Perovskite_band_gap'],
        checkBoxButtons['Encapsulation'],
        checkBoxButtons['Cell_flexible'],
        checkBoxButtons['Cell_semitransparent'], 
        checkBoxButtons['Module'],
        checkBoxButtons['Perovskite_dimension_0D'],
        checkBoxButtons['Perovskite_dimension_2D'],
        checkBoxButtons['Perovskite_dimension_2D3D_mixture'],
        checkBoxButtons['Perovskite_dimension_3D'],
        checkBoxButtons['Perovskite_dimension_3D_with_2D_capping_layer'],
        checkBoxButtons['Perovskite_single_crystal'],
        checkBoxButtons['Perovskite_composition_inorganic'],
        checkBoxButtons['Perovskite_composition_leadfree'],
        checkBoxButtons['Perovskite_composition_perovskite_ABC3_structure'],
        checkBoxButtons['Perovskite_composition_perovskite_inspired_structure'],
        checkBoxButtons['Perovskite_deposition_quenching_induced_crystallisation'],
        checkBoxButtons['Perovskite_deposition_solvent_annealing'],
        )
    controls4 = column(comonAlternatives,
        multiselectsShort['Cell_architecture'],
        multiselectsShort['Substrate_stack_sequence'],
        multiselectsShort['ETL_stack_sequence'],
        multiselectsShort['HTL_stack_sequence'],
        multiselectsShort['Perovskite_additives_compounds'],
        multiselectsShort['Perovskite_composition_short_form'],
        multiselectsShort['Perovskite_deposition_procedure'],
        multiselectsShort['Backcontact_stack_sequence'],
        
        )
    controls5 = row(
        multiselects['Substrate_stack_sequence'],
        column(
            multiselects['ETL_additives_compounds'],
            multiselects['ETL_deposition_procedure'],
        ),
        multiselects['ETL_stack_sequence'],
        column(
            multiselects['HTL_additives_compounds'],
            multiselects['HTL_deposition_procedure'],
        ),
        multiselects['HTL_stack_sequence'],
        multiselects['Perovskite_additives_compounds'],
        multiselects['Perovskite_composition_short_form'],
        column(
            multiselects['Perovskite_deposition_aggregation_state_of_reactants'],
            multiselects['Perovskite_deposition_synthesis_atmosphere'],
        ),
        multiselects['Perovskite_deposition_procedure'],
        column(
            multiselects['Perovskite_deposition_quenching_media'],
            multiselects['Perovskite_deposition_quenching_media_additives_compounds'],
        ),
        multiselects['Perovskite_deposition_solvents'],
        multiselects['Backcontact_stack_sequence'],       
       )
 
    #%% Layout the controlls
    layout_tab1 = row(controls1, p, controls3, controls4, controls5)
    layout_tab2 = column(buttons['update_data_table_button'], buttons['donwload_data_button'], data_table, download_trigger)
    layout_tab3 = column(aboutTheApp)

    #%% Make tabs with the specified layouts 
    tab1 = Panel(child=layout_tab1, title = 'Scatterplot')
    tab2 = Panel(child=layout_tab2, title = 'Data from plot in table')
    tab3 = Panel(child=layout_tab3, title = 'About')

    #%%
    return tab1, tab2, tab3

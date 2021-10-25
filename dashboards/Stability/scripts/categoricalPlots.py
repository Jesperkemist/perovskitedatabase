# =============================================================================
# Bokeh app focusing on stability
# 
# By Jesper Jacobsson
# 2020 08
# =============================================================================

#%% Imports
from dateutil.relativedelta import relativedelta
import datetime
import os
import pathlib
import time

from bokeh.events import ButtonClick
from bokeh.layouts import column, row
from bokeh.models import Button
from bokeh.models import CDSView
from bokeh.models import CheckboxButtonGroup
from bokeh.models import ColumnDataSource
from bokeh.models import CustomJS
from bokeh.models import DateRangeSlider
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
from bokeh.transform import jitter
from bokeh.transform import factor_cmap, factor_mark
import numpy as np
import pandas as pd

from UtilityFunctions.categoricalColors import categoricalColors
from UtilityFunctions.utilityFunctions import (conectToDatabase,
    convertNumerListToFloats,
    databaseCategoriesMostCommon_withBoleanFilter,
    databaseCatagoriesUnique_withBoleanFilter,
    database_details,
    dataManipulation,
    integerList,
    is_number,
    loadData,
    loadData_withBoleanFilter,
    toolTipsDict,
    toolTipsMap)

#%% helper functions
def dataColumnsToUseFromTheStart():
    '''Defines the initial set of data columns'''
    return   ['JV_default_PCE',
              'Perovskite_deposition_procedure',
              'Ref_ID',
              'Ref_DOI_number',
              'Ref_publication_date',
              ]

def make_plot(source, data, view, activeCategories, alphaValue, booleanCategory, colorLabels, currentRowsInData, legendCategory, legendFontSize, markerSize, tooltips, useColorMarkers, x_axis, y_axis, y_scale_select, yAxisLogStart):
    '''Generate the plot'''
    TOOLS = "box_select, box_zoom, hover, lasso_select, pan, reset, save, tap, wheel_zoom"

    #TOOLTIPS = [("Initial PCE", "@Stability_PCE_initial_value"),
    #        ("PCE_f/PCE_i", "@Stability_PCE_end_of_experiment"),
    #        ("Stability protocoll", "@Stability_protocol"),        
    #        ("T80", "@Stability_PCE_T80"),
    #        ("Stack", "@Cell_stack_sequence"),
    #        ("Perovskite", "@Perovskite_composition_long_form"),
    #        ("Author", "@Ref_lead_author"),
    #        ("DOI", "@Ref_DOI_number"),
    #        ("Databse ID", "@Ref_ID"),
    #        ]

    TOOLTIPS = tooltips

    # Remove the All label
    if 'All' in activeCategories:
        activeCategories.remove('All')

    # Initiate figure
    p = figure(plot_width   = 1300, 
                   plot_height  = 800,
                   tools        = TOOLS,
                   tooltips     = TOOLTIPS,
                   toolbar_location = 'above',
                   x_range = activeCategories,
                   y_axis_type= y_scale_select,
                   output_backend="webgl")

    # List of posible marker types
    markerSet = []
    if useColorMarkers: 
        markerSet = ['circle', 'diamond', 'square', 'triangle', 'hex', 'circle_cross', 'diamond_cross', 'square_cross', 'triangle_dot', 'circle_dot', 'diamond_dot', 'square_dot', 'hex_dot', 'circle_x', 'square_pin', 'inverted_triangle', 'plus', 'circle_y', 'square_x', 'triangle_pin']
    else:
        markerSet = ['circle']


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

        # Generate the plot
        GlyphRenderer = p.scatter(y = y_axis[1], x = jitter(x_axis[1], width = 0.6, range = p.x_range), 
                 source = source, view = view,
                 size = markerSize,
                 alpha=alphaValue,
                 marker = factor_mark(legendCategory, markers=markerSet, factors=colorLabels),
                 color = factor_cmap(legendCategory, palette=colorSet, factors=colorLabels),
                 line_alpha = 1
                 )

        # Add an emty legend
        p.add_layout(Legend())

    # If data should be coloured by boolean category
    elif booleanCategory != 'none':
        # Import a colormap for categorical ploting in the form of a list of 61 hex values
        color_mapper = LinearColorMapper(palette=['darkgrey', "slateblue"], low=0, high=1)

        GlyphRenderer = p.scatter(y = y_axis[1], x = jitter(x_axis[1], width = 0.6, range = p.x_range), 
                source = source, view = view,
                size = markerSize,
                alpha=alphaValue, line_alpha = 1,
                marker = 'circle',
                color={'field': booleanCategory, 'transform': color_mapper},
                hover_color="red")

        # Add an emty legend
        p.add_layout(Legend())

    # If no legend color category
    else:
        # Import a colormap for categorical ploting in the form of a list of 61 hex values
        colorSet = categoricalColors('Dark')

        # Define legend entries (sorted in number of ocurances)
        colorLabels = list(data[x_axis[1]].value_counts().index)

        # Ensure that the color palet is large enough by cycling it
        if len(colorLabels) > len(colorSet):
            n = int(len(colorLabels)/len(colorSet)) + 1
            colorSet = colorSet*(n)

        # Generate the plot
        GlyphRenderer = p.circle(y = y_axis[1], x = jitter(x_axis[1], width = 0.6, range = p.x_range), 
                source = source, view = view,
                size = markerSize,
                alpha=alphaValue,
                color = factor_cmap(x_axis[1], palette=colorSet, factors=colorLabels),
                line_alpha = 1
                )

    #%% Add axis labels
    p.yaxis.axis_label = y_axis[0]

    # Axis formating
    p.xaxis.major_label_orientation = np.pi/6

    #%% Axis range
    # The current selection of data in the plot            
    y_selected = data.loc[currentRowsInData,[y_axis[1]]]

    if len(y_selected[y_axis[1]]) == 0:
        y_max = 100
    else:
        y_max = 1.02*max(y_selected[y_axis[1]])

    if y_scale_select == 'log':
        p.y_range=Range1d(10**yAxisLogStart, y_max)
    else:
        p.y_range=Range1d(0, y_max)

    #%% Enable that a tap on a point links to the article's URL (based on the DOI number)
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


#%% The main function that generates the the plot, the controlls, the callbacks, and specifies the layout
def interactiveEngine():
    '''The main function that generates the the plot, the controlls, the callbacks, and specifies the layout '''

    # Internal helper functions
    def download_Data_via_Json():
        '''Activate the dummy glyph that trigers java script for downloading data '''
        download_trigger.text = str(int(download_trigger.text) + 1)  

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

        filters8 = dict(zip([daterangeSliders[item].title for item in list(daterangeSliders.keys())],
                                    [daterangeSliders[item].value for item in list(daterangeSliders.keys())]))

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
                          'daterangeSliders' : filters8,
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

        activeDataColumns += [legendCategory_map[selects['x_axis'].value]]
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

        # Color by category
        if legendCategory_map[selects['x_axis'].value] in presentDataCategories:
            data = data[data[legendCategory_map[selects['x_axis'].value]].isin(updateActiveCategories())]

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

        # The data range slider apears to behave diferently on diferent systems
        if 'Ref_publication_date' in presentDataCategories:
            try:
                datetime.datetime.fromtimestamp(daterangeSliders['Ref_publication_date'].value[0]/1000)
                if datetime.datetime.fromtimestamp(daterangeSliders['Ref_publication_date'].value[0]/1000) > sliderLimits['Ref_publication_date'][0] or datetime.datetime.fromtimestamp(daterangeSliders['Ref_publication_date'].value[1]/1000) < sliderLimits['Ref_publication_date'][1]:
                    data = data[(data['Ref_publication_date'] > datetime.datetime.fromtimestamp(daterangeSliders['Ref_publication_date'].value[0]/1000)) & (data['Ref_publication_date'] < datetime.datetime.fromtimestamp(daterangeSliders['Ref_publication_date'].value[1]/1000))]
            except:
                if datetime.datetime.fromtimestamp(daterangeSliders['Ref_publication_date'].value[0]) > sliderLimits['Ref_publication_date'][0] or datetime.datetime.fromtimestamp(daterangeSliders['Ref_publication_date'].value[1]) < sliderLimits['Ref_publication_date'][1]:
                    data = data[(data['Ref_publication_date'] > datetime.datetime.fromtimestamp(daterangeSliders['Ref_publication_date'].value[0])) & (data['Ref_publication_date'] < datetime.datetime.fromtimestamp(daterangeSliders['Ref_publication_date'].value[1]))]

        #%% Text input
        if 'Ref_ID' in presentDataCategories: 
            if textInputControlls['excludeCellID'].value != '':
                ID_to_drop = integerList(textInputControlls['excludeCellID'].value)
                data = data[~data['Ref_ID'].isin(ID_to_drop)]
            
        return data

    def update():
        ''' Uppdate the data selection'''
        # Fetch handels to the current figure
        p = global_figure[0]

        # If the category depicted in the x-axis is updated the figure must be redrawn
        if p.x_range.factors != updateActiveCategories():
            updatePlotCategories()
        else:
            # Uppdate the selection of data to plot based on the filters selected by the user
            updateColumndataSource()

    def updateActiveCategories():
        '''Returns the list of categories to plot '''
        activeColumn = legendCategory_map[selects['x_axis'].value]

        activeCategories = []
        # If we have both a short and a long list
        if activeColumn in multiselects and activeColumn in multiselectsShort:
            activeCategories = list(set(multiselects[legendCategory_map[selects['x_axis'].value]].value + multiselectsShort[legendCategory_map[selects['x_axis'].value]].value))
        # If only a long list
        elif activeColumn in multiselects: 
            activeCategories = list(multiselects[legendCategory_map[selects['x_axis'].value]].value)
        # If only a short list
        elif activeColumn in multiselectsShort: 
            activeCategories = list(multiselectsShort[legendCategory_map[selects['x_axis'].value]].value)

        if 'All' in activeCategories:
            activeCategories.remove('All')
           
        # In case 'All' is chosen, sort out the five categories with most data (so we do not plot 2000 HTL categories)
        if activeCategories == []:
            if len(mainDataFrame[activeColumn].value_counts()) > 5:
                activeCategories = list(mainDataFrame[activeColumn].value_counts()[0:5].index)
                
            elif len(mainDataFrame[activeColumn].value_counts()) > 0:
                activeCategories = list(mainDataFrame[activeColumn].value_counts().index)

        activeCategories.sort()

        return activeCategories

    def updateColumndataSource():
        ''' Uppdate the data selection'''
        # Read in more data from the database if nessesary
        columnsToDownload = getNewDataColumnsToDownload()
        updateMainDataFrame(columnsToDownload)

        # Uppdate the selection of data to plot based on the filters selected by the user
        newSelectionOfData = select_data(mainDataFrame)
 
        # Uppdate the column data source with the new data selection (older solution. takes a lot of time)
        updateSource(categories = list(newSelectionOfData.columns)) 

        # Update the list of indicies for the selected data so that it can be accessed by remaining internal functions
        global_selectedRows.clear()
        global_selectedRows.extend(list(newSelectionOfData.index))

        # Uppdate the view of the columnDataSource
        view.filters = [IndexFilter(global_selectedRows)]

        # Update and add the legend (if the figure is defined and if it has a legend)
        if global_figure != []:
            if len(global_figure[0].legend) != 0: 
                updateLegend()

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
            newData = loadData_withBoleanFilter(dataColumns = newCategories, boleanColumn = 'Stability_measured', engine = engine)

            # Do data cleaning
            newData = dataManipulation(newData)

            # Merge data to mainDataFrame's index column
            mergedDataFrame = pd.DataFrame(mainDataFrame['Ref_ID']).join(newData.set_index('Ref_ID'), on='Ref_ID')

            # Add all new columns to the mainDataFrame. The reson that this not is done in hte previous line is that we must add to the old datafram and not create a new one if we should be able to directly use it in subfunctions
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

        # Define the complete set of legend lables and sort those based on how common they are. That is, all unique entries in the legendCategory
        if legendCategory != 'none':
            global_legendLabelsComplete.clear()
            global_legendLabelsComplete.extend(list(mainDataFrame[legendCategory].value_counts().index))
        elif booleanCategory != 'none':
            global_legendLabelsComplete.clear()
            global_legendLabelsComplete.extend(['True', 'False'])
        else:
            global_legendLabelsComplete.clear()

        # Tool tips
        hoverTools_map = toolTipsMap()
        tooltips = [hoverTools_map[tips] for tips in hoverToolSelect.value]

        # Initiate the figure
        p, GlyphRenderer = make_plot(source = source, data = mainDataFrame,
                  view = view,
                  activeCategories = multiselectDict[legendCategory_map[selects['x_axis'].value]],
                  alphaValue = sliders['plotAlpha'].value,
                  booleanCategory = booleanCategory_map[selects['booleanCategory'].value], 
                  colorLabels = global_legendLabelsComplete,
                  currentRowsInData = global_selectedRows,                  
                  legendCategory = legendCategory_map[selects['legendCategory'].value],
                  legendFontSize = sliders['legendFontSize'].value,
                  markerSize = sliders['markerSize'].value,
                  tooltips = tooltips,
                  useColorMarkers = useColorMarkers,
                  x_axis = (selects['x_axis'].value, legendCategory_map[selects['x_axis'].value]),
                  y_axis = (selects['y_axis'].value, y_axis_map[selects['y_axis'].value]),
                  y_scale_select = y_scale_select_map[selects['y_scale_select'].value],
                  yAxisLogStart = sliders['yAxisLogStart'].value,
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

        return

    def updatePlotCategories():
        '''Uppdate the categories, scale, alpha, etc. of the plot'''
        #Update the data
        updateColumndataSource()
 
        # Uppdate the plot
        updatePlot()

        # Update the plot dimentions
        updatePlotDimentions()

        # Fetch handels to the current figure
        p = global_figure[0]

        # Insert the updated plot in the layout (notice that the position of the plot must match its layout position)
        layout_tab1.children[2] = p

    def updatePlotDimentions():
        '''update the categories and the dimentions of the x-axis'''
        # get the updated list of categories to plot
        activeCategories = updateActiveCategories()

        # determin the desired width of the figure depending if there is a legend or not
        if legendCategory_map[selects['legendCategory'].value] == 'none' and booleanCategory_map[selects['booleanCategory'].value] == 'none':
            newPlotWidth = 100 + 150 * len(activeCategories)
        elif legendCategory_map[selects['legendCategory'].value] == 'none':
            newPlotWidth = 300 + 150 * len(activeCategories)
        else:
            newPlotWidth = 350 + 150 * len(activeCategories)

        # Fetch handels to the current figure
        p = global_figure[0]

        # update the dimentions of the figure
        p.width = newPlotWidth

        # Update the categories to diplay in the figure
        p.x_range.factors = activeCategories

    def updateSource(categories):
        '''Update the column data source if needed'''
        # If the x-axis, or the y-axis or the hover tools are change, more data may need to be added to the source

        excistingCategories = source.column_names

        # The x-axis
        x_axis = legendCategory_map[selects['x_axis'].value] 
        if x_axis not in excistingCategories:
            source.data[x_axis] = mainDataFrame[x_axis]

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

    #%% Main function #######################################################
    #%% Initial setup
    # Set up a conection to the database
    engine = conectToDatabase()

    # Read in data needed for the initial plot
    mainDataFrame = loadData_withBoleanFilter(dataColumns = dataColumnsToUseFromTheStart(), boleanColumn = 'Stability_measured', engine = engine)

    # Ensure proper formating of the data
    mainDataFrame = dataManipulation(mainDataFrame)

    # Main ColumnDataSource. Pupolate it with the intial values 
    source = ColumnDataSource(data=dict())
    source.data = mainDataFrame.to_dict('series')

    # Set up a view conected to the main column data source
    view = CDSView(source=source)

    #Global lists to keep track of selected data, current fiures, and legend and to provide access to those in sub functions
    global_selectedRows = []
    global_figure = []
    global_GlyphRenderer = []
    global_legendLabelsComplete = []


    #%% Input controlls
    #%% Buttons
    buttons = {
        'donwload_figure_button' : Button(label="Download figure metadata"),
    }

    #%% Checkboxbuttons
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
        'Perovskite_dimension_3D_with_2D_capping_layer' : CheckboxButtonGroup(labels = ['Perovsktie. 3D with 2D capping layer'], active = []),
        'Perovskite_single_crystal' : CheckboxButtonGroup(labels = ['Perovskite. Single crystal'], active = []),
        'Stability_light_UV_filter' : CheckboxButtonGroup(labels = ['Use of UV filter'], active = [], width = 150),
        'Stability_periodic_JV_measurements' : CheckboxButtonGroup(labels = ['Periodic JV measured'], active = [], width = 150),
        'Stability_PCE_burn_in_observed' : CheckboxButtonGroup(labels = ['PCE burn in observed'], active = [], width = 150),
    }
    checkBoxButtonsPlotProperties = {
        'MarkerSymbols' : CheckboxButtonGroup(labels = ['Separate color by marker type'], active = []),
        }

    #%% Multiselects
    # Generate compleat list of alternatives
    multiselectCategories = [
        'Backcontact_stack_sequence',
        'Cell_architecture',
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
        'Stability_atmosphere',    
        'Stability_light_illumination_direction',
        'Stability_light_load_condition',
        'Stability_light_spectra',
        'Stability_light_source_type',
        'Stability_potential_bias_load_condition',
        'Stability_protocol',
        'Stability_relative_humidity_load_conditions',
        'Stability_temperature_load_condition',
        'Substrate_stack_sequence',
        ]

    # Generate alphabetic lists of all alternatives in the database for each multiselect category 
    multiselectDict = {}
    for i, item in enumerate(multiselectCategories):
        multiselectDict[item] = databaseCatagoriesUnique_withBoleanFilter(column = item, boleanColumn = 'Stability_measured', engine = engine)
        multiselectDict[item] = [str(i) for i in multiselectDict[item]]
        multiselectDict[item].insert(0, 'All') 

    # Generate alphabetic lists of the {number} most common alternatives in the database for each multiselect category 
    multiselectDictShort = {}
    numberOfMostComonAlternatives = 30
    for i, item in enumerate(multiselectCategories):
        multiselectDictShort[item] = databaseCategoriesMostCommon_withBoleanFilter(column = item, boleanColumn = 'Stability_measured', number = numberOfMostComonAlternatives, engine = engine)
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
        'Perovskite_deposition_aggregation_state_of_reactants' : MultiSelect(title="Perovskite. Aggregation stat of reactants", value=['All'], options = multiselectDict['Perovskite_deposition_aggregation_state_of_reactants'], size = 22),
        'Perovskite_deposition_procedure' : MultiSelect(title="Perovskite deposition procedure", value=['All'], options = multiselectDict['Perovskite_deposition_procedure'], size = 50, width = 500),
        'Perovskite_deposition_quenching_media' : MultiSelect(title="Perovskite. Quenching media", value=['All'], options = multiselectDict['Perovskite_deposition_quenching_media'], size = 22),
        'Perovskite_deposition_quenching_media_additives_compounds' : MultiSelect(title="Quenching media additives", value=['All'], options = multiselectDict['Perovskite_deposition_quenching_media_additives_compounds'], size = 22),
        'Perovskite_deposition_solvents' : MultiSelect(title="Perovskite. Solvent", value=['All'], options = multiselectDict['Perovskite_deposition_solvents'], size = 50),
        'Perovskite_deposition_synthesis_atmosphere' : MultiSelect(title="Perovskite. Syntesis atmosphere", value=['All'], options = multiselectDict['Perovskite_deposition_synthesis_atmosphere'], size = 22),
        'Stability_atmosphere' : MultiSelect(title=" Measurement atmosphere ", value=['All'], options = multiselectDict['Stability_atmosphere'], size = 7, width = 150),   
        'Stability_light_illumination_direction' : MultiSelect(title="Illumination direction ", value=['All'], options = multiselectDict['Stability_light_illumination_direction'], size = 4), 
        'Stability_light_load_condition' : MultiSelect(title="Illumination load condition ", value=['All'], options = multiselectDict['Stability_light_load_condition'], size = 4), 
        'Stability_light_spectra' : MultiSelect(title="Ligth spectra ", value=['All'], options = multiselectDict['Stability_light_spectra'], size = 7, width = 150),
        'Stability_light_source_type' : MultiSelect(title="Light source ", value=['All'], options = multiselectDict['Stability_light_source_type'], size = 7, width = 150), 
        'Stability_potential_bias_load_condition' : MultiSelect(title="Potential load condition ", value=['All'], options = multiselectDict['Stability_potential_bias_load_condition'], size = 6, width = 150), 
        'Stability_protocol' : MultiSelect(title="Stability protocoll ", value=['All'], options = multiselectDict['Stability_protocol'], size = 19, width = 150), 
        'Stability_relative_humidity_load_conditions' : MultiSelect(title="Humidity load condition ", value=['All'], options = multiselectDict['Stability_relative_humidity_load_conditions'], size = 4), 
        'Stability_temperature_load_condition' : MultiSelect(title="Temperature load condition ", value=['All'], options = multiselectDict['Stability_temperature_load_condition'], size = 4), 
        'Substrate_stack_sequence' : MultiSelect(title="Substrate", value=['All'], options = multiselectDict['Substrate_stack_sequence'], size = 50, width = 300),
    }

    multiselectsShort = {
        'Backcontact_stack_sequence' : MultiSelect(title="Back contact", value=['All'], options = multiselectDictShort['Backcontact_stack_sequence'], size = 15),
        'Cell_architecture' : MultiSelect(title="Cell_architecture", value=['All'], options = multiselectDictShort['Cell_architecture'], size = 6),       
        'ETL_stack_sequence' : MultiSelect(title="ETL stack", value=['All'], options = multiselectDictShort['ETL_stack_sequence'], size = 20),
        'HTL_stack_sequence' : MultiSelect(title="HTL stack", value=['All'], options = multiselectDictShort['HTL_stack_sequence'], size = 20),
        'Perovskite_additives_compounds' : MultiSelect(title="Perovskite additives", value=['All'], options = multiselectDictShort['Perovskite_additives_compounds'], size = 10),
        'Perovskite_composition_short_form' : MultiSelect(title="Perovskite", value=['All'], options = multiselectDictShort['Perovskite_composition_short_form'], size = 20),
        'Perovskite_deposition_procedure' : MultiSelect(title="Perovskite deposition procedure", value=['All'], options = multiselectDictShort['Perovskite_deposition_procedure'], size = 20),
        'Substrate_stack_sequence' : MultiSelect(title="Substrate", value=['All'], options = multiselectDictShort['Substrate_stack_sequence'], size = 15),      
        }

    # Multiselec list of catgories of information given when hovering over a point
    hoverToolSelect =  MultiSelect(title="Data when hoover over a point", value=['DOI', 'Database ID', 'PCE'], options = list(toolTipsDict()), size = 6, width = 300)

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
        'Perovsktie deposition aggeregation state': 'Perovskite_deposition_aggregation_state_of_reactants',
        'Perovsktie deposition antisolvent': 'Perovskite_deposition_quenching_media',
        'Perovsktie deposition antisolvent additives': 'Perovskite_deposition_quenching_media_additives_compounds',
        'Perovskite deposition procedure': 'Perovskite_deposition_procedure',
        'Perovskite deposition synthesis atmpsphere': 'Perovskite_deposition_synthesis_atmosphere',
        'Perovskite solvent': 'Perovskite_deposition_solvents',    
        'Stability atmosphere' : 'Stability_atmosphere',    
        'Stability illumination direction' : 'Stability_light_illumination_direction',
        'Stability light load condition' : 'Stability_light_load_condition',
        'Stability light spectra' : 'Stability_light_spectra',
        'Stability light source' : 'Stability_light_source_type',
        'Stability potential bias condition' : 'Stability_potential_bias_load_condition',
        'Stability protocol' : 'Stability_protocol',
        'Stability relative humidity conditions' : 'Stability_relative_humidity_load_conditions',
        'Stability temperature load condition' : 'Stability_temperature_load_condition',
        'Substrate': 'Substrate_stack_sequence',
        }
    y_axis_map = {
        "PCE after 1000 h [%]": "Stability_PCE_after_1000_h",
        "PCE at the end of experiment [%]" : "Stability_PCE_end_of_experiment",
        "T80 [h]": "Stability_PCE_T80",
        "Ts80 [h]": "Stability_PCE_Ts80",
        "Te80 [h]": "Stability_PCE_Te80",
        "Tse80 [h]": "Stability_PCE_Tse80",
        "T95 [h]": "Stability_PCE_T95",
        "Ts95 [h]": "Stability_PCE_Ts95",
        }
    y_scale_select_map = {
        "Linear": 'linear',
        "log": 'log'
        }

    selects = {
        'booleanCategory' : Select(title="Color by True/False filters", options=list(booleanCategory_map.keys()), value="none"),
        'legendCategory' : Select(title="Color by category", options=list(legendCategory_map.keys()), value="none"),
        'x_axis' : Select(title="X-axis category", options=list(legendCategory_map.keys()), value="Stability protocol"),
        'y_axis' : Select(title="Y-Axis", options=list(y_axis_map.keys()), value="T80 [h]"),
        'y_scale_select' : Select(title="Y-Axis scale", options=list(y_scale_select_map.keys()), value="Linear"),
        }

    #%% Sliders
    sliderLimits ={
        'Cell_area_measured' : (0, 100),
        'Module_area_total' : (0, 1000),
        'Perovskite_band_gap' : (1, 3.5),
        'Module_area_effective' : (0, 150),
        'Module_area_total' : (0, 500),
        'Module_number_of_cells_in_module' : (1, 35),
        'Ref_publication_date' : (min(mainDataFrame['Ref_publication_date']) - relativedelta(months=1), max(mainDataFrame['Ref_publication_date']) + relativedelta(months=1)),
        'Stability_light_intensity' : (0, 500),
        'Stability_relative_humidity_average_value' : (0, 100),
        'Stability_PCE_initial_value' : (0, 25),
        'Stability_temperature_range' : (-80, 100),
        }

    rangeSliders = {
        'Cell_area_measured' : RangeSlider(start=sliderLimits['Cell_area_measured'][0], end=sliderLimits['Cell_area_measured'][1], value=(sliderLimits['Cell_area_measured'][0], sliderLimits['Cell_area_measured'][1]), step=0.1, title="Measured cell area [cm^2]"),
        'Module_area_total' : RangeSlider(start=sliderLimits['Module_area_total'][0], end=sliderLimits['Module_area_total'][1], value=(sliderLimits['Module_area_total'][0], sliderLimits['Module_area_total'][1]), step=1, title="Module area (total) [cm^2]"),
        'Perovskite_band_gap' : RangeSlider(start=sliderLimits['Perovskite_band_gap'][0], end=sliderLimits['Perovskite_band_gap'][1], value=(sliderLimits['Perovskite_band_gap'][0], sliderLimits['Perovskite_band_gap'][1]), step=0.01, title="Band gap [eV]"),
        'Stability_light_intensity' : RangeSlider(start=sliderLimits['Stability_light_intensity'][0], end=sliderLimits['Stability_light_intensity'][1], value=(sliderLimits['Stability_light_intensity'][0], sliderLimits['Stability_light_intensity'][1]), step=1, title="Light Intensity [mW/cm^2]"),
        'Stability_relative_humidity_average_value' : RangeSlider(start=sliderLimits['Stability_relative_humidity_average_value'][0], end=sliderLimits['Stability_relative_humidity_average_value'][1], value=(sliderLimits['Stability_relative_humidity_average_value'][0], sliderLimits['Stability_relative_humidity_average_value'][1]), step=1, title="Relative humidity [%]"),
        'Stability_PCE_initial_value' : RangeSlider(start=sliderLimits['Stability_PCE_initial_value'][0], end=sliderLimits['Stability_PCE_initial_value'][1], value=(sliderLimits['Stability_PCE_initial_value'][0], sliderLimits['Stability_PCE_initial_value'][1]), step=1, title="Initial cell efficinecy [%]"),
        'Stability_temperature_range' : RangeSlider(start=sliderLimits['Stability_temperature_range'][0], end=sliderLimits['Stability_temperature_range'][1], value=(sliderLimits['Stability_temperature_range'][0], sliderLimits['Stability_temperature_range'][1]), step=1, title="Temperature (max) [deg. C]"),
        }

    sliders = {
        'legendFontSize' : Slider(start=4, end=30, value=8, step=1, title="Legend font size"),
        'plotAlpha' : Slider(start=0, end=1, value=0.6, step=0.05, title="Marker alpha"),
        'markerSize' : Slider(start=2, end=30, value=5, step=1, title="Marker size"),
        'fontSize' : Slider(start=5, end=50, value=16, step=1, title="Font size"),
        'yAxisLogStart' : Slider(start=-5, end=5, value=-1, step=1, title="Y-axis. log scale lower limit"),
        }

    daterangeSliders = {
        'Ref_publication_date' : DateRangeSlider(start=sliderLimits['Ref_publication_date'][0], end=sliderLimits['Ref_publication_date'][1], value=(sliderLimits['Ref_publication_date'][0], sliderLimits['Ref_publication_date'][1]), step=1, title="Publication date")       
        }

    #%% TextInput
    textInputControlls = {
        'excludeCellID' : TextInput(title = 'Exclude Cell ID (ID1; ID2; ID3; ...)'),
        }

    #%% Setting up callbacks #######################################################
    # Buttons
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
    daterangeSliders['Ref_publication_date'].on_change('value_throttled', lambda attr, old, new: updatePlotCategories())
    #sliders['plotAlpha'].on_change('value_throttled', lambda attr, old, new: updatePlotCategories()) 
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

    #%% Initial update 
    # Update teh data
    updateColumndataSource()

    # Initiate the figure 
    updatePlot()

    # Initial update of plot dimentions
    updatePlotDimentions()

    # Fetch handels to the current figure
    p = global_figure[0]

    #%% Group the input controlls
    controls1 = column(settingUpFigure,
        selects['y_axis'],
        selects['x_axis'],
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
        daterangeSliders['Ref_publication_date'],
        buttons['donwload_figure_button'],
        concernignTheMeasurement,
        rangeSliders['Stability_PCE_initial_value'],
        rangeSliders['Stability_light_intensity'],  
        rangeSliders['Stability_temperature_range'],
        rangeSliders['Stability_relative_humidity_average_value'],      
        multiselects['Stability_light_load_condition'],        
        multiselects['Stability_temperature_load_condition'],
        multiselects['Stability_relative_humidity_load_conditions'],
        multiselects['Stability_light_illumination_direction'],
        )
    controls2 = column(concernignTheMeasurement,
        checkBoxButtons['Stability_light_UV_filter'],
        checkBoxButtons['Stability_periodic_JV_measurements'],
        checkBoxButtons['Stability_PCE_burn_in_observed'], 
        multiselects['Stability_protocol'],
        multiselects['Stability_potential_bias_load_condition'],
        multiselects['Stability_atmosphere'],
        multiselects['Stability_light_spectra'],
        multiselects['Stability_light_source_type'], 
        )
    controls3 = column(concerningTheCell,
        rangeSliders['Cell_area_measured'],
        rangeSliders['Module_area_total'],
        rangeSliders['Perovskite_band_gap'],
        checkBoxButtons['Encapsulation'],
        checkBoxButtons['Cell_flexible'],
        checkBoxButtons['Cell_semitransparent'],
        checkBoxButtons['Module'],
        checkBoxButtons['JV_certified_values'],
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
        multiselectsShort['Cell_architecture'],
        )
    controls4 = column(comonAlternatives,      
        multiselectsShort['Perovskite_composition_short_form'],
        multiselectsShort['ETL_stack_sequence'],
        multiselectsShort['HTL_stack_sequence'],
        )
    controls5 = column(comonAlternatives,
        multiselectsShort['Perovskite_deposition_procedure'],
        multiselectsShort['Substrate_stack_sequence'],
        multiselectsShort['Backcontact_stack_sequence'],
        multiselectsShort['Perovskite_additives_compounds'],       
        )
    controls6 = row(            
        multiselects['Backcontact_stack_sequence'],
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
        multiselects['Substrate_stack_sequence'],
       )

    #%% Layout the controlls
    layout_tab1 = row(controls1, controls2, p, controls3, controls4, controls5, controls6, download_trigger)

    # Make tabs with the specified layouts 
    tab1 = Panel(child=layout_tab1, title = 'Categorical plots')

    #%%
    return tab1
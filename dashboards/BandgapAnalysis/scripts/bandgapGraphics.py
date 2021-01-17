# =============================================================================
# Bokeh app focusing on perovskite band gap
# 
# By Jesper Jacobsson
# 2020 06
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
               'Cell_area_total',
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
               'Module_area_total',
               'Module_area_effective',
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
              'JV_default_Voc',
              'JV_default_FF',
              'JV_default_Jsc',
              'Perovskite_band_gap',
              'Ref_ID',
              'Ref_DOI_number',
              'Ref_publication_date',
              ]

def make_plot(source, view, QEdata, alphaValue, booleanCategory, markerSize, tooltips, x_axis, xrange):
    ''' Generat the plot'''

    # Initiate figures
    p1 = plotTemplate(tooltips)     
    p2 = plotTemplate(tooltips)     
    p3 = plotTemplate(tooltips)     
    p4 = plotTemplate(tooltips)     

    # A linear color map
    color_mapper = LinearColorMapper(palette=['darkgrey', "slateblue"], low=0, high=1)

    if x_axis == 'keyMetrics':
        #%% Plot the data
        if booleanCategory == 'none':
            p1.scatter(x = 'Perovskite_band_gap', y = 'JV_default_PCE', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color = "navy", hover_color="red")
        else:
            p1.scatter(x = 'Perovskite_band_gap', y = 'JV_default_PCE', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color={'field': booleanCategory, 'transform': color_mapper},
                          hover_color="red")
        p1.line(QEdata['Bandgap (eV)'], QEdata['PCE (%)'] , line_width=3, line_color = 'black')

        #%% Voc
        if booleanCategory == 'none':
            p2.scatter(x = 'Perovskite_band_gap', y = 'JV_default_Voc', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color = "slateblue", hover_color="red")
        else:
            p2.scatter(x = 'Perovskite_band_gap', y = 'JV_default_Voc', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color={'field': booleanCategory, 'transform': color_mapper},
                          hover_color="red")
        p2.line(QEdata['Bandgap (eV)'], QEdata['Bandgap (eV)'] , line_width=3, line_color = "black", line_dash='dotted')
        p2.line(QEdata['Bandgap (eV)'], QEdata['Voc (V)'] , line_width=3,  line_color = "black")

        #%% Jsc
        if booleanCategory == 'none':
            p3.scatter(x = 'Perovskite_band_gap', y = 'JV_default_Jsc', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color = "blueviolet", hover_color="red")
        else:
            p3.scatter(x = 'Perovskite_band_gap', y = 'JV_default_Jsc', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color={'field': booleanCategory, 'transform': color_mapper},
                          hover_color="red")
        p3.line(QEdata['Bandgap (eV)'], QEdata['Jsc (mA/cm^2)'] , line_width=3,  line_color = "black")

        #%% FF
        if booleanCategory == 'none':
            p4.scatter(x = 'Perovskite_band_gap', y = 'JV_default_FF', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color = "cornflowerblue", hover_color="red")
        else:
            p4.scatter(x = 'Perovskite_band_gap', y = 'JV_default_FF', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color={'field': booleanCategory, 'transform': color_mapper},
                          hover_color="red")
        p4.line(QEdata['Bandgap (eV)'], QEdata['FF (%)']/100 , line_width=3,  line_color = "black")

        #%% Set the axis range
        p1.y_range=Range1d(0, 30)
        #p1.x_range=Range1d(1.1, 3.4)
        p1.x_range=Range1d(xrange[0], xrange[1]) 

        p2.y_range=Range1d(0, 2.5)
        p2.x_range = p1.x_range

        p3.y_range=Range1d(0, 40)
        p3.x_range = p1.x_range

        p4.y_range=Range1d(0, 1)
        p4.x_range = p1.x_range

        #%% Title and axis labels
        #p1.title.text       = "PCE vs Eg"
        p1.xaxis.axis_label = 'Band gap [eV]'
        p1.yaxis.axis_label = 'PCE [%]'

        #p2.title.text       = "Voc vs Eg"
        p2.xaxis.axis_label = 'Band gap [eV]'
        p2.yaxis.axis_label = 'Voc [V]'

        #p3.title.text       = "Jsc vs Eg"
        p3.xaxis.axis_label = 'Band gap [eV]'
        p3.yaxis.axis_label = 'Jsc [mA/cm^2]'

        #p4.title.text       = "FF vs Eg"
        p4.xaxis.axis_label = 'Band gap [eV]'
        p4.yaxis.axis_label = 'FF'

    elif x_axis == 'SQ-limit':
        # Plot the data
        #%% PCE
        if booleanCategory == 'none':
            p1.scatter(x = 'Perovskite_band_gap', y = 'PCE_SQ', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color = "navy", hover_color="red")
        else:
            p1.scatter(x = 'Perovskite_band_gap', y = 'PCE_SQ', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color={'field': booleanCategory, 'transform': color_mapper},
                          hover_color="red")

        #%% Voc
        if booleanCategory == 'none':
            p2.scatter(x = 'Perovskite_band_gap', y = 'Voc_SQ', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color = "slateblue", hover_color="red")
        else:
            p2.scatter(x = 'Perovskite_band_gap', y = 'Voc_SQ', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color={'field': booleanCategory, 'transform': color_mapper},
                          hover_color="red")

        #%% Jsc
        if booleanCategory == 'none':
            p3.scatter(x = 'Perovskite_band_gap', y = 'Jsc_SQ', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color = "blueviolet", hover_color="red")
        else:
            p3.scatter(x = 'Perovskite_band_gap', y = 'Jsc_SQ', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color={'field': booleanCategory, 'transform': color_mapper},
                          hover_color="red")

        #%% FF
        if booleanCategory == 'none':
            p4.scatter(x = 'Perovskite_band_gap', y = 'FF_SQ', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color = "cornflowerblue", hover_color="red")
        else:
            p4.scatter(x = 'Perovskite_band_gap', y = 'FF_SQ', source = source, view = view,
                          marker = 'circle', size = markerSize, 
                          alpha = alphaValue, line_alpha = 1,
                          color={'field': booleanCategory, 'transform': color_mapper},
                          hover_color="red")

        #%% Set the axis range
        p1.y_range=Range1d(0, 30)
        p1.x_range=Range1d(xrange[0], xrange[1]) 

        p2.y_range=Range1d(0, 2.5)
        p2.x_range = p1.x_range

        p3.y_range=Range1d(0, 40)
        p3.x_range = p1.x_range

        p4.y_range=Range1d(0, 1)
        p4.x_range = p1.x_range

        #%% Title and axis labels
        #p1.title.text       = "PCE vs Eg"
        p1.xaxis.axis_label = 'Band gap [eV]'
        p1.yaxis.axis_label = 'PCE_SQ - PCE [%]'

        #p2.title.text       = "Voc vs Eg"
        p2.xaxis.axis_label = 'Band gap [eV]'
        p2.yaxis.axis_label = 'Voc_SQ - Voc [V]'

        #p3.title.text       = "Jsc vs Eg"
        p3.xaxis.axis_label = 'Band gap [eV]'
        p3.yaxis.axis_label = 'Jsc_SQ - Jsc [mA/cm^2]'

        #p4.title.text       = "FF vs Eg"
        p4.xaxis.axis_label = 'Band gap [eV]'
        p4.yaxis.axis_label = 'FF_SQ - FF [mA/cm^2]'


    #%% Enable that a tap on a point links to the article's URL (based on the DOI number)
    url = "https://doi.org/@Ref_DOI_number"
    taptool_p1 = p1.select(type=TapTool)
    taptool_p1.callback = OpenURL(url=url)
    taptool_p2 = p2.select(type=TapTool)
    taptool_p2.callback = OpenURL(url=url)
    taptool_p3 = p3.select(type=TapTool)
    taptool_p3.callback = OpenURL(url=url)
    taptool_p4 = p4.select(type=TapTool)
    taptool_p4.callback = OpenURL(url=url)

    #%% Return
    return p1, p2, p3, p4

def plotTemplate(tooltips):
    TOOLS = "box_select, box_zoom, hover, lasso_select, pan, reset, save, tap, wheel_zoom"

    #TOOLTIPS = [("PCE", "@JV_default_PCE"),
    #        ("Voc", "@JV_default_Voc"),
    #        ("Jsc", "@JV_default_Jsc"),
    #        ("FF", "@JV_default_FF"),
    #        ("Stack", "@Cell_stack_sequence"),
    #        ("Perovskite", "@Perovskite_composition_long_form"),
    #        ("Deposition", "@Perovskite_deposition_procedure"),
    #        ("Eg", "@Perovskite_band_gap_string"),
    #        ("Author", "@Ref_lead_author"),
    #        ("DOI", "@Ref_DOI_number"),
    #        ("Databse ID", "@Ref_ID"),
    #        ]
   
    TOOLTIPS = tooltips

    # Initiate figure
    p = figure(plot_width   = 470, 
                plot_height  = 470,
                tools        = TOOLS,
                tooltips     = TOOLTIPS,
                toolbar_location = 'right',
                output_backend = "webgl")

    return p

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

def SQ_potential(data, QEdata):
    ''' Compute the losses with respect to the SQ limit '''
    PCE_SQ = np.interp(data['Perovskite_band_gap'],QEdata['Bandgap (eV)'],QEdata['PCE (%)']) - data['JV_default_PCE']
    Voc_SQ = np.interp(data['Perovskite_band_gap'],QEdata['Bandgap (eV)'],QEdata['Voc (V)']) - data['JV_default_Voc']
    Jsc_SQ = np.interp(data['Perovskite_band_gap'],QEdata['Bandgap (eV)'],QEdata['Jsc (mA/cm^2)']) - data['JV_default_Jsc']
    FF_SQ = np.interp(data['Perovskite_band_gap'],QEdata['Bandgap (eV)'],QEdata['FF (%)'])/100 - data['JV_default_FF']

    return PCE_SQ, Voc_SQ, Jsc_SQ, FF_SQ

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


#%% The main function that generates the the plot, the controlls, the callbacks, and specifies the layout
def interactiveEngine():
    '''The main function that generates the the plot, the controlls, the callbacks, and specifies the layout '''
    #%% Internal helper functions #########################################
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
        Cell_ID_numbers = list(mainDataFrame.loc[global_selectedRows]['Ref_ID'])

        # Forrmat the Cell_ID_numbers for the SQL query
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
 
    def downloadDataTableLasso(event):
        '''Download selected data in table as .csv-file '''

        # Fetch table and scheema names of the database
        bd_details = database_details()
        table = bd_details['table']
        schema = bd_details['schema']
        ID = bd_details['bd_key'] 

        # The Ref_ID for all selected cells
        Cell_ID_numbers = list(mainDataFrame.loc[source.selected.indices]['Ref_ID'])

        # Forrmat the Cell_ID_numbers for the SQL query
        IDnumbersString = [str(x) for x in Cell_ID_numbers]
        IDnumbersString = '(' + ','.join(IDnumbersString) + ')'

        # Query the database for all data for the selected cells
        query = f'''select * from {schema}.{table} where {table}."{ID}" in {IDnumbersString}'''
        query_results = pd.read_sql_query(sql = query, con = engine)

        # Download results
        if len(query_results) != 0:
            
            # Make the data accesible to download
            callback.args['userFilename'] = 'Perovsite database lasso query.csv' 
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

        #if legendCategory_map[selects['legendCategory'].value] != 'none':
            #activeDataColumns += [legendCategory_map[selects['legendCategory'].value]]

        #activeDataColumns += [x_axis_map[selects['x_axis'].value]]
        #activeDataColumns += [y_axis_map[selects['y_axis'].value]]

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
        #data = data[data[y_axis_map[selects['y_axis'].value]] != -1]
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

        # The data range slider apears to behave differently on different systems
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

        # STOP WAINTING SPINNER

    def updateDataTableLasso(event):
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
        dataSelection = mainDataFrame.loc[source.selected.indices]

        # Uppdate the columnDataSource responsible for the datatabel with the currently selected data
        sourceLassoSelect.data = dataSelection.to_dict('series')

        # STOP WAINTING SPINNER

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

            # Add all new columns to the mainDataFrame. The reson that this not is done in hte previous line is that we must add to the old datafram and not create a new one if we should be able to directly use it in subfunctions
            newCategories.remove('Ref_ID')

            for category in newCategories:
                mainDataFrame[category] = newData[category]

    def updatePlot():
        '''Generated the plots'''

        # Tool tips
        hoverTools_map = toolTipsMap()
        tooltips = [hoverTools_map[tips] for tips in hoverToolSelect.value]


        #%% Initiate the figures
        p1, p2, p3, p4 = make_plot(source = source, 
                                   QEdata = QEdata, 
                                   view = view, 
                                   alphaValue = sliders['plotAlpha'].value,
                                   booleanCategory = booleanCategory_map[selects['booleanCategory'].value],
                                   markerSize = sliders['markerSize'].value,
                                   tooltips = tooltips,
                                   x_axis = x_axis_map[selects['x_axis'].value],
                                   xrange = (sliders['Perovskite_band_gap'].value[0], sliders['Perovskite_band_gap'].value[1]),
                                   )

        # Uppdate the styling
        p1 = style(p1, fontSize = sliders['fontSize'].value)
        p2 = style(p2, fontSize = sliders['fontSize'].value)
        p3 = style(p3, fontSize = sliders['fontSize'].value)
        p4 = style(p4, fontSize = sliders['fontSize'].value)
  
        return p1, p2, p3, p4

    def updatePlotCategories():
        '''Update aplpha by reploting figures'''
        # Update the data
        update()

        # Uppdate the plot
        p1, p2, p3, p4 = updatePlot()
 
        # Insert the updated plot in the layout
        layout_tab1.children[1] = column(row(p1, p2), row(p3, p4))        
 
    def updateSource(categories):
        '''Update the column data source if needed'''
        # If the x-axis, or the y-axis or the hover tools are change, more data may need to be added to the source

        excistingCategories = source.column_names

        ## The x-axis
        #x_axis = x_axis_map[selects['x_axis'].value] 
        #if x_axis not in excistingCategories:
        #    source.data[x_axis] = mainDataFrame[x_axis]

        ## The y-axis
        #y_axis = y_axis_map[selects['y_axis'].value] 
        #if y_axis not in excistingCategories:
        #    source.data[y_axis] = mainDataFrame[y_axis]

        # The booleanCategory
        booleanCategory = booleanCategory_map[selects['booleanCategory'].value]
        if booleanCategory != 'none':
            if booleanCategory not in excistingCategories:
                source.data[booleanCategory] = mainDataFrame[booleanCategory]

        ## The legendCategory
        #legendCategory = legendCategory_map[selects['legendCategory'].value]
        #if legendCategory != 'none':
        #    if legendCategory not in excistingCategories:
        #        source.data[legendCategory] = mainDataFrame[legendCategory]

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
    mainDataFrame = loadData(dataColumns = dataColumnsToUseFromTheStart(), engine = engine)

    # Ensure proper formating of the data
    mainDataFrame = dataManipulation(mainDataFrame)

    # Read data for the Schotcley quisier limit
    path = pathlib.Path(__file__).parent.absolute()
    fileName = 'SQ limit.csv'
    filePath = os.path.join(path, fileName)
    QEdata = pd.read_csv(filePath)
  
    # Generate the comparitions to the SQ limit
    PCE_SQ, Voc_SQ, Jsc_SQ, FF_SQ = SQ_potential(mainDataFrame, QEdata)
    mainDataFrame['PCE_SQ'] = PCE_SQ 
    mainDataFrame['Voc_SQ'] = Voc_SQ
    mainDataFrame['Jsc_SQ'] = Jsc_SQ
    mainDataFrame['FF_SQ'] = FF_SQ

    # Main ColumnDataSource. Pupolate it with the intial values 
    source = ColumnDataSource(data=dict())
    source.data = mainDataFrame.to_dict('series')

    # Set up a view conected to the main column data source
    view = CDSView(source=source)
    
    # Set up ColumnDataSources for tables
    sourceDataTable = ColumnDataSource()
    sourceLassoSelect = ColumnDataSource()
    
    # Global lists to keep track of selected data, current figures, and legend, and to provide access to those in sub functions
    global_selectedRows = []

    #%% Read in text instructions about the app to be shown in a separate tab
    appInstructions = getAppInstructions(fileName = 'Instructions.html')

    #%% Input controlls ####################################################
    #%% Buttons
    buttons = {
        'donwload_data_button' : Button(label="Download CSV data", button_type="success"),
        'update_data_table_button' : Button(label="Update data in tabel", button_type="success"),
        'donwload_lassodata_button' : Button(label="Download CSV data", button_type="success"),
        'update_data_lasso_table_button' : Button(label="Update data in tabel", button_type="success"),
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
        'Perovskite_dimension_3D_with_2D_capping_layer' : CheckboxButtonGroup(labels = ['Perovskite. 3D with 2D capping layer'], active = []),
        'Perovskite_single_crystal' : CheckboxButtonGroup(labels = ['Perovskite. Single crystal'], active = []),
        'Stabilised_performance_measured' : CheckboxButtonGroup(labels = ['Stabilised performance measured'], active = []),
    }
    checkBoxButtonsPlotProperties = {
        'MarkerSymbols' : CheckboxButtonGroup(labels = ['Separate color by marker type'], active = []),
        }
    
    #%% Data table
    data_table = DataTable(source=sourceDataTable, columns=tableColumnsForSelectedData(), width=2500, height=800, scroll_to_selection=True, editable=True)
    data_table_lasso = DataTable(source=sourceLassoSelect, columns=tableColumnsForSelectedData(), width=2500, height=800, scroll_to_selection=True, editable=True)

    #%% Multiselects    
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
        'Cell_architecture' : MultiSelect(title="Cell_architecture", value=['All'], options = multiselectDictShort['Cell_architecture'], size = 5),       
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

    x_axis_map = {
        'Key metrics' : 'keyMetrics',
        'SQ-limit - Key metrics': 'SQ-limit',
        }

    selects = {
        'booleanCategory' : Select(title="Color by True/False filters", options=list(booleanCategory_map.keys()), value="none"),
        'x_axis' : Select(title="X-Axis", options=list(x_axis_map.keys()), value="Key metrics"),
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
        }

    sliders = {
        'legendFontSize' : Slider(start=4, end=30, value=8, step=1, title="Legend font size"),
        'plotAlpha' : Slider(start=0, end=1, value=0.5, step=0.05, title="Marker alpha"),
        'markerSize' : Slider(start=2, end=30, value=6, step=1, title="Marker size"),
        'fontSize' : Slider(start=5, end=50, value=16, step=1, title="Font size"),
        'Perovskite_band_gap' : RangeSlider(start=sliderLimits['Perovskite_band_gap'][0], end=sliderLimits['Perovskite_band_gap'][1], value=(sliderLimits['Perovskite_band_gap'][0], sliderLimits['Perovskite_band_gap'][1]), step=0.01, title="Band gap [eV]"),
        }

    daterangeSliders = {
        'Ref_publication_date' : DateRangeSlider(start=sliderLimits['Ref_publication_date'][0], end=sliderLimits['Ref_publication_date'][1], value=(sliderLimits['Ref_publication_date'][0], sliderLimits['Ref_publication_date'][1]), step=1, title="Publication date")       
        }

    #%% TextInput
    textInputControlls = {
        'excludeCellID' : TextInput(title = 'Exclude Cell ID (ID1; ID2; ID3; ...)'),
        }

    #%% Setting up callbacks ###############################################
    # Buttons
    buttons['update_data_table_button'].on_event(ButtonClick, updateDataTable)
    buttons['donwload_data_button'].on_event(ButtonClick, downloadDataTable)
    
    buttons['update_data_lasso_table_button'].on_event(ButtonClick, updateDataTableLasso)
    buttons['donwload_lassodata_button'].on_event(ButtonClick, downloadDataTableLasso)
    
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
    colorByCategory =  Div(text = "<b>Color by category</b>")
    concernignTheMeasurement = Div(text = "<b>Measurement properties</b>")
    concerningTheCell = Div(text = "<b>Sample properties</b>")
    comonAlternatives = Div(text = "<b>Most common alternatives</b>")
    instruction_1 = Paragraph(text="""Filter out all non-True values""")
    blankColumnShort = Div(text = "              ", width=200, height=100)
    aboutTheApp = Div(text = appInstructions, width=700, height=1000)

    #%% Initial update
    # Initial data update
    update()

    # Initiate the figures
    p1, p2, p3, p4 = updatePlot()

    #%% Group the input controlls
    controls1 = column(settingUpFigure,
        selects['x_axis'],
        selects['booleanCategory'],
        textInputControlls['excludeCellID'],
        sliders['plotAlpha'],
        sliders['markerSize'],
        sliders['fontSize'],
        sliders['Perovskite_band_gap'],
        buttons['donwload_figure_button'],
        hoverToolSelect,
        concernignTheMeasurement,
        daterangeSliders['Ref_publication_date'],
        rangeSliders['JV_light_intensity'],
        checkBoxButtons['JV_certified_values'],
        checkBoxButtons['Stabilised_performance_measured'],
        concerningTheCell,
        rangeSliders['Module_number_of_cells_in_module'],
        rangeSliders['Module_area_total'],
        rangeSliders['Module_area_effective'],   
        rangeSliders['Cell_area_measured'],
        )

    controls2 = column(concerningTheCell,
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
        multiselectsShort['Cell_architecture'],
        )

    controls3 = column(comonAlternatives,
        multiselectsShort['Substrate_stack_sequence'],
        multiselectsShort['ETL_stack_sequence'],
        multiselectsShort['HTL_stack_sequence'],
        multiselectsShort['Perovskite_additives_compounds'],
        multiselectsShort['Perovskite_composition_short_form'],
        multiselectsShort['Perovskite_deposition_procedure'],
        multiselectsShort['Backcontact_stack_sequence'],
        )
    controls4 = row(
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

    figureLayout = column(row(p1, p2), row(p3, p4))

    #%% Layout the controlls
    layout_tab1 = row(controls1, figureLayout, controls2, controls3, controls4)
    layout_tab2 = column(buttons['update_data_table_button'], buttons['donwload_data_button'], data_table, download_trigger)
    layout_tab3 = column(buttons['update_data_lasso_table_button'], buttons['donwload_lassodata_button'], data_table_lasso)
    layout_tab4 = column(aboutTheApp)

    #%% Make tabs with the specified layouts 
    tab1 = Panel(child=layout_tab1, title = 'Scatterplot')
    tab2 = Panel(child=layout_tab2, title = 'Data from plot in table')
    tab3 = Panel(child=layout_tab3, title = 'Selected data from plot in table')
    tab4 = Panel(child=layout_tab4, title = 'About')

    #%% Return
    return tab1, tab2, tab3, tab4
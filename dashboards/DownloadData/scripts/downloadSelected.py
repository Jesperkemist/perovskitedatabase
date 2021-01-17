# =============================================================================
# Bokeh app for downloading data from the dataabse
#  
# By Jesper Jacobsson
# 2020 10
# =============================================================================

from dateutil.relativedelta import relativedelta
import datetime
import os

from bokeh.events import ButtonClick
from bokeh.layouts import column, row
from bokeh.models import Button
from bokeh.models import CheckboxButtonGroup
from bokeh.models import CustomJS
from bokeh.models import DateRangeSlider
from bokeh.models import Div
from bokeh.models import MultiSelect
from bokeh.models import Panel
from bokeh.models import RangeSlider
from bokeh.models import Slider

import pandas as pd

from UtilityFunctions.utilityFunctions import (conectToDatabase,
                                               databaseCategoriesMostCommon,
                                               databaseCatagoriesUnique,
                                               database_details,
                                               dataManipulation, 
                                               loadData)

#%% Helper functions
def dataColumnsToUseFromTheStart():
    '''Defines the initial set of data columns'''
    return   ['Ref_ID',
              'Ref_publication_date',
              ]

#%% Seting up the dashboard and the interactivity
def interactiveEngine():
    '''Seting up the dashboard and the interactivity'''
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

        # # The Ref_ID for all selected cells
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

        # Range sliders
        activeDataColumns += [item for item in rangeSliders if rangeSliders[item].value != sliderLimits[item]]

        # Generate list of new categories
        newCategories = [item for item in activeDataColumns if item not in list(mainDataFrame.columns)]

        return newCategories

    def select_data(data):
        '''Start by selecting all data and succesivly narrow it down'''

        # Categories in dataset so far fetched from the database
        presentDataCategories = list(data.columns)

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

        #%% Return
        return data

    def update():
        ''' Uppdate the data selection'''
        # Read in more data from the database if nessesary
        columnsToDownload = getNewDataColumnsToDownload()
        updateMainDataFrame(columnsToDownload)

        # Uppdate the selection of data to plot based on the filters selected by the user
        newSelectionOfData = select_data(mainDataFrame)
        
        # Update the list of indicies for the selected data so that it can be accessed by remaining internal functions
        global_selectedRows.clear()
        global_selectedRows.extend(list(newSelectionOfData.index))

        # Display the amount of data found
        updateLogText(len(global_selectedRows))

    def updateLogText(numerOfPoints):
        '''Display the number of cells found'''
        status_update_text.text = f'The database contains <b>{numerOfPoints}</b> entries matching the selection criterias'

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
       
    #%% Main function #######################################################
    #%% Initial setup
    # Set up a conection to the database
    engine = conectToDatabase()

    # Read in data needed for the initial plot
    mainDataFrame = loadData(dataColumns = dataColumnsToUseFromTheStart(), engine = engine)

    # Ensure proper formating of the data
    mainDataFrame = dataManipulation(mainDataFrame)
    
    #Global lists to keep track of selected data, current figures, and legend and to provide access to those in sub functions
    global_selectedRows = []

    #%% Input controlls ####################################################
    # Buttons
    buttons = {
                'download_data_button' : Button(label="Download data", button_type="success"),
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
        'Stability_light_UV_filter' : CheckboxButtonGroup(labels = ['Use of UV filter'], active = [], width = 150),
        'Stability_periodic_JV_measurements' : CheckboxButtonGroup(labels = ['Periodic JV measured'], active = [], width = 150),
        'Stability_PCE_burn_in_observed' : CheckboxButtonGroup(labels = ['PCE burn in observed'], active = [], width = 150),
        'Outdoor_periodic_JV_measurements' : CheckboxButtonGroup(labels = ['Periodic JV measured'], active = [], width = 150),
        'Outdoor_PCE_burn_in_observed' : CheckboxButtonGroup(labels = ['PCE burn in observed'], active = [], width = 150),
        'Outdoor_detaild_weather_data_available' : CheckboxButtonGroup(labels = ['Weather data available'], active = [], width = 150),
        'Outdoor_spectral_data_available' : CheckboxButtonGroup(labels = ['Spectral data available'], active = [], width = 150),
        'Outdoor_irradiance_measured' : CheckboxButtonGroup(labels = ['Irradiance data available'], active = [], width = 150),
    }

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
        'Outdoor_installation_number_of_solar_tracking_axis',
        'Outdoor_location_country',
        'Outdoor_location_city',
        'Outdoor_location_climate_zone',
        'Outdoor_time_season',
        'Outdoor_potential_bias_load_condition',
        'Outdoor_protocol',     
        'Outdoor_temperature_load_condition',
        'Perovskite_additives_compounds',
        'Perovskite_composition_short_form',
        'Perovskite_deposition_aggregation_state_of_reactants',
        'Perovskite_deposition_procedure',
        'Perovskite_deposition_quenching_media',
        'Perovskite_deposition_quenching_media_additives_compounds',
        'Perovskite_deposition_solvents',
        'Perovskite_deposition_synthesis_atmosphere',
        'Substrate_stack_sequence',
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
        'Outdoor_installation_number_of_solar_tracking_axis' : MultiSelect(title="Number of tracking axis", value=['All'], options = multiselectDict['Outdoor_installation_number_of_solar_tracking_axis'], size = 3, width = 150), 
        'Outdoor_location_country' : MultiSelect(title="Country", value=['All'], options = multiselectDict['Outdoor_location_country'], size = 15),
        'Outdoor_location_city' : MultiSelect(title="City", value=['All'], options = multiselectDict['Outdoor_location_city'], size = 15),
        'Outdoor_location_climate_zone' : MultiSelect(title="Climate zoon", value=['All'], options = multiselectDict['Outdoor_location_climate_zone'], size = 5),
        'Outdoor_time_season' : MultiSelect(title="Seasons", value=['All'], options = multiselectDict['Outdoor_time_season'], size = 10),
        'Outdoor_potential_bias_load_condition' : MultiSelect(title="Potential load condition", value=['All'], options = multiselectDict['Outdoor_potential_bias_load_condition'], size = 6, width = 150), 
        'Outdoor_protocol' : MultiSelect(title="Measurement protocoll ", value=['All'], options = multiselectDict['Outdoor_protocol'], size = 10, width = 150),     
        'Outdoor_temperature_load_condition' : MultiSelect(title="Temperature load condition", value=['All'], options = multiselectDict['Outdoor_temperature_load_condition'], size = 4), 
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

    #%% Sliders
    sliderLimits ={
        'Cell_area_measured' : (0, 1000),
        'JV_light_intensity' : (0, 1000),
        'Module_area_effective' : (0, 25),
        'Module_area_total' : (0, 10000),
        'Module_number_of_cells_in_module' : (1, 100),
        'Perovskite_band_gap' : (1, 3.5),
        'Outdoor_installation_tilt' : (0, 90),
        'Outdoor_installation_cardinal_direction' : (0, 360),
        'Outdoor_PCE_initial_value' : (0, 25),
        'Outdoor_temperature_range_max' : (-70, 100),
        'Ref_publication_date' : (min(mainDataFrame['Ref_publication_date']) - relativedelta(months=1), max(mainDataFrame['Ref_publication_date']) + relativedelta(months=1)),
        'Stability_light_intensity' : (0, 1000),
        'Stability_relative_humidity_average_value' : (0, 100),
        'Stability_PCE_initial_value' : (0, 25),
        'Stability_temperature_range_max' : (-70, 100),
        }

    rangeSliders = {
        'Cell_area_measured' : RangeSlider(start=sliderLimits['Cell_area_measured'][0], end=sliderLimits['Cell_area_measured'][1], value=(sliderLimits['Cell_area_measured'][0], sliderLimits['Cell_area_measured'][1]), step=0.1, title="Active cell area [cm^2]"),
        'JV_light_intensity' : RangeSlider(start=sliderLimits['JV_light_intensity'][0], end=sliderLimits['JV_light_intensity'][1], value=(90, 110), step=0.1, title="Light intensity [mW/cm^2]"),
        'Module_number_of_cells_in_module' : RangeSlider(start=sliderLimits['Module_number_of_cells_in_module'][0], end=sliderLimits['Module_number_of_cells_in_module'][1], value=(sliderLimits['Module_number_of_cells_in_module'][0], sliderLimits['Module_number_of_cells_in_module'][1]), step=1, title="Number of cells in module"),
        'Module_area_effective' : RangeSlider(start=sliderLimits['Module_area_effective'][0], end=sliderLimits['Module_area_effective'][1], value=(sliderLimits['Module_area_effective'][0], sliderLimits['Module_area_effective'][1]), step=1, title="Active Module area [cm^2]"),
        'Module_area_total' : RangeSlider(start=sliderLimits['Module_area_total'][0], end=sliderLimits['Module_area_total'][1], value=(sliderLimits['Module_area_total'][0], sliderLimits['Module_area_total'][1]), step=1, title="Total Module area [cm^2]"),
        'Perovskite_band_gap' : RangeSlider(start=sliderLimits['Perovskite_band_gap'][0], end=sliderLimits['Perovskite_band_gap'][1], value=(sliderLimits['Perovskite_band_gap'][0], sliderLimits['Perovskite_band_gap'][1]), step=0.01, title="Band gap [eV]"),
        'Outdoor_installation_tilt' : RangeSlider(start=sliderLimits['Outdoor_installation_tilt'][0], end=sliderLimits['Outdoor_installation_tilt'][1], value=(sliderLimits['Outdoor_installation_tilt'][0], sliderLimits['Outdoor_installation_tilt'][1]), step=1, title="Tilt of instalation [deg]"),
        'Outdoor_installation_cardinal_direction' : RangeSlider(start=sliderLimits['Outdoor_installation_cardinal_direction'][0], end=sliderLimits['Outdoor_installation_cardinal_direction'][1], value=(sliderLimits['Outdoor_installation_cardinal_direction'][0], sliderLimits['Outdoor_installation_cardinal_direction'][1]), step=1, title="Cardinal direction"),
        'Outdoor_PCE_initial_value' : RangeSlider(start=sliderLimits['Outdoor_PCE_initial_value'][0], end=sliderLimits['Outdoor_PCE_initial_value'][1], value=(sliderLimits['Outdoor_PCE_initial_value'][0], sliderLimits['Outdoor_PCE_initial_value'][1]), step=1, title="Initial cell efficinecy [%]"),
        'Outdoor_temperature_range_max' : RangeSlider(start=sliderLimits['Outdoor_temperature_range_max'][0], end=sliderLimits['Outdoor_temperature_range_max'][1], value=(sliderLimits['Outdoor_temperature_range_max'][0], sliderLimits['Outdoor_temperature_range_max'][1]), step=1, title="Outdoor temperature (max) [deg. C]"),
        'Stability_light_intensity' : RangeSlider(start=sliderLimits['Stability_light_intensity'][0], end=sliderLimits['Stability_light_intensity'][1], value=(sliderLimits['Stability_light_intensity'][0], sliderLimits['Stability_light_intensity'][1]), step=1, title="Light Intensity [mW/cm^2]"),
        'Stability_relative_humidity_average_value' : RangeSlider(start=sliderLimits['Stability_relative_humidity_average_value'][0], end=sliderLimits['Stability_relative_humidity_average_value'][1], value=(sliderLimits['Stability_relative_humidity_average_value'][0], sliderLimits['Stability_relative_humidity_average_value'][1]), step=1, title="Relative humidity [%]"),
        'Stability_PCE_initial_value' : RangeSlider(start=sliderLimits['Stability_PCE_initial_value'][0], end=sliderLimits['Stability_PCE_initial_value'][1], value=(sliderLimits['Stability_PCE_initial_value'][0], sliderLimits['Stability_PCE_initial_value'][1]), step=1, title="Initial cell efficinecy [%]"),
        'Stability_temperature_range_max' : RangeSlider(start=sliderLimits['Stability_temperature_range_max'][0], end=sliderLimits['Stability_temperature_range_max'][1], value=(sliderLimits['Stability_temperature_range_max'][0], sliderLimits['Stability_temperature_range_max'][1]), step=1, title="Stability temperature (max) [deg. C]"),
        }

    sliders = {
        'legendFontSize' : Slider(start=4, end=30, value=8, step=1, title="Legend font size"),
        'plotAlpha' : Slider(start=0, end=1, value=0.6, step=0.05, title="Marker alpha"),
        'markerSize' : Slider(start=2, end=30, value=8, step=1, title="Marker size"),
        'xAxisLogStart' : Slider(start=-5, end=5, value=-1, step=1, title="X-axis. log scale lower limit"),
        'yAxisLogStart' : Slider(start=-5, end=5, value=-1, step=1, title="Y-axis. log scale lower limit"),
        'fontSize' : Slider(start=5, end=50, value=16, step=1, title="Font size"),
        }

    daterangeSliders = {
        'Ref_publication_date' : DateRangeSlider(start=sliderLimits['Ref_publication_date'][0], end=sliderLimits['Ref_publication_date'][1], value=(sliderLimits['Ref_publication_date'][0], sliderLimits['Ref_publication_date'][1]), step=1, title="Publication date")       
        }
 
    #%% Setting up callbacks ###############################################
    # Buttons
    buttons['download_data_button'].on_event(ButtonClick, downloadDataTable)

    # Checkboxbuttons
    for item in checkBoxButtons:
        checkBoxButtons[item].on_change('active', lambda attr, old, new: update())

    # Multiselects long
    for item in multiselects:
        multiselects[item].on_change('value', lambda attr, old, new: update())

    # Multiselects short
    for item in multiselectsShort:
        multiselectsShort[item].on_change('value', lambda attr, old, new: update())

    # Sliders
    daterangeSliders['Ref_publication_date'].on_change('value_throttled', lambda attr, old, new: update())

    for item in sliders:
        sliders[item].on_change('value_throttled', lambda attr, old, new: update())

    for item in rangeSliders:
        rangeSliders[item].on_change('value_throttled', lambda attr, old, new: update())

   #%% Set up a dummy glyph which when triggered runs a javascript based function for downloading selected data
    filename = 'Perovskite_database_content.csv'
    download_trigger = Div(text="1", visible=False)
    callback = CustomJS(args=dict(data={}, userFilename=filename),
                        code=open(os.path.join(os.path.dirname(__file__), "download.js")).read())
    download_trigger.js_on_change('text', callback)

    #%% Text fields
    instruction_1 =  Div(text = "Download data from the database based on the chosen filters", width=300)
    status_update_text = Div(text = '', width=300, height=1000)
    comonAlternatives = Div(text = "<b>Most common alternatives</b>")

    #%% Display the amount of data found
    updateLogText(len(mainDataFrame))

    #%% Group the input controlls
    controls0 = column(instruction_1, buttons['download_data_button'], status_update_text)

    controls1 = column(
        daterangeSliders['Ref_publication_date'],
        rangeSliders['JV_light_intensity'],
        rangeSliders['Module_number_of_cells_in_module'],
        rangeSliders['Module_area_total'],
        rangeSliders['Module_area_effective'],   
        rangeSliders['Cell_area_measured'],
        rangeSliders['Perovskite_band_gap'],
        checkBoxButtons['JV_certified_values'],
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
        checkBoxButtons['Stabilised_performance_measured'],
        )

    controls2 = column(comonAlternatives,
        multiselectsShort['Cell_architecture'],                       
        multiselectsShort['Perovskite_composition_short_form'],
        multiselectsShort['ETL_stack_sequence'],
        multiselectsShort['HTL_stack_sequence'],
        )

    controls3 = column(comonAlternatives,
        multiselectsShort['Perovskite_deposition_procedure'],
        multiselectsShort['Substrate_stack_sequence'],
        multiselectsShort['Backcontact_stack_sequence'],
        multiselectsShort['Perovskite_additives_compounds'],       
        )

    controls5 = column(Div(text = "<b>Stability</b>"),
        multiselects['Stability_protocol'],
        multiselects['Stability_potential_bias_load_condition'],
        multiselects['Stability_atmosphere'],
        multiselects['Stability_light_spectra'],
        multiselects['Stability_light_source_type'], 
        )

    controls6 = column(Div(text = "<b>Stability</b>"),
        checkBoxButtons['Stability_light_UV_filter'],
        checkBoxButtons['Stability_periodic_JV_measurements'],
        checkBoxButtons['Stability_PCE_burn_in_observed'],
        rangeSliders['Stability_PCE_initial_value'],
        rangeSliders['Stability_light_intensity'],  
        rangeSliders['Stability_temperature_range_max'],
        rangeSliders['Stability_relative_humidity_average_value'],
        multiselects['Stability_light_load_condition'],        
        multiselects['Stability_temperature_load_condition'],
        multiselects['Stability_relative_humidity_load_conditions'],
        multiselects['Stability_light_illumination_direction'],
        )

    controls7 = column(Div(text = "<b>Outdoor testing</b>"),
        multiselects['Outdoor_protocol'],
        multiselects['Outdoor_potential_bias_load_condition'],
        multiselects['Outdoor_installation_number_of_solar_tracking_axis'],
        )

    controls8 = column(Div(text = "<b>Outdoor testing</b>"),
        checkBoxButtons['Outdoor_periodic_JV_measurements'],
        checkBoxButtons['Outdoor_PCE_burn_in_observed'], 
        checkBoxButtons['Outdoor_detaild_weather_data_available'],
        checkBoxButtons['Outdoor_spectral_data_available'],
        checkBoxButtons['Outdoor_irradiance_measured'],
        rangeSliders['Outdoor_PCE_initial_value'], 
        rangeSliders['Outdoor_temperature_range_max'],
        rangeSliders['Outdoor_installation_tilt'], 
        rangeSliders['Outdoor_installation_cardinal_direction'],       
        multiselects['Outdoor_temperature_load_condition'],
        )

    controls9 =column(Div(text = "<b>Outdoor testing</b>"),
            multiselects['Outdoor_location_climate_zone'],
            multiselects['Outdoor_time_season'],
            multiselects['Outdoor_location_country'],
            multiselects['Outdoor_location_city'],
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

    #%% Layout the controlls
    layout_tab1 = row(controls0, controls1, controls2, controls3, controls5, controls6, controls7, controls8, controls9, controls4, download_trigger)

    #%% Make tabs with the specified layouts
    tab1 = Panel(child=layout_tab1, title = 'Download selected data')

    #%%
    return tab1
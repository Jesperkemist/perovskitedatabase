# =============================================================================
# Bokeh app for downloading data from the dataabse
#  
# By Jesper Jacobsson
# 2020 10
# =============================================================================

import os
import pathlib

from bokeh.events import ButtonClick
from bokeh.layouts import column, row
from bokeh.models import Button
from bokeh.models import CustomJS
from bokeh.models import Div
from bokeh.models import Panel

import pandas as pd

from UtilityFunctions.utilityFunctions import (conectToDatabase, database_details)


#%% Helper functions
def getAppInstructions(fileName = 'Instructions.txt'):
    '''Read in text file with instructions'''

    #The file shoud be placed in the same folder as the main script
    path = pathlib.Path(__file__).parent.absolute()

    # Read file
    filePath = os.path.join(path, fileName)
    with open(filePath, 'r') as f:
        appInstructions = f.read()

    return appInstructions

#%% Seting up the dashboard and the interactivity
def interactiveEngine():
    '''Seting up the dashboard and the interactivity'''
    #%% Internal helper functions #########################################
    def download_Data_via_Json():
        '''Activate the dummy glyph that trigers java script for downloading data '''          
        download_trigger.text = str(int(download_trigger.text) + 1)
 
    def downloadDataFromDatabase(event):
        '''Prepare data for download'''
        # Uppdate status text
        updateStatusText(text = f'Conection to the database is established')

        # Fetch table and scheema names of the database
        bd_details = database_details()
        table = bd_details['table']
        schema = bd_details['schema']

        # Fetch all data from the database 
        query = f'''select * from {schema}.{table}'''
        query_results = pd.read_sql_query(sql = query, con = engine)

        # Download resutls
        if len(query_results) != 0:

            # Make the data accesible to download
            callback.args['userFilename'] = 'Perovskite_database_content_all_data.csv'
            callback.args['data'] = query_results.to_csv(header=True, index=False)

            # Uppdate status text      
            updateStatusText(text = f' Data for {len(query_results)} devices have been fetched from the database')

            download_Data_via_Json()

    def updateStatusText(text):
        '''Update status text '''
        status_update_text.text = text


    #%% Main function #######################################################
    # Set up a conection to the database
    engine = conectToDatabase()

    #%% Input controlls ####################################################
    # Buttons
    buttons = {'download_data_button' : Button(label="Download all data in the database", button_type="success"),}
    
    #%% Setting up callbacks ###############################################
    buttons['download_data_button'].on_event(ButtonClick, downloadDataFromDatabase)

    #%% Set up a dummy glyph which when triggered runs a javascript based function for downloading selected data
    filename = 'Perovskite_database_content_all_data.csv'
    download_trigger = Div(text="1", visible=False)
    callback = CustomJS(args=dict(data={}, userFilename=filename),
                        code=open(os.path.join(os.path.dirname(__file__), "download.js")).read())
    download_trigger.js_on_change('text', callback)

    #%% Read in the information about the app that will be displayd as a separate tab
    appInstructions = getAppInstructions(fileName = 'Instructions.html')

    #%% Text fields
    aboutTheApp = Div(text = appInstructions, width=700, height=1000)
    instruction_1 =  Div(text = "Download all data in the database. Can take a few minutes", width=700)
    status_update_text = Div(text = '', width=700, height=1000)

    #%% Layout the controlls
    layout_tab1 = column(aboutTheApp)
    layout_tab2 = column(instruction_1, buttons['download_data_button'], status_update_text, download_trigger)

    #%% Make tabs with the specified layouts
    tab1 = Panel(child=layout_tab1, title = 'About')
    tab2 = Panel(child=layout_tab2, title = 'Download all data')

    #%%
    return tab1, tab2
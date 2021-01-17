# =============================================================================
# Bokeh app for downloading data from the dataabse
#  
# By Jesper Jacobsson
# 2020 10
# =============================================================================

import os

from bokeh.layouts import column, row
from bokeh.models import CustomJS
from bokeh.models import Div
from bokeh.models import Panel
from bokeh.models import TextInput

import pandas as pd

from UtilityFunctions.utilityFunctions import (conectToDatabase, database_details)


#%% Helper functions

#%% Seting up the dashboard and the interactivity
def interactiveEngine():
    '''Seting up the dashboard and the interactivity'''

    #%% Internal helper functions
    def downloadDOI_Data_via_Json():
        '''Activate the dummy glyph that trigers java script for downloading data '''          
        download_trigger.text = str(int(download_trigger.text) + 1)

    def update():
        '''Run the download data rutine'''
        # Uppdate status text
        updateStatusText(text = f'Conection to the database is established')

        # Fetch table and scheema names of the database
        bd_details = database_details()
        table = bd_details['table']
        schema = bd_details['schema']

        # User input
        DOInumber = textInputControlls['DOI'].value

        # Format the DOI number
        DOInumber = str(DOInumber)
        DOInumber = DOInumber.strip()
        DOInumber = DOInumber.replace('https://doi.org/', '')
        DOInumber = DOInumber.replace('http://doi.org/', '')
        DOInumber = DOInumber.replace('doi.org/', '')

        # Read in all data for the specified DOI number
        query = f''' SELECT * FROM singeljunction.data WHERE data."Ref_DOI_number" = '{DOInumber}' '''
        query_results = pd.read_sql_query(query, engine)

        # Download resutls
        if len(query_results) != 0:
            # Make the data accesible to download
            callback.args['userFilename'] = 'Perovskite_database_content_by_DOI.csv'
            callback.args['data'] = query_results.to_csv(header=True, index=False)

           # Uppdate status text
            updateStatusText(text = f'The database contains {len(query_results)} cells from paper with DOI: {DOInumber}')

            downloadDOI_Data_via_Json()

        else:
            # Uppdate status text
            updateStatusText(text = f'The database contains no solar cell data from paper with DOI: {DOInumber}')


    def updateStatusText(text):
        '''Update status text '''
        status_update_text.text = text

    #%% Main function #######################################################
    # Set up a conection to the database
    engine = conectToDatabase()

    #%% Input controlls ####################################################
    # TextInput
    textInputControlls = {
        'DOI' : TextInput(title = 'DOI number e.g. 10.1039/C6EE00030D'),
        }
 
    #%% Setting up callbacks ###############################################
    # Text input
    textInputControlls['DOI'].on_change('value', lambda attr, old, new: update())

    #%% Set up a dummy glyph which when triggered runs a javascript based function for downloading selected data
    filename = 'Perovskite_database_content_by_DOI.csv'
    download_trigger = Div(text="1", visible=False)
    callback = CustomJS(args=dict(data={}, userFilename=filename),
                        code=open(os.path.join(os.path.dirname(__file__), "download.js")).read())
    download_trigger.js_on_change('text', callback) 

    #%% Text fields
    instruction_1 =  Div(text = "Download data from the database. Can take a few minutes", width=700)
    status_update_text = Div(text = '', width=700, height=1000)

    #%% Layout the controlls
    layout_tab1 = column(instruction_1, textInputControlls['DOI'], status_update_text, download_trigger)

    #%% Make tabs with the specified layouts
    tab1 = Panel(child=layout_tab1, title = 'Download data based on DOI')

    #%%
    return tab1
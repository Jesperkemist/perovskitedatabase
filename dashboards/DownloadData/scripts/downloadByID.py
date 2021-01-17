# =============================================================================
# Bokeh app for downloading data from the dataabse
#  
# By Jesper Jacobsson
# 2020 10
# =============================================================================

import base64
import os

from bokeh.events import ButtonClick
from bokeh.layouts import column
from bokeh.models import CustomJS
from bokeh.models import Div
from bokeh.models import FileInput
from bokeh.models import Panel
from bokeh.models import TextInput

import pandas as pd

from UtilityFunctions.utilityFunctions import (conectToDatabase, database_details, is_int)

#%% Helper functions
def formatInputString(inputString):
    '''Take text input and returns tuple with integers found in the comma separated text input '''
    # Format the ID number
    if type(inputString) == bytes:
            inputString = str(inputString.decode())
    else:
        inputString = str(inputString)

    inputString = inputString.replace(" ","") 

    # Split on (,)
    inputStringList = inputString.split(',')

    # Convert to list of numbers
    IDnumbers = []
    for ID in inputStringList:
        if is_int(ID):
            IDnumbers.append(int(ID))

    # Convert to string
    IDnumbersString = [str(x) for x in IDnumbers]
    IDnumbersString = '(' + ','.join(IDnumbersString) + ')'

    return IDnumbersString


#%% Seting up the dashboard and the interactivity
def interactiveEngine():
    '''Seting up the dashboard and the interactivity'''
    #%% Internal helper functions #########################################
    def download_Data_via_Json():
        '''Activate the dummy glyph that trigers java script for downloading data '''          
        download_trigger.text = str(int(download_trigger.text) + 1)

    def downloadData(IDnumbers):
        '''Run the download data rutine'''
        # Uppdate status text
        updateStatusText(text = f'Conection to the database is established')

        # Fetch table and scheema names of the database
        bd_details = database_details()
        table = bd_details['table']
        schema = bd_details['schema']

        # Read in all data for the specified ID numbers
        query = f''' SELECT * FROM singeljunction.data WHERE data."Ref_ID" in {IDnumbers} '''
        query_results = pd.read_sql_query(query, engine)

        # Download resutls
        if len(query_results) != 0:
            # Make the data accesible to download
            callback.args['userFilename'] = 'Perovskite_database_content_by_ID.csv'
            callback.args['data'] = query_results.to_csv(header=True, index=False)

            # Uppdate status text
            updateStatusText(text = f'The database contains {len(query_results)} entries coresponding to ID numbers: {IDnumbers}')

            download_Data_via_Json()

        else:
            # Uppdate status text
            updateStatusText(text = f'The database contains no entries with iD: {IDnumbers}')

    def fileInputUpdate(attr, old, new):
        '''Read textfile from user'''

        # Read in the text file
        inputString = base64.b64decode(file_input.value)

        # Extract numbers from input
        IDnumbers = formatInputString(inputString)

        # Run the data dowload rutine
        downloadData(IDnumbers)

    def textInputUpdate():
        '''On text input '''
        # User input
        inputString = textInputControlls['ID'].value
        
        # Extract numbers from input
        IDnumbers = formatInputString(inputString)

        # Run the data dowload rutine
        downloadData(IDnumbers)

    def updateStatusText(text):
        '''Update status text '''
        status_update_text.text = text

    #%% Main function #######################################################
    # Set up a conection to the database
    engine = conectToDatabase()

    #%% Input controlls ####################################################
    # File inputs
    file_input = FileInput(accept=".txt")

    # TextInput
    textInputControlls = {
        'ID' : TextInput(title = 'Download data based on database id (Ref_ID). Give ID as a comma separated list'),
        }
     
    #%% Setting up callbacks ###############################################
    # Text input
    textInputControlls['ID'].on_change('value', lambda attr, old, new: textInputUpdate())

    # File inputs
    file_input.on_change('value', fileInputUpdate)

    #%% Set up a dummy glyph which when triggered runs a javascript based function for downloading selected data
    filename = 'Perovskite_database_content_by_ID.csv'
    download_trigger = Div(text="1", visible=False)
    callback = CustomJS(args=dict(data={}, userFilename=filename),
                        code=open(os.path.join(os.path.dirname(__file__), "download.js")).read())
    download_trigger.js_on_change('text', callback)    

    #%% Text fields
    instruction_1 =  Div(text = "Download data from the database based in database ID (Ref_ID). Give values as a comma separated list, either in the text box below or as a .txt file", width=700)
    status_update_text = Div(text = '', width=700, height=1000)

    #%% Layout the controlls
    layout_tab1 = column(instruction_1, textInputControlls['ID'], file_input, status_update_text, download_trigger)

    #%% Make tabs with the specified layouts
    tab1 = Panel(child=layout_tab1, title = 'Download data based on database ID')

    #%%
    return tab1

# =============================================================================
#  Bokeh app for changing values in the database that are wrong 
#   
# By Jesper Jacobsson
# 2020 12
# =============================================================================

from datetime import date
import os

from bokeh.models import Button
from bokeh.events import ButtonClick
from bokeh.layouts import column
from bokeh.models import CustomJS
from bokeh.models import Div
from bokeh.models import Panel
from bokeh.models import Select
from bokeh.models import TextInput

import pandas as pd

from sqlalchemy.orm import sessionmaker, scoped_session

from UtilityFunctions.utilityFunctions import (conectToDatabase, database_details)
from UtilityFunctions.dataColumns import csv_data_columns_complet
from UtilityFunctions.updateDataValidation import cleaningFuncions

from dotenv import load_dotenv
load_dotenv()


#%% Seting up the dashboard and the interactivity
def interactiveEngine():
    '''Seting up the dashboard and the interactivity'''
    #%% Internal helper functions #########################################

    def databaseID_Excist():
        '''Check if database ID excist'''
        input = str(textInput['ID'].value) 
        ID_string = '(' + input + ')'

        # If user did not wrote aneyting in the ID field
        if len(input) == 0:
            updateStatusText('No database ID given')
            return False

        # Fetch table and scheema names of the database
        bd_details = database_details()
        table = bd_details['table']
        schema = bd_details['schema']

        # Query the database for the specified ID_number
        query = f''' SELECT "Ref_ID" FROM {schema}.{table} WHERE data."Ref_ID" in {ID_string} '''
        query_results = pd.read_sql_query(query, engine)

        # If no such cell in the database
        if len(query_results) == 0:
            updateStatusText(f'Database contain no cell with ID: {input}')
            return False

        return True

    def checkIfDataCategoryIsGiven():
        '''Check if a data category is chosen '''
        # Check if database column is chosen
        if Selects['column'].value == 'none':
            updateStatusText('No database column is specified. Data can only be updated if a database column is chosen')
            return False
        else:
            return True

    def checkIfNameIsGiven():
        '''Check if user have stated his/her name '''
        name = str(textInput['Your_name'].value)

        if len(name) == 0:
            updateStatusText('No name was given. Data vill only be updated if you state your name')
            return False


        updateStatusText('Name was given')
        return True

    def checkIfNewDataIsGiven():
        '''Check if new data is given'''

        newValue = str(textInput['new_value'].value) 

        # If user did not wrote aneyting in the old value field
        if len(newValue) == 0:
            updateStatusText('No new value is given. Data vill only be updated if a new value is given')
            return False

        return True

    def checkOldValue():
        '''check if the old value is the same as that given in the database '''
        input = str(textInput['ID'].value) 
        ID_string = '(' + input + ')'

        oldValue = str(textInput['Old_value'].value)
        oldValue_string = '(' + oldValue + ')' 

        column = Selects['column'].value

        # If user did not wrote aneyting in the old value field
        if len(oldValue) == 0:
            updateStatusText('No old value is given. Data vill only be updated if the old value is equal to the value in the database')
            return False

        # Fetch table and scheema names of the database
        bd_details = database_details()
        table = bd_details['table']
        schema = bd_details['schema']

        # Query the database for the specified value
        query = f''' SELECT "{column}" FROM {schema}.{table} WHERE data."Ref_ID" in {ID_string} '''
        query_results = pd.read_sql_query(query, engine)
        oldValueInDtabase = query_results.loc[0,column]

        # Check if the value was empty
        if oldValue.lower() == 'empty':
            if str(oldValueInDtabase) != 'None':
                updateStatusText(f'Value of {column} at database ID {input} is not empty but {oldValueInDtabase}')
                return False

        # Check if values agree
        if oldValue != str(oldValueInDtabase):
            updateStatusText(f'Value of {column} at database ID {input} is not {oldValue} but {oldValueInDtabase}')
            return False

        updateStatusText(f'Value of {column} at dataabse ID {input} is indead {oldValue} as you stated:{oldValueInDtabase}')

        return True

    def validateNewData():
        '''Run the data cleaning rutine on the data given'''
        newValue = str(textInput['new_value'].value) 

        # Check if the new value is empty
        if newValue.lower() == 'empty':
            newValue = ''

        # Generate a pandas datafram with the new value
        dfNew = pd.DataFrame()
        dfNew[Selects['column'].value] = [newValue]

        # Run the data update rutine on the new value
        newValueCleaned = cleaningFuncions[Selects['column'].value](dfNew[Selects['column'].value])

        return newValueCleaned

    def saveUpdateToFile():
        '''Save update information to file'''

        # Check if file excist. If not create it
        # The top directory of the app
        root = os.path.abspath(os.getcwd())

        # Check if directories excist. If not create them
        up = os.path.join(root, 'uploads')
        if os.path.exists(up) == False:
            os.mkdir(up)

        folder = os.path.join(root, 'uploads', 'databaseCorections')
        if os.path.exists(folder) == False:
            os.mkdir(folder)

        # corection file
        corectionFile = os.path.join(root, 'uploads', 'databaseCorections', 'corectionFile.txt')

        # Create file if it does not excist
        if os.path.exists(corectionFile) == False:
            file = open(corectionFile,"w+")

            header = 'Date of corection, Database ID, Database column, Old value, New vaue, Name of person doing the corection\n'
            
            file.write(header)
            file.close()
            
        # save new data
        with open(corectionFile, 'a') as file:
            dataList = [str(date.today()), str(textInput['ID'].value), Selects['column'].value, str(textInput['Old_value'].value), str(textInput['new_value'].value), str(textInput['Your_name'].value)]
            dataString = ','.join(dataList) + '\n'
            
            file.write(dataString)
            file.close

    def updateDatabase(newData):
        '''Insert the new value in the database'''

        # Fetch table and scheema names of the database
        bd_details = database_details()
        table = bd_details['table']
        schema = bd_details['schema']

        input = str(textInput['ID'].value) 
        ID_string = '(' + input + ')'

        column = Selects['column'].value

        dataToInsert = str(newData[0])

        # The SQL update statement
        sql = f'''UPDATE {schema}.{table} SET "{column}" = '{dataToInsert}' WHERE data."Ref_ID" in {ID_string}'''

        # Create a session and run the sql comand
        db = scoped_session(sessionmaker(bind=engine))
        db.execute(sql)
        db.commit()
        db.close()

        updateStatusText(f'Value of {Selects["column"].value} at database ID {textInput["ID"].value} is {textInput["Old_value"].value} and has now been replaced with {newData[0]} by {str(textInput["Your_name"].value)}')

    def submittNewValue(event):
        '''Runs rutine for updating values'''

        # Chech if database ID excist
        if databaseID_Excist() == False:            
            return False

        # Check if data category is given
        if checkIfDataCategoryIsGiven() == False:
            return False

        # Check if old value is corect
        if checkOldValue() == False:
            return False

        # check if Name is given
        if checkIfNameIsGiven() == False:
            return False

        # Check if new data is given
        if checkIfNewDataIsGiven() == False:
            return False

        # Validate that new data is corecly formated
        newData = validateNewData()

        updateStatusText(f'Value of {Selects["column"].value} at database ID {textInput["ID"].value} is {textInput["Old_value"].value} and will be replaced with {newData[0]} by {str(textInput["Your_name"].value)}')

        # Uppdate the database with the new value
        updateDatabase(newData)

        # Save corection to file
        saveUpdateToFile()

    def updateStatusText(text):
        '''Update status text '''
        status_update_text.text = text

    #%% Main function #######################################################
    # Set up a conection to the database
    engine = conectToDatabase()

    #%% Input controlls ####################################################
    # Buttons
    buttons = {
    'submittNewValue' : Button(label="Submitt new value", button_type="success"),
    }

    # Selects
    categories = csv_data_columns_complet()
    categories.remove('Ref_ID')
    categories.sort()
    categories.insert(0,'none')

    Selects = {
        'column' : Select(title="Database column", options=categories, value="none"),
    }

    # TextInput
    textInput= {
        'ID' : TextInput(title = 'Database ID. Required field'),
        'Old_value' : TextInput(title = 'Old value. Required field. If no value in the database, write: Empty'),
        'new_value' : TextInput(title = 'New value. Required field. If the field should have no value, write: Empty'),
        'Your_name' : TextInput(title = 'Your name. Required field. For transparency and traseability'),
        }


    #%% Setting up callbacks ###############################################
    # Buttons
    buttons['submittNewValue'].on_event(ButtonClick, submittNewValue)


    #%% Text fields
    instruction_1 =  Div(text = "If you find a datapoint that is wrong in the database, you can correct it here by stating both the old and the new value ", width=700)
    status_update_text = Div(text = '', width=700, height=1000)

    #%% Layout the controlls
    layout_tab1 = column(instruction_1, 
                         textInput['ID'],
                         Selects['column'],
                         textInput['Old_value'],
                         textInput['new_value'],
                         textInput['Your_name'],
                         buttons['submittNewValue'], 
                         status_update_text)

    #%% Make tabs with the specified layouts
    tab1 = Panel(child=layout_tab1, title = 'Correct a value in the database')

    #%%
    return tab1
# =============================================================================
# Bokeh app for reading in data from user and writing it to the database
#  
# By Jesper Jacobsson
# 2020 10
# =============================================================================

#%% Imports
import base64
import datetime
import io
import os
import pathlib
import shutil
import sys

#from bokeh.events import ButtonClick
#from bokeh.io import curdoc
from bokeh.layouts import column, row
#from bokeh.models import Button
from bokeh.models import Div
from bokeh.models import FileInput
from bokeh.models import Panel
from bokeh.models.widgets import Paragraph
#from bokeh.models.widgets import Tabs
#import numpy as np
import pandas as pd

import UtilityFunctions.CleanDataV5 as cleanData
import UtilityFunctions.CompleatDataV5 as compleatData
import UtilityFunctions.dataBaseFunctions as dbf
from UtilityFunctions.utilityFunctions import (conectToDatabase, database_details, dataCitationData, dataCleaning, dataDeriveNewColumns, dataMergeData)

# Test commet to see if it is the right version that is pushed to github

#%% Helper functions
def backupToStorage(filePaths):
    '''Backup files to centralised storage '''

    # TODO
    # Save original file
    # Save compleated data

    return 1

#%% to remove
#def dataCitationData(DOInumbers, defaultDate, defaultAuthor, DOIPath, filePaths):
#    '''Extract citation data from CrossRef based on the DOI number '''

#    # Get citation data
#    referenceData = compleatData.citationData(DOInumbers, defaultDate, defaultAuthor, DOIPath)
    
#    # Save the citation data
#    try:
#        #referenceData.to_excel(filePaths['dataCitationFilePath'], index = False)
#        referenceData.to_csv(filePaths['dataCitationFilePath'], index = False)
#        print(f'Saved citation data')
#    except:
#        print(f'Failed to save citation data based on: {filePaths["dataOriginalFileName"]}')

#    return referenceData

#def dataCleaning(userData, filePaths):
#    '''Run a data cleaning and formating rutine on the data'''

#    # Clean the data
#    try:
#        cleanedData = cleanData.cleanUserData(userData, fileName = filePaths['dataOriginalFileName'])
#    except:
#        print(f'Failed to clean data for: {filePaths["dataOriginalFileName"]}')

#    # Save cleaned data
#    try:
#        #cleanedData.to_excel(filePaths['dataCleanedFilePath'], index = False)
#        cleanedData.to_csv(filePaths['dataCleanedFilePath'], index = False)
#        print(f'Saved cleaned data')
#    except:
#        try:
#            cleanedData = cleanedData.applymap(lambda x: x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x)
#            #cleanedData.to_excel(filePaths['dataCleanedFilePath'], index = False)
#            cleanedData.to_csv(filePaths['dataCleanedFilePath'], index = False)
#            print(f'Saved cleaned data after unicode escape')
#        except:
#            print(f'Failed to saved clean data at {filePaths["dataOriginalFileName"]}')

#    return cleanedData

#def dataDeriveNewColumns(cleanedData, filePaths):
#    '''Deriv data for aditional columns based on the cleaned data'''

#    # Derive the data
#    try:
#        derivedData = compleatData.DerivedtUserData(cleanedData, fileName = filePaths['dataOriginalFileName'])
#    except:
#        print(f'Failed to derive additional data based on: {filePaths["dataOriginalFileName"]}')

#    # Save the derived data
#    try:
#        #derivedData.to_excel(filePaths['dataDerivedFilePath'], index = False)
#        derivedData.to_csv(filePaths['dataDerivedFilePath'], index = False)
#        print(f'Saved derived data')
#    except:
#        print(f'Failed to save derived aditional data based on: {filePaths["dataOriginalFileName"]}')

#    return derivedData

#def dataMergeData(cleanedData, derivedData, citationData, filePaths):
#    '''Merge cleanedData, derivedData and citationData into one document ready for databse uploading'''

#    # Merge the data
#    try:
#        mergedData = compleatData.mergeData(cleanedData, derivedData, citationData)
#    except:
#        print(f'Failed to merged data into one file for: {filePaths["dataOriginalFileName"]}')

#    # Save the merged data
#    try:
#        #mergedData.to_excel(filePaths['dataCompleatFilePath'], index = False)
#        mergedData.to_csv(filePaths['dataCompleatFilePath'], index = False)
#        print(f'Saved compleated data')
#    except:
#        print(f'Failed to save compleated data based on: {filePaths["dataOriginalFileName"]}')

#    return mergedData
dummy = 1
#%%
def defaultFilePaths():
    '''Predifined file paths '''
    # The top directory of the app
    root = os.path.abspath(os.getcwd())

    filePaths = {
        'dataOriginalDirectoryPath' : os.path.join(root, 'uploads', 'dataOriginal'),
        'dataCleanedDirectoryPath' : os.path.join(root, 'uploads', 'dataCleaned'),
        'dataCompleatDirectoryPath' : os.path.join(root, 'uploads', 'dataCompleat'),
        'dataDerivedDirectoryPath' : os.path.join(root, 'uploads', 'dataDerived'),
        'dataCitationDirectoryPath' : os.path.join(root, 'uploads', 'dataCitation'),
        'dataLogDirectoryPath' : os.path.join(root, 'uploads', 'dataLogFiles'),
        'DOIPath': os.path.join(root, 'uploads', 'DOI_saved_files'),                  
            }

    # Check if directories excist. If not create them
    up = os.path.join(root, 'uploads')
    if os.path.exists(up) == False:
        os.mkdir(up)

    newpaths = ['dataOriginalDirectoryPath', 'dataCleanedDirectoryPath', 'dataCompleatDirectoryPath', 'dataDerivedDirectoryPath', 'dataCitationDirectoryPath', 'dataLogDirectoryPath']
    for item in newpaths:
        if os.path.exists(filePaths[item]) == False:
            os.mkdir(filePaths[item])

    return filePaths

def getAppInstructions(fileName = 'Instructions.txt'):
    '''Read in text file with instructions'''

    #The file shoud be placed in the same folder as the main script
    path = pathlib.Path(__file__).parent.absolute()

    # Read file
    filePath = os.path.join(path, fileName)
    with open(filePath, 'r') as f:
        appInstructions = f.read()

    return appInstructions

def processUserData(filePaths):
        '''Organising data treatment'''
        print('Starts to process the data')

        # Redirecting print statements to file
        original_stdout = sys.stdout
        logfile = open('logfile.txt', 'w+')
        sys.stdout = logfile

        # Read in userdata from file as a pandas dataframe
        userData = readOriginalData(filePath = filePaths['dataOriginalFilePath'], sheetName = 'Master')

        # Clean data
        cleanedData = dataCleaning(userData = userData, filePaths = filePaths)

        # Deriv data for aditional columns based on the cleaned data
        derivedData = dataDeriveNewColumns(cleanedData = cleanedData, filePaths = filePaths)

        # Extract citation data from CrossRef based on the DOI number
        citationData = dataCitationData(cleanedData['Ref_DOI_number'], cleanedData['Ref_publication_date'], cleanedData['Ref_lead_author'], filePaths['DOIPath'], filePaths = filePaths)

        # Merge the data to the format for the database
        mergedData = dataMergeData(cleanedData, derivedData, citationData, filePaths = filePaths)

        print('-----------------------------------------\nFinished processing user data')

        ## Upload data to database
        uploadUserDataToDatabase(filePath = filePaths['dataCompleatFilePath'])
        #dbf.run_csvToDatabase(filePath = filePaths['dataCompleatFilePath'], table = 'data', schema = 'singeljunction')

        print('-----------------------------------------\nFinished uploading user data')

        # Reverse back standard output to promt and close logfile
        logfile.close()
        sys.stdout = original_stdout

        # Copy logfile to storage
        shutil.copyfile('logfile.txt', filePaths['logFilePath'])

        # Copy processed data to centralised storage for backup
        backupToStorage(filePaths)

def readOriginalData(filePath, sheetName):
    '''Read in original data'''
    # Read in file object
    file = pd.ExcelFile(filePath)

    # For vertical template
    if 'Master' in file.sheet_names:
        data = file.parse('Master', index_col=0)

        # transpose the data. i.e. make rows to columns
        data = data.transpose(copy=True)

    elif 'Master H' in file.sheet_names:
        data = file.parse('Master H', index_col=0)

    else:
        print(f'Did not find a sheet named Master in the excel file')

    return data

def uniqueFilename(filename, savePath):
    '''Returns a unique file name'''
    # List of filenames in target directory
    filenames = os.listdir(savePath)

    # Add a date to the file name
    filename = str(datetime.date.today()) + ' ' + filename

    # Propose a file name
    uniqueName = filename.split('.xlsx')[0] + '_v1.xlsx'

    # Ensure that the file name is unique
    i = 1
    while uniqueName in filenames:
        i += 1
        uniqueName = filename.split('.xlsx')[0] + '_v' + str(i) + '.xlsx'

    return uniqueName

def updateFilePaths(filename, saveFilename, filePaths, filetype):
    '''Update dictionary with filepaths for where to save files localy '''
    #filetype to save to. .xlsx or .csv
    filetype = '.csv'

    # update dictionary of relevant file paths
    filePaths['dataBaseFileName'] =  filename
    filePaths['dataOriginalFileName'] = saveFilename
    filePaths['dataOriginalFilePath'] = os.path.join(filePaths['dataOriginalDirectoryPath'], saveFilename)

    filePaths['dataCleanedFileName'] = saveFilename.rsplit('.', 1)[0] + '_Cleaned' + filetype
    filePaths['dataCleanedFilePath'] = os.path.join(filePaths['dataCleanedDirectoryPath'], filePaths['dataCleanedFileName'])

    filePaths['dataCompleatFileName'] = saveFilename.rsplit('.', 1)[0] + '_Compleat' + filetype
    filePaths['dataCompleatFilePath'] = os.path.join(filePaths['dataCompleatDirectoryPath'], filePaths['dataCompleatFileName'])

    filePaths['dataDerivedFileName'] = saveFilename.rsplit('.', 1)[0] + '_Derived' + filetype
    filePaths['dataDerivedFilePath'] = os.path.join(filePaths['dataDerivedDirectoryPath'], filePaths['dataDerivedFileName'])

    filePaths['dataCitationFileName'] = saveFilename.rsplit('.', 1)[0] + '_Citation' + filetype
    filePaths['dataCitationFilePath'] = os.path.join(filePaths['dataCitationDirectoryPath'], filePaths['dataCitationFileName'])

    filePaths['logFileName'] = saveFilename.rsplit('.', 1)[0] + '_log.txt'
    filePaths['logFilePath'] = os.path.join(filePaths['dataLogDirectoryPath'], filePaths['logFileName'])

    return filePaths

def uploadUserDataToDatabase(filePath):
    '''Uppload user data '''
    # Fetch table and scheema names of the database
    bd_details = database_details()
    table = bd_details['table']
    schema = bd_details['schema']

    # Set up a conection to the database
    engine = conectToDatabase()

    # Run rutine for uploading the data    
    #dbf.run_csvToDatabase(filePath = filePaths['dataCompleatFilePath'], table = table, schema = schema)
    dbf.csvToDatabase(filePath = filePath, table = table, engine = engine, schema = schema)

#%% Seting up the dashboard and the interactivity
def interactiveEngine():
    '''Seting up the dashboard and the interactivity'''
    #%% Internal helper functions #########################################
    def updateLogText():
        '''Display stored consol output on dashboard '''
        logfile = open('logfile.txt', 'r')
        log_list = logfile.read()
        log_list = log_list.split('\n')
        logfile.close()

        log_num = len(log_list)
        outputText = ''
        for log in log_list:
            outputText += '<li>{}</li>'.format(log)
        status_update_text.text = '<ul>{}</ul>'.format(outputText)

    def upload_data(attr, old, new):
        '''Organising data treatment'''
        # Get the name of the selected file
        filename = file_input.filename

        print('User filename: {filename}')

        # Import paths to where to find and save files
        filePaths = defaultFilePaths()

        # define a unique file name
        saveFilename = uniqueFilename(filename, filePaths['dataOriginalDirectoryPath'])

        # Update filePaths to where to save files localy
        filePaths = updateFilePaths(filename, saveFilename, filePaths, filetype = '.csv')

        # Save userfile to local storage
        userfile = open(filePaths['dataOriginalFilePath'], 'wb')
        userfile.write(base64.b64decode(file_input.value))
        userfile.close()

        print('Saved original file')

        # Run script for processing data
        processUserData(filePaths)

        # Show consol log
        updateLogText()


    #%% Main function #######################################################
    # Read in the information about the app that will be displayd as a separate tab
    appInstructions = getAppInstructions(fileName = 'Instructions.html')
    aboutTheApp = Div(text = appInstructions, width=700, height=1000)

    #%% Input controlls ####################################################
    # File inputs
    file_input = FileInput(accept=".xlsx")

    #%% Setting up callbacks ###############################################
    # File inputs
    file_input.on_change('value', upload_data)

    #%% Text fields
    instruction_1 =  Div(text = getAppInstructions(fileName = "uploadinstruction_paragraph1.html"), width=700)

    log_list = []
    status_update_text = Div(text = 'Log', width=700, height=1000)

    #%% Layout the controlls
    layout_tab1 = column(aboutTheApp)
    layout_tab2 = column(instruction_1, file_input, status_update_text)

    #%% Make tabs with the specified layouts
    tab1 = Panel(child=layout_tab1, title = 'About')
    tab2 = Panel(child=layout_tab2, title = 'Upload data')

    #%% Return
    return tab1, tab2
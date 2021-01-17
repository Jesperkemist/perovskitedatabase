# =============================================================================
# dataBaseFunctions
# Moduel with function for interacting with postgres databases 
# 
# By Jesper Jacobsson
# 2020 10
# =============================================================================

#%% Imports
import os
import shutil
import datetime

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema

from ConectionDetails.databaseConfiguration import databaseConfiguration

import UtilityFunctions.dataColumns as dataColumns
import UtilityFunctions.dataTableClass_V5_31 as dataTable_1


#%% Functions
def conectToDataBase():
    '''Conect to the database'''

    # Reading in configuration details for accessing the database
    dbConfig = databaseConfiguration()

    # The conection string to the Postgres database
    conection_string = 'postgresql+psycopg2://' + dbConfig['user'] + ':' + dbConfig['password'] + '@' + dbConfig['host'] + '/' + dbConfig['database']

    # Conect to the database
    try:
        engine = create_engine(conection_string)
        print(f"Connection to {dbConfig['host']} established")
    except:
        print(f"Conection to {dbConfig['host']} failed")

    return engine

def createTables(engine, nameOfDatabase, tableClass):
    ''' Create tables in the database {nameOfDatabase} Use the engine {engine}. 
    {tableClass} is a class that contains the name of the tables to create and specifications for its columns'''   

    # Create tables
    try:
        # Create the table. This is equivalent to the "Create Table" statement in raw SQL.
        tableClass.metadata.create_all(engine)
        print(f"Successfully created new tables")
    except:
        print(f"Unable to create the table in: {nameOfDatabase}")

def csvToDatabase(filePath, table, engine, schema):
    '''Read in data to the database'''

    # Read in user data
    if os.path.splitext(filePath)[1] == '.csv':
        userData = pd.read_csv(filePath, low_memory = False)
    else:
        userData = pd.read_excel(filePath)

    # Name the data columns to match the header in the database. A safeguard against misspellings 
    userData.columns = dataColumns.csv_data_columns_complet()

    # Due to an incomprehensible effect making only one of the boolean columns a floating point column
    userData['Perovskite_dimension_3D'] = userData['Perovskite_dimension_3D'].astype('bool')

    # Update the Ref_ID column
    ref_id = update_Ref_ID(userData, table = table, schema = schema, engine = engine)
    userData['Ref_ID'] = ref_id

    # Insert data into the database
    userData.to_sql(table, con=engine, schema = schema, if_exists='append', index=False)

def defaultFilePathsWithRootFolder(root):
    '''Predifined file paths '''
    # The top directory of the app
    #root = os.path.abspath(os.getcwd())

    filePaths = {
        'dataOriginalDirectoryPath' : os.path.join(root, 'dataOriginal'),
        'dataCleanedDirectoryPath' : os.path.join(root,  'dataCleaned'),
        'dataCompleatDirectoryPath' : os.path.join(root,  'dataCompleat'),
        'dataDerivedDirectoryPath' : os.path.join(root, 'dataDerived'),
        'dataCitationDirectoryPath' : os.path.join(root,  'dataCitation'),
        'dataLogDirectoryPath' : os.path.join(root, 'dataLogFiles'),
        'DOIPath': os.path.join(root, 'utilityFunctions', 'DOI_saved_files'),                  
            }

    return filePaths

def deleteTables(engine, tableClass):
    ''' Dropp the specified table'''
    try:
        # Dropp the specified table
        #engine.execute("DROP Table IF EXISTS " + nameOfTable + " CASCADE;")
        tableClass.metadata.drop_all(engine)
        print(f"Tables succesfully dropped")
    except:
        print(f"Unable to dropp the tables")

def getDataFileFromDisk(filePath, filePaths, filetype = '.csv'):
    '''Get datafile from Disk. filepath is path to file. filepaths is a ditionary with filepaths. return the file name and folder'''

    # Extract filename
    filename = os.path.basename(filePath)

    # define a unique file name
    saveFilename = uniqueFilename(filename, filePaths['dataOriginalDirectoryPath'])

    #filetype to save to. .xlsx or .csv
    #filetype = '.csv'
    #filetype = '.xlsx'

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

    # Copy original file to storage with unique file name
    shutil.copyfile(filePath, filePaths['dataOriginalFilePath'])

    return filePaths

def readDataFromDatabase(engine, table, schema, dataColumns):
    '''Read in data from dataColumns in table in schema in the database specified in the configuration file'''

    data = pd.read_sql_table(table_name = table,
                                con = engine,
                                schema = schema,
                                columns = dataColumns)
    #try:
    #    data = pd.read_sql_table(table_name = table,
    #                             con = engine,
    #                             schema = schema,
    #                             columns = dataColumns)
    #except:
    #    print(f"failed to read in data from: {schema}.{table}")

    return data

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

 
    ## Read in data
    #data = pd.read_excel(filePath, sheet_name = sheetName, index_col=0)

    ## transpose the data. i.e. make rows to columns
    #data = data.transpose(copy=True)

    return data

def run_createNewTables(schema):
    '''Run a runtine for creating datatable under specified schema '''

    ## Specify scheema to work with
    #schema = 'singeljunction_2'

    # Conect to database
    engine = conectToDataBase() 

    # Reading in configuration details for accessing the database
    dbConfig = databaseConfiguration()

    # Create schema (schema name should match schema name specified in tableClass
    engine.execute(CreateSchema(schema))

    # Create the tables specified in tableClass under the specified schema
    createTables(engine = engine, nameOfDatabase = dbConfig['database'], tableClass = dataTable_1.perovskitedata)

def run_csvToDatabase(filePath, table, schema):
    '''Upload data in file to database'''
    # Conect to database
    engine = conectToDataBase() 

    # Reading in configuration details for accessing the database
    dbConfig = databaseConfiguration()

    # Read in data
    csvToDatabase(filePath = filePath, engine = engine, table = table, schema = schema)

    #
    print(f'data uploaded to database')

def run_deleateTables():
    '''Run deleat tables rutine '''
    # Conect to database
    engine = conectToDataBase() 

    # Reading in configuration details for accessing the database
    dbConfig = databaseConfiguration()

    # Dropp tables
    deleteTables(engine = engine, tableClass = dataTable_1.perovskitedata)

def uniqueFilename(filename, savePath):
    '''Returns a unique file name'''

    # List of filenames in target directory
    filenames = os.listdir(savePath)

    # Add a date to the file name
    #filename = str(datetime.date.today()) + ' ' + filename

    # Propose a file name
    uniqueName = filename.split('.xlsx')[0] + '_v1.xlsx'

    # Ensure that the file name is unique
    i = 1
    while uniqueName in filenames:
        i += 1
        uniqueName = filename.split('.xlsx')[0] + '_v' + str(i) + '.xlsx'

    return uniqueName

def update_Ref_ID(userData, table, schema, engine):
    '''Identifies the higest ID number in the database, and  start to counts from that'''

    # Read in reference data from the database
    data = readDataFromDatabase(engine = engine, table = table, schema = schema, dataColumns = ['Ref_ID'])

    if len(data) == 0:
        startID = 1
    else:
        startID = max(data['Ref_ID']) + 1

    # New database ID counting upwards from the higest previous database ID
    ref_id = list(range(startID, startID + len(userData)))

    return ref_id


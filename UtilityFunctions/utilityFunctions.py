# =============================================================================
# Utility functions for the interactive graphics
# 
# By Jesper Jacobsson
# 2020 12
# =============================================================================

from datetime import datetime
import os

import pandas as pd
from sqlalchemy import create_engine

from ConectionDetails.databaseConfiguration import databaseConfiguration

import UtilityFunctions.CleanDataV5 as cleanData
import UtilityFunctions.CompleatDataV5 as compleatData


def conectToDatabase():
    '''Create a conection to the database and return the conection engine'''

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

def convertNumerListToFloats(numberList):
    '''Convert a numerlist to floats. If more than one value, keep the first one'''

    # Convert data to strings
    numberList = numberList.astype(str)

    # identify all strings with more than one element, by utlising that they contain the pattern ' | '
    x = numberList.str.contains(' | ') == True

    # Get a list of the indexes where the abowe condition holds
    indexlist = list(numberList[x].index)

    # Loop over all instances with more than one number
    for index in indexlist:
        # Ensure that entry is a string
        y = str(numberList[index]).strip()

        # Keep the first entry
        y = y.split(' | ')[0].strip()

        # Convert number into a float
        try:
            number = float(y)
        except:
            number = np.nan

        # Uppdate data
        numberList.loc[index] = number

    # Convert everything to floats
    numberList = pd.to_numeric(numberList, errors = 'coerce')

    return numberList

def database_details():
    '''Returns detailes of the database to work with '''

    bd_details = {
            'table' : 'data', 
            'schema' : 'singeljunction',
            'bd_key' : 'Ref_ID'
            }

    return bd_details

def databaseCategoriesMostCommon(column, number, engine):
    '''Extract the {number} most comon categories in the column {column} in the database'''
    # Database details
    bd_details = database_details()
    table = bd_details['table']
    schema = bd_details['schema']

    # String maipulation to get it to work with the sql statement
    columnString = f'"{column}"'

    # Query the database. Coresponds to pd.values_count()
    valueCounts = pd.read_sql_query(sql=f"select {columnString}, count(*) from {schema}.{table} GROUP BY {columnString}", con=engine)

    # Sort categories in order of occurance
    categories = list(valueCounts.sort_values(by='count', ascending=False)[column])
    
    # Select the {number} most common categories
    categories = categories[0:number]

    # Make sure everything is treated as a string
    categories = [str(item) for item in categories]

    # Sort remaining categories in alphabetic order
    categories.sort()

    return categories

def databaseCategoriesMostCommon_withBoleanFilter(column, boleanColumn, number, engine):
    '''Extract the {number} most comon categories in the column {column} in the database'''
    # Database details
    bd_details = database_details()
    table = bd_details['table']
    schema = bd_details['schema']

    # String maipulation to get it to work with the sql statement
    columnString = f'"{column}"'
    boleanColumnString = f'"{boleanColumn}"'

    # Query the database. Coresponds to pd.values_count()
    valueCounts = pd.read_sql_query(sql=f"select {columnString}, count(*) from {schema}.{table} where {table}.{boleanColumnString} is TRUE GROUP BY {columnString}", con=engine)

    # Sort categories in order of occurance
    categories = list(valueCounts.sort_values(by='count', ascending=False)[column])
    
    # Select the {number} most common categories
    categories = categories[0:number]

    # Make sure everything is treated as a string
    categories = [str(item) for item in categories]

    # Sort remaining categories in alphabetic order
    categories.sort()

    return categories

def databaseCatagoriesUnique(column, engine):
    '''Extract all unique values in the column {column} in the database'''
    # Database details
    bd_details = database_details()
    table = bd_details['table']
    schema = bd_details['schema']

    # String maipulation to get it to work with the sql statement
    columnString = f'"{column}"'

    # Query the database for uniue values
    values = pd.read_sql_query(sql=f"select distinct {columnString} from {schema}.{table}", con=engine)

    # Sort categoreis in alphabetic order
    values.sort_values(by=column, inplace=True)

    # Extract the categoreis
    categories = list(values[column])

    return categories

def databaseCatagoriesUnique_withBoleanFilter(column, boleanColumn, engine):
    '''Extract all unique values in the column {column} in the database'''
    # Database details
    bd_details = database_details()
    table = bd_details['table']
    schema = bd_details['schema']

    # String maipulation to get it to work with the sql statement
    columnString = f'"{column}"'
    boleanColumnString = f'"{boleanColumn}"'

    # Query the database for uniue values
    values = pd.read_sql_query(sql=f"select distinct {columnString} from {schema}.{table} where {table}.{boleanColumnString} is TRUE", con=engine)

    # Sort categoreis in alphabetic order
    values.sort_values(by=column, inplace=True)

    # Extract the categoreis
    categories = list(values[column])

    return categories

def dataCitationData(DOInumbers, defaultDate, defaultAuthor, DOIPath, filePaths):
    '''Extract citation data from CrossRef based on the DOI number '''

    # Get citation data
    referenceData = compleatData.citationData(DOInumbers, defaultDate, defaultAuthor, DOIPath)
    
    # Extract file ending
    fileEnding = os.path.splitext(os.path.basename(filePaths['dataCitationFilePath']))[1]

    # Save cleaned data
    if fileEnding == '.xlsx':
        try:
            referenceData.to_excel(filePaths['dataCitationFilePath'], index = False)
            print(f'Saved citation data')
        except:
            print(f'Failed to save citation data based on: {filePaths["dataOriginalFileName"]}')

    else:
        try:
            referenceData.to_csv(filePaths['dataCitationFilePath'], index = False, encoding='utf-8-sig')
            print(f'Saved citation data')
        except:
            print(f'Failed to save citation data based on: {filePaths["dataOriginalFileName"]}')

    return referenceData

def dataCleaning(userData, filePaths):
    '''Run a data cleaning and formating rutine on the data'''

    # Clean the data
    try:
        cleanedData = cleanData.cleanUserData(userData, fileName = filePaths['dataOriginalFileName'])
    except:
        print(f'Failed to clean data for: {filePaths["dataOriginalFileName"]}')

    # Extract file ending
    #fileEnding = os.path.splitext(os.path.basename(filePaths['dataOriginalFileName']))[1]
    fileEnding = os.path.splitext(os.path.basename(filePaths['dataCleanedFilePath']))[1]

    # Save cleaned data
    if fileEnding == '.xlsx':
        try:
           cleanedData.to_excel(filePaths['dataCleanedFilePath'], index = False)
           print(f'Saved cleaned data')
        except:
           print(f'Failed to saved clean data at {filePaths["dataOriginalFileName"]}')

    else:
        try:
            cleanedData.to_csv(filePaths['dataCleanedFilePath'], index = False, encoding='utf-8-sig')
            print(f'Saved cleaned data')
        except:
            try:
                cleanedData = cleanedData.applymap(lambda x: x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x)
                cleanedData.to_csv(filePaths['dataCleanedFilePath'], index = False)
                print(f'Saved cleaned data after unicode escape')
            except:
                print(f'Failed to saved clean data at {filePaths["dataOriginalFileName"]}')

    return cleanedData

def dataDeriveNewColumns(cleanedData, filePaths):
    '''Deriv data for aditional columns based on the cleaned data'''

    # Derive the data
    try:
        derivedData = compleatData.DerivedtUserData(cleanedData, fileName = filePaths['dataOriginalFileName'])
    except:
        print(f'Failed to derive additional data based on: {filePaths["dataOriginalFileName"]}')

    # Extract file ending
    fileEnding = os.path.splitext(os.path.basename(filePaths['dataDerivedFilePath']))[1]

    # Save cleaned data
    if fileEnding == '.xlsx':
        try:
           derivedData.to_excel(filePaths['dataDerivedFilePath'], index = False)
           print(f'Saved derived data')
        except:
           print(f'Failed to saved derived data at {filePaths["dataOriginalFileName"]}')

    else:
        try:
            derivedData.to_csv(filePaths['dataDerivedFilePath'], index = False, encoding='utf-8-sig')
            print(f'Saved derived data')
        except:
            print(f'Failed to save derived aditional data based on: {filePaths["dataOriginalFileName"]}')

    return derivedData

def dataMergeData(cleanedData, derivedData, citationData, filePaths):
    '''Merge cleanedData, derivedData and citationData into one document ready for databse uploading'''

    # Merge the data
    try:
        mergedData = compleatData.mergeData(cleanedData, derivedData, citationData)
    except:
        print(f'Failed to merged data into one file for: {filePaths["dataOriginalFileName"]}')

    # Extract file ending
    fileEnding = os.path.splitext(os.path.basename(filePaths['dataCompleatFilePath']))[1]

    # Save cleaned data
    if fileEnding == '.xlsx':
        try:
            mergedData.to_excel(filePaths['dataCompleatFilePath'], index = False)
            print(f'Saved compleated data')
        except:
            print(f'Failed to save compleated data based on: {filePaths["dataOriginalFileName"]}')

    else:
        try:  
            mergedData.to_csv(filePaths['dataCompleatFilePath'], index = False, encoding='utf-8-sig')
            print(f'Saved compleated data')
        except:
            print(f'Failed to save compleated data based on: {filePaths["dataOriginalFileName"]}')

    return mergedData

def dataManipulation(data):
    '''Do data manipulation required by the app'''

    numericColumns = ['JV_default_PCE', 
                      'JV_default_Voc', 
                      'JV_default_FF', 
                      'JV_default_Jsc', 
                      'Cell_area_measured', 
                      'Cell_area_total', 
                      'Module_area_effective', 
                      'Module_area_total',
                      'Outdoor_PCE_T80',
                      'Outdoor_PCE_Ts80',
                      'Outdoor_PCE_Te80',
                      'Outdoor_PCE_Tse80',
                      'Outdoor_PCE_T95',
                      'Outdoor_PCE_Ts95',
                      'Outdoor_PCE_after_1000_h',
                      'Outdoor_PCE_end_of_experiment',
                      'Outdoor_PCE_initial_value',
                      'Outdoor_power_generated',
                      'Outdoor_time_total_exposure',
                      'Stability_PCE_T80',
                      'Stability_PCE_Ts80',
                      'Stability_PCE_Te80',
                      'Stability_PCE_Tse80',
                      'Stability_PCE_T95',
                      'Stability_PCE_Ts95',
                      'Stability_PCE_after_1000_h',
                      'Stability_PCE_end_of_experiment',
                      'Stability_PCE_initial_value',
                      'Stability_time_total_exposure',
                      ]
            
    # replace Nan with -1 in the columns that may be plotted
    for column in list(data.columns):
        if column in numericColumns:
            data[column].fillna(value = -1, inplace = True)

    # Convert the band gap column to numeric values (and keeping the first value if multiple values)
    if 'Perovskite_band_gap' in list(data.columns):
        data['Perovskite_band_gap_string'] = data['Perovskite_band_gap'] 
        data['Perovskite_band_gap'] = convertNumerListToFloats(data['Perovskite_band_gap'])
        data['Perovskite_band_gap'].fillna(value = -1, inplace = True)

    # Time data
    if 'Ref_publication_date' in list(data.columns):
        data['Ref_publication_date'] = pd.to_datetime(data['Ref_publication_date'], errors="coerce")
        # Replace corupt values with todays date
        todays_time = pd.to_datetime(datetime.now().strftime("%Y-%m-%d"))
        data['Ref_publication_date'].fillna(todays_time, inplace=True)

    # Extract the higher temperature in the temperature range and add that as a separate column
    if 'Outdoor_temperature_range' in list(data.columns):
        #data['Outdoor_temperature_range_max'] = getMaxTemperature(data['Outdoor_temperature_range'])
        data['Outdoor_temperature_range'] = getMaxTemperature(data['Outdoor_temperature_range'])


    # Extract the higher temperature in the temperature range and add that as a separate column
    if 'Stability_temperature_range' in list(data.columns):
        #data['Stability_temperature_range_max'] = getMaxTemperature(data['Stability_temperature_range'])
        data['Stability_temperature_range'] = getMaxTemperature(data['Stability_temperature_range'])


    return data

def getMaxTemperature(data):
    '''Take a panadas series with entries as strings in the format 'value1; value2' and returns a list with the highest of the two numbers '''

    # Internal helper function
    def convertToNumber(x):
        try:
            number = float(x)
        except:
            number = np.nan

        return number

    maxTemp = []
    for item in data:
        # Ensure that data is a string
        temperaturString = str(item).strip()

        # Separate the entries into a list
        temperaturListString = temperaturString.split(';')

        T = []
        for temperature in temperaturListString:
            # Remove blank spaces
            temperature = temperature.strip()

            # convert to a number and add to temporary list
            T.append(convertToNumber(temperature))

        # Append the higest number
        maxTemp.append(max(T))   

    return maxTemp

def integerList(item):
    '''Takes in text string with integers separated by ; and returns a list of the integers'''
    numbers = []
    # The input is converted to a string (regardless if it is or not)
    item = str(item)

    # Remove all blank spaces
    item = item.strip().replace(" ","")

    # Split on ;
    itemList = item.split(';')

    for element in itemList:
        # Check if element is a number
        if is_number(element):
            numbers.append(int(float(element)))

    return numbers

def is_int(s):
    ''' Simple function to see if a string is an int'''
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_number(s):
    ''' Simple function to see if a string is a float'''
    try:
        float(s)
        return True
    except ValueError:
        return False

def loadData(dataColumns, engine):
    '''Read in the data from the database. Takes a list of columns and a conection engine as argument and returns the fetched data'''
    # Database details
    bd_details = database_details()
    table = bd_details['table']
    schema = bd_details['schema']

    # String maipulation to get it to work with the sql statement
    dataColumnsString = ', '.join(f'"{c}"' for c in dataColumns)

    # Get data from the database
    data = pd.read_sql_query(sql=f"select {dataColumnsString} from {schema}.{table}", con = engine)

    return data

def loadData_withBoleanFilter(dataColumns, boleanColumn, engine):
    '''Read in the data from the database. Takes a list of columns, a column hat must be true, and a conection engine as argument and returns the fetched data'''
    # Database details
    bd_details = database_details()
    table = bd_details['table']
    schema = bd_details['schema']

    boleanColumn = [boleanColumn]

    # String maipulation to get it to work with the sql statement
    dataColumnsString = ', '.join(f'"{c}"' for c in dataColumns)
    boleanColumnString = ', '.join(f'"{c}"' for c in boleanColumn)

    # Get data from the database
    data = pd.read_sql_query(sql=f"select {dataColumnsString} from {schema}.{table} where {table}.{boleanColumnString} is TRUE", con = engine)

    return data

def readDataFromDatabase(table, schema, dataColumns):
    '''Read in data from dataColumns in table in schema in the database specified in the configuration file'''

    # Conecto the database
    engine = conectToDatabase()

    ## Reading in configuration details for accessing the database
    #dbConfig = databaseConfiguration()

    ## The conection string to the Postgres database
    #conection_string = 'postgresql+psycopg2://' + dbConfig['user'] + ':' + dbConfig['password'] + '@' + dbConfig['host'] + '/' + dbConfig['database']

    ## Conect to the database
    #try:
    #    engine = create_engine(conection_string)
    #    print(f"Connection to {dbConfig['host']} established")
    #except:
    #    print(f"Conection to {dbConfig['host']} failed")

    # data = pd.read_sql_table(table_name = table,
    #                             con = engine,
    #                             schema = schema,
    #                             columns = dataColumns)

    dataColumnsString = ', '.join(f'"{c}"' for c in dataColumns)
    #data = pd.read_sql_query(sql=f"select {dataColumnsString} from {schema}.{table}", # limit 1000
    #                         con = engine)

    data = pd.read_sql_query(sql=f"select {dataColumnsString} from {schema}.{table} limit 1000", con = engine)


    #try:
    #    data = pd.read_sql_table(table_name = table,
    #                             con = engine,
    #                             schema = schema,
    #                             columns = dataColumns)
    #except:
    #    print(f"failed to read in data from: {dbConfig['host']}.{schema}.{table}")

    return data

def readDataFromDatabase_v2(table, schema, dataColumns, engine):
    '''Read in data from dataColumns in table in schema in the database specified in the configuration file'''

    dataColumnsString = ', '.join(f'"{c}"' for c in dataColumns)
    data = pd.read_sql_query(sql=f"select {dataColumnsString} from {schema}.{table}", con = engine)

    return data

def toolTipsDict():
    '''Return dictionary of posible selected hover tools '''

    return   {"Cell aria" : 'Cell_area_measured',
         "Cell stack" : 'Cell_stack_sequence',
        "ETL" : 'ETL_stack_sequence',
        "HTL" : 'HTL_stack_sequence',
        "FF" : 'JV_default_FF',
        "Jsc" : 'JV_default_Jsc',
        "PCE" : 'JV_default_PCE',
        "Voc" : 'JV_default_Voc',
        "Perovskite additives" : 'Perovskite_additives_compounds',
        "Eg" : 'Perovskite_band_gap',
        "Perovskite" : 'Perovskite_composition_long_form',
        "Perovskite deposition" : 'Perovskite_deposition_procedure',
        "Antisolvent" : 'Perovskite_deposition_quenching_media',
        "Perovskite solvent" : 'Perovskite_deposition_solvents',
        "DOI": 'Ref_DOI_number',
        "Database ID" : 'Ref_ID',
        "Author" : 'Ref_lead_author',
        "Publiation date" : 'Ref_publication_date',
        "Stability PCE_f/PCE_i" : 'Stability_PCE_end_of_experiment',
        "Stability protocoll" : 'Stability_protocol',
        }

def toolTipsMap():
    '''Return a maping of names to hoover tools '''
    return {
        "Cell aria" : ("Cell aria","@Cell_area_measured"),
        "Cell stack" : ("Cell stack","@Cell_stack_sequence"),
        "ETL" : ("ETL","@ETL_stack_sequence"),
        "HTL" : ("HTL","@HTL_stack_sequence"),
        "FF" : ("FF","@JV_default_FF"),
        "Jsc" : ("Jsc","@JV_default_Jsc"),
        "PCE" : ("PCE","@JV_default_PCE"),
        "Voc" : ("Voc","@JV_default_Voc"),
        "Perovskite additives" : ("Perovskite additives","@Perovskite_additives_compounds"),
        "Eg" : ("Eg","@Perovskite_band_gap"),
        "Perovskite" : ("Perovskite","@Perovskite_composition_long_form"),
        "Perovskite deposition" :("Perovskite deposition","@Perovskite_deposition_procedure"),
        "Antisolvent" : ("Antisolvent","@Perovskite_deposition_quenching_media"),
        "Perovskite solvent" : ("Perovskite solvent","@Perovskite_deposition_solvents"),
        "DOI" : ("DOI","@Ref_DOI_number"),
        "Database ID" : ("Database ID","@Ref_ID"),
        "Author" : ("Author","@Ref_lead_author"),
        "Publiation date" : ("Publiation date","@Ref_publication_date"),
        "Stability PCE_f/PCE_i" : ("PCE_f/PCE_i", "@Stability_PCE_end_of_experiment"),
        "Stability protocoll" : ("Stability protocoll", "@Stability_protocol")
        }

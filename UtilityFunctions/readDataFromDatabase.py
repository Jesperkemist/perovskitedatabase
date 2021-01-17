# Function for reading in data from the database and returnign a pandas datafram

import pandas as pd
from sqlalchemy import create_engine

from ConectionDetails.databaseConfiguration import databaseConfiguration

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

def database_details():
    '''Returns detailes of the database to work with '''

    bd_details = {
            'table' : 'data', 
            'schema' : 'singeljunction',
            'bd_key' : 'Ref_ID'
            }

    return bd_details

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



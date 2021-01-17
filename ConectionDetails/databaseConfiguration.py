import os
from mz_bokeh_package.environment import get_environment

def databaseConfiguration():
    """Database configuration details"""

    env = get_environment()

    if env in ('staging', 'production'):
        host = 'localhost'
        port = 5432
        database = os.getenv('DB_DATABASE')
        username = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD')
    elif env == 'dev':
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT', 5432)
        database = os.getenv('DB_DATABASE')
        username = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD')
    else:
        raise Exception("Unknown environment, cannot obtain database connection string")

    dbConfig = {'host': host + ":" + str(port),
                'user': username,
                'password': password,
                'database': database}

    return dbConfig

# =============================================================================
# bokehServerRun.py
# Start a bokehserver running the appliactions in the folder Bokeh_server
# If run localay go to http://localhost:5006/
# 
# By Jesper Jacobsson
# 2020 07
# =============================================================================

import os
from pathlib import Path

from bokeh.server.server import Server
from bokeh.command.util import build_single_handler_applications
from threading import Thread
from tornado.ioloop import IOLoop

# load environment variables with database connection details from .env file (this file is git ignored,
# and should be added for each developer, see README file)
from dotenv import load_dotenv
load_dotenv()


#%% list of filepaths to the bokeh apps to serve
files = [os.path.join('dashboards', 'RecordEvolution'),
         os.path.join('dashboards', 'GeneralDevelopment'),
         os.path.join('dashboards', 'BandgapAnalysis'),
         os.path.join('dashboards', 'DownloadData'),
         os.path.join('dashboards', 'Scaling'),
         os.path.join('dashboards', 'Stability'),
         os.path.join('dashboards', 'Modules'),
         os.path.join('dashboards', 'OutdoorTesting'),
         os.path.join('dashboards', 'UploadData'),
         os.path.join('dashboards', 'CorectDataInDatabase'),
         ]

#%% Convert filepaths to system independent form
paths = []
argvs = {}
for app in files:
    argvs[app]=None
    paths.append(app)

# Turn file path into bokeh apps
apps = build_single_handler_applications(paths, argvs)

# Function that starts the server   
def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py

    #myServer = Server(apps, io_loop=IOLoop(), allow_websocket_origin=["127.0.0.1:5006", "127.0.0.1:5100",  "localhost:5006", "localhost:5100"])  
    myServer = Server(apps, io_loop=IOLoop(), allow_websocket_origin=["*"])  
    myServer.start()
    myServer.io_loop.start()

#%% Runing a thred starting the server (do not realy understand how this works)
Thread(target=bk_worker).start()   
# =============================================================================
# Initiate an interactive Bokeh app that focus on general development
# 
# By Jesper Jacobsson
# 2020 08
# =============================================================================

import os
import sys

import time

# Make sure that imports can be made from the top folder of the project
sys.path.append(os.path.abspath(os.getcwd()))

from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.models import CustomJS
from bokeh.layouts import column
from bokeh.models.widgets.markups import Div

from dashboards.GeneralDevelopment.scripts import development
from dashboards.GeneralDevelopment.scripts import categoricalPlots

# from modules.auth import CurrentUser
from mz_bokeh_package.utilities import CurrentUser
from mz_bokeh_package.components import LoadingSpinner

# For autentication
user_name = CurrentUser().get_user_id()


# Start the interactive graphics and get the tabs
tab1, tab2, tab3, tab4 = development.interactiveEngine()
categorical = categoricalPlots.interactiveEngine()

# Put all the tabs in one application
tabs = Tabs(tabs = [tab1, categorical, tab2, tab3, tab4], name="main")
#tabs = Tabs(tabs = [tab1, tab2, tab3, tab4], name="main")

# Put the tabs in the current document which will be displayed in the application
curdoc().add_root(tabs)

# ADD LOADING SPINNER
loading_spinner = LoadingSpinner()
curdoc().add_root(loading_spinner.layout)

# enable/disable loading mode
def enable_loading_mode(enable: bool):
    loading_spinner.enabled = enable

# start loading data only after empty front end has been rendered and loading spinner is visible
def on_document_ready(event):
    enable_loading_mode(False)

curdoc().on_event('document_ready', on_document_ready)

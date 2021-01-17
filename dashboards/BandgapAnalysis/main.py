# =============================================================================
# Initiate an interactive Bokeh app that focus on perovskite band gap
# 
# By Jesper Jacobsson
# 2019 09
# =============================================================================

import os
import sys

# Make sure that imports can be made from the top folder of the project
sys.path.append(os.path.abspath(os.getcwd()))

from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.models import CustomJS
from bokeh.layouts import column
from bokeh.models.widgets.markups import Div

from dashboards.BandgapAnalysis.scripts import bandgapGraphics
#from dashboards.BandgapAnalysis.scripts import SQ_limits

# from modules.auth import CurrentUser
from mz_bokeh_package.auth import CurrentUser

# For autentication
user_name = CurrentUser.get_user_id()

#%% Create each of the tabs in the Bokeh application adn add them together
graph, tabel1, tabel3, about = bandgapGraphics.interactiveEngine()
#SQ_graph, SQ_tabel1, SQ_tabel2 = SQ_limits.interactiveEngine(data)

# Put all the tabs in one application
#tabs = Tabs(tabs = [graph, SQ_graph, tabel1, tabel3, SQ_tabel1, SQ_tabel2, about])
tabs = Tabs(tabs = [graph, tabel1, tabel3, about], name="main")

# Put the tabs in the current document which will be displayed in the application
curdoc().add_root(tabs)

# ADD LOADING SPINNER
# add a dummy element that will trigger the event for enabling/disabling the loading spinner
loader_trigger = Div(text="1", visible = False)
callback = CustomJS(code="")
loader_trigger.js_on_change('text', callback)
curdoc().add_root(column(loader_trigger, name="loaderTrigger"))

# enable/disable loading mode
def enable_loading_mode(enable: bool):
    callback.code = f"""
        document.getElementById('loaderContainer').style.visibility = '{'visible' if enable else 'hidden'}';
    """
    loader_trigger.text = str(int(loader_trigger.text) + 1)

# start loading data only after empty front end has been rendered and loading spinner is visible
def on_document_ready(event):
    enable_loading_mode(False)

curdoc().on_event('document_ready', on_document_ready)
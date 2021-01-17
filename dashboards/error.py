from bokeh.io import curdoc
from bokeh.models import Div
from bokeh.models.layouts import Row, Column

# step caption
caption = Div(
    text="Error: could not load page",
    style={"font-size": "120%", "font-family": "inherit", "font-weight": "bold"}
)

# subcaption
subcaption = Div(
    text="Authentication error",
    style={"font-size": "100%", "font-family": "inherit"}
)

layout = Column(
    caption,
    subcaption
)

curdoc().add_root(layout)
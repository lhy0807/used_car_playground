from random import random

from bokeh.layouts import column
from bokeh.models import Button, Select
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np

from atlas_db import atlas
import pymongo



from bokeh.io import show, output_notebook
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter, 
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import figure

print("loading geojson file...")
ny = gpd.read_file("bokehapp/geojson/ny.geojson")
ny = ny.set_index('ZIP_CODE')
ny_source = GeoJSONDataSource(geojson = ny.to_json())
print("finish loading geojson file...")

# Define color palettes
palette = brewer['OrRd'][8]
palette = palette[::-1] # reverse order of colors so higher values have darker colors
# Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 1)


# Create color bar.
color_bar = ColorBar(color_mapper = color_mapper, 
                     label_standoff = 8,
                     width = 500, height = 20,
                     border_line_color = None,
                     location = (0,0), 
                     orientation = 'horizontal')

# Create figure object.
p = figure(name="bokeh_jinja_figure",
           title = 'Calculated Weighted Points', 
           plot_height = 650 ,
           plot_width = 950, 
           toolbar_location = 'below',
           tools = "pan, wheel_zoom, box_zoom, reset",
           output_backend="webgl")
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
# Add patch renderer to figure.
states = p.patches('xs','ys', source = ny_source,
                   fill_color = {'field' :'Points',
                                 'transform' : color_mapper},
                   line_color = "gray", 
                   line_width = 0.25, 
                   fill_alpha = 1)
# Create hover tool
p.add_tools(HoverTool(renderers = [states],
                      tooltips = [('PO Name','@PO_NAME'),
                                  ('Points','@Points')
                                ]))

color_bar = ColorBar(color_mapper = color_mapper, 
                     label_standoff = 8,
                     width = 950, height = 20,
                     border_line_color = None,
                     location = (0,0), 
                     orientation = 'horizontal')
p.add_layout(color_bar, 'below')

print("finish setting figure")
# create a callback that will add a number in a random location
def callback(attr, old, new):
  global ny
  print("changing data source from {} to {}".format(old, new))
  file_name = "bokehapp/geojson/{}.json".format(new)
  with open(file_name, 'r') as f:
    global ny
    data = json.load(f)
    avg_points = data[0]
    quantity = data[1]
    for i in avg_points:
      ny.at[i, 'Points'] = avg_points[i]

    for i in quantity:
      ny.at[i, 'Quantity'] = quantity[i]

    states.data_source = GeoJSONDataSource(geojson = ny.to_json())
    curdoc().remove_root(p)
    curdoc().add_root(p)
  print("finish changing data source")

select = Select(name="select", title="Option:", value="c21411", options=["c21411","c22000","c23512"])
select.on_change("value", callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(select)
curdoc().add_root(p)
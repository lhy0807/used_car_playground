from random import random

from bokeh.layouts import column
from bokeh.models import Button
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

print("loading zipcode file...")
usa = gpd.read_file('../zipcodes.shp')
usa = usa.set_index('ZIP_CODE')
ny = usa[usa['STATE'] == 'NY']
plt.rcParams['figure.figsize'] = [20, 10]

print("finish loading zipcode file")
print("loading data from MongoDB...")
client = pymongo.MongoClient(atlas)
db = client["usedcar"]
usedcar = db.cargurus
data = pd.DataFrame(list(usedcar.find()),dtype=str)
print("finish loading data from MongoDB")

ny.insert(3,'Points',np.NaN)
ny.insert(3,'Quantity',np.NaN)

#first collect data and calculate avg price
#then put into dataframe
avg_price = {}
counter = {}
print("initialize...")
#initialize
for _,car in data.iterrows():
    zip_code = car['zipcode']
    avg_price[zip_code] = {}
    counter[zip_code] = {}
    
for _,car in data.iterrows():
    zip_code = car['zipcode']
    avg_price[zip_code][car['model']] = 0
    counter[zip_code][car['model']] = 0

for _,car in data.iterrows():
    avg_price[car['zipcode']][car['model']] += int(car['price'].replace(',', ''))
    counter[car['zipcode']][car['model']] += 1

for i in avg_price:
    for j in avg_price[i]:
        avg_price[i][j] /= counter[i][j]

#make a copy of counter as quantity
quantity = counter.copy()
print("start calculating points and quantity...")        
#normalize values for each model
max_values = {}
min_values = {}

max_q = {}
min_q = {}
#init
for i in avg_price:
    for j in avg_price[i]:
        max_values[j] = 0
        min_values[j] = 99999

for i in quantity:
    for j in quantity[i]:
        max_q[j] = 0
        min_q[j] = 99999

for i in avg_price:
    for j in avg_price[i]:
        price = avg_price[i][j]
        max_values[j] = max(max_values[j], price)
        #skip 0 (not exist)
        if price == 0:
            continue
        min_values[j] = min(min_values[j], price)
        
for i in quantity:
    for j in quantity[i]:
        q = quantity[i][j]
        max_q[j] = max(max_q[j], q)
        min_q[j] = min(min_q[j], q)

for i in avg_price:
    for j in avg_price[i]:
        if avg_price[i][j] == 0:
            continue
        avg_price[i][j] = (avg_price[i][j] - min_values[j])/(max_values[j] - min_values[j])

#calculate average points
avg_points = {}
for i in avg_price:
    avg_points[i] = 0

for i in avg_price:
    counter = 0
    for j in avg_price[i]:
        if avg_price[i][j] == 0:
            continue
        counter += 1
        avg_points[i] += avg_price[i][j]
    avg_points[i] /= counter
    
#calculate sum of quantity
quantity_sum = {}
for i in quantity:
    quantity_sum[i] = 0
for i in quantity:
    for j in quantity[i]:
        quantity_sum[i] += quantity[i][j]

for i in avg_points:
    ny.at[i, 'Points'] = avg_points[i]

for i in quantity:
    ny.at[i, 'Quantity'] = quantity_sum[i]
print("finish calculating points and quantity")        

from bokeh.io import show, output_notebook
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter, 
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import figure

ny_source = GeoJSONDataSource(geojson = ny.to_json())

# Define color palettes
palette = brewer['OrRd'][8]
palette = palette[::-1] # reverse order of colors so higher values have darker colors
# Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette, low = ny['Points'].min(), high = ny['Points'].max())


# Create color bar.
color_bar = ColorBar(color_mapper = color_mapper, 
                     label_standoff = 8,
                     width = 500, height = 20,
                     border_line_color = None,
                     location = (0,0), 
                     orientation = 'horizontal')

# Create figure object.
p = figure(title = 'Calculated Weighted Points', 
           plot_height = 650 ,
           plot_width = 950, 
           toolbar_location = 'below',
           tools = "pan, wheel_zoom, box_zoom, reset")
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

# create a callback that will add a number in a random location
def callback():
    pass

# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, p))
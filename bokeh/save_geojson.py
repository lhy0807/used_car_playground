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

ny.to_file("ny.geojson", driver='GeoJSON')
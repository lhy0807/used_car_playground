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
ny.insert(3,'Quantity',0.0)
ny.insert(3,'Points',0.0)
ny.to_file("geojson/ny.geojson", driver='GeoJSON')
plt.rcParams['figure.figsize'] = [20, 10]

print("finish loading zipcode file")

client = pymongo.MongoClient(atlas)
db = client["usedcar"]
usedcar = db.cargurus

car_models = db.modelcode.find()
codes = []
for model in car_models:
    codes.append(model['code'])

for code in codes:
    print("loading data from MongoDB...", code)
    data = pd.DataFrame(list(usedcar.find({"model":code})),dtype=str)
    print("finish loading data from MongoDB: ", code)

    #first collect data and calculate avg price
    #then put into dataframe
    avg_price = {}
    counter = {}
    print("initialize...")
    #initialize
    for _,car in data.iterrows():
        zip_code = car['zipcode']
        avg_price[zip_code] = 0
        counter[zip_code] = 0

    for _,car in data.iterrows():
        avg_price[car['zipcode']] += int(car['price'].replace(',', ''))
        counter[car['zipcode']] += 1

    for i in avg_price:
        avg_price[i] /= counter[i]

    #make a copy of counter as quantity
    quantity = counter.copy()
    print("start calculating points and quantity...")        
    #normalize values for each model
    max_values = 0
    min_values = 99999

    max_q = 0
    min_q = 99999

    for i in avg_price:
        price = avg_price[i]
        max_values = max(max_values, price)
        #skip 0 (not exist)
        if price == 0:
            continue
        min_values = min(min_values, price)
            
    for i in quantity:
        q = quantity[i]
        max_q = max(max_q, q)
        min_q = min(min_q, q)

    #calculate average points
    avg_points = {}
    for i in avg_price:
        avg_points[i] = 0

    for i in avg_price:
        if avg_price[i] == 0:
            continue
        avg_points[i] = (avg_price[i] - min_values)/(max_values - min_values)
    print("finish calculating points and quantity")        

    file_name = "geojson/" + code + ".json"
    with open(file_name, 'w') as f:
        json.dump([avg_points, quantity], f)

    print("finish saving " + file_name)
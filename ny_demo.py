import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np
from bokeh_plot import plot

usa = gpd.read_file('zipcodes.shp')
usa = usa.set_index('ZIP_CODE')

ny = usa[usa['STATE'] == 'NY']

# Plot NY Map using GeoPandas
# ny.plot()

data = pd.read_json('usedcar/usedcar.json',dtype=str)
ny.insert(3,'Points',np.NaN)

models = data.model.unique()

#first collect data and calculate avg price
#then put into dataframe
avg_price = {}
counter = {}

#initialize
for _,car in data.iterrows():
    zip_code = car['zip']
    avg_price[zip_code] = {}
    counter[zip_code] = {}
for _,car in data.iterrows():
    zip_code = car['zip']
    avg_price[zip_code][car['model']] = 0
    counter[zip_code][car['model']] = 0

for _,car in data.iterrows():
    avg_price[car['zip']][car['model']] += int(car['price'].replace(',', ''))
    counter[car['zip']][car['model']] += 1

for i in avg_price:
    for j in avg_price[i]:
        avg_price[i][j] /= counter[i][j]

#normalize values for each model
max_values = {}
min_values = {}
#init
for i in avg_price:
    for j in avg_price[i]:
        max_values[j] = 0
        min_values[j] = 99999

for i in avg_price:
    for j in avg_price[i]:
        price = avg_price[i][j]
        max_values[j] = max(max_values[j], price)
        #skip 0 (not exist)
        if price == 0:
            continue
        min_values[j] = min(min_values[j], price)

for i in avg_price:
    for j in avg_price[i]:
        if avg_price[i][j] == 0:
            continue
        avg_price[i][j] = (avg_price[i][j] - min_values[j])/(max_values[j] - min_values[j])

#calculate weighted points
weighted_points = {}
for i in avg_price:
    weighted_points[i] = 0

for i in avg_price:
    counter = 0
    for j in avg_price[i]:
        if avg_price[i][j] == 0:
            continue
        counter += 1
        weighted_points[i] += avg_price[i][j]
    weighted_points[i] /= counter

for i in weighted_points:
    ny.at[i, 'Points'] = weighted_points[i]

# Plot using GeoPandas
# fig, ax = plt.subplots(1, 1)
# ny.plot(column='price',ax=ax, legend=True,cmap='OrRd')
# plt.show()

plot(ny)
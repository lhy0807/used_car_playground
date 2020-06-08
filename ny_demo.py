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

with open('usedcar/usedcar.json') as f:
    data = json.load(f)
ny.insert(3,'price',np.NaN)

#first collect data and calculate avg price
#then put into dataframe
avg_price = {}
counter = {}

#initialize
for car in data:
    avg_price[car['zip']] = 0
    counter[car['zip']] = 0

for car in data:
    avg_price[car['zip']] += int(car['price'].replace(',', ''))
    counter[car['zip']] += 1

for i in avg_price:
    avg_price[i] /= counter[i]

for i in avg_price:
    ny.at[i, 'price'] = avg_price[i]

# Plot using GeoPandas
# fig, ax = plt.subplots(1, 1)
# ny.plot(column='price',ax=ax, legend=True,cmap='OrRd')
# plt.show()

plot(ny)
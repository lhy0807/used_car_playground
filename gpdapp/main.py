from random import random

import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import json
import numpy as np
from io import BytesIO
import base64

from atlas_db import atlas
import pymongo

from flask import Flask, redirect, url_for, render_template, request

print("loading geojson file...")
ny = gpd.read_file("geojson/ny.geojson")
ny = ny.set_index('ZIP_CODE')
print("finish loading geojson file...")

app = Flask(__name__)

@app.route("/")
def index(df = ny):
  fig, ax = plt.subplots(1, 1)
  ny.plot(column="Points", missing_kwds={'color': 'lightgrey'}, ax=ax, legend=True)
  buf = BytesIO()
  fig.savefig(buf, format="png")
  data = base64.b64encode(buf.getbuffer()).decode("ascii")
  return render_template('index.html', fig=data)

@app.route("/model", methods=['POST'])
def model():
  code = request.form['code']
  df = ny.copy()
  file_name = "geojson/{}.json".format(code)
  with open(file_name, 'r') as f:
    data = json.load(f)
    avg_points = data[0]
    quantity = data[1]
    for i in avg_points:
      df.at[i, 'Points'] = avg_points[i]

    for i in quantity:
      df.at[i, 'Quantity'] = quantity[i]
  return redirect(url_for('index', df=df))

if __name__ == "__main__":
  app.run(host="0.0.0.0",port="5100")
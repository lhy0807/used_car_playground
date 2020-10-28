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
print("connecting to mongodb...")
client = pymongo.MongoClient(atlas)
db = client["usedcar"]
usedcar = db.cargurus
modelcode = db.modelcode
print("mongodb connected!")

app = Flask(__name__)

def model_num():
  print("get model number")
  return len(usedcar.distinct("model"))

def model_table():
  print("get models")
  return list(modelcode.find({"code":{"$in":usedcar.distinct("model")}}))

def make_pie():
#pie chart for each car make
  make = modelcode.find({"code":{"$in":usedcar.distinct("model")} }).distinct("make")
  num = []
  for i in make:
    num.append(usedcar.find({"model":{"$in":modelcode.find({"make":i},{"code":1}).distinct("code") }}).count())
  #porpotion
  porp = []
  for i in num:
    porp.append(float(np.round((i/sum(num)*100), 2)))
  return [make, porp]

@app.route("/")
def index(df = ny):
  fig, ax = plt.subplots(1, 1)
  df.plot(column="Points", missing_kwds={'color': 'lightgrey'}, ax=ax, legend=True)
  buf = BytesIO()
  fig.savefig(buf, format="png")
  data = base64.b64encode(buf.getbuffer()).decode("ascii")
  return render_template('index.html', fig=data, model_num=model_num(), model_table=model_table(),
   pie_name=json.dumps(make_pie()[0]), pie_porp=json.dumps(make_pie()[1]), pie_name_no_json=make_pie()[0] )

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
  return index(df=df)

if __name__ == "__main__":
  app.run(host="0.0.0.0",port="5100")
from random import random

import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import json
import time
import numpy as np
from io import BytesIO
import base64

from atlas_db import atlas
import pymongo

from flask import Flask, redirect, url_for, render_template, request, make_response
from concurrent.futures import ThreadPoolExecutor

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

def model_num_fn():
  print("get model number")
  return len(usedcar.distinct("model"))

def model_table_fn():
  print("get models")
  return list(modelcode.find({"code":{"$in":usedcar.distinct("model")}}))

def make_pie_fn():
#pie chart for each car make
  print("get pie chart data")
  make = modelcode.find({"code":{"$in":usedcar.distinct("model")} }).distinct("make")
  num = []
  for i in make:
    num.append(usedcar.find({"model":{"$in":modelcode.find({"make":i},{"code":1}).distinct("code") }}).count())
  #porpotion
  porp = []
  for i in num:
    porp.append(float(np.round((i/sum(num)*100), 2)))
  return [make, porp]

#init
model_num = 0
model_table = list()
pie_name = list()
pie_porp = list()
#start threads
with ThreadPoolExecutor() as executor:
  model_num_thread = executor.submit(model_num_fn)
  model_table_thread = executor.submit(model_table_fn)
  make_pie_thread = executor.submit(make_pie_fn)

@app.route("/")
def index(df = ny):

  model_num = model_num_thread.result()
  model_table = model_table_thread.result()
  pie_name = make_pie_thread.result()[0]
  pie_porp = make_pie_thread.result()[1]

  return render_template('index.html', model_num=model_num, model_table=model_table,
   pie_name=json.dumps(pie_name), pie_porp=json.dumps(pie_porp), pie_name_no_json=pie_name )

@app.route("/model", methods=['POST'])
def model():
  code = request.form['code']
  resp = make_response(redirect(url_for('index')))
  resp.set_cookie('map_code',code)
  return resp

@app.route("/ajax/map")
def ajax(df = ny):
  code = request.cookies.get("map_code")
  if code != "" and code is not None:
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

  fig, ax = plt.subplots(1, 1)
  df.plot(column="Points", missing_kwds={'color': 'lightgrey'}, ax=ax, legend=True)

  if code != "" and code is not None:
    info = modelcode.find({"code":code})[0]
    ax.set_title("New York State {} {} {}".format(info['year'],info['make'],info['model']))
  else:
    ax.set_title("New York State Map")
  buf = BytesIO()
  fig.savefig(buf, format="png", dpi=1200)
  data = base64.b64encode(buf.getbuffer()).decode("ascii")
  return data

if __name__ == "__main__":
  app.run(host="0.0.0.0",port="5100")
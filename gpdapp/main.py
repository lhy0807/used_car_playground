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
from flask_wtf.csrf import CSRFProtect


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
csrf = CSRFProtect(app)

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

@csrf.exempt
@app.route("/model", methods=['POST'])
def model():
  code = request.form['code']
  resp = make_response(redirect(url_for('index')))
  resp.set_cookie('map_code',code)
  return resp

@app.route("/ajax/map")
def ajax(df = ny):
  #TODO:
  #Modify the algo here
  df = ny.copy()
  codes = request.cookies.get("map_code")
  if codes != "" and codes is not None:
    codes = json.loads(codes)
    avg_points = {}
    quantity = {}
    for code in codes:
      file_name = "geojson/{}.json".format(code)
      with open(file_name, 'r') as f:
        data = json.load(f)
        #sum up avg_points
        for i in data[0]:
          if i in avg_points:
            avg_points[i] = avg_points[i] + data[0][i]
          else:
            avg_points[i] = data[0][i]
        
        #sum up quantity
        for i in data[1]:
          if i in quantity:
            quantity[i] = quantity[i] + data[1][i]
          else:
            quantity[i] = data[1][i]

    #calculate avg of avg_points and quantity
    max_points = 0
    min_points = 9
    max_quantity = 0
    min_quantity = 9
    for i in avg_points:
      avg_points[i] = avg_points[i] / len(codes)
      if avg_points[i] > max_points:
        max_points = avg_points[i]
      if avg_points[i] < min_points:
        min_points = avg_points[i]

    for i in quantity:
      quantity[i] = quantity[i] / len(codes)
      if quantity[i] > max_quantity:
        max_quantity = quantity[i]
      if quantity[i] < min_quantity:
        min_quantity = quantity[i]
    #normalization again
    for i in avg_points:
      avg_points[i] = (avg_points[i]-min_points)/(max_points-min_points)
    for i in quantity:
      quantity[i] = (quantity[i]-min_quantity)/(max_quantity-min_quantity)

    for i in avg_points:
      df.at[i, 'Points'] = avg_points[i]

    for i in quantity:
      df.at[i, 'Quantity'] = quantity[i]

  fig, ax = plt.subplots(1, 1)
  df.plot(column="Points", missing_kwds={'color': 'lightgrey'}, ax=ax, legend=True)

  if codes != [] and codes is not None:
    if len(codes) == 1:
      info = modelcode.find({"code":code})[0]
      ax.set_title("New York State {} {} {}".format(info['year'],info['make'],info['model']))
    else:
      ax.set_title("Multiple models in New York State")
  else:
    ax.set_title("New York State Map")
  buf = BytesIO()
  fig.savefig(buf, format="png", dpi=1200)
  data = base64.b64encode(buf.getbuffer()).decode("ascii")
  #close figure
  plt.close(fig)
  return data

if __name__ == "__main__":
  app.run(host="0.0.0.0",port="5100")
'''
THIS IS A CONVERTER!
covert the old version python class sytle model code
to mongodb database format and upload to the mongodb
'''

from model_code import model_code
from atlas_db import atlas
import pymongo

#model code recorded til the convertion
models = ['c21411','c22000','c23512','c24539','c26131','c25072','c28991','c24654','c24466','c24582','c24684','c24348']

client = pymongo.MongoClient(atlas)
db = client["usedcar"]

for code in models:
    [year, make, model] = model_code(code)
    db.modelcode.insert(
        {
            "code": code,
            "year": year,
            "make": make,
            "model": model
        }
    )
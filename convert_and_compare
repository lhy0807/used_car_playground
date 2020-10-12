
# now we will open a file for writing 
#++++++++++++converting jSON file into csv+++++++++++++++++++++++++

import json 
import csv  
import  sys

def find_deep_value(data):
# Find a the value of keys hidden within a dict[dict[...]]
    for i in data:#the value for each dic 
        text_value = i['text']
        model_value = i['model']
        zip_value = i['zip']
        price_value = i['price']
        mileage_value = i['mileage']
        writer.writerow([text_value,model_value,zip_value,price_value,mileage_value])
        
        
def create_modelVSzip(data):
    for i in data:#the value for each dic 
        model_value = i['model']
        zip_value = i['zip']
        writer.writerow([model_value,zip_value])
        
def create_modelVSprice(data):
    for i in data:#the value for each dic 
        model_value = i['model']
        price_value = i['price']
        writer.writerow([model_value,price_value])

def create_modelVSmileage(data):
    for i in data:#the value for each dic 
        model_value = i['model']
        mileage_value = i['mileage']
        writer.writerow([model_value,mileage_value])
        
        
inputFile = open("usedcar.json", 'r')  # open json file
#outputFile = open("usedcar.csv", 'w')  # load csv file
data = json.load(inputFile)  # load json content
inputFile.close() 







#-------------general data, with all info in csv file
with open('usedcar.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Text", "Model", "Zip","Price","Mileage"])
    find_deep_value(data)
    
#--------------model vs zip in csv file    
with open('usedcar_zip.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([ "Model", "Zip"])
    create_modelVSzip(data)
    
#--------------model vs price in csv file 
with open('usedcar_price.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Model","Price"])
    create_modelVSprice(data)
    
#--------------model vs mileage in csv file     
with open('usedcar_mileage.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([ "Model","Mileage"])
    create_modelVSmileage(data)


#might add more if we need to compare more different choices !!!!
#################################################################

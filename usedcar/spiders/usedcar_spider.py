import scrapy
from .url_generator import generator
import time
import re
from ..items import UsedcarItem
from .atlas_db import atlas
import pymongo
import random
import requests
from bs4 import BeautifulSoup

class UsedCarSpider(scrapy.Spider):
    name = "usedcar"

    
    def __init__(self):
        self.client = pymongo.MongoClient(atlas)
        self.db = self.client["usedcar"]
        codes = list(self.db.modelcode.find({"make":{"$in": [ "Toyota"] }},{"code":1})) 
        models = []
        for code in codes:
            models.append(code['code'])
        del codes
        self.start_urls = generator(models)
        del models
        random.shuffle(self.start_urls)
        self.url_num = len(self.start_urls)
        self.counter = 0
        self.init_time = time.time()

    def parse(self, response):
        self.counter += 1

        #parse zip code from URL
        result = re.search('zip=(.*)&show', response.url)
        zip_code = result.group(1)

        print("Zip Code: {}, Crawling {} / {}, Total Time: {} s".format(zip_code, self.counter, self.url_num, time.time()-self.init_time))
        code = response.url.split("=")[-1]

        

        '''filename = 'model-%s.html' % code
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)'''

        #read year, make, model from model code
        year = list(self.db.modelcode.find({"code":code}))[0]['year']

        #find link to the model
        for link in response.css('a'):
            if 'href="#listing=' not in link.get():
                continue
            else:
                #only search car that is in NY
                if "NY" not in link.get():
                    continue
                #find zipcode
                if re.findall("NY [0-9]{5}",link.get()) != []:
                    zip_code = re.findall("NY [0-9]{5}",link.get())[0].split(" ")[1]
                for heading in link.css('h4'):
                    if len(heading.css('span::text')) < 1:
                        continue
                    #filter irrelevant information
                    if "\n" in heading.css('span::text')[0].get():
                        continue
                    
                    #skip search with incorrect matching
                    if str(year) not in heading.css('span::text')[0].get():
                        break
                    
                    #parse price
                    if re.search('- \$(.*) - ', heading.css('span::text')[0].get()) is None:
                        continue
                    price = re.search('- \$(.*) - ', heading.css('span::text')[0].get()).group(1)
                    

                    #parse mileage
                    if re.search(' - ([0-9,]*) miles ', heading.css('span::text')[0].get()) is None:
                        continue
                    mileage = re.search(' - ([0-9,]*) miles ', heading.css('span::text')[0].get()).group(1)
                    

                    #parse model
                    model = response.url.split("selectedEntity=")[1]

                    usedcar = UsedcarItem()
                    usedcar['text'] = heading.css('span::text')[0].get()
                    usedcar['year'] = year
                    usedcar['model'] = model
                    usedcar['zipcode'] = zip_code
                    usedcar['price'] = price
                    usedcar['mileage'] = mileage
                    
                    yield usedcar
    def parse2(self, response):
        print(response)
        return response
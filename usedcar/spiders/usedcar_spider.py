import scrapy
from .model_code import model_code
from .url_generator import generator
import time
import re


class UsedCarSpider(scrapy.Spider):
    name = "usedcar"
    '''
    Selected Models (in order):
    2015 BMW 3 Series - c24539
    2015 Toyota Camry - c24654
    2015 VW Jetta - c24466
    2015 MB E-Class - c24582
    2015 Honda CRV - c24684
    2015 Subaru Forester - c24348
    '''
    #models = ['c24539','c24654','c24466','c24582','c24684','c24348']
    #start_urls = generator(models)
    
    def __init__(self):
        models = ['c24539','c24654','c24466','c24582','c24684','c24348']
        start_urls = generator(models)
        self.start_urls = generator(models)
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
        [year, make, model] = model_code(code)

        
        for heading in response.css('h4'):
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

            #year
            yield {
                'text': heading.css('span::text')[0].get(),
                'model': model,
                'zip': zip_code,
                'price': price,
                'mileage': mileage
            }
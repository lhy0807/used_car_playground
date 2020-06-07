import scrapy
from .model_code import model_code
from .url_generator import generator
import time
import re


class UsedCarSpider(scrapy.Spider):
    name = "usedcar"

    start_urls = generator()
    
    def __init__(self):
        self.start_urls = generator()
        self.url_num = len(self.start_urls)
        self.counter = 0
        self.init_time = time.time()

    def parse(self, response):
        self.counter += 1

        #parse zip code from URL
        result = re.search('zip=(.*)&show', response.url)
        zip_code = result.group(1)

        print("Zip Code: {}, Crawling {} / {}, {} s".format(zip_code, self.counter, self.url_num, time.time()-self.init_time))
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
            price = re.search('- \$(.*) - ', heading.css('span::text')[0].get()).group(1)

            #parse mileage
            mileage = re.search(' - ([0-9,]*) miles ', heading.css('span::text')[0].get()).group(1)

            #year
            yield {
                'text': heading.css('span::text')[0].get(),
                'zip': zip_code,
                'price': price,
                'mileage': mileage
            }
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UsedcarItem(scrapy.Item):
    text = scrapy.Field()
    year = scrapy.Field()
    model = scrapy.Field()
    zipcode = scrapy.Field()
    price = scrapy.Field()
    mileage = scrapy.Field()
    pass

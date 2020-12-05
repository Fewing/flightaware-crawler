# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlightawareItem(scrapy.Item):
    # define the fields for your item here like:
    data_type = scrapy.Field()
    ident = scrapy.Field() #航班标识符
    airline = scrapy.Field() #航空公司
    type = scrapy.Field() #机型
    origin = scrapy.Field() #出发地
    destination = scrapy.Field() #目的地
    departure_time = scrapy.Field() #出发时间
    arrive_time = scrapy.Field() #到达时间

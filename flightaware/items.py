# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlightawareItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    data_type = scrapy.Field()
    f_ident = scrapy.Field()
    f_airline = scrapy.Field()
    f_type = scrapy.Field()
    f_from = scrapy.Field()
    f_to = scrapy.Field()
    f_depart = scrapy.Field()
    f_arrive = scrapy.Field()

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

class WeatherItem(scrapy.Item):
    data_type = scrapy.Field()
    date = scrapy.Field() #日期
    time = scrapy.Field() #时间（EST）
    flight_rules = scrapy.Field() #飞行准则
    wind_dir = scrapy.Field() #风向
    wind_speed = scrapy.Field() #风速
    type = scrapy.Field() #不知道是啥
    high_agl = scrapy.Field() #不知道是啥
    visibility = scrapy.Field() #能见度
    remarks = scrapy.Field() #备注

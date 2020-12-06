# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from os import supports_bytes_environ
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter


class FlightawarePipeline:
    
    weather = []
    arrive = []
    departure = []
    enroute = []
    scheduled = []

    def open_spider(self, spider):
        file_name =  spider.airport
        self.file = open(f'{file_name}.json', 'wb')
        spider.logger.info(f'开始爬取{spider.airport}机场数据')

    def close_spider(self, spider):
        spider.logger.info(f'爬取天气预报信息{len(self.weather)}')
        spider.logger.info(f'爬取到达航班{len(self.arrive)}',)
        spider.logger.info(f'爬取离港航班{len(self.departure)}')
        spider.logger.info(f'爬取计划前往航班{len(self.enroute)}')
        spider.logger.info(f'爬取计划离港航班{len(self.scheduled)}')
        output_json = {}
        output_json['weather'] = self.weather
        output_json['arrive'] = self.arrive
        output_json['departure'] = self.departure
        output_json['enroute'] = self.enroute
        output_json['scheduled'] = self.scheduled
        self.file.write(json.dumps(output_json,ensure_ascii=False,indent=4, sort_keys=True).encode('utf-8')) #输出到文件
        self.file.close()

    def process_item(self, item, spider):
        #暂存数据到列表
        if item['data_type'] == 'arrive':
            item_dict = dict(item)
            item_dict.pop('data_type')
            self.arrive.append(item_dict)
        elif item['data_type'] == 'departure':
            item_dict = dict(item)
            item_dict.pop('data_type')
            self.departure.append(item_dict)
        elif item['data_type'] == 'enroute':
            item_dict = dict(item)
            item_dict.pop('data_type')
            self.enroute.append(item_dict)
        elif item['data_type'] == 'scheduled':
            item_dict = dict(item)
            item_dict.pop('data_type')
            self.scheduled.append(item_dict)
        elif item['data_type'] == 'weather':
            item_dict = dict(item)
            item_dict.pop('data_type')
            self.weather.append(item_dict)
        return item

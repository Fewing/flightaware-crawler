# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter


class FlightawarePipeline:

    arrive = []
    departure = []
    enroute = []
    scheduled = []

    def open_spider(self, spider):
        self.file = open('kjfk.json', 'wb')

    def close_spider(self, spider):
        output_json = {}
        output_json['arrive'] = self.arrive
        output_json['departure'] = self.departure
        output_json['enroute'] = self.enroute
        output_json['scheduled'] = self.scheduled
        self.file.write(json.dumps(output_json,ensure_ascii=False).encode('utf-8')) #输出到文件
        self.file.close()

    def process_item(self, item, spider):
        if item['data_type'] == 'arrive':
            self.arrive.append(dict(item))
        elif item['data_type'] == 'departure':
            self.departure.append(dict(item))
        elif item['data_type'] == 'enroute':
            self.enroute.append(dict(item))
        elif item['data_type'] == 'scheduled':
            self.scheduled.append(dict(item)) #暂存到列表
        return item

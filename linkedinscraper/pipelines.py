# -*- coding: utf-8 -*-
import json

from itemadapter import ItemAdapter
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%d_%m_%Y_%H_%M")
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class ScraperPipeline(object):
#    def process_item(self, item, spider):
#        return item

class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open(spider.name + dt_string + '.json', 'w')
        self.file.write("'items': { [")

    def close_spider(self, spider):
        self.file.write("]}")
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict())
        self.file.write(line + ",")
        return item

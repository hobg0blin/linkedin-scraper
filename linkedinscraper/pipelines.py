# -*- coding: utf-8 -*-
import json

from itemadapter import ItemAdapter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class ScraperPipeline(object):
#    def process_item(self, item, spider):
#        return item

class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open('company.json', 'w')
        self.file.write("'items': { [")

    def close_spider(self, spider):
        self.file.write("]}")
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict())
        self.file.write(line + ",")
        return item

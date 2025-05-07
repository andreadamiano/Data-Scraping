# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime 
from string import whitespace
from wikiSpider.items import Article

class WikispiderPipeline: #process the data asynchronously
    def process_item(self, article, spider):
        return article

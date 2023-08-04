# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json
import logging
import sqlite3
import pymongo

class GloboesportePipeline:

    def open_spider(self, spider):
        logging.warning('***************** SPIDER OPENED - PIPELINE *****************')

    def close_spider (self, spider):
        logging.warning('***************** SPIDER CLOSED - PIPELINE *****************')

    def process_item(self, item, spider):
        return item
   
    
class MongodbPipeline:
    collection_name = 'GE_Flamengo_2023_News'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://globoesporte_webscraping:gPbuLCGnbnH2ApAG@globoesporte.o6lbwjs.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['GloboEsporte_Scraped_Data']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


class SQLitePipeline:
    collection_name = 'articles'

    def open_spider(self, spider):
        self.connection = sqlite3.connect("ge_articles.db")
        self.c = self.connection.cursor()

        try:
            self.c.execute('''
                CREATE TABLE ge_transcripts(
                    title TEXT,
                    subtitle TEXT,
                    author TEXT,
                    text TEXT,
                    quotes TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass 

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        # Convert the quotes list of dictionaries to a JSON string
        item['quotes'] = json.dumps(item['quotes'])

        self.c.execute('''
            INSERT INTO ge_transcripts (title, subtitle, author, text, quotes) VALUES (?, ?, ?, ?, ?)
        ''', (
            item['title'],
            item['subtitle'],
            item['author'],
            item['text'],
            item['quotes'],
        ))
        self.connection.commit()
        return item
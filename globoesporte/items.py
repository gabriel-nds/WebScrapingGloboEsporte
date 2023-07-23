# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GloboesporteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JournalItem(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    author = scrapy.Field()
    city = scrapy.Field()
    text = scrapy.Field()
    quotes = scrapy.Field()
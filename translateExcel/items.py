# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TranslateexcelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    package = scrapy.Field()
    summary = scrapy.Field()
    pass

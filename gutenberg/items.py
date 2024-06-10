# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GutenbergItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GutenbergEbook(scrapy.Item):
    index = scrapy.Field()
    id = scrapy.Field()
    bookshelf_name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    downloads = scrapy.Field()
    text = scrapy.Field()
    text_file = scrapy.Field()
    
    pass
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AmazonProduct(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    asin = scrapy.Field()
    item_name = scrapy.Field()
    bullet_point = scrapy.Field()
    images = scrapy.Field()
    image_count = scrapy.Field()
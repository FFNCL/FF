# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IqiyiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
        title = scrapy.Field()  # 字段,标题
        img = scrapy.Field()  # 图片
        subject = scrapy.Field()

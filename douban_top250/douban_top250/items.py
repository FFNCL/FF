import scrapy


class DoubanTop250Item(scrapy.Item):
    link = scrapy.Field()  # 链接
    imgSrc = scrapy.Field()  # 图片
    ctitle = scrapy.Field()  # 中文名
    otitle = scrapy.Field()  # 英文名
    rating = scrapy.Field()  # 评分
    judgeNum = scrapy.Field()  # 评价数
    inq = scrapy.Field()  # 概况
    bd = scrapy.Field()  # 相关信息
    optional = scrapy.Field()  # 国家
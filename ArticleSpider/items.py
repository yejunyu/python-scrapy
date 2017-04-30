# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import os
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
import datetime

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#会把title取的值传给value
def add_jobbole(value):
    return value+"-jobbole"


def date_convert(value):
    #os.system(u"echo %s >> a.txt"%value)
    try:
        create_date = datetime.datetime.strptime(value,"%Y/%m/%d").date()
    except Exception as e:
     #   os.system("echo %s >> a.txt"% e)
        create_date = datetime.datetime.now().date()

    return create_date


class ArticleItemLoader(ItemLoader):
    #自定义的ItemLoader，使默认取第一个
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        #input_processor = MapCompose(add_jobbole)
        #input_processor = MapCompose(lambda x:x+'-jobbole'),
    )
    create_date = scrapy.Field(
        #input_processor = MapCompose(date_convert),
        #output_processor = TakeFirst()
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()

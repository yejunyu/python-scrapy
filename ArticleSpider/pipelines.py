# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy.pipelines.images import ImagesPipeline

#这里来写入数据库
class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class ArticleImagePipeline(ImagesPipeline):
    #重写这个方法，这个方法用来存放图片实际url
    def item_completed(self, results, item, info):
        #results第一个值为True代表下载成功
        for ok,value in results:
            image_file_path = value['path']
        item["front_image_path"] = image_file_path
        return item
        pass

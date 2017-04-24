# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import codecs
import json
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

#这里来写入数据库
class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipelines(object):
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False)+"\n"
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()

class JsonExporterPipeline(object):
    #调用scrapy提供的到处json功能
    def __init__(self):
        self.file = open('articleexport.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding="utf8",ensure_ascii=False)
        self.exporter.start_exporting()
    def process_item(self,item,spider):
        self.exporter.export_item(item=item)
        return item
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('0.0.0.0','root','123456','scrapy',charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()
    def process_item(self,item,spider):
        insert_sql = """
            insert into jobbole(title,url,create_date,fav_nums)
            values(%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item['title'],item['url'],item['create_date'],item['fav_nums']))
        self.conn.commit()

class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    #固定用法from_settings
    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)
    def process_item(self,item,spider):
        #用twisted异步写数据库
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)

    def handle_error(self,failure):
        print (failure)

    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = """
            insert into jobbole(title,url,create_date,fav_nums)
            values(%s,%s,%s,%s)
        """
        cursor.execute(insert_sql,(item['title'],item['url'],item['create_date'],item['fav_nums']))



class ArticleImagePipeline(ImagesPipeline):
    #重写这个方法，这个方法用来存放图片实际url
    def item_completed(self, results, item, info):
        #results第一个值为True代表下载成功
        for ok,value in results:
            image_file_path = value['path']
        item["front_image_path"] = image_file_path
        return item
        pass

# -*- coding: utf-8 -*-
import pymysql
from scrapy.pipelines.images import ImagesPipeline


class GirlspiderPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', db='girs',
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'insert into mmjpg(title,tags,url,path) values (%s,%s,%s,%s)'
        self.cursor.execute(sql, (item['title'], item['tags'], item['img_url'][0], item['path']))
        self.conn.commit()
        return item


class MMJPGImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'img_url' in item:
            for ok, value in results:
                image_file_path = value['path']
            item['path'] = image_file_path[5:]
        return item


class MM131SpiderPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', db='girs',
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'insert into mm131 (title,tag,url,path) values (%s,%s,%s,%s)'
        self.cursor.execute(sql, (item['title'], item['tag'], item['img_url'][0], item['path']))
        self.conn.commit()
        return item

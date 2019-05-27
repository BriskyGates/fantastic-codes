# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import hashlib
import os

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

from meinv import settings
from meinv.utils.mydb import DB


class MeinvPipeline(object):
    def __init__(self):
        self.db=DB()

    def process_item(self, item, spider):
        self.db.add(item)
        return item

    def __del__(self):
        self.db.conn.close()


# class CsvPipeline(object):
#     def __init__(self):
#
#         self.file = open(os.path.join(settings.CSV_DIR, 'mv.csv'), 'a',encoding='utf-8')
#
#     def process_item(self, item, spider):
#         # 保存数据
#         """
#
#
#         :param item:
#         :param spider:
#         :return:
#
#         {'star_name': '秋瓷炫 Choo Ja Hyun',
#
#         'image_urls': ['http://www.meinv.hk/wp-content/uploads/2017/10/2017102623334659.jpg',
#                         'http://www.meinv.hk/wp-content/uploads/2017/10/2017102623334787.jpg'],
#
#         'images': ['images\\秋瓷炫 Choo Ja Hyun/0056470443b56d0d7a24c70c0c1334bd.jpg',
#                     'images\\秋瓷炫 Choo Ja Hyun/f3994d0151d1d2013c7e525f45b8d43e.jpg']}
#
#         """
#
#         data={
#             'star_name':item['star_name'],
#             'images':item['images']
#         }
#
#         writer = csv.DictWriter(self.file,
#                                 fieldnames=('star_name', 'images'))
#
#         writer.writerow(data)
#
#         return item
#     # 整个csv文件填写完毕后关闭文件指针
#     def __del__(self):
#         self.file.close()


class MeinvImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        """

        :param item:
        :param info:
        :return:
        """
        for img_url in item.get('image_urls'):
            yield Request(img_url,meta={
                # 将美女的name加入到info
                'star_name':item.get('star_name')
            })

    def file_path(self, request, response=None, info=None):
        # 定制 下载的每张图片存放的位置， 相对于IMAGES_STORE位置
        dirname=request.meta.get('star_name') # 每位明星放在自己的目录中
        # mn_dir = os.path.join('images', dirname)的结果如下:
        # mn_dir是基于IMAGES_STORE的
        # 原本是在IMAGES_STORE的基础上,又创建了各位明星的目录(IMAGES_STORE/star_name)
        # 然而最终图片存储放在mv_dir中,也就是IMAGES_STORE/images/dirname
        mn_dir=os.path.join(settings.IMAGES_STORE,dirname)
        if not os.path.exists(mn_dir):
            os.makedirs(mn_dir)  # 创建多级目录os.mkdir()创建单级目录

        img_url=request.url.split('/')[-1]
        ext_name=os.path.splitext(img_url)[-1]

        # 将文件名转成32位的编码格式
        md5_=hashlib.md5()
        md5_.update(img_url.encode())
        filename=md5_.hexdigest()+ext_name

        # 相对settings.IMAGES_STORE的子目录
        return f'{mn_dir}/{filename}'

    def item_completed(self, results, item, info):
        # 当下载完成以后，获取下载图片存放的位置
        # 将位置设置到 item中， 以便于存储数据（csv,  excel,  mysql, sqlite）
        '''
        [(True,
          {'checksum': '2b00042f7481c7b056c4b410d28f33cf',
           'path': 'full/0a79c461a4062ac383dc4fade7bc09f1384a3910.jpg',
           'url': 'http://www.example.com/files/product1.pdf'
           }
         ),
         (False,
          Failure(...))]
        '''
        print(results)
        image_paths=[x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('此item 不包含图片')
        item['images']=image_paths
        return item
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MnSpider(CrawlSpider):
    name = 'mn'
    allowed_domains = ['www.meinv.hk']
    start_urls = ['http://www.meinv.hk/']

    rules = (
        # 因为在要提取的链接后头加入/,出错
        Rule(LinkExtractor(allow=r'http://www.meinv.hk/\?p=\d+'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        print('gogoogogogog')
        item = {}

        item['star_name'] = response.xpath('//h1[@class="title"]/text()').get()
        print(item['star_name'])
        item['image_urls'] = response.xpath('//div[@class="post-content"]//img/@src').extract()
        print(item['image_urls'])
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item

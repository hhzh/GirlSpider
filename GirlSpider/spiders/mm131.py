# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import Request
from GirlSpider.items import MM131SpiderItem


class Mm131Spider(scrapy.Spider):
    name = "mm131"
    allowed_domains = ["mm131.com"]
    start_urls = ['http://mm131.com/xinggan/', 'http://mm131.com/qingchun/', 'http://mm131.com/xiaohua/',
                  'http://mm131.com/chemo/', 'http://mm131.com/qipao/', 'http://mm131.com/mingxing/']

    def parse(self, response):
        tag = response.xpath('//div[@class="main"]/dl/dt[@class="public-title"]/a[2]/text()').extract_first('')
        title = response.xpath('//div[@class="main"]/dl/dd/a/text()').extract_first('')
        img_packages = response.xpath('//div[@class="main"]/dl/dd/a/@href').extract()
        for img_package in img_packages:
            yield Request(url=parse.urljoin(response.url, img_package), meta={'title': title, 'tag': tag},
                          callback=self.parse_detail)
        next_node = response.xpath('//div[@class="main"]/dl/dd[@class="package"]/a[@class="page-en"]')
        next_title = next_node.xpath('text').extract_first('')
        if '下一页' in next_title:
            next_url = next_node.xpath('@href').extract_first('')
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        item = MM131SpiderItem()
        title = response.meta.get('title', '')
        tag = response.meta.get('tag', '')
        img_url = response.xpath('//div[@class="content"]/div[@class="content-pic"]/a/img/@src').extract_first('')
        item['title'] = title
        item['tag'] = tag
        item['img_url'] = [img_url]
        next_detail = response.xpath(
            '//div[@class="content"]/div[@class="content-page"]/a[last()]/@href').extract_first('none')
        if 'none' not in next_detail:
            yield Request(url=parse.urljoin(response.url, next_detail), meta={'title': title, 'tag': tag},
                          callback=self.parse_detail)
        yield item

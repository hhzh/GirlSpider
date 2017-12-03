# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from GirlSpider.items import MMJPGSpiderItem


class MmjpgSpider(scrapy.Spider):
    name = "mmjpg"
    allowed_domains = ["mmjpg.com"]
    start_urls = ['http://mmjpg.com/']

    def parse(self, response):
        img_nodes = response.xpath('//div[@class="pic"]/ul/li/a')
        for img_node in img_nodes:
            img_package = img_node.xpath('@href').extract_first('')
            title = img_node.xpath('img/@alt').extract_first('')
            yield Request(url=parse.urljoin(response.url, img_package), meta={'title': title},
                          callback=self.parse_detail)
        next_url = response.xpath('//div[@class="page"]/a[@class="ch"]/@href').extract_first('')
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        item = MMJPGSpiderItem()
        title = response.meta.get('title', '')
        img_url = response.xpath('//div[@id="content"]/a/img/@src').extract_first('')
        item['title'] = title
        item['img_url'] = [img_url]

        next_detail = response.xpath('//div[@id="page"]/a[@class="ch next"]/@href').extract_first('')
        next_title = response.xpath('//div[@id="page"]/a[@class="ch next"]/text()').extract_first('')
        if next_detail and '页' in next_title:
            yield Request(url=parse.urljoin(response.url, next_detail), meta={'title': title},
                          callback=self.parse_detail)
        yield item

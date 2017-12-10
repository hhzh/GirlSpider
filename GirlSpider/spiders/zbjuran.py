# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import Request
from GirlSpider.items import ZbjuranSpiderItem


class ZbjuranSpider(scrapy.Spider):
    name = "zbjuran"
    allowed_domains = ["zbjuran.com"]
    start_urls = ['http://www.zbjuran.com/mei/xiaohua/']

    def parse(self, response):
        img_nodes = response.xpath('//div[@class="main"]/div/ul/li')
        for img_node in img_nodes:
            title = img_node.xpath('div[@class="name"]/a/text()').extract_first('')
            img_package = img_node.xpath('div[@class="picbox"]/div/b/a/@href').extract_first('')
            yield Request(url=parse.urljoin(response.url, img_package), meta={'title': title},
                          callback=self.parse_detail)
        next_node = response.xpath('//div[@class="pages"]/a[last()-1]')
        next_title = next_node.xpath('text()').extract_first('')
        if '下一页' in next_title:
            next_url = next_node.xpath('@href').extract_first('')
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        item = ZbjuranSpiderItem()
        title = response.meta.get('title', '')
        tag = 'xiaohua'
        img_url = response.xpath('//div[@class="main"]/div[@class="arc"]/div[@class="box"]/center/div[@class="picbox"]/img/@src').extract_first('')
        item['title'] = title
        item['tag'] = tag
        item['img_url'] = [parse.urljoin('http://img.zbjuran.com', img_url)]
        next_detail = response.xpath('//div[@class="page"]/li[last()-1]/a')
        next_title = next_detail.xpath('text()').extract_first('')
        next_url = next_detail.xpath('@href').extract_first('')
        if '下一页' in next_title and '.html' in next_url:
            yield Request(url=parse.urljoin(response.url, next_url), meta={'title': title}, callback=self.parse_detail)
        yield item

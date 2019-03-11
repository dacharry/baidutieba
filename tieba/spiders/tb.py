# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
from lxml import etree

from tieba.items import TiebaItem


class TbSpider(scrapy.Spider):
    name = 'tb'
    allowed_domains = ['baidu.com']
    start_urls = ['http://tieba.baidu.com/f?kw=%E7%8C%AB']
    page = 0
    max_page = 4
    def parse(self, response):
        html = re.findall(r'pagelet_html_frs-list/pagelet/thread_list" style="display:none;"><!--(.*?)--></code>',
                          response.body.decode(), re.S)[0]
        html = etree.HTML(html)
        li_list = html.xpath('//ul[@id="thread_list"]//li[@class=" j_thread_list clearfix"]')
        for li in li_list:
            item = TiebaItem()
            item['title'] = li.xpath('.//a/text()')[0]
            item['li_url'] = li.xpath('.//a/@href')[0]
            # print(item)
            item['img_list'] = []
            if item['li_url']:
                yield response.follow(
                    item['li_url'], callback=self.parse_detail,
                    meta={'item': item})
        next_page = html.xpath('//div[@id="frs_list_pager"]/a[contains(@class,"next")]/@href')[0]
        if next_page and self.page < self.max_page:
            self.page += 1
            yield response.follow(
                next_page,
                callback=self.parse
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['img_list'] = response.xpath('//cc//img[@class="BDE_Image"]/@src').extract()
        # item['img_list'].extend()
        next_page = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse_detail, meta={'item': item})
        else:
            yield item

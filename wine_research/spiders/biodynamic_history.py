# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.loader import ItemLoader
from scrapy.http import Request

from wine_research.items import BiodynamicHistoryItem


class BiodynamicHistorySpider(Spider):
    name = 'BiodynamicHistorySpider'
    start_urls = ['https://web.archive.org/web/*/http://www.biodynamicfood.org/beyond-organic/a/']

    def parse(self, response):





    #
    #     for _ in range(5):
    #         yield Request('http://www.google.com/', callback=self.test, dont_filter=True)
    #
    # def test(self, response):
    #     loader = ItemLoader(item=BiodynamicHistoryItem(), response=response)
    #     print('hello world')
    #
    #     loader.add_value('name', 'test1')
    #     loader.add_value('value', 'test2')
    #
    #     return loader.load_item()

# -*- coding: utf-8 -*-
import scrapy


class SipspiderSpider(scrapy.Spider):
    name = 'SIPSpider'
    allowed_domains = ['sipcertified.org']
    start_urls = ['http://sipcertified.org/']

    def parse(self, response):
        pass

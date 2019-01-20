# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.loader import ItemLoader
from scrapy.http import Request

from wine_research.items import BiodynamicHistoryItem


class BiodynamicHistorySpider(Spider):
    name = 'BiodynamicHistorySpider'
    start_urls = ['https://web.archive.org/web/20141009050729/http://www.biodynamicfood.org:80/beyond-organic/a']

    def parse(self, response):
        for organization in response.xpath('//*[starts-with(@class, "abc_list_item index")]'):
            loader = ItemLoader(item=BiodynamicHistoryItem(), selector=organization)
            loader.add_value('date', response.url[28:36])

            name = organization.xpath('(.//a[@class="list_link"])[1]/text()').extract_first()
            loader.add_value('name', name)

            relative_link = organization.xpath('.//a/@href').extract()[0]
            link = response.urljoin(relative_link)
            loader.add_value('link', link)

            address = organization.xpath('.//div/div/div/p/text()').extract()[:2]
            loader.add_value('address', address)

            yield loader.load_item()
            yield Request(link, callback=self.parse_organization)

        abc_relative_urls = response.xpath('(//*[@class="links-abc list-inline"])[1]/li/a/@href').extract()
        abc_absolute_urls = [response.urljoin(url) for url in abc_relative_urls]
        for url in abc_absolute_urls:
            yield Request(url, callback=self.parse)

        next_page = response.xpath('//*[@class="f"]/a/@href').extract_first()
        if next_page:
            yield Request(next_page, callback=self.parse)

        previous_page = response.xpath('//*[@class="b"]/a/@href').extract_first()
        if previous_page:
            yield Request(previous_page, callback=self.parse)

    def parse_organization(self, response):

        next_record = response.xpath('//*[@class="f"]/a/@href').extract_first()
        if next_record:
            yield Request(next_record, callback=self.parse_organization)

        previous_record = response.xpath('//*[@class="b"]/a/@href').extract_first()
        if previous_record:
            yield Request(previous_record, callback=self.parse_organization)

        loader = ItemLoader(item=BiodynamicHistoryItem(), response=response)

        loader.add_value('date', response.url[28:36])
        loader.add_value('link', response.url)
        loader.add_xpath('name', '//h1/text()')

        address = response.xpath('//div[@class="member-address"]/p/text()').extract()[:2] or ''
        loader.add_value('address', address)

        contact_info = response.xpath('//div[@class="member-address"]/p/text()').extract()
        contact_info = [line.strip() for line in contact_info]
        phone = [line for line in contact_info if line.startswith('Phone: ')] or ''
        loader.add_value('phone', phone)

        email = response.xpath('//div[@class="member-address"]//a[1]/text()').extract_first() or ''
        loader.add_value('email', email)

        website = response.xpath('//div[@class="member-address"]//a[2]/text()').extract_first() or ''
        loader.add_value('website', website)

        profile = response.xpath('//div[@class="member-profile"]/div/p/text()').extract()
        profile = [element.strip() for element in profile]
        profile = [element for element in profile if element] or ''
        acreage = [element for element in profile if element.startswith('Total Acreage')] or ''
        loader.add_value('acreage', acreage)
        loader.add_value('profile', profile)

        crops = response.xpath('//div[p/*/text()="Crops"]//li//text()').extract() or ''
        loader.add_value('crops', crops)

        processed_products = response.xpath('//div[p/*/text()="Processed Product"]//li//text()').extract() or ''
        loader.add_value('processed_products', processed_products)

        business = response.xpath('//*[@class="business-type"]/text()').extract_first()
        loader.add_value('business', business)

        yield loader.load_item()

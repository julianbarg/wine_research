# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.loader import ItemLoader
from scrapy.http import Request

from wine_research.items import BiodynamicHistoryItem


class BiodynamicHistorySpider(Spider):
    name = 'BiodynamicHistorySpider'
    start_urls = ['https://web.archive.org/web/20141009050729/http://www.biodynamicfood.org:80/beyond-organic/a']

    def parse(self, response):
        # Get months
        next_page = response.xpath('//*[@class="f"]/a/@href').extract_first()
        if next_page:
            yield Request(next_page, callback=self.parse)

        abc_relative_urls = response.xpath('(//*[@class="links-abc list-inline"])[1]/li/a/@href').extract()
        abc_absolute_urls = [response.urljoin(url) for url in abc_relative_urls]
        for url in abc_absolute_urls:
            yield Request(url, callback=self.find_organizations)

    def find_organizations(self, response):
        organization_relative_urls = response.xpath(
            '//*[starts-with(@class, "abc_list_item index")]/div/div/h3/a/@href').extract()
        organization_absolute_urls = [response.urljoin(url) for url in organization_relative_urls]
        for url in organization_absolute_urls:
            yield Request(url, callback=self.parse_organizations)

    def parse_organizations(self, response):

        loader = ItemLoader(item=BiodynamicHistoryItem(), response=response)

        date = response.url[28:36]
        loader.add_value('date', date)

        name = response.xpath('//h1/text()').extract_first()
        loader.add_value('name', name)

        category = response.xpath('//h2[@class="business-type"]/text()').extract_first()
        loader.add_value('category', category)

        address_field_1 = response.xpath('//div[@class="member-address"]/p/text()[1]').extract_first().strip()
        address_field_2 = response.xpath('//div[@class="member-address"]/p/text()[2]').extract_first().strip()
        address = address_field_1 + '\n' + address_field_2
        loader.add_value('address', address)

        contact_info = response.xpath('//div[@class="member-address"]/p/text()').extract()
        contact_info = [line.strip() for line in contact_info]
        phone = [line for line in contact_info if line.startswith('Phone: ')]
        if phone:
            phone = phone[0]
            phone = phone.replace('Phone: ', '')
        loader.add_value('phone', phone)
        email = response.xpath('//div[@class="member-address"]//a[1]/text()').extract_first()
        loader.add_value('email', email)
        website = response.xpath('//div[@class="member-address"]//a[2]/text()').extract_first()
        loader.add_value('website', website)
        short_description = response.xpath('//p[@class="quote"]/text()').extract_first()
        loader.add_value('short_description', short_description)

        profile = response.xpath('//div[@class="member-profile"]/div/p/text()').extract()
        profile = [element.strip() for element in profile]
        profile = [element for element in profile if element]
        acreage = [element for element in profile if element.startswith('Total Acreage')]
        if acreage:
            acreage = acreage[0]
            acreage = acreage.replace('Total Acreage: ', '')
        loader.add_value('acreage', acreage)
        profile = '\n'.join(profile)
        loader.add_value('profile', profile)

        crops = response.xpath('//div[p/*/text()="Crops"]//li//text()').extract()
        crops = ','.join(crops)
        loader.add_value('crops', crops)

        processed_products = response.xpath('//div[p/*/text()="Processed Product"]//li//text()').extract()
        processed_products = ','.join(processed_products)
        loader.add_value('processed_products', processed_products)

        return loader.load_item()

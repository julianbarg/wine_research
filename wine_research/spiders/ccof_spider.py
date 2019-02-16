# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request


class CcofSpiderSpider(Spider):
    name = 'ccof_spider'
    allowed_domains = ['ccof.org']
    start_urls = ['http://www.ccof.org/members?title=&field_contact_address_locality=&field_contact_address'\
                  + '_administrative_area=4&field_contact_address_postal_code=&field_chapter_ref=All&field_'\
                  + 'products_services=wine%2CGrapes+%28Wine%29%2CRed+Wine%2CWhite+Wine%2CWine%2CWine+%28Sparkling'\
                  + '%29&field_products_services_1=%2C+%22Wine+Bottling+%28Client+Profile+Products+only%29%22%2C'\
                  + '+%22Wine+Making+%28Client+Profile+Products+only%29%22%2C+%22Vinegar+%28Wine%29%22%2C+%22Swine'\
                  + '%22%2C+%22Wine+Bottling%22%2C+%22Wine+Making%22%2C+%22Grapes+%28Wine%29+%28Transitional%29%22']

    def parse(self, response):
        for organization in response.urljoin(response.xpath('//h3/a/@href')):
            yield Request(organization, callback=self.parse_organization)

        relative_next_page = response.xpath('//*[@class="pager-next"]/a/@href').extract_first()
        if relative_next_page:
            absolute_next_page = response.urljoin(relative_next_page)
            yield Request(absolute_next_page, callback=self.parse)

    def parse_organization(self, response):
        chapters = response.xpath('//*[starts-with(@class, "field field-name-field-chapter-ref")]//a/text()').extract()

        description = response.xpath(
            '//*[starts-with(@class, "field field-name-body field-type-text-with-summary")]//text()').extract_first()

        products = response.xpath(
            '//*[starts-with(@class, "field field-name-field-products-services")]//li/text()').extract()

        channels = response.xpath(
            '//*[starts-with(@class, "field field-name-field-sales-methods")]//li/text()').extract()

        acres = response.xpath('(//*[starts-with(@class, "field field-name-field-acres")]//text())[2]').extract_first()

        crops_license = response.xpath('//*[text()="Crops"]/../../..//text()').extract()

        handling_license = response.xpath('//*[text()="Handling"]/../../..//text()').extract()

        USDA_NOP_license = response.xpath('//*[text()="USDA NOP"]/../../..//text()').extract()


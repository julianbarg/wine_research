# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.loader import ItemLoader
from scrapy.http import Request

from wine_research.items import CCOFItem


class CCOFSpider(Spider):
    name = 'CCOFSpider'
    allowed_domains = ['ccof.org']
    start_urls = ['http://www.ccof.org/members?title=&field_contact_address_locality=&field_contact_address'\
                  + '_administrative_area=4&field_contact_address_postal_code=&field_chapter_ref=All&field_'\
                  + 'products_services=wine%2CGrapes+%28Wine%29%2CRed+Wine%2CWhite+Wine%2CWine%2CWine+%28Sparkling'\
                  + '%29&field_products_services_1=%2C+%22Wine+Bottling+%28Client+Profile+Products+only%29%22%2C'\
                  + '+%22Wine+Making+%28Client+Profile+Products+only%29%22%2C+%22Vinegar+%28Wine%29%22%2C+%22Swine'\
                  + '%22%2C+%22Wine+Bottling%22%2C+%22Wine+Making%22%2C+%22Grapes+%28Wine%29+%28Transitional%29%22']

    custom_settings = {
        'ITEM_PIPELINES': {
            'wine_research.pipelines.CCOFPipeline': 300,
        }
    }

    def parse(self, response):
        organization_relative_links = response.xpath('//h3/a/@href').extract()
        organization_absolute_links = [response.urljoin(link) for link in organization_relative_links]
        for organization in organization_absolute_links:
            yield Request(organization, callback=self.parse_organization)

        relative_next_page = response.xpath('//*[@class="pager-next"]/a/@href').extract_first()
        if relative_next_page:
            absolute_next_page = response.urljoin(relative_next_page)
            yield Request(absolute_next_page, callback=self.parse)

    def parse_organization(self, response):
        loader = ItemLoader(item=CCOFItem(), response=response)

        chapters = response.xpath('//*[starts-with(@class, "field field-name-field-chapter-ref")]//a/text()').extract()
        loader.add_value('chapters', chapters)

        description = response.xpath(
            '//*[starts-with(@class, "field field-name-body field-type-text-with-summary")]//text()').extract_first()
        loader.add_value('description', description)

        products = response.xpath(
            '//*[starts-with(@class, "field field-name-field-products-services")]//li/text()').extract()
        loader.add_value('products', products)

        channels = response.xpath(
            '//*[starts-with(@class, "field field-name-field-sales-methods")]//li/text()').extract()
        loader.add_value('channels', channels)

        acres = response.xpath('(//*[starts-with(@class, "field field-name-field-acres")]//text())[2]').extract_first()
        loader.add_value('acres', acres)

        crops_license = response.xpath('//*[text()="Crops"]/../../..//text()').extract() or ''
        loader.add_value('crops_license', crops_license)

        handling_license = response.xpath('//*[text()="Handling"]/../../..//text()').extract() or ''
        loader.add_value('handling_license', handling_license)

        USDA_NOP_license = response.xpath('//*[text()="USDA NOP"]/../../..//text()').extract() or ''
        loader.add_value('USDA_NOP_license', USDA_NOP_license)

        email = response.xpath(
            '(//*[starts-with(@class, "field field-name-field-member-contact-email")]//text())[2]').extract_first()
        loader.add_value('email', email)

        thoroughfare = response.xpath('//*[@class="thoroughfare"]/text()').extract_first()
        locality = response.xpath('//*[@class="locality"]/text()').extract_first()
        state = response.xpath('//*[@class="state"]/text()').extract_first()
        postal_code = response.xpath('//*[@class="postal-code"]/text()').extract_first()
        address = thoroughfare + '\n' + locality + ', ' + state + ' ' + postal_code
        loader.add_value('address', address)

        website = response.xpath(
            '(//*[starts-with(@class, "field field-name-field-web-site")]//text())[2]').extract_first()
        loader.add_value('website', website)

        phone = response.xpath(
            '(//*[starts-with(@class, "field field-name-field-phone-no")]//text())[2]').extract_first()
        loader.add_value('phone', phone)

        facebook = response.xpath(
            '//*[starts-with(@class, "field field-name-field-facebook")]//a/@href').extract_first()
        loader.add_value('facebook', facebook)

        yield loader.load_item()


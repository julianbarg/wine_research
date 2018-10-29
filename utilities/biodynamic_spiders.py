from time import sleep
import csv
import os
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from scrapy.selector import Selector
from scrapy import Spider
from scrapy.crawler import CrawlerProcess


class VineyardSpider:

    def __init__(self, driver: webdriver, destination: str, log=True):
        """Start an instance of the VineyardSpider, which can then be used
        to download data from http://www.biodynamicfood.org/"""
        self.driver = driver
        self.destination = destination
        self.log = log
        self._create_csv()
        self.time = None
        self.process = None

    def _create_csv(self):
        if not os.path.isfile(self.destination):
            with open(self.destination, 'w') as output:
                writer = csv.writer(output)
                writer.writerow(['Name',
                                 'Date',
                                 'Category',
                                 'Address',
                                 'Phone',
                                 'Email',
                                 'Website',
                                 'Short description',
                                 'Description',
                                 'Crops',
                                 'Processed products',
                                 'Cropped_acreage',
                                 'Total_acreage'
                                 ])
        else:
            pass

    def load_vineyards(self, link: str, time: date):
        self.time = time

        self.driver.get(link)

        # Select category 'Crops'
        product_selector = self.driver.find_element_by_id('filter_3_primary')
        product_selector.click()
        product_selector.send_keys(Keys.ARROW_DOWN)
        product_selector.send_keys(Keys.ENTER)
        sleep(0.3)
        if self.log:
            print('Loading category "Crops" successful.')

        # Select subcategory 'Fruit
        crop_selector = self.driver.find_element_by_id('filter_3_secondary')
        crop_selector.click()
        crop_selector.send_keys(Keys.ARROW_DOWN)
        crop_selector.send_keys(Keys.ARROW_DOWN)
        crop_selector.send_keys(Keys.ENTER)
        sleep(0.3)
        if self.log:
            print('Loading subcategory "Fruit" successful.')

        # Select 'Grapes For Wine'
        fruit_selector = self.driver.find_element_by_id('filter_3_tertiary')
        fruit_selector.click()
        for i in range(19):
            sleep(0.1)
            fruit_selector.send_keys(Keys.ARROW_DOWN)
        fruit_selector.send_keys(Keys.ENTER)
        if self.log:
            print('Loading "Grapes For Wine" successful.')

        # Load all producers
        load_button = self.driver.find_element_by_id('scrollDown')
        n_elements = len(self.driver.find_elements_by_class_name('results_list_item'))
        while True:
            if self.log:
                print('Loading more vineyards.')
            for i in range(20):
                load_button.click()
                sleep(0.1)
            n_elements_new = len(self.driver.find_elements_by_class_name('results_list_item'))
            if n_elements < n_elements_new:
                n_elements = n_elements_new
            else:
                if self.log:
                    print('Loaded all vineyards.')
                break

    def get_vineyard_links(self):
        selector = Selector(text=self.driver.page_source)
        links = ['http://www.biodynamicfood.org' + link
                 for link in selector.xpath('//*[@class="results_list_item"]//a/@href').extract()]
        return links

    def prepare_vineyard_parsing(self, links):
        destination = self.destination
        time = self.time

        class GenericSpider(Spider):
            name = 'vineyards'
            allowed_domains = []
            start_urls = links

            def parse(self, response):
                sel = Selector(response)
                name = sel.xpath('//h1/text()').extract_first()
                category = sel.xpath('//h2[@class="business-type"]/text()').extract_first()

                address_field_1 = sel.xpath('//div[@class="member-address"]/p/text()[1]').extract_first().strip()
                address_field_2 = sel.xpath('//div[@class="member-address"]/p/text()[2]').extract_first().strip()
                address = address_field_1 + '\n' + address_field_2

                contact_info = sel.xpath('//div[@class="member-address"]/p/text()').extract()
                contact_info = [line.strip() for line in contact_info]
                phone = [line for line in contact_info if line.startswith('Phone: ')][0]
                phone = phone.replace('Phone: ', '')
                email = sel.xpath('//div[@class="member-address"]//a[1]/text()').extract_first()
                website = sel.xpath('//div[@class="member-address"]//a[2]/text()').extract_first()
                short_description = sel.xpath('//p[@class="quote"]/text()').extract_first()

                profile = sel.xpath('//div[@class="member-profile"]/div/p/text()').extract()
                profile = [element.strip() for element in profile]
                len_description = max([len(element) for element in profile])
                description = [element for element in profile if len(element) == len_description][0]
                crops = sel.xpath('//div[p/*/text()="Crops"]//li//text()').extract()
                crops = ', '.join(crops)
                processed_products = sel.xpath('//div[p/*/text()="Processed Product"]//li//text()').extract()
                processed_products = ', '.join(processed_products)

                all_text = sel.xpath('//p/text()').extract()
                all_text = [text.strip() for text in all_text]
                acreage = [text for text in all_text if 'Acres' in text]
                try:
                    cropped_acreage = acreage[0]
                    total_acreage = acreage[1]

                except IndexError:
                    print('Acreage not specified for one organization.')
                    cropped_acreage = ''
                    total_acreage = ''

                with open(destination, 'a', newline='') as output:
                    writer = csv.writer(output)
                    writer.writerow([name,
                                     time,
                                     category,
                                     address,
                                     phone,
                                     email,
                                     website,
                                     short_description,
                                     description,
                                     crops,
                                     processed_products,
                                     cropped_acreage,
                                     total_acreage])

        # Run spider
        self.process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        self.process.crawl(GenericSpider)

    def parse_organizations(self):
        self.process.start()

    def close_parser(self):
        self.process.stop()

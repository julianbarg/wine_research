from time import sleep
import csv
from selenium import webdriver
from datetime import date
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector

from scrapy import Spider
from scrapy.crawler import CrawlerProcess

def get_vineyards(link: str, driver: webdriver, destination: str, date: date):
    driver.get(link)

    # Select category 'Crops'
    product_selector = driver.find_element_by_id('filter_3_primary')
    product_selector.click()
    product_selector.send_keys(Keys.ARROW_DOWN)
    product_selector.send_keys(Keys.ENTER)
    sleep(0.3)
    print('Loading category "Crops" successful.')

    # Select subcategory 'Fruit
    crop_selector = driver.find_element_by_id('filter_3_secondary')
    crop_selector.click()
    crop_selector.send_keys(Keys.ARROW_DOWN)
    crop_selector.send_keys(Keys.ARROW_DOWN)
    crop_selector.send_keys(Keys.ENTER)
    sleep(0.3)
    print('Loading subcategory "Fruit" successful.')

    # Select 'Grapes For Wine'
    fruit_selector = driver.find_element_by_id('filter_3_tertiary')
    fruit_selector.click()
    for i in range(19):
        sleep(0.1)
        fruit_selector.send_keys(Keys.ARROW_DOWN)
    fruit_selector.send_keys(Keys.ENTER)
    print('Loading "Grapes For Wine" successful.')

    # Load all producers
    load_button = driver.find_element_by_id('scrollDown')
    n_elements = len(driver.find_elements_by_class_name('results_list_item'))
    while True:
        print('Loading more vineyards.')
        for i in range(20):
            load_button.click()
            sleep(0.1)
        n_elements_new = len(driver.find_elements_by_class_name('results_list_item'))
        if n_elements < n_elements_new:
            n_elements = n_elements_new
        else:
            print('Loaded all vineyards.')
            break

    # Create .csv
    with open(destination, 'w') as output:
        writer = csv.writer(output)
        writer.writerow(['Name',
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

    # Prepare spider
    selector = Selector(text=driver.page_source)
    links = ['http://www.biodynamicfood.org' + link
             for link in selector.xpath('//*[@class="results_list_item"]//a/@href').extract()]
    class MySpider(Spider):
        name='biodynamic'
        allowed_domains = ['http://www.biodynamicfood.org/']
        start_urls = links

        def parse(self, response):
            sel = Selector(response)
            Name = sel.xpath('//h1/text()').extract_first()
            Category = sel.xpath('//h2[@class="business-type"]/text()').extract_first()

            address_field_1 = sel.xpath('//div[@class="member-address"]/p/text()[1]').extract_first().strip()
            address_field_2 = sel.xpath('//div[@class="member-address"]/p/text()[2]').extract_first().strip()
            Address = address_field_1 + '\n' + address_field_2

            contact_info = sel.xpath('//div[@class="member-address"]/p/text()').extract()
            contact_info = [line.strip() for line in contact_info]
            Phone = [line for line in contact_info if line.startswith('Phone: ')][0]
            Phone = Phone.replace('Phone: ', '')
            Email = sel.xpath('//div[@class="member-address"]//a[1]/text()').extract_first()
            Website = sel.xpath('//div[@class="member-address"]//a[2]/text()').extract_first()
            Short_description = sel.xpath('//p[@class="quote"]/text()').extract_first()

            profile = sel.xpath('//div[@class="member-profile"]/div/p/text()').extract()
            profile = [element.strip() for element in profile]
            len_Description = max([len(element) for element in profile])
            Description = [element for element in profile if len(element) == len_Description][0]
            Crops = sel.xpath('//div[p/*/text()="Crops"]//li//text()').extract()
            Crops = ', '.join(Crops)
            Processed_products = sel.xpath('//div[p/*/text()="Processed Product"]//li//text()').extract()
            Processed_products = ', '.join(Processed_products)

            all_text = sel.xpath('//p/text()').extract()
            all_text = [text.strip() for text in all_text]
            Acreage = [text for text in all_text if 'Acres' in text]
            try:
                Cropped_acreage = Acreage[0]
                Total_acreage = Acreage[1]

            except IndexError:
                print('Acreage not specified for one organization.')
                Cropped_acreage = ''
                Total_acreage = ''

            with open(destination, 'a', newline='') as output:
                writer = csv.writer(output)
                writer.writerow([Name,
                                 Category,
                                 Address,
                                 Phone,
                                 Email,
                                 Website,
                                 Short_description,
                                 Description,
                                 Crops,
                                 Processed_products,
                                 Cropped_acreage,
                                 Total_acreage])

    # Run spider
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(MySpider)
    process.start()
    process.stop()
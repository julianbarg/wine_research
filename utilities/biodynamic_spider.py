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
                         'Features',
                         'Sales channels',
                         'Acerage'
                         ])

    # Prepare spider
    selector = Selector(text=driver.page_source)
    links = ['http://www.biodynamicfood.org' + link
             for link in selector.xpath('//*[@class="results_list_item"]//a/@href').extract()]
    from scrapy.crawler import CrawlerProcess
    class MySpider(Spider):
        name='biodynamic'
        allowed_domains = ['http://www.biodynamicfood.org/']
        start_urls = links

        def parse(self, response):
            Name = ''
            Category = ''
            Address = ''
            Phone = ''
            Email = ''
            Website = ''
            Short_description = ''
            Description = ''
            Crops = ''
            Processed_products = ''
            Features = ''
            Sales_channels = ''
            Acerag = ''

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
                                 Features,
                                 Sales_channels,
                                 Acerag])

    # Run spider
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(MySpider)
    process.start()

# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.loader import ItemLoader
from scrapy.http import Request
from datetime import datetime

from wine_research.items import LODIItem


class LodiSpider(Spider):
    name = 'LODISpider'
    allowed_domains = ['archive.org', 'lodigrowers.com']
    start_urls = ['https://web.archive.org/web/20131127132141/http://www.lodigrowers.com:80/lodi-rules/growers/',
                  'https://web.archive.org/web/20160926101912/http://www.lodigrowers.com/lodirules/growers/',
                  'https://www.lodigrowers.com/growers/'
                  ]

    def parse(self, response):
        # Handle archived version of website.
        if 'archive.org' in response.url:
            organizations = response.xpath('//*[@class="entry"]//td')
        # Handle live website.
        else:
            organizations = response.xpath('//*[@class="v65-col3 col3-certvineyard"]')

        for organization in organizations:
            info = organization.xpath('.//text()').extract()
            info = list(map(str.strip, info))
            # info = [line.replace('\n', '') for line in info]
            # Check first address format.
            if len(info) > 2 and any(term in info[2] for term in ('CA', 'California')):
                loader = ItemLoader(item=LODIItem(), selector=organization)

                name = info[0]
                loader.add_value('name', name)

                date = datetime.strptime(response.url[28:36], '%Y%m%d').strftime('%Y-%m-%d')
                loader.add_value('date', date)

                address = '\n'.join(info[1:3])
                loader.add_value('address', address)

                if len(info) > 3:
                    phone = info[3]
                    loader.add_value('phone', phone)

                if len(info) > 4:
                    contact = info[4]
                    loader.add_value('contact', contact)

                yield loader.load_item()

            # Check second address format.
            elif len(info) > 1 and any(term in info[1] for term in ('CA', 'California')):
                loader = ItemLoader(item=LODIItem(), selector=organization)

                name = info[0]
                loader.add_value('name', name)

                date = datetime.strptime(response.url[28:36], '%Y%m%d').strftime('%Y-%m-%d')
                loader.add_value('date', date)

                address = info[1]
                loader.add_value('address', address)

                if len(info) > 2:
                    phone = info[2]
                    loader.add_value('phone', phone)

                    contact = info[3]
                    loader.add_value('contact', contact)

                yield loader.load_item()

        next_page = response.xpath('//*[@class="f"]/a/@href').extract_first()
        if next_page:
            yield Request(next_page, callback=self.parse)

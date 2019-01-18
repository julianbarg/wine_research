# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from datetime import datetime
import re


class BiodynamicHistoryPipeline(object):
    def process_item(self, item, spider):

        for field in item.fields:
            item.setdefault(field, '')

        if item['date']:
            item['date'] = datetime.strptime(item['date'][0], '%Y%m%d').date()

        if item['address']:
            item['address'] = [element.strip() for element in item['address']]
            item['address'] = '\n'.join(item['address'][:2])
            state_pattern = '\n\w+, (\w{2})\s'
            item['state'] = re.findall(item['address'], state_pattern)

        if item['phone']:
            item['phone'] = item['phone'][0]
            item['phone'] = item['phone'].replace('Phone: ', '')

        if item['acreage']:
            item['acreage'] = item['acreage'][0]
            item['acreage'] = item['acreage'].replace('Total Acreage: ', '')

        if item['profile']:
            item['profile'] = '\n'.join(item['profile'])

        if item['crops']:
            item['crops'] = ','.join(item['crops'])

        if item['processed_products']:
            item['processed_products'] = ','.join(item['processed_products'])

        if 'wine' in item['crops'].lower():
            item['vineyard'] = True

        if 'wine' in item['processed_products'].lower():
            item['winery'] = True

        if ('wine' in item['profile']).lower() and (len(item['crops']) > len(item['processed_products'])):
            item['vineyard'] = True

        if ('wine' in item['profile']).lower() and (len(item['crops']) < len(item['processed_products'])):
            item['winery'] = True

        if ('vineyard' in item['name'].lower()) or ('vineyard' in item['business'].lower()):
            item['vineyard'] = True

        if 'vineyard' in item['profile'].lower():
            item['vineyard'] = True

        if ('winery' in item['name'].lower()) or ('winery' in item['business'].lower()):
            item['winery'] = True

        if 'winery' in item['profile'].lower():
            item['winery'] = True

        return item

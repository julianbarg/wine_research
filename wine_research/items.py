# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BiodynamicHistoryItem(Item):
    # define the fields for your item here like:
    date = Field()
    name = Field()
    link = Field()
    category = Field()
    address = Field()
    state = Field()
    phone = Field()
    email = Field()
    website = Field()
    acreage = Field()
    profile = Field()
    crops = Field()
    processed_products = Field()

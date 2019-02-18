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
    address = Field()
    state = Field()
    phone = Field()
    email = Field()
    website = Field()
    acreage = Field()
    profile = Field()
    crops = Field()
    processed_products = Field()
    business = Field()
    vineyard = Field()
    winery = Field()


class CCOFItem(Item):
    chapters = Field()
    description = Field()
    products = Field()
    channels = Field()
    acres = Field()
    crops_license = Field()
    crops_license_status = Field()
    crops_license_date = Field()
    handling_license = Field()
    handling_license_status = Field()
    handling_license_date = Field()
    USDA_NOP_license = Field()
    USDA_NOP_license_status = Field()
    USDA_NOP_license_date = Field()
    vineyard = Field()
    winery = Field()
    organic_grape_wine = Field()
    email = Field()
    address = Field()
    website = Field()
    phone = Field()
    facebook = Field()

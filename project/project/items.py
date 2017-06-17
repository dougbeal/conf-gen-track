# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import re

import scrapy
import scrapy.loader.processors as processors

from slugify import slugify




    
class EmulatorItem(scrapy.Item):
    tabs = scrapy.Field(
        input_processor=processors.Identity())
    name = scrapy.Field(
        input_processor=processors.TakeFirst(),
        output_processor=processors.TakeFirst()
    )
    
class TabItem(scrapy.Item):
    tab_index = scrapy.Field()
    resolution = scrapy.Field(
        input_processor=processors.TakeFirst(),
        output_processor=processors.TakeFirst())
    scripts = scrapy.Field(
        input_processor=processors.Identity())
    
class ScriptItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    resolution = scrapy.Field(
        input_processor=processors.TakeFirst(),
        output_processor=processors.TakeFirst()
    )
    emulator_name = scrapy.Field(
        output_processor=processors.TakeFirst())
    name = scrapy.Field(
        input_processor = processors.Compose(u' '.join, unicode.strip),
        output_processor=processors.TakeFirst()
    )
    refill = scrapy.Field(
        input_processor = processors.Compose(u' '.join, unicode.strip),
        output_processor=processors.TakeFirst()
    )
    duration = scrapy.Field(
        input_processor = processors.Compose(u' '.join, unicode.strip),
        output_processor=processors.TakeFirst()
    )
    setting_note = scrapy.Field(
        input_processor = processors.Compose(u' '.join, unicode.strip),
        output_processor=processors.TakeFirst()
    )
    setting_image_url = scrapy.Field()
    pastebin_url = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()
    
    file_urls = scrapy.Field()
    files = scrapy.Field()




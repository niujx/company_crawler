# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader.processors import Compose, MapCompose, Join


def parse_field(text):
    return str(text).strip()


class LagouItem(scrapy.Item):
    company_name = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    product_name = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    trade = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    location = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    stage = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    management_team = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    introduction = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    company_url = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    ext_info = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    crawler_url = scrapy.Field(
        input_processor=MapCompose(parse_field),
        output_processor=Join(),
    )
    crawler_spider = scrapy.Field()

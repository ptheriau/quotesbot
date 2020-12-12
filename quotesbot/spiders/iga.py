# -*- coding: utf-8 -*-
import scrapy

class IGA_Spider(scrapy.Spider):
    name = "IGA-spider"
    start_urls = [
        'https://www.whatsmybrowser.org/',
    ]
        
    def parse(self, response):
        for row in response.css("div.row"):
            yield {
                'name': row.css("div.name::text").extract_first(),
                'value': row.css("div.value::text").extract_first(),
            }

        yield {
                'useragent': response.css("div.user-agent::text").extract_first(),
                }

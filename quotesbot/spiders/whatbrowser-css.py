# -*- coding: utf-8 -*-
import scrapy

class ToScrapeCSSSpider(scrapy.Spider):
    name = "whatbrowser-css"
    start_urls = [
        'https://www.whatsmybrowser.org/',
    ]
        
    def parse(self, response):
        for row in response.css("div.row"):
            yield {
                'name': row.css("div.name::text").extract_first(),
                'value': row.css("div.value::text").extract_first(),
            }

            
    def parse(self, response):
        yield {
                'useragent': response.css("div.user-agent::text").extract_first(),
                }

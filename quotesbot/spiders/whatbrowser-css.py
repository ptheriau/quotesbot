# -*- coding: utf-8 -*-
import scrapy

class ToScrapeCSSSpider(scrapy.Spider):
    name = "whatbrowser-css"
    start_urls = [
        'https://www.whatsmybrowser.org/',
    ]

    def parse(self, response):
        yield {
                'useragent': response.css("div.user-agent::text").extract_first(),
                }

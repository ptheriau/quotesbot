# -*- coding: utf-8 -*-
import scrapy

class ToScrapeCSSSpider(scrapy.Spider):
    name = "whatbrowser-css"
    start_urls = [
        'https://www.whatsmybrowser.org/',
    ]

    def parse(self, response):
        response.css("div.user-agent")
        yield {
                'useragent': quote.css("span.text::text").extract_first(),
                }

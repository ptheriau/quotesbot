# -*- coding: utf-8 -*-
import scrapy

class IGA_Spider(scrapy.Spider):
    name = "IGA-spider"
    allowed_domains = ["iga.net"]
    start_urls = [
        'https://www.iga.net/fr/epicerie_en_ligne/sushis',
    ]
        
    def parse(self, response):
        for product in response.css("div.item-product__content"):
            yield {
                'brand': product.css("a.item-product__brand::text").extract_first(),
                'name': product.css("a.js-ga-productname::text").extract_first(),
                'link': product.css("a.js-ga-productname::href").extract_first(),
            }

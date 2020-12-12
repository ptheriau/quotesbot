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
                'brand': product.css("div.item-product__brand::text").extract_first().strip(),
                'name': product.css("a.js-ga-productname::text").extract_first().strip(),
                'link': product.css("a.js-ga-productname::attr(href)").extract_first(),
                'size': product.css("div.item-product__info::text").extract_first().strip(),
                'price': product.css("span.price::text").extract_first().strip(),
            }

# -*- coding: utf-8 -*-
import scrapy


class GrocerySpider(scrapy.Spider):
    name = "iga"
    allowed_domains = ["iga.net"]
    start_urls = [
        'https://www.iga.net/fr/epicerie_en_ligne/sushis',
    ]

    def parse_grocery_page(self, response):
        item = {}
        product = response.css("div.item-product")
        item["name"] = product.css("a.js-ga-productname::text").extract_first()
        item['brand'] = product.css("a.item-product__brand push--top::text").extract_first()
        item['size'] = product.css("div.item-product__info::text").extract_first()
        item['price'] = product.css('div.item-product__price push--bottom::text').extract_first()
        yield item

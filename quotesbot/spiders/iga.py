# -*- coding: utf-8 -*-
import scrapy
from random import randint
from time import sleep


class IGA_Spider(scrapy.Spider):
    name = "IGA-spider"
    allowed_domains = ["iga.net"]
    start_urls = [
        #'https://www.iga.net/fr/epicerie_en_ligne/sushis',
        #'https://www.iga.net/fr/epicerie_en_ligne/boulangerie_industrielle',
        'https://www.iga.net/fr/epicerie_en_ligne/parcourir',
    ]
        
    def parse(self, response):
        #2020-12-12 Must go up the chain to grap promotions
        #for product in response.css("div.item-product__content"):
        #2020-12-13 item-product used twice, must go up again
        #for product in response.css("div.item-product"):
        for product in response.css("div.js-ga"):
            
            priceselector=product.css("span.price::text")
            regpriceselector=product.css("span.price-amount::text")
            if regpriceselector:
                tempregprice=regpriceselector.extract_first().strip()
                tempsaleprice=priceselector.extract_first().strip()
            else:
                tempregprice=priceselector.extract_first().strip()
                tempsaleprice=""
                
            promotionselector=product.css("span.js-ga-promotion::text")
            if promotionselector:
                temppromotion=promotionselector.extract_first().strip()
            else:
                temppromotion=""
                
            brand=""
            brandselector=product.css("div.item-product__brand::text")
            if brandselector:
                brand=brandselector.extract_first().strip()
            
            yield {
                'brand': brand,
                'name': product.css("a.js-ga-productname::text").extract_first().strip(),
                'link': product.css("a.js-ga-productname::attr(href)").extract_first(),
                'size': product.css("div.item-product__info::text").extract_first().strip(),
                #'price': product.css("span.price::text").extract_first().strip(),
                'regprice': tempregprice,
                'saleprice': tempsaleprice,
                'promotion': temppromotion,
            }
            nextpagelinkselector=response.css(".icon--arrow-skinny-right::attr(href)")
            if nextpagelinkselector:
                nextpagelink=nextpagelinkselector[0].extract()
                sleep(randint(2,7))
                yield scrapy.Request(url=response.urljoin(nextpagelink))

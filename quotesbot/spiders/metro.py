# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.http import FormRequest
import re
import logging

class Metro_Spider(scrapy.Spider):
    name = "Metro-spider"
    allowed_domains = ["metro.ca"]
    start_urls = [
        'https://www.metro.ca/trouver-une-epicerie',
    ]
    
    def parse(self, response):
        yield scrapy.FormRequest(url="https://www.metro.ca/stores/setmystore/64", method="POST", formdata={'userConfirmation':'false','lang':'fr'}, callback=self.store_set)
        
    def store_set(self, response):
        logging.info(response)
        yield scrapy.Request(url="https://www.metro.ca/epicerie-en-ligne/recherche", callback=self.start_scraping)
        
    def start_scraping(self, response):
        logging.info(response)
        for product in response.css("div.products-tile-list__tile"):
                               
            regpriceperlb=""
            salepriceperlb=""
            secondarypriceselector=product.css("div.pi-secondary-price")
            if secondarypriceselector:
                previous=""
                for temp in product.css("div.pi-secondary-price *::text").extract():
                    if temp=="lb":
                        previous=previous.replace(',', '.')
                        regpriceperlb=re.sub('[^\d\.]', '', previous)
                    previous=temp
            regularpriceselector=product.css("div.pi-regular-price")
            if regularpriceselector:
                salepriceperlb=regpriceperlb
                regpriceperlb=""
                tempstring=""
                previous=""
                for temp in product.css("div.pi-regular-price *::text").extract():
                    tempstring+=str(temp)
                    if "kg" in tempstring:
                        tempstring=tempstring.replace(',', '.')
                        tempstring=re.sub('[^\d\.]', '', tempstring)
                        regpriceperlb=str(round(float(tempstring)/2.2046, 2))
                        
            salepriceunit=''
            regpriceunit=''
            if regpriceperlb=="" and salepriceperlb=="":
                specialselector=product.css("div.pi-sale-price .price-promo")
                if specialselector:
                    salepriceunit=product.css("div.pi-sale-price .price-promo::text").extract_first().strip()
                    regpriceunit=product.css("div.pi-regular-price .pi-price::text").extract_first().strip()
                else:
                    #regpriceunit=product.css("div.pi-sale-price .pi-price::text").extract_first().strip()
                    regpriceunit=product.css("div.pi--main-price@data-main-price").extract_first().strip()
            
            brandselector=product.css("span.pt-brand::text")
            if brandselector:
                tempbrand=brandselector.extract_first().strip()
            else:
                tempbrand=""
                
            sizeselector=product.css("span.pt-weight::text")
            if sizeselector:
                tempsize=sizeselector.extract_first().strip(),
            else:
                tempsize="none"
            
            estimatedweight=""
            estimatedweightselector=product.css("span.unit-update::text")
            if estimatedweightselector:
                #estimatedweightselector=estimatedweightselector.extract.strip()
                #for temp in estimatedweightselector
                for temp in product.css("span.unit-update *::text").extract():
                    estimatedweight+=str(temp)
            
            yield {
                'brand': tempbrand,
                'name': product.css("div.pt-title::text").extract_first().strip(),
                'link': product.css("a.product-details-link::attr(href)").extract_first(),
                'size': tempsize,
                'regpriceunit': regpriceunit,
                'salepriceunit': salepriceunit,
                'regpriceperlb': regpriceperlb,
                'salepriceperlb': salepriceperlb,
                'estimatedweight': estimatedweight,
            }
            #nextpagelinkselector=response.css(".icon--arrow-skinny-right::attr(href)")
            #if nextpagelinkselector:
            #    nextpagelink=nextpagelinkselector[0].extract()
            #    yield scrapy.Request(url=response.urljoin(nextpagelink))

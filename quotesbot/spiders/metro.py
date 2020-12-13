# -*- coding: utf-8 -*-
import scrapy

class IGA_Spider(scrapy.Spider):
    name = "Metro-spider"
    allowed_domains = ["metro.ca"]
    start_urls = [
        'https://www.metro.ca/en/online-grocery/search',
    ]
        
    def parse(self, response):
        for product in response.css("div.products-tile-list__tile"):
            
            promoselector=product.css("div.pi-price-promo::text")
            if promoselector:
                tempsaleprice=product.css("div.pi-sale-price .pi-price::text").extract_first().strip()
                tempregprice=product.css("div.pi-regular-price .pi-price::text").extract_first().strip()
            else:
                tempsaleprice=""
                tempregprice=product.css("span.pi-price::text").extract_first().strip()
            
            brandselector=product.css("span.pt-brand::text")
            if brandselector:
                tempbrand=brandselector.extract_first().strip()
            else:
                tempbrand=""
                
            sizeselector=product.css("span.pt-weight::text")
            if sizeselector:
                tempsize=sizeselector.extract_first().strip(),
            else:
                tempsize=""                    
            
            yield {
                'brand': tempbrand,
                'name': product.css("div.pt-title::text").extract_first().strip(),
                'link': product.css("a.product-details-link::attr(href)").extract_first(),
                'size': tempsize;
                'regprice': tempregprice,
                'saleprice': tempsaleprice,
            }
            #nextpagelinkselector=response.css(".icon--arrow-skinny-right::attr(href)")
            #if nextpagelinkselector:
            #    nextpagelink=nextpagelinkselector[0].extract()
            #    yield scrapy.Request(url=response.urljoin(nextpagelink))
# -*- coding: utf-8 -*-
import scrapy

class Metro_Spider(scrapy.Spider):
    name = "Metro-spider"
    allowed_domains = ["metro.ca"]
    start_urls = [
        'https://www.metro.ca/epicerie-en-ligne/recherche',
    ]
        
    def parse(self, response):
        for product in response.css("div.products-tile-list__tile"):
            
            regpriceunit=""
            salepriceunit=""
            promoselector=product.css("div.pi-price-promo")
            if promoselector:
                salepriceunit=product.css("div.pi-sale-price .pi-price::text").extract().strip()
                regpriceunit=product.css("div.pi-regular-price .pi-price::text").extract_first().strip()
            else:
                for temp in product.css("span.pi-price *::text").extract():
                    regpriceunit+=str(temp).strip()
                    
            regpriceperlb=""
            salepriceperlb=""
            secondarypriceselector=product.css("div.pi-secondary-price")
            if secondarypriceselector
                regpriceperlb=secondarypriceselector.extract_first().strip()
            
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

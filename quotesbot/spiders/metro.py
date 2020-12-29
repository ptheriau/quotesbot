# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.http import FormRequest
import re
import logging

class Metro_Spider(scrapy.Spider):
    name = "Metro-spider"
    allowed_domains = ["metro.ca"]
    login_page = 'https://www.metro.ca/trouver-une-epicerie'
    start_urls = [
        'https://www.metro.ca/trouver-une-epicerie',
    ]
    
    def parse(self, response):
        #frmdata = {"userConfirmation":"false","lang":'fr'}
        #url = "https://www.metro.ca/stores/setmystore/64"
        #yield FormRequest(url, callback=self.after_select_store, formdata=frmdata)
        
        #yield FormRequest(url="https://www.metro.ca/stores/setmystore/64", method="POST", formdata={'userConfirmation':'false','lang':'fr'})
        #scrapy.Request(url="https://www.metro.ca/epicerie-en-ligne/recherche", callback=self.start_scraping)
        logging.DEBUG('testing')
        pass
    
    def init_request(self):
        logging.DEBUG('init_request')
        return Request(url=self.login_page, callback=self.login)
        
    def login(self, response):
        logging.DEBUG('logging in...')
        logging.DEBUG(response)
        return scrapy.FormRequest.form_response(
                                         response,
                                         formdata={'userConfirmation':'false','lang':'fr'},
                                         callback=self.check_login_response
                                        )

    def check_login_response(self, response):
        logging.DEBUG('check_login_response')
        if "<li class=\"logout\">" in response.body:
            logging.DEBUG('signed in correctly')
            self.initialized()
        else:
            logging.DEBUG('still not signed in...')

    def parse_item(self, response):
      console.log('parse_item')
      i['url'] = response.url
      logging.DEBUG('response.url:' + response.url)
      return i
    
    
    
    
    
    def after_select_store(self, response):
        #if "Error while logging in" in response.body:
        #    self.logger.error("Login failed!")
        #else:
        #    self.logger.error("Login succeeded!")
        #    item = SampleItem()
        #    item["quote"] = response.css(".text").extract()
        #    item["author"] = response.css(".author").extract()
        #    return item
        scrapy.Request(url="https://www.metro.ca/epicerie-en-ligne/recherche", callback=self.start_scraping)
        
        
    def start_scraping(self, response):
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
                        #regpriceperlb=str(round(float(tempstring)/2.2046, 2))
                        regpriceperlb=tempstring
                        
            regpriceunit=""
            salepriceunit=""
            if regpriceperlb=="" and salepriceperlb=="":
                promoselector=product.css("div.pi-price-promo")
                if promoselector:
                    salepriceunit=product.css("div.pi-sale-price .pi-price::text").extract().strip()
                    regpriceunit=product.css("div.pi-regular-price .pi-price::text").extract_first().strip()
                else:
                    for temp in product.css("span.pi-price *::text").extract():
                        regpriceunit+=str(temp).strip()
            
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

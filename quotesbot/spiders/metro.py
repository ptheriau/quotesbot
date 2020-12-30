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
            tempmultiprice='false'
                               
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
                currentprice=product.css("div.pi--main-price::attr(data-main-price)").extract_first().strip()
                regpriceselector=product.css("div.pi-regular-price")
                multiprice=''
                for temp in product.css("div.pi-secondary-price .pi-price *::text").extract_first():
                    multiprice+=str(temp)
                if regpriceselector or 'ou' in multiprice:
                    #en special
                    salepriceunit=currentprice
                    if 'ou' in multiprice:
                        regpriceunit=multiprice
                        tempmultiprice='true'
                    else:
                        for temp in product.css("div.pi-regular-price *::text").extract():
                            regpriceunit+=str(temp)

                    #20201230 Remove everything but numbers, dot (replace , prior) and / so no need to drop prix régulier, must remove 'ch.' because of dot.
                    regpriceunit=regpriceunit.replace('ch.', '')
                    #regpriceunit=regpriceunit.replace('Prix régulier', '')
                    regpriceunit=regpriceunit.replace(',', '.')
                    regpriceunit=re.sub('[^\d\.\/]', '', regpriceunit)
                    #20201230 Convert 2/5.00 prices
                    if '/' in regpriceunit:
                        temp=regpriceunit.split('/')
                        #regpriceunit=str(round(float(temp[1])/float(temp[0]), 2))
                        regpriceunit=float(temp[1])/int(temp[0])
                        regpriceunit='%.2f' % regpriceunit
                else:
                    #prixreg
                    regpriceunit=currentprice
                    salepriceunit=''
            
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
                for temp in product.css("span.unit-update *::text").extract():
                    estimatedweight+=str(temp)
            
            templegalnotes=""
            templegalnotesselector=product.css("div.tile-product__bottom-section__pricing__legal-notes::text")
            if templegalnotesselector:
                for temp in product.css("div.tile-product__bottom-section__pricing__legal-notes *::text").extract():
                    templegalnotes+=str(temp)
                    
            # ' '.join(templegalnotes.split()) espaces, tab, newline et replace par un espace singulier entre les mots.
            #source: https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string
            yield {
                'brand': tempbrand,
                'name': product.css("div.pt-title::text").extract_first().strip(),
                'link': product.css("a.product-details-link::attr(href)").extract_first(),
                'size': tempsize,
                'regpriceunit': ' '.join(regpriceunit.split()),
                'salepriceunit': salepriceunit,
                'multiprice': tempmultiprice,
                'regpriceperlb': regpriceperlb,
                'salepriceperlb': salepriceperlb,
                'estimatedweight': estimatedweight,
                'legalnotes': ' '.join(templegalnotes.split()),
            }
            #nextpagelinkselector=response.css(".icon--arrow-skinny-right::attr(href)")
            #nextpagelinkselector=response.find_elements_by_css_selector("a[aria-label='Suivant']")
            nextpagelinkselector=response.css('a[aria-label=Suivant]::attr(href)')
            if nextpagelinkselector:
                nextpagelink=nextpagelinkselector[0].extract()
                yield scrapy.Request(url=response.urljoin(nextpagelink), callback=self.start_scraping)

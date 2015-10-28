import urllib2,requests, pprint
from lxml import html
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
import urlparse, re, csv

def snapdeal(self,response):
		sel = Selector(response)
		# item = response.meta['item']
		name = response.url
		if sel.xpath("//div[@class='notifyMe-popup-divtwo']").extract():
			stock = "Out Of Stock"
			sp = mrp = ''
		else:      
			mrp = response.xpath("//span[@id='original-price-id']/text()").extract()
			if mrp:
				sp = response.xpath("//span[@id='selling-price-id']/text()").extract()[0]
				mrp = response.xpath("//span[@id='original-price-id']/text()").extract()[0]
			else:
				mrp = response.xpath("//span[@id='selling-price-id']/text()").extract()[0]				
				product_name = response.xpath("//h1[@itemprop='name']/text()").extract()[0].replace(",","")
      
		stock = response.xpath("//div[@class='notifyMe-soldout']").extract()
		discntnd = response.xpath("//div[@class='noLongerProduct']").extract()
		if stock or discntnd:
			stock = "Out Of Stock"
		else:
			stock = "In Stock"
		
		snapdeal_row = [product_name,mrp,sp,stock,url]
		print snapdeal_row
		return snapdeal_row
		
  # def amazonin(self,response):
    # sel = Selector(response)
    # item = response.meta['item']
    # if sel.xpath('//div[@id="outOfStock"]').extract():
       # item ["AmazonStock"] = "Out Of Stock"
    # else:
      # item ["AmazonURL"] = response.url
      # item ["AmazonProductName"] = response.xpath("//h1/span[@id='productTitle']/text()").extract()[0].replace(",","")
      # mrp = response.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()").extract()
      # saleprice = response.xpath("//span[@id='priceblock_saleprice']/text()").extract()
      # ourprice = response.xpath("//span[@id='priceblock_ourprice']").extract()
      # item ["AmazonMRP"] = ""
      # saleshipping = response.xpath("//span[@class='a-size-base a-color-secondary']/text()").extract()
      # url1 = response.xpath("//span[@class='a-size-medium a-color-success']//a/@href").extract()
      # if mrp and saleprice:
        # item ["AmazonSP"] = response.xpath("//span[@id='priceblock_saleprice']/text()").extract()[0].replace(",","")
        # item ["AmazonMRP"] = response.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()").extract()[0].replace(",","")

      # elif mrp and ourprice:
        # item ["AmazonSP"] = response.xpath("//span[@id='priceblock_ourprice']/text()").extract()[0].replace(",","")
        # item ["AmazonMRP"] = response.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()").extract()[0].replace(",","")

      # elif saleshipping and mrp:
        # item ["AmazonSP"] = response.xpath("//span[@class='a-size-base a-color-secondary']/text()").extract()[0].replace(",","")
        # item ["AmazonMRP"] = response.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()").extract()[0].replace(",","")

      # elif saleprice:
        # item ["AmazonSP"] = response.xpath("//span[@id='priceblock_saleprice']/text()").extract()[0].replace(",","")

      # elif ourprice:
        # item ["AmazonSP"] = response.xpath("//span[@id='priceblock_ourprice']/text()").extract()[0].replace(",","").replace(" ","")

      # elif url1:#Fetching from MarketPlace Listings
        # url = response.xpath("//span[@class='a-size-medium a-color-success']/a/@href").extract()[0]
        # request = Request("http://www.amazon.in/"+url,callback=self.amazonmarketplace)
        # request.meta["item"] = item
        # return request


    # try:#Calling Flipkart
      # self.driver.get('https://www.google.co.in')
      # searchbox = self.driver.find_element_by_xpath("//input[@title='Search']")
      # searchbox.send_keys("site:flipkart.com "+item ["LYSProduct_Name"])
      # searchbox.submit();
      # element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h3[@class='r']/a")))
      # url =  element.get_attribute("href")
      # request=Request(url,self.flipkart)
      # request.meta["item"] = item
      # return request
    # except:
      # self.to_csv(item)
      # return item


  # def amazonmarketplace(self,response):
    # print "AmazonMarketplace"
    # sel = Selector(response)
    # item = response.meta['item']
    # sp = response.xpath("//span[@style='text-decoration: inherit; white-space: nowrap;']/text()").extract()[0].replace(",","")
    # shippingcost = response.xpath("//span[@class='olpShippingPrice']/span/text()").extract()
    # if shippingcost:
      # item ["AmazonSP"] = str(float(sp) + float(response.xpath("//span[@class='olpShippingPrice']/span/text()").extract()[0].replace(",","")))
    # else:
      # item ["AmazonSP"] = sp
    # try:#CallingFlipkart
      # self.driver.get('https://www.google.co.in')
      # searchbox = self.driver.find_element_by_xpath("//input[@title='Search']")
      # searchbox.send_keys("site:flipkart.com "+item ["LYSProduct_Name"])
      # searchbox.submit();
      # element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h3[@class='r']/a")))
      # url =  element.get_attribute("href")
      # request=Request(url,self.flipkart)
      # request.meta["item"] = item
      # return request
    # except:
      # self.to_csv(item)
      # return item


  # def flipkart(self,response):
    # print "Flipkart"
    # sel = Selector(response)
    # item = response.meta['item']
    # if response.xpath("//h1[@class='title']/text()").extract():
      # item["FlipkartProductName"] = response.xpath("//h1[@class='title']/text()").extract()[0].replace(",","")
      # item["FlipkartURL"] = response.url
      # mrp = response.xpath("//span[@class='price']/text()").extract()
      # if mrp:
        # item["FlipkartMRP"] = response.xpath("//span[@class='price']/text()").extract()[0].replace(",","").replace("Rs.","")
      # sp = response.xpath("//span[@class='selling-price omniture-field']/text()").extract()
      # if sp:
        # item["FlipkartSP"] = response.xpath("//span[@class='selling-price omniture-field']/text()").extract()[0].replace(",","").replace("Rs.","")
      # stock = response.xpath("//div[@class='out-of-stock-status']").extract()
      # if stock:
        # item["FlipkartStock"] = "Out of Stock"

    # self.to_csv(item)
    # return item

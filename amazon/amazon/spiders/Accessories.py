from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request, HtmlResponse, Response
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
import BeautifulSoup
import urlparse,re,json,unicodecsv
import demjson
import pprint
import requests

from ..helpers import mycsv, scripts, converter

initialize_csv = True

class Spider(CrawlSpider):
		name = 'amazon_accessories'
		# allowed_domains = ['amazon.com']
		start_urls = [
        # 'http://www.amazon.com/ASICS-Gel-Kayano-Running-Lightning-Yellow/dp/B00IEVUIJU/ref=lp_679286011_1_1?s=apparel&ie=UTF8&qid=1442306231&sr=1-1&nodeID=679286011'		
        # 'http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=cycling+accessories',
        # 'http://www.amazon.com/s/ref=sr_pg_1?rh=i%3Aaps%2Ck%3Afitness+accessories&keywords=fitness+accessories&ie=UTF8&qid=1442815455&spIA=B00OBXGPAG,B00UNW6RAC,B00OBXGQQE,B00XV3JQ8A,B00OBXGO2A,B00PNHAFBY',
        # 'http://www.amazon.com/b/ref=amb_link_84594631_10?ie=UTF8&node=698866011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-leftnav&pf_rd_r=17R4JQS6SZ0RKSX30DQV&pf_rd_t=101&pf_rd_p=2189403462&pf_rd_i=3407731',
        # 'http://www.amazon.com/s/ref=sr_nr_n_1?fst=as%3Aoff&rh=n%3A672097011%2Ck%3Afitness+accessories&keywords=fitness+accessories&ie=UTF8&qid=1442815293&rnid=2941120011',
        # 'http://www.amazon.com/s/ref=lp_11051400011_nr_n_0?fst=as%3Aoff&rh=n%3A3375251%2Cn%3A%213375301%2Cn%3A706814011%2Cn%3A11051400011%2Cn%3A10184604011&bbn=11051400011&ie=UTF8&qid=1442815566&rnid=11051400011',
        # 'http://www.amazon.com/b/ref=s9_acss_bw_en_WT_d_1_3?_encoding=UTF8&node=10048714011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-top-3&pf_rd_r=1DHSDEXSMYGY1S86YWTF&pf_rd_t=101&pf_rd_p=2169498882&pf_rd_i=10048700011',        
        # 'http://www.amazon.com/b/ref=s9_acss_bw_en_WT_d_1_4?_encoding=UTF8&node=10048708011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-top-3&pf_rd_r=1DHSDEXSMYGY1S86YWTF&pf_rd_t=101&pf_rd_p=2169498882&pf_rd_i=10048700011',
        # 'http://www.amazon.com/b/ref=s9_acss_bw_en_WT_d_1_8?_encoding=UTF8&node=9959132011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-top-3&pf_rd_r=1DHSDEXSMYGY1S86YWTF&pf_rd_t=101&pf_rd_p=2169498882&pf_rd_i=10048700011',
        # 'http://www.amazon.com/b/ref=s9_acss_bw_en_WT_d_1_10?_encoding=UTF8&node=10824740011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-top-3&pf_rd_r=1DHSDEXSMYGY1S86YWTF&pf_rd_t=101&pf_rd_p=2169498882&pf_rd_i=10048700011',
        # 'http://www.amazon.com/b/ref=s9_acss_bw_en_WT_d_1_2?_encoding=UTF8&node=8916179011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-top-3&pf_rd_r=1DHSDEXSMYGY1S86YWTF&pf_rd_t=101&pf_rd_p=2169498882&pf_rd_i=10048700011',
        # 'http://www.amazon.com/b/ref=s9_acss_bw_ct_refTest_ct8_a4?_encoding=UTF8&node=3395071&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-5&pf_rd_r=17R4JQS6SZ0RKSX30DQV&pf_rd_t=101&pf_rd_p=2172326642&pf_rd_i=3407731',
        # 'http://www.amazon.com/s/ref=amb_link_399000942_19?ie=UTF8&rh=i%3Asporting%2Cn%3A3411111&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-leftnav&pf_rd_r=13EN981WSE782CYVV2SF&pf_rd_t=101&pf_rd_p=1964816822&pf_rd_i=3410851',
        # 'http://www.amazon.com/b/ref=lp_3403201_cy_ln_4?node=3404731&ie=UTF8&qid=1442815563',
        # 'http://www.amazon.com/Garmin-Vivofit-Fitness-Band-Black/dp/B00HFPOXM4/ref=sr_1_3?s=hpc&ie=UTF8&qid=1445413344&sr=1-3&keywords=garmin+vivofit',
        'http://www.amazon.com/WOLFBIKE-POLARIZE-Cycling-Sunglasses-Interchangeable/dp/B00JBB374U',
        'http://www.amazon.com/dp/B004JU0E2G/ref=psdc_491337011_t1_B003Y5H17I'
        'http://www.amazon.com/ASICS-Kayano-Running-Lightning-Silver/dp/B00BMLV9D8/',
        'http://www.amazon.com/Garmin-Vivofit-Fitness-Band-Black/dp/B00HFPOXM4',
        'http://www.amazon.com/dp/B004JU0E2G/ref=psdc_491337011_t1_B003Y5H17I'        
       	]

		
		rules = (
				# Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//span[@class="pagnLink"]',)), follow= True),
				Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]',)), 
					callback="parse_category" , follow= True),)

		
		def parse(self, response):
		# def parse_category(self, response):
			# print response.text
			global initialize_csv
			if initialize_csv:
				global mywriter
				mywriter = mycsv.initialize_csv('Amazon_Sports_Accessories.csv')
				initialize_csv = False

			sel = Selector(response)
			product_name = sel.xpath("//span[@id='productTitle']/text()").extract()[0]						
			parent_asin = sel.xpath("//div[@id='tell-a-friend']/@data-dest").extract()[0].split('parentASIN=')[-1].split('&')[0]						
			try:
				price  = sel.xpath("//span[@id='priceblock_ourprice']/text()").extract()[0].replace('$','')	
				price = converter.cleanup_price(price)
			except:
				price = ''			
			try:
				brand = sel.xpath("//a[@id='brand']/text()").extract()[0]
			except:
				brand =  sel.xpath("//a[@id='brand']/@href").extract()[0].split("/")[-2]
			row = ['Product', parent_asin, brand, product_name,'',price]
			mywriter.writerow(row)

			size_script = sel.xpath("//script[@language='JavaScript'][contains(text(),'window.isTwisterAUI = 1')]").extract()[0]
			color_script = sel.xpath("//script[@type='text/javascript'][contains(text(),'customerImages')]").extract()[0]
					
			'''
			Initializing Dictionaries for Variants(Asin, Variant Values), Pricing(Asin, Price) and Images(Asin, Images)
			'''
			variant_dict, price_dict, image_dict = {}, {}, {}

			size_script = size_script.split('dimensionValuesDisplayData')[-1].split('"deviceType')[0]
			new_script = re.findall('"(.*?)]',size_script.split("hidePopover")[0])

			for i in new_script:
				asin = i.split('[')[0].replace(':{"','').replace('":','')				
				variants = i.split('["')[-1]
				variant_dict[asin] = variants		

			color_script = color_script.split('data["colorImages"] =')[-1].split('data["heroImage"] = {};')[0].rsplit(';',1)[0]		
			color_script = demjson.decode(color_script)

			for key,value in variant_dict.iteritems():
				try:
					color = value.split('"')[-2].split('"')[0]					
					image_dict[color] = []
					
					for images in color_script[color]:					
						image_dict[color].append(images['large'])	
				except:
					pass

			price_url = sel.xpath("//script[contains(text(),'immutableURL')]/text()").extract()[0].split('immutableURLPrefix":"')[-1].split('"')[0]
			price_url = 'http://www.amazon.com' + price_url + '&psc=1&isFlushing=2&dpEnvironment=softlines&mType=full'

			'''
			To check if Swatches exist
			'''			
			swatches  = response.xpath( "//div[@id='variation_style_name']//li[contains(@id,'style')]")
			if swatches:				
				for swatch in swatches:
					swatch_price = swatch.xpath(".//div[@class='twisterSlotDiv']//span[@class='a-size-mini']/text()").extract()					
					if swatch_price:
						swatch_price = swatch_price[0].replace('$','').strip()
						swatch_price = converter.cleanup_price(swatch_price)

					else:
						swatch_price = False
					swatch_asin = swatch.xpath("@data-dp-url").extract()[0].split('dp/')[-1].split('/')[0]					
					price_dict[swatch_asin] = swatch_price

			pprint.pprint(variant_dict)
			for asin, variants in variant_dict.iteritems():	
				row = []
				color =  variants.split('"')[-2]				
				size  = variants.split('"')[0]				
				row = ['SKU', asin, '', color, size, '','' , '', '']

				for image in image_dict[color]:
						row.append(image)
				'''
				If the swatch container exists of the product page, avoiding requests to Ajax scripts
				'''
				if swatches:
					if asin in price_dict:
						variant_price = price_dict[asin]					
						if variant_price == False:
							continue				
					else:
						variant_price = price					
					row[5] = variant_price
					mywriter.writerow(row)

				else:					
					url = price_url + '&asinList=%s&id=%s' %(asin,asin)
					__price_request = Request(url, callback = self.parse_price)
					__price_request.meta['row'] = row				
					yield __price_request

		
		def parse_price(self, response):
			row = response.meta['row']
			if 'a-size-medium a-color-price\\">' in response.body:
				price = response.body.split('a-size-medium a-color-price\\">')[-1].split('<\/')[0].replace('$','')
				if float(price):
					row[5] = converter.cleanup_price(price)
					mywriter.writerow(row)
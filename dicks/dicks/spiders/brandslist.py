# import re,json,csv
# from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
# from scrapy.selector import Selector
# from dicks.items import DicksItem
# output = open("Brandslist.csv","wb")
# mywriter = csv.writer(output)

# f = open("pagination1.csv")
# csv_file = csv.reader(f)
# urllist =[]

# for row in csv_file:
    # urllist.append(row[0])
    
# class MySpider(CrawlSpider):
    # name = "brands"
    # allowed_domains = ["dicksportinggoods.com"]
    # start_urls = [url.strip() for url in urllist]

    # def parse(self,response):
        # sel = Selector(response)
        # item = DicksItem()
        # brandnames = sel.xpath("//div[@id='module_Brand']//div/a/text()").extract()
        
        # for i in range(len(brandnames)):
            # row = (brandnames[i],"")
            # mywriter.writerow(row)

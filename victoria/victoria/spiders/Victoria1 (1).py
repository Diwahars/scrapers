from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from victoria.items import CraigslistSampleItem
from scrapy.selector import Selector


class MySpider(CrawlSpider):
    name = "mojo"
    allowed_domains = ["victoriasportsco.com"]
    start_urls = ["http://www.victoriasportsco.com/snooker_biliard_table.php#vs20",
                  "http://www.victoriasportsco.com/pool_table.php",
                  "http://www.victoriasportsco.com/billiard_accessories.php",
                  "http://www.victoriasportsco.com/air_hockey_table.php",
                  "http://www.victoriasportsco.com/soccer_table.php",
                  "http://www.victoriasportsco.com/table_tennis_table.php",
                  "http://www.victoriasportsco.com/billiard_cloth_slate.php"]
    

    def parse(self, response):
        item = CraigslistSampleItem()
        sel = Selector(response)
        names = sel.xpath('//td[@class="product_name"]/strong/text()')

        products = sel.xpath('//tr[td/@class="product_text"]')[:-1]
        imageurls = products.xpath('.//img/@src')
        descriptions = products.xpath('.//td/ul')

        for name, url, description in zip(names, imageurls, descriptions):
            item["productname"] = name.extract()
            item["imgurl"] = url.extract()

            # Join individual list items into a string delimited by a new line
            # character
            item["description"] = '\n'.join(description.xpath('.//li/text()')
                                            .extract())
            yield item

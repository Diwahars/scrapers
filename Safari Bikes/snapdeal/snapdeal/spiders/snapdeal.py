import csv


from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import Selector

from ..items import SnapItem

from ..helpers import helper
from ..helpers import mycsv


# Globals
output = open("file.csv", "wb")
items_in_category = []  # Global list to help get sort-order

# Write base row to CSV
writer = csv.writer(output)
writer.writerow(mycsv.HEADER)


class snapdeal(BaseSpider):
    name = "snapdeal"
    allowed_domains = ['snapdeal.com']
    start_urls = [
        'http://www.snapdeal.com/seller/safari-international/Sadf02',
        'http://www.snapdeal.com/json/sellerStoreFront/20/20?view=List&vc=Sadf02&categoryId=&lang=en'
    ]

    def parse(self, response):
        '''
        Decides if response has json or initial products. If products, 
        it creates a request for individual pages; else, gets json and creates dict
        '''

        sel = Selector(response)

        if response.url == self.start_urls[0]:
            # Snapdeal page
            urls = set(sel.xpath('//*[@v="p"]/@href').extract())
            urls = helper.get_scrape_urls(urls)
            for url in urls:
                request = Request(url, self.parse_item)
                yield request
        elif response.url == self.start_urls[1]:
            # JSON
            json = sel.xpath('//text()').extract()[0]
            json_d = helper.get_dict_from_json(json)

            urls = []

            for thing in json_d:
                urls.append(thing['pageUrl'])

            for url in urls:
                request = Request('http://www.snapdeal.com/' + url, self.parse_item)
                yield request


    def parse_item(self, response):
        '''
        Gets item data from an item's page
        '''

        item = SnapItem()
        sel = Selector(response)

        # Setting type
        item['type'] = 'Product'

        # Setting product_type
        item['id'] = ''

        # Setting name
        name = sel.xpath('//h1[@itemprop = "name"]/text()').extract()[0]
        item['name'] = helper.convert_to_string(name)

        # Setting brand
        # brand = sel.xpath('//*[@class="key-features"]/li[1]/text()').extract()[0]
        # brand = helper.cleanup_brand(brand)

        item['brand_name'] = 'Hi-Bird'

        # Setting price and MRP
        price = sel.xpath("//div[@class='row pdp-e-i-MRP  ']//span/text()").extract()[1]

        price = helper.convert_to_string(price)

        item['price'] = price
        item['MRP'] = price

        # Setting SP
        sp = sel.xpath("//div[@class='col-xs-8 pdp-e-i-PAY-r']//span/text()").extract()[1]
        sp = helper.convert_to_string(sp)

        item['SP'] = sp

        # Setting desc
        # desc = 
        # desc = helper.convert_to_string(desc)

        item['desc'] = sel.xpath("//div[@class='spec-section expanded']").extract()

        # Setting sku
        
        item['sku'] = sel.xpath("//script[contains(text(),'var primaryEMIDTOs')]").extract()[0].split('vendorSKU":')[-1].split('"')[1].strip() + 'SAFARIBIKES'

        # Setting bin picking num
        item['bin_picking_num'] = 'SAFARIBIKES'

        # Setting category
        cat_list = sel.xpath('//*[@id="breadCrumbWrapper"]//span[@itemprop="title"]/text()').extract()

        category = helper.generate_category(cat_list, name)
        item['category'] = category

        # Setting option set
        item['option_set'] = name

        # Setting Availability
        item['availability'] = 'Y'

        # Setting Stock level
        item['stock_level'] = 100

        # Setting free shipping
        # free = sel.xpath('//*[@id="Ship_charges"]/text()').extract()[0]

        # if helper.is_free_shipping(free):
            # item['free_shipping'] = 'Y'
        
        item['free_shipping'] = 'N'

        # Setting sort_order
        item['sort_order'] = ''

        # Setting title
        item['page_title'] = ('Buy the %s Online in India at LiveYourSport.com '
                        '| Free Shipping and Massive Discounts') % name

        # Settings meta desc
        item['meta_desc'] = ('Get your hands on the %s. Buy it Online in'
                            ' India at LiveYourSport.com | Free Shipping '
                            'and Massive Discounts') % name

        # Settings img_desc_1
        item['img_desc_1'] = ('Buy %s Online in India at LiveYourSport.com'
                             ' | Free Shipping and Massive Discounts') % name

        # Setting is_thumbnail
        item['is_thumbnail'] = 'Y'

        # Setting track inventory
        item['track_inventory'] = 'By Product'

        # Setting images
        imgs = sel.xpath('//*[@id="product-thumbs"]/li/img/@src').extract()

        imgs = helper.cleanup_img_urls(imgs)
        item['product_image_files'] = []
        item['product_image_files'] = imgs

        row = [
            item['type'],
            item['id'],
            item['name'],
            item['brand_name'],
            item['price'],
            item['MRP'],
            item['SP'],
            item['desc'],
            item['sku'],
            item['bin_picking_num'],
            item['category'],
            item['option_set'],
            item['availability'],
            item['stock_level'],
            item['free_shipping'],
            item['sort_order'],
            item['meta_desc'],
            item['page_title'],
            item['img_desc_1'],
            item['is_thumbnail'],
            item['track_inventory'],
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',    
        ]

        for img in item['product_image_files']:
            row.append(img)

        writer.writerow(row)         

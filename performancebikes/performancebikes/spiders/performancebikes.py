import csv


from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector

from ..items import PBItem

from ..helpers import helper
from ..helpers import mycsv


# Globals
output = open("file.csv", "wb")
items_in_category = []  # Global list to help get sort-order
brands = []  # Global list of all brands


# Write base row to CSV
writer = csv.writer(output)
writer.writerow(mycsv.HEADER)

restrict_1 = ('(//*[@id="snVerticalMenu"]/li)[position() > 1 '
             'and not(position() = last())]//h3/a')


class Spider(CrawlSpider):
    name = 'performancebikes'
    allowed_domains = ['performancebike.com']
    start_urls = [
        'http://www.performancebike.com/bikes/CategoryDisplay?storeId=10052&catalogId=10551&langId=-1&orderBy=&searchTerm=&beginIndex=1&pageSize=251&parent_category_rn=400002&top_category=400002&categoryId=400038&metaData=%22',
        'http://www.performancebike.com/webapp/wcs/stores/servlet/AllBrandsView?catalogId=10551&langId=-1&categoryId=400345&storeId=10052'
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=(),
                               restrict_xpaths=(restrict_1,)),
                               callback='parse_category_initial',
                               follow=True),
    )

    def parse_category_initial(self, response):
        '''
        Used to scrape initial category page to get max-items and
        request the page with all items in the category

        BUT

        if url == brand-url, get brands
        '''
        sel = Selector(response)

        if response.url == ('http://www.performancebike.com/webapp/wcs/stores/servlet/AllBrandsView?catalogId=10551&langId=-1&categoryId=400345&storeId=10052'):
            # BRAND PAGE
            brand_list = sel.xpath('//a[contains(@id, "_Link_ForSubCat_")]/text()').extract()
            for brand in brand_list:
                brands.append(helper.convert_to_string(brand))
        else:
            max_items_raw = sel.xpath('//span[@class="item-numbers"]/text()').extract()[0]
            max_items = helper.get_max_items(max_items_raw)
            url = helper.get_full_category_url(response.url, max_items)

            request = Request(url, self.parse_category)
            yield request

    def parse_category(self, response):
        '''
        Used to scrape a category page loaded with all the items in the 
        category.
        '''
        print response.url
        sel = Selector(response)

        global items_in_category
        items_in_category = []  # Empty out list for each new category
        items_in_category = sel.xpath('//*[@class="product-info"]/h2/a/text()').extract()

        urls = sel.xpath('//*[@class="product-info"]/h2/a/@href').extract()
        for url in urls:
            request = Request('http://www.performancebike.com/bikes/' + url, self.parse_item)
            yield request

    def parse_item(self, response):
        '''
        Used to scrape content from the item page
        '''        
        sel = Selector(response)

        item = PBItem()

        # Setting id
        item['id'] = ''

        # Setting price and retail price
        prices = sel.xpath('//*[@class="sr_product_price"]/span/text()').extract()
        price = helper.cleanup_price(prices[0])

        item['price'] = price
        item['MRP'] = price

        # Setting sale price if it exists
        try:
            sp = helper.cleanup_price(prices[1])
            item['SP'] = sp
        except IndexError:
            item['SP'] = ''

        # Setting description
        desc = sel.xpath('//*[@id="overviewDiv"]/text()').extract()
        desc = helper.convert_to_string(''.join(desc)).strip()

        item['desc'] = desc

        # Setting bin_picking_num
        item['bin_picking_num'] = 'PERFORMANCEBIKEUSA'

        # Setting category
        breadcrumbs = sel.xpath('//*[@class="pb-breadcrumb"]'
                                '/li[position() > 1]/a/text()').extract()
        active_crumb = sel.xpath('//*[@class="active-page"]/text()').extract()

        item['category'] = helper.generate_category(breadcrumbs, active_crumb)

        # Settings option-set
        set = sel.xpath('//*[@class="product_title"]/text()').extract()[0]
        set = helper.convert_to_string(set)
        set = set.strip()
	print set

        item['option_set'] = set
		

        # Setting title
        item['page_title'] = ('Buy the %s Online in India at LiveYourSport.com '
                        '| Free Shipping and Massive Discounts') % set

        # Settings Meta desc
        item['meta_desc'] = ('Get your hands on the %s. Buy it Online in'
                            ' India at LiveYourSport.com | Free Shipping '
                            'and Massive Discounts') % set

        item['img_desc_1'] = ('Buy %s Online in India at LiveYourSport.com'
                             ' | Free Shipping and Massive Discounts') % set


        # Setting brand name
        # for brand in brands:
            # if brand in set:
                # item['brand_name'] = brand.strip()
                # break

        # # Setting sort order
        # sort_order = helper.get_sort_order(items_in_category, set)
        # item['sort_order'] = sort_order

        # # Getting productItems json
        # script = sel.xpath('//*[@class="media_addtocart_container"]//script').extract()[0]
        # variants = helper.get_variants_from_script(script)

        # # some comment, bruh
        # base_img_url = 'http://media.performancebike.com/images/performance/products/1500/'

        # # Getting image urls
        # item['product_image_file'] = []
        # for img in variants[0]['images']:
                # item['product_image_file'].append('%s%s' % (base_img_url, img["image"]))

        # if len(variants) == 1:
            # item['type'] = 'Product'
            # item['track_inventory'] = 'By Product'
            # item['name'] = set
            # item['sku'] = helper.get_clean_id(sel.xpath('//*[@class="product_number"]/text()').extract()[0])
            # if (variants[0]["inventoryNumber"] > 1):
                # item['stock_level'] = 100
            # else:
                # item['stock_level'] = 0

            # item['availability'] = 'Y'
            # item['free_shipping'] = 'N'
            # item['is_thumbnail'] = variants[0]["inVentoryMessage"]

            # row = [
                # item['type'],
                # item['id'],
                # item['name'],
                # item['brand_name'],
                # item['price'],
                # item['MRP'],
                # item['SP'],
                # item['desc'],
                # item['sku'],
                # item['bin_picking_num'],
                # item['category'],
                # item['option_set'],
                # item['availability'],
                # item['stock_level'],
                # item['free_shipping'],
                # item['sort_order'],
                # item['meta_desc'],
                # item['page_title'],
                # item['img_desc_1'],
                # item['is_thumbnail'],
                # item['track_inventory'],
                # '1',
                # '2',
                # '3',
                # '4',
                # '5',
                # '6',
                # '7',
                # '8',    
            # ]

            # for img in item['product_image_file']:
                # row.append(img)

            # writer.writerow(row)         

        # else:
            # item['track_inventory'] = 'By Option'
            # item['type'] = 'Product'
            # item['name'] = set
            # item['sku'] = helper.get_clean_id(sel.xpath('//*[@class="product_number"]/text()').extract()[0])
            # if (variants[0]["inventoryNumber"] > 1):
                # item['stock_level'] = 100
            # else:
                # item['stock_level'] = 0

            # item['availability'] = 'Y'
            # item['free_shipping'] = 'N'
            # item['is_thumbnail'] = variants[0]["inVentoryMessage"]

            # row = [
                # item['type'],
                # item['id'],
                # item['name'],
                # item['brand_name'],
                # item['price'],
                # item['MRP'],
                # item['SP'],
                # item['desc'],
                # item['sku'],
                # item['bin_picking_num'],
                # item['category'],
                # item['option_set'],
                # item['availability'],
                # item['stock_level'],
                # item['free_shipping'],
                # item['sort_order'],
                # item['meta_desc'],
                # item['page_title'],
                # item['img_desc_1'],
                # item['is_thumbnail'],
                # item['track_inventory'],
                # '1',
                # '2',
                # '3',
                # '4',
                # '5',
                # '6',
                # '7',
                # '8',    
            # ]

            # for img in item['product_image_file']:
                # row.append(img)         

            # writer.writerow(row)  

            # # ..

            # for variant in variants:
                # item = PBItem()
                # item['type'] = 'SKU'

                # if (variant['color'] != ""):
                    # color = variant['color']
                # else: 
                    # color = ''
                # if (len(variant['size']) > 0): 
                    # size = variant['size'][0]['longform']
                # else: 
                    # size = ''

                # if color == '':
                    # item['name'] = '[S]Size = %s' % (size)
                # elif size == '':
                    # item['name'] = '[C]Color = %s' % (color)
                # else:
                    # item['name'] = '[S]Size = %s, [C]Color = %s' % (size, color)    
                
                # item['sku'] = variant['itemId'] + 'PFRMCBKS'

                # if (variant["inventoryNumber"] > 1):
                    # item['stock_level'] = 100
                # else:
                    # item['stock_level'] = 0

                # item['bin_picking_num'] = 'PERFORMANCEBIKEUSA'

                # row = [
                    # item['type'],
                    # '',
                    # item['name'],
                    # '',
                    # '',
                    # '',
                    # '',
                    # '',
                    # item['sku'],
                    # item['bin_picking_num'],
                    # '',
                    # '',
                    # '',
                    # item['stock_level'],
                # ]

                # writer.writerow(row)

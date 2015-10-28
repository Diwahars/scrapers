import mycsv
import unicodecsv
from pprint import pprint
from itertools import product
output = open("Output.csv", "wb")
mywriter = unicodecsv.writer(output)
header = True

if header:
	header_row = ('Item Type','ASIN','Brand Name', 'Product Name', 'Size', 'Price', 'Description', 'Specification', 'Item Number', 'Category','Images')
	mywriter.writerow(header_row)
	header = False


def product_row(product_dict):

	product_row = [
		'Product',
		'',
		product_dict['Product Name'],		
		product_dict['Brand'],
		product_dict['Price'],
		product_dict['Price'],
		'',
		product_dict['Description'],
		product_dict['Product Code/SKU'],
		product_dict['Bin Picking Number'],
		product_dict['Category'],
		product_dict['Product Name'],
		product_dict['Product Availability'],
		100,
		'N',
		product_dict['Sort Order'],
		'Buy %s Online in India at LiveYourSport.com| Free Shipping and Massive Discounts' %(product_dict['Product Name']),
		'Buy %s Online in India at LiveYourSport.com| Free Shipping and Massive Discounts' %(product_dict['Product Name']),
		'Buy %s Online in India at LiveYourSport.com| Free Shipping and Massive Discounts' %(product_dict['Product Name']),
		'Y',
		product_dict['Track Inventory'],
		1,2,3,4,5,6,7,8,
		]

	for image in product_dict['Images']:
		product_row.append(image)
		print image

	mywriter.writerow(product_row)
	print 'Product'

def sku_row(variant_dict):
	
	sku_rows = [dict(zip(variant_dict, v)) for v in product(*variant_dict.values())]
	for row in sku_rows:
		for key, value in row.iteritems():
			name = '[S]%s = %s' %(key, value)

		mywriter.writerow(['SKU','',name,'','','','','',variant_dict[key][value]])

		



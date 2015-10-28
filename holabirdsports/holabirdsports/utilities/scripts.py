import re
import csv
import demjson
from pprint import pprint


def variants(color_script, size_script, mywriter):
		variant_dict, price_dict,image_dict = {}, {}, {}			

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


								
		for asin, variants in variant_dict.iteritems():

			price_request = Request()
			color =  variants.split('"')[-2]
			row = []
			size  = variants.split('"')[0]
			row = ['SKU', asin, '', color, size, '', '', '']

			for image in image_dict[color]:
				row.append(image)
			mywriter.writerow(row)

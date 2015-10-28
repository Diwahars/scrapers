import unicodecsv
import os

def initialize_csv(output_file):

	path = ('Outputs')
	if not os.path.exists(path):
		os.makedirs(path)

	output = open(os.path.join(path, output_file), 'wb')
	mywriter = unicodecsv.writer(output)
	header_row = ('Item Type','ASIN','Brand Name', 'Product Name', 'Size', 'Price', 'Description', 'Specification','Images')
	mywriter.writerow(header_row)
	return mywriter



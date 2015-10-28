import unicodecsv

def initialize_csv(output_file):
    output = open(output_file, "wb")
    mywriter = unicodecsv.writer(output)
    header_row = ('Item Type','ASIN','Brand Name', 'Product Name', 'Size', 'Price', 'Description', 'Specification','Images')
    mywriter.writerow(header_row)
    return mywriter



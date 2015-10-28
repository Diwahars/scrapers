import unicodecsv

def initialize(filename):
	filename = '%s.csv' %(filename)

	output = open(filename,"wb")
	mywriter = unicodecsv.writer(output)
	output.write('Item Type,Product ID,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Code/SKU,Bin Picking Number,Category,'
             'Current Stock Level,Option Set,Product Availability,Free Shipping,Sort Order,Meta Description,Page Title,Track Inventory,Product Description,'
             'Product Image Description - 1,Product Image Is Thumbnail - 1,'
             'Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7,\n')
	return mywriter

def pricing(mrp, sp, id1):
	sale_price = ''

	x = float(mrp.split('-')[-1])

	if float(mrp)<15:
		retail_price = str(float(mrp)*4*66)
		if sp:
			sale_price = str(float(sp[0].split("-")[-1].replace("$",""))*4*66)        
	
	elif id1 == 'Apparel':
		
		retail_price = str((x*65+600+x*30/100*65)*112.5/100 + x*65*29/100)
		if sp:
			y= float(sp[0].split("-")[-1].replace("$",""))
			sale_price = str((y*65+600+x*30/100*65)*112.5/100 + y*65*29/100)
	
	elif id1 == 'Accessories':
		retail_price = str((x*65 +x*30/100+550)*110.5/100 + x*65*29/100)
		if sp:
			y= float(sp[0].split("-")[-1].replace("$",""))
			sale_price = str((y*65 + y*30/100+550)*110.5/100 + y*65*29/100)
	
	elif id1 == 'Gear':
		retail_price = str((x*65 +x*30/100*50/100*65)*110.5/100 + x*65*35/100)
    	if sp:
    		y= float(sp[0].split("-")[-1].replace("$",""))
		sale_price = str((y*65 + y*30/100*53/100*65)*110.5/100 + y*65*35/100)
	elif id1 == 'Shoes':
		
		retail_price = str((x*65 +x*30/100*70/100*65)*115/100 + x*65*45/100)
		if sp:
			y= float(sp[0].split("-")[-1].replace("$",""))
			sale_price = str((y*65 + y*30/100*73/100*65)*114.5/100 + y*65*45/100)
	elif id1 == 'Electronics':
		
		retail_price = str((x*65 +x*30/100*65+1470)*115.5/100*129/100)
		if sp:
			y= float(sp[0].split("-")[-1].replace("$",""))
			sale_price = str((y*65 + y*30/100*65+1450)*115.5/100*129/100)

	return retail_price,sale_price

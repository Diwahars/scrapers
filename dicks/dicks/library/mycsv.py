import unicodecsv

def initialize_csv():
	header = ('Item Type','Product ID','Product Name','Brand Name','Price','Retail Price','Sale Price','Product Description','Product Code/SKU','Bin Picking Number','Category',
                 'Option Set','Product Availability','Current Stock Level','Free Shipping','Sort Order','Allow Purchases','Meta Description','Page Title',
             'Product Image Description - 1','Product Image Is Thumbnail - 1','Track Inventory','Product Image Sort - 1','Product Image Sort - 2','Product Image Sort - 3','Product Image Sort - 4','Product Image Sort-5','Product Image Sort-6','Product Image Sort-7','Product Image Sort-8',
             'Product Image File - 1','Product Image File - 2','Product Image File - 3','Product Image File - 4','Product Image File - 5 ',
    'Product Image File - 6','Product Image File - 7','Product Image File - 8')

	global output
	output  = open("DickSportingGoods1.csv","wb")
	global output2 
	output2 = open("DickSportingGoods2.csv","wb")
	global output3 
	output3 = open("DickSportingGoods3.csv","wb")
	global output4 
	output4 = open("DickSportingGoods4.csv","wb")
	global output5 
	output5 = open("DickSportingGoods5.csv","wb")
	mywriter = unicodecsv.writer(output)
	mywriter1 = unicodecsv.writer(output)
	mywriter2 = unicodecsv.writer(output2)
	mywriter3 = unicodecsv.writer(output3)
	mywriter4 = unicodecsv.writer(output4)
	mywriter5 = unicodecsv.writer(output5)	
	mywriter.writerow(header)
	mywriter2.writerow(header)
	mywriter3.writerow(header)
	mywriter4.writerow(header)
	mywriter5.writerow(header)
	
	# rulewriter = unicodecsv.writer(rulesfile)
	# rulewriter.writerow(mycsv.header)
	
def file_to_write(productcount):
		
		if productcount<2000:
			global output
			mywriter=unicodecsv.writer(output)
		elif productcount>=2000 and productcount<4000:
			global output2
			mywriter=unicodecsv.writer(output2)
		elif productcount>=4000 and productcount<6000:
			global output3
			mywriter=unicodecsv.writer(output3)
		elif productcount>=6000 and productcount<8000:
			global output4
			mywriter=unicodecsv.writer(output4)
		else:
			global output5
			mywriter=unicodecsv.writer(output5)
		
		# mywriter = ( 
		# 			unicodecsv.writer(output)*(productcount<2000)
		# 			or 
		# 			unicodecsv.writer(output1)*(2000<=productcount<4000)
		# 			or
		# 			unicodecsv.writer(output2)*(4000<=productcount<6000)
		# 			or
		# 			unicodecsv.writer(output3)*(6000<=productcount<8000)
		# 			or					
		# 			unicodecsv.writer(output4)*(8000<=productcount)
		# 			)
		# mywriter = ( 
		# 			(output)*(productcount<2000)
		# 			or 
		# 			(output1)*(2000<=productcount<4000)
		# 			or
		# 			(output2)*(4000<=productcount<6000)
		# 			or
		# 			(output3)*(6000<=productcount<8000)
		# 			or					
		# 			(output4)*(8000<=productcount)
		# 			)
					
		
					
		return mywriter
		
		

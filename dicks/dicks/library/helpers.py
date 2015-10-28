def brandname(pname,brandlist):
	for brand in brandlist:       
		if brand.lower() in pname.lower():
			brandname = brand
			break
		else:
			brandname = "NA"	
	return brandname
	
def meta_information(pname):
	image_description = "Buy "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
	meta_information = "Get your hands on the "+pname +". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
	title_tag = "Buy the "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"   
	
	return image_description,meta_information,title_tag

def sortorder_brand(brandname):
	if brandname in ("Under Armour"):
		sortorder = "-410"
	elif brandname in ("adidas","Adidas","Nike"):
		sortorder = "-400"
	else:
		sortorder = "-380"
	
	return float(sortorder)
	
	
def pricing_parent(mrp,sp,id):
	
	mrp =  float(mrp)
	sp = float(sp)
	curreny_rate = 67
	india_delivery = 200	
	customs = .70*.33
	shipito_cost = 800
	
	if float(mrp)<50:
		mrp+= 7
		sp+= 7			

	if id == '1': #Accessories
		usa_delivery = 0
		VAT = 110/100
		margin = 123/100
	
	elif id == '2': #Apparel
		usa_delivery = 300
		VAT = 110/100
		margin = 123/100
	
	elif id == '3': #Equipment
		usa_delivery = 1000
		VAT = 110/100
		margin = 135/100
     
	elif id == '4':  #Shoes
		usa_delivery = 2000
		VAT = 115/100
		margin = 133/100
	
	#Converting to Rupees	
	mrp *= curreny_rate
	sp *= curreny_rate
	
	#Delivery from USA
	mrp += usa_delivery
	sp += usa_delivery

	#shipito Delivery
	mrp += shipito_cost
	sp += shipito_cost

	#Customs
	mrp = mrp + mrp*customs 
	sp = sp + sp*customs	
	
	#Margin
	mrp *= margin
	sp *= margin

	#VAT in India
	mrp *= VAT
	sp *= VAT	
	
	#Delivery in India
	mrp += india_delivery
	sp += india_delivery
	
	mrp = round(mrp,2)
	sp = round(sp,2)
	
	mrp = str(mrp)
	sp = str(mrp)
	
	return mrp,sp
	
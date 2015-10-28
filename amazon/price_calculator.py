cost_price = float(raw_input("Enter Cost Price in Dollars: "))

#cost_price = cost_price * 68
#Cc_Avenue = 3/100 
#VAT = 14.5/100
#int_shipping  = 1500
#customs = (cost_price*30/100 + int_shipping)*30/100
#delivery = 300
#
#selling_price = 13705

cost_price = float(cost_price) * 68
CC_Avenue = 3/100
VAT = 5.5/100
international_shipping = 500
customs = (cost_price*30/100 + international_shipping)*30/100
delivery = 150

for selling_price in range(int(cost_price), 250000):     
    deductions =  (selling_price*VAT) + (selling_price*3/100)+ delivery + customs + international_shipping 
    net_profit = (selling_price - cost_price - deductions)/selling_price*100
    if net_profit>20:
        return selling_price
        break 

for selling_price in range(int(cost_price), 25000):	
	
	deductions =  (selling_price*VAT) + (selling_price*3/100)+ delivery + customs + int_shipping 

	net_profit = (selling_price - cost_price - deductions)/selling_price*100
	if net_profit>15:
		print deductions
		print net_profit
		print selling_price
		break





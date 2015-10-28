import csv
import re
import json


    
class vlookup(object):

    def __init__(self):        
        self.input_file = raw_input('Enter the name file name: ')
        self.binpicking_number = raw_input('Enter the Bin Picking Number: ')
        # self.input_file = 'DickSportingGoods1.csv'
        # self.binpicking_number = 'DICKSPORTINGGOODS'
              
        master_file = open('masterfile.csv', 'r')
        master_dict = csv.DictReader(master_file) 

        self.product_id_dict = {}
        '''Dictionary of all products from the masterfile 
        with SKU as the key and Product ID as values'''
        for row in master_dict:
            if row['Bin Picking Number'].lower().strip() == self.binpicking_number.lower().strip():
                self.product_id_dict[row['Product Code/SKU']+row['Item Type'].strip()] = row['Product ID']
            # print row['Product Code/SKU']+row['Item Type'].strip()
        
        self.header = True
        master_file.close()

        self.vlookup()
        

    def vlookup(self):
        csv_file = open(self.input_file, 'r')
        csv_dict = csv.DictReader(csv_file)

        output_file = open(self.input_file.replace(".csv","")+"_New.csv","wb")
        mywriter = csv.writer(output_file)
        
        for new_row in csv_dict:
            if (new_row['Product Code/SKU'] + new_row['Item Type'].strip()) in self.product_id_dict:                
                    new_row['Product ID'] = self.product_id_dict[new_row['Product Code/SKU']+new_row['Item Type'].strip()]
                    self.product_id_dict.pop(new_row['Product Code/SKU'], None)
                
            else:
                 new_row['Product ID'] = ''      
            self.csv_writer(new_row, mywriter)

        csv_file.close()   
        output_file.close()
        self.out_of_stock()

    
    def csv_writer(self, new_row, mywriter):            
        header_row, row = [], []
        for key,values in new_row.iteritems():
            if self.header == True:                
                header_row += [key]                               
            
            row += [values]
        if header_row:
                self.header = False 
                mywriter.writerow(header_row)

        mywriter.writerow(row)

    def out_of_stock(self):         
        output_file = open(self.input_file.replace(".csv","")+"_OutOfStock.csv","wb")
        mywriter = csv.writer(output_file)
        header = ('Product SKU','Current Stock Level')
        mywriter.writerow(header)
        
        for key,value in self.product_id_dict.iteritems():
            row = (key,0)            
            mywriter.writerow(row)

        output_file.close()

if __name__ == '__main__':
    
    a = vlookup()
    # a.product_match()





# oldsize = 0

# for row in mastersheet:
#     oldlist.append(row)
#     oldsku.append(row[4])
#     oldsize = oldsize+1
#     productidlist.append(row[1])
#     binpickinglist.append(row[5])

	
# newsize = 0
# for row in scrappedsheet:
	
#     newlist.append(row)
#     newsku.append(row[8])    
#     itemtypelist.append(row[0])    
#     newsize = newsize+1

# temp = 0
# for i in range(1,newsize):
#     productid = ''
#     for t in range(1,oldsize):
#         if binpickinglist[t] == binpickingnumber:
#             temp = 1
#             if newsku[i].strip() == oldsku[t].strip():
                
#                 productid = productidlist[t]            
#                 break       
#     if "SKU" in newlist[i] :
#         newlist[i] = [w.replace(";",",") for w in newlist[i]]        
#     newlist[i][1]=productid
#     mywriter.writerow(newlist[i])

# #FOR OUT OF STOCK PRODUCTS
# #Creating a new File for them with different csv headers
# outofstockheader = ('Item Type','Product ID','Product Name','Product Type','Product Code/SKU','Bin Picking Number','Brand Name',
#                     'Option Set','Option Set Align','Price','Cost Price','Retail Price','Sale Price','Free Shipping','Track Inventory',
#                     'Current Stock Level','Category','Product Image File - 1','Product Image File - 2','Product Image File - 3',
#                     'Sort Order')

# output1 = open(scrappedfile+"_OutOfStock.csv","wb")
# outofstockwriter = csv.writer(output1)
# outofstockwriter.writerow(outofstockheader)

# temp1 = 0
# for t in range(1,oldsize):
#     if binpickinglist[t] == binpickingnumber:
#         temp1 = 1
#         found =0
#         for i in range(1,newsize):
#             if oldsku[t] == newsku[i]:
#                 found = 1
#                 break
#         if found ==0:
#             oldlist[t][15] = "0"
#             oldlist[t][20:len(oldlist)] = []
#             oldlist[t].append("0")
#             outofstockwriter.writerow(oldlist[t])


# x.close()
# output1.close()
# output.close()
# f.close()

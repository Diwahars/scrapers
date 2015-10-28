import csv
import re

class input():
    def __init__(self):

        self.input_file = raw_input('Enter the name file name: ')
        self.binpicking_number = raw_input('Enter the Bin Picking Number: ')

        x = open("masterfile.csv")
        self.mastersheet = csv.reader(x)

class vlookup(input):

    def __init__(self):        
        output_file = open(scrappedfile.replace(".csv","")+"_New.csv","wb")
        mywriter = csv.writer(output_file)
        compare_sheet = csv.reader(f)

        header = (
                'Item Type','Product ID','Product Name','Brand Name','Price','Retail Price','Sale Price','Product Description','Product Code/SKU','Bin Picking Number','Category',
                     'Option Set','Product Availability','Current Stock Level','Free Shipping','Sort Order','Meta Description','Page Title',''
                 'Product Image Description - 1','Product Image Is Thumbnail - 1',''
                 'Track Inventory','Product Image Sort - 1','Product Image Sort - 2','Product Image Sort - 3','Product Image Sort - 4','Product Image Sort-5','Product Image Sort-6','Product Image Sort-7','Product Image Sort-8',
                 'Product Image File - 1','Product Image File - 2','Product Image File - 3','Product Image File - 4','Product Image File - 5 ',
                    'Product Image File - 6','Product Image File - 7','Product Image File - 8'
                    )
        mywriter.writerow(header)
        
        csv_file = open(self.input_file, 'r')
        self.csv_dict = csv.DictReader(csv_file)    

        master_file = open(self.mastersheet, 'r')
        self.master_dict = csv.DictReader(master_file) 

        product_id_dict = {}

        for row in self.master_dict:
            if row['Bin Picking Number'].lower().strip() == binpickingnumber.lower().strip():
                product_id_dict[row['Product_Code/SKU']] = row['Product ID']

        print self.product_id_dict

    # def product_match(self):


if __name__ == '__main__':
    a = vlookup()
    a.product_match()





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

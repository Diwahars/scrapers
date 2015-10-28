
import string
import urlparse
import re
import json
import csv

f = open("SwimOutlet.csv")
csv_file = csv.reader(f)
output1 = open("SwimOutlet1.csv","wb")
output2 = open("SwimOutlet2.csv","wb")
output3 = open("SwimOutlet3.csv","wb")
output4 = open("SwimOutlet4.csv","wb")
output5 = open("SwimOutlet5.csv","wb")
output6 = open("SwimOutlet6.csv","wb")
output7 = open("SwimOutlet7.csv","wb")

mywriter1 = csv.writer(output1)
mywriter2 = csv.writer(output2)
mywriter3 = csv.writer(output3)
mywriter4 = csv.writer(output4)
mywriter5 = csv.writer(output5)
mywriter6 = csv.writer(output6)
mywriter7 = csv.writer(output7)



output2.write('Item Type,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Code/SKU,Category,Bin Picking Number,Product Description,'
             'Current Stock Level,Option Set,Product Availability,Free Shipping,Sort Order,Meta Description,Page Title,'
             'Product Image Description - 1,Product Image Is Thumbnail - 1,'
             'Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,'
             'Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7,\n')
output3.write('Item Type,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Code/SKU,Category,Bin Picking Number,Product Description,'
             'Current Stock Level,Option Set,Product Availability,Free Shipping,Sort Order,Meta Description,Page Title,'
             'Product Image Description - 1,Product Image Is Thumbnail - 1,'
             'Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,'
             'Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7,\n')
output4.write('Item Type,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Code/SKU,Category,Bin Picking Number,Product Description,'
             'Current Stock Level,Option Set,Product Availability,Free Shipping,Sort Order,Meta Description,Page Title,'
             'Product Image Description - 1,Product Image Is Thumbnail - 1,'
             'Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,'
             'Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7,\n')
output5.write('Item Type,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Code/SKU,Category,Bin Picking Number,Product Description,'
             'Current Stock Level,Option Set,Product Availability,Free Shipping,Sort Order,Meta Description,Page Title,'
             'Product Image Description - 1,Product Image Is Thumbnail - 1,'
             'Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,'
             'Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7,\n')
output6.write('Item Type,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Code/SKU,Category,Bin Picking Number,Product Description,'
             'Current Stock Level,Option Set,Product Availability,Free Shipping,Sort Order,Meta Description,Page Title,'
             'Product Image Description - 1,Product Image Is Thumbnail - 1,'
             'Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,'
             'Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7,\n')
output7.write('Item Type,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Code/SKU,Category,Bin Picking Number,Product Description,'
             'Current Stock Level,Option Set,Product Availability,Free Shipping,Sort Order,Meta Description,Page Title,'
             'Product Image Description - 1,Product Image Is Thumbnail - 1,'
             'Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,'
             'Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7,\n')




count=0

for row in csv_file:
  
    
  if count>=1000 and count<2000:
    mywriter2.writerow(row)
  elif count>=2000 and count<3000:
    mywriter3.writerow(row)
  elif count>=3000 and count<4000:
    mywriter4.writerow(row)
  elif count>=4000 and count<5500:
    mywriter5.writerow(row)
  elif count>=5500 and count<7000:
    mywriter6.writerow(row)
  elif count>=7000 and count<9000:
    mywriter7.writerow(row)
  elif count<300:
    mywriter1.writerow(row)
  else:
    print count
    
  if row[0]=='Product':
    count= count + 1


print count

import unicodecsv
import json

def script_printing(script, mywriter, imageDict):

   script = script.split('skus')[1].split(';')[0].replace('\n','').strip().split("]")[0]
   script = script.replace("\'",'"').replace("[,{","[{")
   varscript = "["+script.split("[")[-1] + "]"
   variantDict = json.loads(varscript) #json containing all variant information
   

   enhanced = 0
   for variant in variantDict:
		counter = 0

		if variant['avail'] == 'IN_STOCK':

			for k in imageDict:
				if variant['colorId'] == k['id'] and 'enhancedImageURL' in k:           
					url = "http://www.dickssportinggoods.com" +k['enhancedImageURL']				
					# item['image_urls']= [url]
					# filename = item ["Product_Code"]+"_"+k['id']
					# # # item['title'] = [filename]
					enhanced = 1
					# # # url = 'http://liveyoursport.com/product_images/dicks/'+filename+'.jpg'
					# # # rulerow.append('http://liveyoursport.com/product_images/dicks/'+filename+'.jpg')
					# # # yield item
					break	
			
			if enhanced == 1:
				link = ':%s' %url
				skurow = ['SKU','','[S]Size= '+variant['size']+',[CS]Color= '+variant['color']+link,"","","","","",variant['sku_id']+'DSPRTG','DICKSPORTINGGOODS',
			  "","","","100","","",'',"","","","","","","","","","","","",""]

				rulerow = ['Rule','','[CS]Size= '+variant['size']+',[S]Color= '+variant['color'],"","","","","",variant['sku_id']+'DSPRTG','',
			  "","","","","","",'Y',"","","","","","","","","","","","",""]   
				rulerow.append(url)
				mywriter.writerow(skurow)
				mywriter.writerow(rulerow)
				# mywriter.writerow(rulerow)
			else:
				skurow = ['SKU','','[S]Size= '+variant['size']+',[S]Color= '+variant['color'],"","","","","",variant['sku_id']+'DSPRTG','DICKSPORTINGGOODS',
			  "","","","100","","",'',"","","","","","","","","","","","",""]			    
				mywriter.writerow(skurow)


	
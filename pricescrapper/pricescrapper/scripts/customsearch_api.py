import pprint
import urllib2,requests, pprint
from lxml import html
import urlparse, re, csv,unicodecsv
from googleapiclient.discovery import build
	
def amazon(query):
	try:
		service = build("customsearch", "v1",developerKey=" AIzaSyCMGfdDaSfjqv5zYoS0mTJnOT3e9MURWkU")	
		
		res = service.cse().list(q='site:amazon.in '+query,cx='003190724308582426242:oojgya2rem4',).execute()
				
		return res['items'][0]['link']
	except:
		return ''

	
def flipkart(query):
	try:
		service = build("customsearch", "v1",	
						developerKey=" AIzaSyCMGfdDaSfjqv5zYoS0mTJnOT3e9MURWkU")
	
		res = service.cse().list(q='site:flipkart.com '+query,cx='003190724308582426242:oojgya2rem4',).execute()
		return res['items'][0]['link']
	except:
		return ''
		
def snapdeal(query):
	try:
		service = build("customsearch", "v1",	
						developerKey=" AIzaSyCMGfdDaSfjqv5zYoS0mTJnOT3e9MURWkU")
	
		res = service.cse().list(q='site:snapdeal.com '+query,	cx='003190724308582426242:oojgya2rem4',).execute()
		return res['items'][0]['link']
	except:
		return ''

def paytm(query):
	try:
		service = build("customsearch", "v1",	
						developerKey=" AIzaSyCMGfdDaSfjqv5zYoS0mTJnOT3e9MURWkU")
	
		res = service.cse().list(q='site:paytm.com '+query,	cx='003190724308582426242:oojgya2rem4',).execute()
		return res['items'][0]['link']
	except:
		return ''
	
# if __name__ == '__main__':
	# snapdeal('Babolat Pro Hurricane Tennis String')
	

	
	
	
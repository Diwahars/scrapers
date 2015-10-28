import re
import demjson
import unicodedata


def get_text_from_html(string):
    '''
    Converts HTML to plain text with some regex magic.
    '''
    return re.sub(r'<(.*?)>', '', string)


def convert_to_string(uni):
    '''
    Converts unicode to plain text
    '''
    return unicodedata.normalize('NFKD', uni).encode('ascii', 'ignore')


def get_max_items(raw):
    '''
    Extracts the max items count from a messy unicode string.
    '''
    thing = convert_to_string(raw)
    thing = thing.strip()
    thing = thing.split('OF')
    return thing[1].strip()


def get_full_category_url(response_url, max):
    '''
    Generates a url to query ALL products in a category using a base url, 
    query string and max item count.
    '''
    base_url = 'http://www.performancebike.com/'
    query = '/CategoryDisplay?storeId=10052&catalogId=10551&langId=-1&orderBy=&searchTerm=&beginIndex=1&pageSize=%s&parent_category_rn=400002&top_category=400002&categoryId=400038&metaData="' % max
    url = response_url.split(base_url)
    url = url[1].split('/')
    return base_url + url[0] + query


def cleanup_price(uni_price):
    '''
    Takes price in unicode and returns price in text without '$'
    '''
    price = convert_to_string(uni_price)
    price = price.replace(',', '')
    price = float(price.strip('$'))
    return price


def generate_category(cat_breadcrumbs, cat_active):
    '''
    Takes breadcrumbs list and active product and generates a / separated category
    '''

    category = ''
    for item in cat_breadcrumbs:
        category += '%s/' % convert_to_string(item).strip()

    for item in cat_active:
        category += '%s' % convert_to_string(item).strip()

    return category


def get_sort_order(all_items, title):		
		for i, item in enumerate(all_items):
			print i
			if item == title:
				return i
			else:
				return -1
			
def get_variants_from_script(script):
    '''
    Takes script and extracts variants from it and
    sends back as variant dicts.
    '''
    script = convert_to_string(script)
    script = script.replace('<script>', '')
    script = script.replace('var productItems', '')
    script = script.replace('=', '')
    script = script.split('var')
    return demjson.decode(script[0])


def get_clean_id(id):
    id = convert_to_string(id)
    id = id.replace('#', '')
    id = id.replace('-','')
    return id


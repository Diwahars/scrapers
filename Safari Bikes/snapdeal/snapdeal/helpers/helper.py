import re
import demjson
import unicodedata


def get_text_from_html(string):
    '''
    Converts HTML to plain text with some regex magic.
    '''
    return (re.sub(r'<(.*?)>', '', string)).strip()


def convert_to_string(uni):
    '''
    Converts unicode to plain text
    '''
    return unicodedata.normalize('NFKD', uni).encode('ascii', 'ignore')


def get_scrape_urls(urls):
    '''
    Takes a list of urls and returns the hi-bird ones.
    '''
    u = []
    for item in urls:
        if 'hibird' in item.lower():
            u.append(item)

    return u 


def cleanup_price(uni_price):
    '''
    Takes price in unicode and returns price in text without '$'
    '''
    price = convert_to_string(uni_price)
    price = price.replace(',', '')
    price = float(price.strip('$'))
    return price


def generate_category(cat_list, product):
    '''
    Takes breadcrumbs list and product and generates a / separated category
    '''

    category = ''
    for item in cat_list:
        category += '%s/' % convert_to_string(item).strip()

    category += product
    return category


def get_sort_order(all_items, title):
    '''
    Takes a list of all items in a category and then looks for the 
    position of a particular item and returns sort order accordingly.
    '''
    for i, item in enumerate(all_items):
        if item == title:
            return i


def cleanup_brand(brand):
    '''
    Cleans up brand string and returns only the brand
    '''
    return convert_to_string(brand.split(':')[1])


def get_proper_sku(id):
    id = convert_to_string(id)
    return id + 'SNAPDEAL'


def is_free_shipping(string):
    '''
    Takes string and if it equals `Free Shipping`, returns true.
    '''

    if convert_to_string(string) == 'Free Delivery':
        return True


def cleanup_img_urls(urls):
    '''
    Takes a list of small img urls and returns back a list of larger images.
    '''
    u = []
    for url in urls:
        url = convert_to_string(url)
        url = url.replace('/small', '')
        u.append(url)

    return u


def get_dict_from_json(json):
    '''
    Converts json string to a dict object using demjson.
    '''
    return demjson.decode(convert_to_string(json))


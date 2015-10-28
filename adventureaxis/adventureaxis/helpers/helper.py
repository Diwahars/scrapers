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


def cleanup_price(uni_price):
    '''
    Takes price in unicode and returns price in text without '$'
    '''
    price = convert_to_string(uni_price)
    price = price.strip()
    price = price.replace(',', '')
    price = float(price.strip('Rs'))
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


def get_variants_from_script(script):
    '''
    Takes script and extracts variants from it and
    sends back as variant dicts.
    '''
    script = convert_to_string(script)
    script = get_text_from_html(script)
    script = script.replace('var spConfig = new Product.Config(', '')
    script = script.replace(');', '')
    script = script.strip()
    return demjson.decode(script)


def get_clean_id(id):
    id = convert_to_string(id)
    return id + 'ADVNTURAXIS'


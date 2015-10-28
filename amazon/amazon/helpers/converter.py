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


def cleanup_price(cost_price):
    '''
    Takes price in dollars and returns price with margins in rupees 
    '''
    if '-' in cost_price:
        cost_price = cost_price.split('-')[1] 

    cost_price = float(cost_price) * 68
    CC_Avenue = 3/100
    VAT = 14.5/100
    international_shipping  = 1500
    customs = (cost_price*30/100 + international_shipping)*30/100
    delivery = 300

    for selling_price in range(int(cost_price), 25000):     
        deductions =  (selling_price*VAT) + (selling_price*3/100)+ delivery + customs + international_shipping 
        net_profit = (selling_price - cost_price - deductions)/selling_price*100
        if net_profit>15:

            return selling_price
            break



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


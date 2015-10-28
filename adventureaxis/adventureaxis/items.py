from scrapy import Field, Item


class AXItem(Item):
    type = Field()
    id = Field()
    name = Field()
    brand_name = Field()
    price = Field()
    MRP = Field()
    SP = Field()
    desc = Field()
    sku = Field()  # ask
    bin_picking_num = Field()
    category = Field()
    option_set = Field()
    availability = Field()
    stock_level = Field()
    free_shipping = Field()
    sort_order = Field()
    meta_desc = Field()
    page_title = Field()
    img_desc_1 = Field()
    is_thumbnail = Field()  # do
    track_inventory = Field()
    product_image_sort = Field()
    product_image_file = Field()  

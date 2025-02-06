
amazon_order_id_pattern = r"\d{3}-\d{7}-\d{7}"




post_order_id_pattern = r'#\d{4,5}'
post_track_id_pattern = r"^E[LZ]\d{9}IN$"


shpy_prod_variant = r" - \d GM|ML - \d"

shpy_product_name_pattern = r""
post_product_line_pattern = fr"Ref:{post_order_id_pattern},\s?Item" 



# Ref: #20106, Item(s): Kudampuli Lehyam - 1000 GM - 2

gst_pattern = r""


# AMAZON PATTERNS
# LWA  credentials ie, client id and client secret have "amzn1." in the starting.
LWA_credentials_starting_pattern = r'^amzn1.'

amazon_order_id_pattern = r"\d{3}-\d{7}-\d{7}"

post_order_id_pattern = r'#\d{4,5}'

post_track_id_pattern = r"^E[LZ]\d{9}IN$"

gst_pattern = r""


# AMAZON PATTERNS
# LWA  credentials ie, client id and client secret have "amzn1." in the starting.
LWA_credentials_starting_pattern = r'^amzn1.'
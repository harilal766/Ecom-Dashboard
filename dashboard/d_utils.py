from helpers.messages import better_error_handling,color_text
from helpers.input_handling import menu_processor
from amazon.sp_api_models import *
from amazon.a_models import *

def postal_tracking():
    pass


def amazon_initiator():
    # activate amazon model classes
    order_inst = Orders(); rep_ins = Reports()


def report_generator():
    
    platform_menu = {
        1:("Amazon",),
        2: ("Shopify",0),
    }
    try:
        menu_processor(
            menu_dict=platform_menu,
            choice_text="Select the platform",
            menu_heading="Platforms"
        )
    except Exception as e:
        better_error_handling(e)





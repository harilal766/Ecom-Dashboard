from helpers.terminal_scripts import clear_terminal,recompile
from helpers.messages import *
from dashboard.d_utils import *
from dashboard.d_utils import *
from helpers.input_handling import menu_processor
from helpers.label_sorter import shipping_label_sort

# Menu4
options_menu = {
    0:("Clear Terminal",clear_terminal),
    1:("Amazon shipment report",report_generator),
    2:("Postal tracking details",postal_tracking),
    3:("Label sorter",shipping_label_sort)
}
# Split into 2 menu dictionaries
feat_last_key = list(options_menu.keys())[-1]
exit_menu = {
    99:("Recompile",recompile)
    }

main_menu = {**options_menu, **exit_menu}

            
if __name__ == "__main__":
    menu_processor(menu_dict=main_menu,choice_text="Select an option",menu_heading="Main Menu")
from helpers.terminal_scripts import clear_terminal,recompile

from helpers.messages import *
from dashboard.d_utils import *
from dashboard.d_utils import report_generator
from helpers.input_handling import menu_processor

# Menu4
options_menu = {
    0:("Clear Terminal",clear_terminal),
    1:("Amazon shipment report",report_generator),
}
# Split into 2 menu dictionaries
feat_last_key = list(options_menu.keys())[-1]
exit_menu = {
    99:("Recompile",recompile)
    }

main_menu = {**options_menu, **exit_menu}

            
if __name__ == "__main__":
    menu_processor(menu_dict=main_menu,choice_text="Select an option")
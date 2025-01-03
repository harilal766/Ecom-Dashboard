from report_generator import report_driver
from helpers.terminal_scripts import clear_terminal,recompile
from helpers.file_ops import function_boundary
from helpers.messages import *
from post_tracking import post_tracking
from api_driver import api_menus_driver


# Menu4
feature_menu = {
    0:("Clear Terminal",clear_terminal),
    1:("Amazon shipment report", report_driver),
    2:("Shopify shipment report",report_driver),
    3:("Post Tracking",post_tracking),
    4:("Amazon Todays Orders API",api_menus_driver),
    5:("Amazon Order API",api_menus_driver),
    6:("Amazon shipment report API",report_driver)
}
# Split into 2 menu dictionaries
feat_last_key = list(feature_menu.keys())[-1]
exit_menu = {
    99:("Recompile",recompile)
    }

menu = {**feature_menu, **exit_menu}
space = "-"*15

def main():
    while True:
        # Prompting the user for an option
        function_boundary(title="MENU")
        for option in menu:
            color_text(message=f"{option}. {menu[option][0]}",color='green')
        print(f"{space}-----{space}")
        try:
            selection = int(input("Select an option : "))
        except ValueError:
            color_text(message="Please enter a number\n",color='red')
            continue
        except KeyboardInterrupt:
            color_text(message="No option selected.\n",color='red')
            continue

        # Processing the selected input
        if (selection in menu):
            print(f"You have selected : {menu[selection][0]}")
            argument = menu[selection][0].lower()
            # selectin api and report functions
            color_text(message=f"{space}Execution Log{space}",color='blue')
            if "api" in argument:
                menu[selection][1](argument)
            else:
                menu[selection][1]()
            if selection:
                color_text(message=f"{space}END{space}",color='red')
        else:
            print("Invalid Selection,Try again.")

        

            
if __name__ == "__main__":
    main()
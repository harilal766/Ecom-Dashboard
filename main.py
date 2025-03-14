from helpers.terminal_scripts import clear_terminal,recompile
from helpers.file_ops import function_boundary
from helpers.messages import *
from dashboard.utils import *



# Menu4
feature_menu = {
    0:("Clear Terminal",clear_terminal),
    1:("Amazon shipment report",report_generator),
    2:("Shopify shipment report",0),
    3:("Post Tracking",0),
    4:("Amazon Todays Orders API",0),
    5:("Amazon Order API",0),
    6:("Amazon shipment report API",0)
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
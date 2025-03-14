from helpers.file_ops import function_boundary
from helpers.messages import *



def menu_processor(menu_dict,choice_text):
    space = "-"*15
    while True:
        # Prompting the user for an option
        function_boundary(title="MENU")
        for option in menu_dict:
            color_text(message=f"{option}. {menu_dict[option][0]}",color='green')
        print(f"{space}-----{space}")
        try:
            selection = int(input(f"{choice_text} : "))
        except ValueError:
            color_text(message="Please enter a number\n",color='red')
            continue
        except KeyboardInterrupt:
            color_text(message="No option selected.\n",color='red')
            continue

        # Processing the selected input
        if (selection in menu_dict):
            print(f"You have selected : {menu_dict[selection][0]}")
            argument = menu_dict[selection][0].lower()
            # selectin api and report functions
            color_text(message=f"{space}Execution Log{space}",color='blue')
            if "api" in argument:
                menu_dict[selection][1](argument)
            else:
                menu_dict[selection][1]()
            if selection:
                color_text(message=f"{space}END{space}",color='red')
        else:
            print("Invalid Selection,Try again.")

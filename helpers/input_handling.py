from helpers.file_ops import function_boundary
from helpers.messages import *


def menu_processor(menu_dict,choice_text,menu_heading):
    space = "-"*15
    while True:
        # Prompting the user for an option
        function_boundary(title=menu_heading)
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

            selection_text = menu_dict[selection][0]
            selection_function = menu_dict[selection][1]

            print(f"You have selected : {selection_text}")
            argument = selection_text.lower()
            # selectin api and report functions
            color_text(message=f"{space}Execution Log{space}",color='blue')
            if "api" in argument:
                selection_function(argument)
            else:
                selection_function()
            if selection:
                color_text(message=f"{space}END{space}",color='red')
        else:
            print("Invalid Selection,Try again.")

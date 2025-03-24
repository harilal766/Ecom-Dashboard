from loguru import logger
from colorama import Fore,Style,init


hyphen = "-"* 110
red_boundary = ""


green_boundary = f"{Fore.GREEN}{hyphen}{Style.RESET_ALL}"
def better_error_handling(error):

    exceptions = {
        # File related errors
        FileNotFoundError : "The file not found on the directory",
        # Import related
        ImportError : "The libraries you tried to import does not exist"
    }
    """
    Establish a boundary
    Error heading
    Mesaage printing
    End of boundary
        """
    boundary = f"\033[31m {hyphen} \033[0m"
    print(boundary)
    logger.exception(f"\n{exceptions[error]}" if error in exceptions else f"Error : {error}")
    print(boundary)


def success_status_msg(status):
    #print(green_boundary)
    print(f"{Fore.GREEN}{status}{Style.RESET_ALL}")
    #print(green_boundary)

def color_text(message,color=None,end=None,bold=None):
    foregreen = None
    if color != None:
        if color.lower() == 'red':
            foregreen = Fore.RED
        elif color.lower() == 'green':
            foregreen = Fore.GREEN
        elif color.lower() == "blue":
            foregreen = Fore.BLUE
        """
        if type(message) == str:
            message = message.capitalize()
        """
    else:
        foregreen = Fore.GREEN

    message_string = f"{foregreen}{message}{Style.RESET_ALL}"

    if bold == "yes":
	    message_string = Style.BRIGHT+message_string

    print(message_string,end=end)



        

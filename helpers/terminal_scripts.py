import os,sys,subprocess
import time
from helpers.messages import better_error_handling,color_text
from helpers.file_ops import *
def clear_terminal():
    print("Clearing Terminal...")
    time.sleep(0.5)
    os.system( 'cls' if os.name == 'nt' else 'clear')

def recompile():
    try:
        #python_path = str(sys.executable)
        python_path = dir_switch(win=sys.executable,lin="/bin/python3")
        script_path = dir_switch(win=win_main, lin=lin_main)
        color_text(f"python : {python_path}\n main.py : {script_path}")
        command = f'"{python_path}" "{script_path}"'
        color_text(message=python_path,color='blue')
        color_text(message="Recompiling....",color='blue')
        clear_terminal()
        subprocess.run(command, check=True) 
    except Exception as e:
        better_error_handling(e)


import sys
import time
import datetime
import os

def banner(lang):
    print("\033[1;35m")
    print("████████╗███████╗██████╗ ███╗   ███╗███████╗")
    print("╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔════╝")
    print("   ██║   █████╗  ██████╔╝██╔████╔██║█████╗  ")
    print("   ██║   ██╔══╝  ██╔═══╝ ██║╚██╔╝██║██╔══╝  ")
    print("   ██║   ███████╗██║     ██║ ╚═╝ ██║███████╗")
    print("   ╚═╝   ╚══════╝╚═╝     ╚═╝     ╚═╝╚══════╝")
    print(lang.get("banner_subtitle"))
    print("\033[0m")

def loading_animation(text, duration):
    for _ in range(duration * 3):
        for ch in "|/-\\":
            sys.stdout.write(f"\r{text} {ch}")
            sys.stdout.flush()
            time.sleep(0.1)
    print("\r" + " " * len(text) + "\r", end="")

def progress_bar(text, duration=1):
    """Menampilkan animasi progress bar sederhana."""
    total_steps = 20
    print() 
    for i in range(total_steps + 1):
        percent = (i * 100) // total_steps
        filled = "#" * i
        empty = "-" * (total_steps - i)
        sys.stdout.write(f"\r{text}: [{filled}{empty}] {percent}%")
        sys.stdout.flush()
        time.sleep(duration / total_steps)
    print("\n") 

def get_prompt(sandbox_root, lang): 
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    
    full_path = os.path.abspath(os.getcwd())
    abs_sandbox_root = os.path.abspath(sandbox_root)
    display_path = ""

    if full_path.startswith(abs_sandbox_root):
        display_path = full_path[len(abs_sandbox_root):]
        if not display_path: 
            display_path = "/" 
        display_path = "~" + display_path.replace("\\", "/") 
    else:
        display_path = os.path.basename(full_path) 
    prompt_prefix = lang.get('prompt_prefix')
    return f"\033[1;34m┌─[\033[1;32m{display_path}\033[1;34m]──[\033[1;36m{time_str}\033[1;34m]\n└──╼ \033[1;35m{prompt_prefix} > \033[0m"

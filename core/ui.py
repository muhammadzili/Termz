import sys
import time
import datetime
import os

def banner(lang):
    banner_text = [
        "\033[1;35m",
        "    ___       ___       ___       ___       ___    ",
        "   /\  \     /\  \     /\  \     /\__\     /\  \   ",
        "   \:\  \   /::\  \   /::\  \   /::L_L_   _\:\  \  ",
        "   /::\__\ /::\:\__\ /::\:\__\ /:/L:\__\ /::::\__\ ",
        "  /:/\/__/ \:\:\/  / \;:::/  / \/_/:/  / \::;;/__/ ",
        "  \/__/     \:\/  /   |:\/__/    /:/  /   \:\__\   ",
        "             \/__/     \|__|     \/__/     \/__/   ",
        "\033[0m",
        lang.get("banner_subtitle"),
        "\033[0m"
    ]
    for line in banner_text:
        print(line)
        time.sleep(0.05) 

def type_text(text, delay=0.01, newline=True):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    if newline:
        print()

def print_success(text):
    print(f"\033[1;32m[✓]\033[0m {text}")

def print_error(text):
    print(f"\033[1;31m[✗]\033[0m {text}")

def print_info(text):
    print(f"\033[1;34m[*]\033[0m {text}")

def print_warning(text):
    print(f"\033[1;33m[?]\033[0m {text}")

def loading_animation(text, duration):
    for _ in range(duration * 3):
        for ch in "|/-\\":
            sys.stdout.write(f"\r\033[1;34m[*]\033[0m {text} {ch}")
            sys.stdout.flush()
            time.sleep(0.1)
    print("\r" + " " * (len(text) + 5) + "\r", end="")

def progress_bar(text, duration=1):
    total_steps = 20
    print() 
    for i in range(total_steps + 1):
        percent = (i * 100) // total_steps
        filled = "█" * i
        empty = "░" * (total_steps - i)
        sys.stdout.write(f"\r\033[1;34m[*]\033[0m {text}: \033[1;32m[{filled}{empty}] {percent}%\033[0m")
        sys.stdout.flush()
        time.sleep(duration / total_steps)
    print("\n") 

def get_prompt(sandbox_root, lang): 
    time_str = datetime.datetime.now().strftime("%H:%M")
    
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
    
    top_line = f"\033[1;34m╭─[\033[1;32m{prompt_prefix}\033[1;34m]─[\033[1;36m{display_path}\033[1;34m]─[\033[1;33m{time_str}\033[1;34m]\033[0m"
    bottom_line = f"\033[1;34m╰─❯\033[0m "
    
    return f"{top_line}\n{bottom_line}"

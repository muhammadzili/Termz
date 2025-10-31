# Termz 🚀
## 🌐 Read README in different languages
1. 🇬🇧 [English](https://github.com/muhammadzili/tree/main/readme/english.md)
2. 🇮🇷🇺 [Russia](https://github.com/muhammadzili/tree/main/readme/russia.md)
3. 🇮🇧🇷 [Brazil](https://github.com/muhammadzili/tree/main/readme/brazil.md)


<pre>
████████╗███████╗██████╗ ███╗   ███╗███████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔════╝
   ██║   █████╗  ██████╔╝██╔████╔██║█████╗  
   ██║   ██╔══╝  ██╔═══╝ ██║╚██╔╝██║██╔══╝  
   ██║   ███████╗██║     ██║ ╚═╝ ██║███████╗
   ╚═╝   ╚══════╝╚═╝     ╚═╝     ╚═╝╚══════╝
</pre>

**A terminal inside a terminal? Why not?**
A shell sandbox made by our nation's children! 🇮🇩

## ❓ What is this?

**Termz** is *not* a real shell like `bash` or `zsh`.

It is a **sandboxed terminal environment**. This means that all file commands (such as `ls`, `cd`, `mkdir`, `rm`) that you run only apply within the `Termz/home` folder. It cannot damage or mess up your original system files.

It's very safe for tinkering, testing, or learning the command line without worry!

## ✨ Cool Features

* **100% Sandboxed**: All system file actions are *confined* to the `Termz/home` directory.
* **Built-in Package Manager**: Has its own `pkg install`, `pkg remove`, `pkg update`.
* **Flexible Package Repositories**: You can switch package sources (`trm change repo`), from the default GitHub repository to your own mirror.
* **Built-in Commands**: Basic commands like `ls`, `cd`, `mkdir`, `rm`, `rm -rf`, `clear`, and `exit` are already available.
* **Text Editor**: There is a `tre` command for editing files (using `nano` from your host system).
* **Ready-to-Use Git**: You can `git clone` directly inside the sandbox.

## 💻 How to Run

This project requires Python 3.

### 1. Clone the Repository

```bash
git clone https://github.com/muhammadzili/Termz.git
cd Termz
```

### 2. Install the Required Modules
```
pip install -r requirements.txt
```

### 4. Run!
```
python termz.py
```

### List of Commands
#### Here's the list of commands. You can also enter termz and type help.
```
Available commands:
  --- Navigation & Files ---
  ls [path]              - Display directory contents
  cd <dir>               - Change directory (supports ‘..’ to go up)
  mkdir <dir>            - Create a new directory
  rm <file>              - Delete file
  rm -rf <dir/file>      - Force delete folder or file
  tre <filename>         - Edit file (using host ‘nano’)
  git clone <url> [dir]  - Clone repository from GitHub
  
  --- Package Management ---
  trm change repo        - Change package repository URL (interactive)
  pkg install <name>     - Install package from repo
  pkg remove <name>      - Remove installed package
  pkg update             - Update package list from repo
  pkg upgrade            - Upgrade all installed packages
  trm installed          - Show installed packages
  trm search <keyword>   - Search package in repo
  trm run <command>      - Run a command from an installed package
  
  --- Others ---
  clear                  - Clear screen
  exit                   - Exit Termz
  
  You can also run installed packages directly
  by typing: <package_name> [subcommand]
```

## Want to create your own package?
1. You can create your own package for Termz. It's super easy!
2. You just need to create a .json file containing the package info and the Python commands you want to run.
3. Check out the examples in the package repo (e.g., art.json or cowsay-lite.json).
4. Upload your .json file to your own server/repo.
5. Update the index.json file on your server to notify Termz about your new package.
6. Run `trm change repo` in Termz to point to your repository, then `pkg update` and `pkg install package_name`!

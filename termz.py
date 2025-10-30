import os
import subprocess
import shutil
from core.ui import banner, get_prompt
from core.package import PackageManager
from core.command import CommandHandler

SANDBOX_ROOT = os.path.abspath("Termz/home")
ORIGINAL_CWD = os.getcwd()

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    banner()

    os.makedirs(SANDBOX_ROOT, exist_ok=True)
    
    try:
        os.chdir(SANDBOX_ROOT)
    except Exception as e:
        print(f"Error fatal: Gagal masuk ke direktori home {SANDBOX_ROOT}: {e}")
        return

    pkg = PackageManager()
    
    installed_packages_cache = pkg.load()
    cmd_handler = CommandHandler(pkg, installed_packages_cache) 

    print("\033[1;32mWelcome to Termz v1.0! (Beta Testing) Type 'help' for command list.\033[0m")
    print(f"\033[1;33mRunning on: {SANDBOX_ROOT}\033[0m\n")


    while True:
        try:
            prompt = get_prompt(SANDBOX_ROOT) 
            cmd = input(prompt).strip()

            if not cmd:
                continue

            if cmd == "help":
                print("""
Available commands:
  --- Navigasi & File ---
  ls [path]              - Tampilkan isi direktori
  cd <dir>               - Pindah direktori (mendukung '..' untuk naik)
  mkdir <dir>            - Buat direktori baru
  rm <file>              - Hapus file
  rm -rf <dir/file>      - Hapus folder atau file secara paksa
  tre <filename>         - Edit file (menggunakan 'nano' host)
  git clone <url> [dir]  - Clone repository dari GitHub
  
  --- Manajemen Paket ---
  trm change repo        - Ganti URL repository paket (interaktif)
  pkg install <name>     - Install package from repo
  pkg remove <name>      - Remove installed package
  pkg update             - Update package list from repo
  pkg upgrade            - Upgrade all installed packages
  trm installed          - Show installed packages
  trm search <keyword>   - Search package in repo
  trm run <command>      - Run a command from installed package
  
  --- Lainnya ---
  clear                  - Clear screen
  exit                   - Exit Termz
  
  Anda juga bisa menjalankan paket terinstall langsung
  dengan mengetik: <package_name> [subcommand]
""")
            elif cmd == 'ls' or cmd.startswith("ls "):
                parts = cmd.split()
                target_dir = parts[1] if len(parts) > 1 else "."
                
                abs_target = os.path.abspath(target_dir)
                if not abs_target.startswith(SANDBOX_ROOT):
                    print("❌ Error: Akses ditolak.")
                    continue

                try:
                    for f in sorted(os.listdir(abs_target)):
                        path = os.path.join(abs_target, f)
                        if os.path.isdir(path):
                            print(f"\033[1;34m{f}/\033[0m")
                        else:
                            print(f)
                except Exception as e:
                    print(f"❌ Error ls: {e}")

            elif cmd.startswith("cd "):
                target_dir = cmd.split(" ", 1)[1]
                try:
                    prospective_path = os.path.abspath(os.path.join(os.getcwd(), target_dir))
                    
                    if prospective_path.startswith(SANDBOX_ROOT):
                        os.chdir(target_dir)
                    else:
                        if os.path.abspath(os.getcwd()) == SANDBOX_ROOT and (target_dir == ".." or target_dir == "../"):
                             print("Berada di root sandbox, tidak bisa naik lagi.")
                        else:
                             print(f"❌ Error: Akses ditolak (di luar sandbox).")

                except FileNotFoundError:
                    print(f"❌ Error: Direktori '{target_dir}' tidak ditemukan.")
                except Exception as e:
                    print(f"❌ Error cd: {e}")

            elif cmd.startswith("mkdir "):
                target_dir = cmd.split(" ", 1)[1]
                abs_target = os.path.abspath(target_dir)
                if not abs_target.startswith(SANDBOX_ROOT):
                    print("❌ Error: Akses ditolak.")
                    continue
                try:
                    os.makedirs(target_dir, exist_ok=True)
                    print(f"✅ Direktori '{target_dir}' dibuat.")
                except Exception as e:
                    print(f"❌ Error mkdir: {e}")

            elif cmd.startswith("rm -rf ") or cmd.startswith("rm -r "):
                target = cmd.split(maxsplit=2)[-1]
                abs_target = os.path.abspath(target)

                if not abs_target.startswith(SANDBOX_ROOT):
                    print("❌ Error: Akses ditolak.")
                    continue
                
                if abs_target == SANDBOX_ROOT:
                    print("❌ Error: Tidak bisa menghapus direktori root home.")
                    continue
                
                try:
                    if os.path.isdir(abs_target):
                        shutil.rmtree(abs_target)
                        print(f"🗑️  Direktori '{target}' dihapus.")
                    elif os.path.isfile(abs_target):
                        os.remove(abs_target)
                        print(f"🗑️  File '{target}' dihapus.")
                    else:
                        print(f"❌ Error: '{target}' tidak ditemukan.")
                except Exception as e:
                    print(f"❌ Error rm -rf: {e}")

            elif cmd.startswith("rm "):
                target = cmd.split(" ", 1)[1]
                abs_target = os.path.abspath(target)

                if not abs_target.startswith(SANDBOX_ROOT):
                    print("❌ Error: Akses ditolak.")
                    continue
                
                try:
                    if os.path.isfile(abs_target):
                        os.remove(abs_target)
                        print(f"🗑️  File '{target}' dihapus.")
                    elif os.path.isdir(abs_target):
                        print(f"❌ Error: '{target}' adalah direktori. Gunakan 'rm -rf' untuk menghapus.")
                    else:
                        print(f"❌ Error: File '{target}' tidak ditemukan.")
                except Exception as e:
                    print(f"❌ Error rm: {e}")

            elif cmd.startswith("tre "):
                filename = cmd.split(" ", 1)[1]
                abs_target = os.path.abspath(filename)
                if not abs_target.startswith(SANDBOX_ROOT):
                    print("❌ Error: Akses ditolak.")
                    continue
                
                try:
                    print(f"Membuka {filename} dengan nano...")
                    subprocess.run(["nano", filename], check=True)
                    print(f"Nano ditutup.")
                except FileNotFoundError:
                    print("❌ Error: 'nano' tidak terinstall di sistem host.")
                    print("   'tre' memerlukan 'nano' untuk berfungsi.")
                except Exception as e:
                    print(f"❌ Error menjalankan nano: {e}")

            elif cmd.startswith("git clone "):
                parts = cmd.split()
                if len(parts) < 3:
                    print("Usage: git clone <repo_url> [optional_dir]")
                    continue
                
                repo_url = parts[2]
                target_dir = parts[3] if len(parts) > 3 else repo_url.split('/')[-1].replace('.git', '')

                abs_target = os.path.abspath(target_dir)
                if not abs_target.startswith(SANDBOX_ROOT):
                    print("❌ Error: Akses ditolak.")
                    continue
                
                try:
                    print(f"Cloning '{repo_url}' ke '{target_dir}'...")
                    subprocess.run(["git", "clone", repo_url, target_dir], check=True)
                    print(f"✅ Selesai clone.")
                except FileNotFoundError:
                     print(f"❌ Error: 'git' tidak terinstall di sistem host.")
                except Exception as e:
                    print(f"❌ Error git clone: {e}")
            
            elif cmd == "trm change repo":
                print("\n--- Ganti Repository ---")
                print("Repo saat ini:", pkg.api_url)
                print("\nPilih repo baru:")
                print("  1. Repo Default (GitHub)")
                print("  2. Repo Mirror (tinkrow.space)")
                print("  3. Kustom (Masukkan URL)")
                print("\n  0. Batal")
                
                try:
                    choice = input("Pilihan [0-3]: ").strip()
                except EOFError:
                    choice = "0"
                
                if choice == "1":
                    pkg.set_repo()
                elif choice == "2":
                    pkg.set_repo("https://termz.tinkrow.space/packages/")
                elif choice == "3":
                    try:
                        custom_url = input("Masukkan URL repo kustom: ").strip()
                        if custom_url:
                            pkg.set_repo(custom_url)
                        else:
                            print("URL kosong, dibatalkan.")
                    except EOFError:
                        print("\nDibatalkan.")
                else:
                    print("Ganti repo dibatalkan.")
                print("")
            
            elif cmd.startswith("trm repo"):
                print("Perintah 'trm repo <url>' sudah diganti.")
                print("Gunakan 'trm change repo' untuk menu interaktif.")

            elif cmd.startswith("pkg install"):
                name = cmd.split(" ")[-1]
                installed_packages_cache = pkg.install(name)
                cmd_handler.update_cache(installed_packages_cache)
                
            elif cmd.startswith("pkg remove"):
                name = cmd.split(" ")[-1]
                installed_packages_cache = pkg.remove(name)
                cmd_handler.update_cache(installed_packages_cache)
                
            elif cmd == "pkg update":
                pkg.update_repo()
            elif cmd == "pkg upgrade":
                pkg.upgrade_all()
            elif cmd == "trm installed":
                pkg.list_installed()
            elif cmd.startswith("trm search"):
                keyword = cmd.replace("trm search", "").strip()
                pkg.search(keyword)
            elif cmd.startswith("trm run"):
                command_string = cmd.replace("trm run", "").strip()
                cmd_handler.run_command(command_string)
            elif cmd == "clear":
                os.system('clear' if os.name != 'nt' else 'cls')
            elif cmd == "exit":
                print("\033[1;33mGoodbye 👋\033[0m")
                os.chdir(ORIGINAL_CWD)
                break
            else:
                command_base = cmd.split(" ")[0]
                
                if command_base in installed_packages_cache:
                    cmd_handler.run_command(cmd)
                else:
                    print("Unknown command. Type 'help' for help.")

        except KeyboardInterrupt:
            print("\nInterrupted. Type 'exit' to quit.")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()

import os
import subprocess
import shutil
from core import ui
from core.package import PackageManager
from core.command import CommandHandler
from core.language import LanguageManager

SANDBOX_ROOT = os.path.abspath("Termz/home")
ORIGINAL_CWD = os.getcwd()

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    os.makedirs(SANDBOX_ROOT, exist_ok=True)
    try:
        os.chdir(SANDBOX_ROOT)
    except Exception as e:
        ui.print_error(f"Error fatal: Gagal masuk ke direktori home {SANDBOX_ROOT}: {e}")
        return
    lang = LanguageManager()
    ui.banner(lang)

   
    pkg = PackageManager(lang) 
    installed_packages_cache = pkg.load()
    cmd_handler = CommandHandler(pkg, installed_packages_cache, lang) 

    ui.type_text(f"\033[1;32m{lang.get('welcome_message')}\033[0m", delay=0.005)
    ui.print_info(f"\033[1;33m{lang.get('running_on')}: {SANDBOX_ROOT}\033[0m")
    
    print("\n\033[1;36m" + "┌" + "─" * 50 + "┐")
    print("│ " + f"{lang.get('announcement_title'):^48}" + " │")
    print("│ " + f"{lang.get('announcement_body'):^48}" + " │")
    print("└" + "─" * 50 + "┘" + "\033[0m\n")

    while True:
        try:

            prompt = ui.get_prompt(SANDBOX_ROOT, lang) 
            cmd = input(prompt).strip()

            if not cmd:
                continue

            parts = cmd.split()
            command = parts[0]
            args_str = cmd.split(" ", 1)[1] if len(parts) > 1 else ""

            if command == "help":
                print(f"""
{lang.get('help_title')}
  {lang.get('help_nav_file')}
  ls [path]              - {lang.get('help_ls')}
  cd <dir>               - {lang.get('help_cd')}
  mkdir <dir>            - {lang.get('help_mkdir')}
  touch <file>           - {lang.get('help_touch')}
  cat <file>             - {lang.get('help_cat')}
  cp <src> <dest>        - {lang.get('help_cp')}
  mv <src> <dest>        - {lang.get('help_mv')}
  rm <file>              - {lang.get('help_rm')}
  rm -rf <dir/file>      - {lang.get('help_rm_rf')}
  tre <filename>         - {lang.get('help_tre')}
  git clone <url> [dir]  - {lang.get('help_git_clone')}
  
  {lang.get('help_pkg_mgmt')}
  trm change repo        - {lang.get('help_trm_change_repo')}
  trm set language     - {lang.get('help_trm_set_lang')}
  pkg install <name>     - {lang.get('help_pkg_install')}
  pkg remove <name>      - {lang.get('help_pkg_remove')}
  pkg update             - {lang.get('help_pkg_update')}
  pkg upgrade            - {lang.get('help_pkg_upgrade')}
  trm installed          - {lang.get('help_trm_installed')}
  trm search <keyword>   - {lang.get('help_trm_search')}
  run <command>          - {lang.get('help_trm_run')}
  
  {lang.get('help_other')}
  clear                  - {lang.get('help_clear')}
  exit                   - {lang.get('help_exit')}
  
  {lang.get('help_footer')}
""")
            elif command == 'ls':
                target_dir = args_str if args_str else "."
                
                abs_target = os.path.abspath(target_dir)
                if not abs_target.startswith(SANDBOX_ROOT):
                    ui.print_error(lang.get('access_denied'))
                    continue

                try:
                    for f in sorted(os.listdir(abs_target)):
                        path = os.path.join(abs_target, f)
                        if os.path.isdir(path):
                            print(f"\033[1;34m{f}/\033[0m")
                        else:
                            print(f)
                except Exception as e:
                    ui.print_error(f"{lang.get('error_ls')}: {e}")

            elif command == "cd":
            
                if not args_str:
                    ui.print_warning(f"Usage: cd <dir>") 
                    continue
                
                target_dir = args_str
                try:
                    prospective_path = os.path.abspath(os.path.join(os.getcwd(), target_dir))
                    
                    if prospective_path.startswith(SANDBOX_ROOT):
                        os.chdir(target_dir)
                    else:
                        current_abs = os.path.abspath(os.getcwd())
                        if current_abs == SANDBOX_ROOT and target_dir in ("..", "../"):
                             ui.print_warning(lang.get('cannot_go_up'))
                        else:
                             ui.print_error(lang.get('access_denied'))

                except FileNotFoundError:
                    ui.print_error(lang.get('dir_not_found', target_dir=target_dir))
                except Exception as e:
                    ui.print_error(f"{lang.get('error_cd')}: {e}")

            elif command == "mkdir":
                if not args_str:
                    ui.print_warning(f"Usage: mkdir <dir>")
                    continue
                
                target_dir = args_str
                abs_target = os.path.abspath(target_dir)
                if not abs_target.startswith(SANDBOX_ROOT):
                    ui.print_error(lang.get('access_denied'))
                    continue
                try:
                    os.makedirs(target_dir, exist_ok=True)
                    ui.print_success(lang.get('dir_created', target_dir=target_dir))
                except Exception as e:
                    ui.print_error(f"{lang.get('error_mkdir')}: {e}")

            elif command == "touch":
                if not args_str:
                    ui.print_warning(lang.get('usage_touch'))
                    continue
                
                target_file = args_str
                abs_target = os.path.abspath(target_file)
                if not abs_target.startswith(SANDBOX_ROOT):
                    ui.print_error(lang.get('access_denied'))
                    continue
                try:
                    with open(abs_target, 'a'):
                        os.utime(abs_target, None)
                    ui.print_success(lang.get('file_created', target=target_file))
                except Exception as e:
                    ui.print_error(f"{lang.get('error_touch')}: {e}")

            elif command == "cat":
                if not args_str:
                    ui.print_warning(lang.get('usage_cat'))
                    continue
                
                target_file = args_str
                abs_target = os.path.abspath(target_file)
                if not abs_target.startswith(SANDBOX_ROOT):
                    ui.print_error(lang.get('access_denied'))
                    continue
                
                try:
                    if os.path.isdir(abs_target):
                        ui.print_error(lang.get('error_cat_is_dir', target=target_file))
                    elif os.path.isfile(abs_target):
                        with open(abs_target, 'r', encoding='utf-8') as f:
                            print(f.read())
                    else:
                        ui.print_error(lang.get('file_not_found', target=target_file))
                except Exception as e:
                    ui.print_error(lang.get('error_cat_read', file=target_file, e=e))

            elif command == "cp":
                if len(parts) < 3:
                    ui.print_warning(lang.get('usage_cp'))
                    continue
                
                src, dest = parts[1], parts[2]
                abs_source = os.path.abspath(src)
                abs_dest = os.path.abspath(dest)

                if not abs_source.startswith(SANDBOX_ROOT) or not abs_dest.startswith(SANDBOX_ROOT):
                    ui.print_error(lang.get('access_denied'))
                    continue
                
                try:
                    if not os.path.exists(abs_source):
                        ui.print_error(lang.get('not_found', target=src))
                        continue
                    
                    if os.path.isdir(abs_source):
                        shutil.copytree(abs_source, abs_dest)
                    else:
                        shutil.copy(abs_source, abs_dest)
                    ui.print_success(lang.get('cp_success', dest=dest))
                except Exception as e:
                    ui.print_error(f"{lang.get('error_cp_general')}: {e}")

            elif command == "mv":
                if len(parts) < 3:
                    ui.print_warning(lang.get('usage_mv'))
                    continue
                
                src, dest = parts[1], parts[2]
                abs_source = os.path.abspath(src)
                abs_dest = os.path.abspath(dest)

                if not abs_source.startswith(SANDBOX_ROOT) or not abs_dest.startswith(SANDBOX_ROOT):
                    ui.print_error(lang.get('access_denied'))
                    continue

                try:
                    if not os.path.exists(abs_source):
                        ui.print_error(lang.get('not_found', target=src))
                        continue
                    
                    shutil.move(abs_source, abs_dest)
                    ui.print_success(lang.get('mv_success', dest=dest))
                except Exception as e:
                    ui.print_error(f"{lang.get('error_mv_general')}: {e}")

            elif command == "rm" and len(parts) > 1 and parts[1] in ("-rf", "-r"):
                if len(parts) < 3:
                    ui.print_warning("Usage: rm -rf <dir/file>")
                    continue
                
                target = parts[2]
                abs_target = os.path.abspath(target)

                if not abs_target.startswith(SANDBOX_ROOT):
                    ui.print_error(lang.get('access_denied'))
                    continue
                
                if abs_target == SANDBOX_ROOT:
                    ui.print_error(lang.get('cannot_delete_root'))
                    continue
                
                try:
                    if os.path.isdir(abs_target):
                        shutil.rmtree(abs_target)
                        ui.print_success(lang.get('dir_deleted', target=target))
                    elif os.path.isfile(abs_target):
                        os.remove(abs_target)
                        ui.print_success(lang.get('file_deleted', target=target))
                    else:
                        ui.print_error(lang.get('not_found', target=target))
                except Exception as e:
                    ui.print_error(f"{lang.get('error_rm_rf')}: {e}")

            elif command == "rm":
                if not args_str:
                    ui.print_warning("Usage: rm <file>")
                    continue
                
                target = args_str
                abs_target = os.path.abspath(target)

                if not abs_target.startswith(SANDBOX_ROOT):
                    ui.print_error(lang.get('access_denied'))
                    continue
                
                try:
                    if os.path.isfile(abs_target):
                        os.remove(abs_target)
                        ui.print_success(lang.get('file_deleted', target=target))
                    elif os.path.isdir(abs_target):
                        ui.print_error(lang.get('is_dir_use_rf', target=target))
                    else:
                        ui.print_error(lang.get('file_not_found', target=target))
                except Exception as e:
                    ui.print_error(f"{lang.get('error_rm')}: {e}")

            elif command == "tre":
                if not args_str:
                    ui.print_warning("Usage: tre <filename>")
                    continue
                
                filename = args_str
                abs_target = os.path.abspath(filename)
                if not abs_target.startswith(SANDBOX_ROOT):
                    ui.print_error(lang.get('access_denied'))
                    continue
                
                try:
                    ui.print_info(lang.get('nano_opening', filename=filename))
                    subprocess.run(["nano", filename], check=True)
                    ui.print_success(lang.get('nano_closed'))
                except FileNotFoundError:
                    ui.print_error(lang.get('nano_not_found'))
                    ui.print_warning(f"   {lang.get('nano_required')}")
                except Exception as e:
                    ui.print_error(f"{lang.get('nano_error')}: {e}")

            elif command == "git" and len(parts) > 1 and parts[1] == "clone":
                if len(parts) < 3:
                    ui.print_warning(lang.get('usage_git_clone'))
                    continue
                
                repo_url = parts[2]
                target_dir = parts[3] if len(parts) > 3 else repo_url.split('/')[-1].replace('.git', '')

                abs_target = os.path.abspath(target_dir)
                if not abs_target.startswith(SANDBOX_ROOT):
                    ui.print_error(lang.get('access_denied'))
                    continue
                
                try:
                    ui.print_info(lang.get('cloning', repo_url=repo_url, target_dir=target_dir))
                    subprocess.run(["git", "clone", repo_url, target_dir], check=True)
                    ui.print_success(lang.get('clone_success'))
                except FileNotFoundError:
                     ui.print_error(lang.get('git_not_found'))
                except Exception as e:
                    ui.print_error(f"{lang.get('error_git_clone')}: {e}")
            
            elif cmd == "trm change repo":
                ui.print_info(f"\n{lang.get('repo_change_title')}")
                print(f"{lang.get('current_repo')}:", pkg.api_url)
                print(f"\n{lang.get('repo_select_new')}")
                print(f"  1. {lang.get('repo_default')}")
                print(f"  2. {lang.get('repo_mirror')}")
                print(f"  3. {lang.get('repo_custom')}")
                print(f"\n  0. {lang.get('repo_cancel')}")
                
                try:
                    choice = input(lang.get('repo_choice')).strip()
                except EOFError:
                    choice = "0"
                
                if choice == "1":
                    pkg.set_repo()
                elif choice == "2":
                    pkg.set_repo("https://termz.tinkrow.space/packages/")
                elif choice == "3":
                    try:
                        custom_url = input(lang.get('repo_custom_url')).strip()
                        if custom_url:
                            pkg.set_repo(custom_url)
                        else:
                            ui.print_warning(lang.get('repo_url_empty'))
                    except EOFError:
                        print(f"\n{lang.get('repo_cancelled')}")
                else:
                    ui.print_info(lang.get('repo_cancelled'))
                print("")
        
            elif cmd == "trm set language":
                ui.print_info(f"\n{lang.get('lang_change_title')}")
                print(f"{lang.get('lang_select_new')}")
                
                available = lang.get_available_languages()
                options = {} 
                
                i = 1
                for code, name in available.items():
                    print(f"  {i}. {name} ({code})")
                    options[str(i)] = code
                    i += 1
                
                print(f"\n  0. {lang.get('repo_cancel')}")
                
                try:
                    choice = input(lang.get('lang_choice', count=len(options))).strip()
                except EOFError:
                    choice = "0"

                if choice in options:
                    lang_code = options[choice]
                    success, lang_name = lang.set_language(lang_code)
                    if success:
                        ui.print_success(lang.get('lang_set_success', lang_name=lang_name))
                    else:
                        ui.print_error(lang.get('lang_set_fail', lang_code=lang_code))
                else:
                    ui.print_info(lang.get('lang_cancelled'))
                print("")
            
            elif cmd.startswith("trm repo"):
                ui.print_warning(lang.get('repo_cmd_deprecated'))
                ui.print_info(lang.get('repo_cmd_use_interactive'))

            elif command == "pkg" and len(parts) > 1 and parts[1] == "install":
                if len(parts) < 3:
                    ui.print_warning(lang.get('usage_pkg_install'))
                    continue
                name = parts[2]
                installed_packages_cache = pkg.install(name)
                cmd_handler.update_cache(installed_packages_cache)
                
            elif command == "pkg" and len(parts) > 1 and parts[1] == "remove":
                if len(parts) < 3:
                    ui.print_warning(lang.get('usage_pkg_remove'))
                    continue
                name = parts[2]
                installed_packages_cache = pkg.remove(name)
                cmd_handler.update_cache(installed_packages_cache)
                
            elif cmd == "pkg update":
                pkg.update_repo()
            elif cmd == "pkg upgrade":
                pkg.upgrade_all()
            elif cmd == "trm installed":
                pkg.list_installed()
                
            elif command == "trm" and len(parts) > 1 and parts[1] == "search":
                keyword = args_str.replace("search", "", 1).strip()
                if not keyword:
                    ui.print_warning(lang.get('usage_trm_search'))
                    continue
                pkg.search(keyword)
                
            elif command == "run":
                command_string = args_str
                if not command_string:
                    ui.print_warning(lang.get('usage_trm_run'))
                    continue
                cmd_handler.run_command(command_string)
                
            elif command == "clear":
                os.system('clear' if os.name != 'nt' else 'cls')
            elif command == "exit":
                ui.type_text(f"\033[1;33m{lang.get('goodbye')}\033[0m\n", delay=0.02)
                os.chdir(ORIGINAL_CWD)
                break
            else:
                if command in installed_packages_cache:
                    cmd_handler.run_command(cmd)
                else:
                    ui.print_error(lang.get('unknown_command'))

        except KeyboardInterrupt:
            print()
            ui.print_warning(f"\n{lang.get('interrupted')}")
        except Exception as e:
            ui.print_error(f"{lang.get('generic_error')}: {e}")


if __name__ == "__main__":
    main()


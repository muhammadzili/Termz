import subprocess

class CommandHandler:
    def __init__(self, package_manager, initial_cache):
        self.package_manager = package_manager
        self.installed_cache = initial_cache

    def update_cache(self, new_cache):
        """Fungsi untuk update cache internal dari termz.py"""
        self.installed_cache = new_cache

    def run_command(self, command_string):
        if not command_string:
            print("Usage: trm run <command> [subcommand]")
            return

        parts = command_string.split()
        package_name = parts[0]
        sub_command = parts[1] if len(parts) > 1 else "__default__"

        installed = self.installed_cache 

        if installed is None:
            print("⚠️ Cache internal kosong, memuat ulang dari disk...")
            installed = self.package_manager.load()
            self.installed_cache = installed

        if package_name in installed:
            info = installed[package_name]
            commands_dict = info.get("commands", {})

            command_to_run = None
            
            if sub_command in commands_dict:
                command_to_run = commands_dict[sub_command]
            
            elif sub_command == "__default__":
                if "__default__" in commands_dict:
                    command_to_run = commands_dict["__default__"]
                elif "default" in commands_dict:
                    print("   (Info: Menggunakan key 'default' format lama.)")
                    command_to_run = commands_dict["default"]
                else:
                    print(f"❌ Paket '{package_name}' tidak punya command default ('__default__' atau 'default').")
                    return
            
            elif "__default__" in commands_dict:
                print(f"Subcommand '{sub_command}' tidak ditemukan. Menjalankan default:")
                command_to_run = commands_dict["__default__"]
                
            elif "default" in commands_dict:
                print(f"Subcommand '{sub_command}' tidak ditemukan. Menjalankan default (format lama):")
                command_to_run = commands_dict["default"]
                
            else:
                print(f"❌ Paket '{package_name}' tidak punya subcommand '{sub_command}' atau command default.")
                return

            if command_to_run:
                display_subcommand = sub_command if sub_command != "__default__" else "default"
                print(f"🔹 Running '{package_name} {display_subcommand}'...")
                
                command_clean = command_to_run.replace('\u00A0', ' ')

                try:
                    exec(command_clean)
                    
                except SyntaxError as e:
                    error_msg = str(e)
                    # --- INI DIA FIX-NYA ---
                    # Kita cek dua-duanya, EOL (PC) dan unterminated (Termux)
                    if "EOL while scanning string literal" in error_msg or "unterminated string literal" in error_msg:
                        print("   (Info: Mendeteksi string multi-baris, mencoba fallback...)")
                        try:
                            command_escaped = command_clean.replace('\n', '\\n')
                            exec(command_escaped)
                        except Exception as e_escaped:
                            print(f"Error executing (escaped fallback): {e_escaped}")
                    else:
                        print(f"Error executing command (SyntaxError): {e}")
                except Exception as e:
                    print(f"Error executing command: {e}")
            return

        print(f"❌ Command '{package_name}' not found in installed packages.")


import subprocess

class CommandHandler:
    def __init__(self, package_manager, initial_cache, lang):
        self.package_manager = package_manager
        self.installed_cache = initial_cache
        self.lang = lang

    def update_cache(self, new_cache):
        self.installed_cache = new_cache

    def run_command(self, command_string):
        if not command_string:
            print(self.lang.get('cmd_usage'))
            return

        parts = command_string.split()
        package_name = parts[0]
        sub_command = parts[1] if len(parts) > 1 else "__default__"

        installed = self.installed_cache 

        if installed is None:
            print(self.lang.get('cmd_cache_empty'))
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
                    print(self.lang.get('pkg_command_parse_info_2'))
                    command_to_run = commands_dict["default"]
                else:
                    print(self.lang.get('cmd_no_default', package_name=package_name))
                    return
            
            elif "__default__" in commands_dict:
                print(self.lang.get('cmd_subcommand_not_found_default', sub_command=sub_command))
                command_to_run = commands_dict["__default__"]
                
            elif "default" in commands_dict:
                print(self.lang.get('cmd_subcommand_not_found_default', sub_command=sub_command))
                print(self.lang.get('pkg_command_parse_info_2'))
                command_to_run = commands_dict["default"]
                
            else:
                print(self.lang.get('cmd_subcommand_not_found_no_default', package_name=package_name, sub_command=sub_command))
                return

            if command_to_run:
                display_subcommand = sub_command if sub_command != "__default__" else "default"
                print(self.lang.get('cmd_running', package_name=package_name, display_subcommand=display_subcommand))
                
                command_clean = command_to_run.replace('\u00A0', ' ')

                safe_builtins = {
                    'print': print,
                    'input': input,
                    'len': len,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                    'tuple': tuple,
                    'range': range,
                    'True': True,
                    'False': False,
                    'None': None,
                    'Exception': Exception,
                    'KeyError': KeyError,
                    'ValueError': ValueError,
                    'TypeError': TypeError,
                    'IndexError': IndexError,
                    'AttributeError': AttributeError,
                    'max': max,
                    'min': min,
                    'sum': sum,
                    'abs': abs,
                    'round': round,
                    'pow': pow,
                    'repr': repr,
                    'bool': bool,
                    'set': set,
                    'issubclass': issubclass,
                    'isinstance': isinstance,
                    'hasattr': hasattr,
                    'getattr': getattr,
                    'setattr': setattr,
                    'delattr': delattr,
                    'any': any,
                    'all': all,
                    'sorted': sorted,
                    'zip': zip,
                    'enumerate': enumerate,
                    'reversed': reversed,
                    '__import__': __import__,
                }

                try:
                    exec(command_clean, {"__builtins__": safe_builtins})
                    
                except SyntaxError as e:
                    error_msg = str(e)
                    if "EOL while scanning string literal" in error_msg or "unterminated string literal" in error_msg:
                        print(self.lang.get('cmd_multiline_fallback'))
                        try:
                            command_escaped = command_clean.replace('\n', '\\n')
                            exec(command_escaped, {"__builtins__": safe_builtins})
                        except Exception as e_escaped:
                            print(self.lang.get('cmd_error_fallback', e=e_escaped))
                    else:
                        print(self.lang.get('cmd_error_syntax', e=e))
                except Exception as e:
                    print(self.lang.get('cmd_error_generic', e=e))
            return

        print(self.lang.get('cmd_not_found', package_name=package_name))


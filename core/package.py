import os
import json
import re
import requests
import time
import base64
from core.ui import progress_bar

DEFAULT_API_URL = "https://api.github.com/repos/muhammadzili/termz-package/contents/packages"

class PackageManager:
    def __init__(self, lang):
        self.lang = lang
        os.makedirs("data", exist_ok=True)
        self.file = "data/installed.json"
        self.repo_cache = "data/repo_cache.json"
        self.config_file = "data/config.json"
        self.headers = {'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}

        self._load_config() 
        
        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump({}, f)
        if not os.path.exists(self.repo_cache):
            with open(self.repo_cache, "w") as f:
                json.dump({}, f)

    def _load_config(self):
        """Memuat file config.json atau membuatnya jika tidak ada."""
        try:
            if not os.path.exists(self.config_file):
                print(self.lang.get('pkg_creating_default_config'))
                self.config = {"repo_url": DEFAULT_API_URL}
                self._save_config()
            else:
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)
        except json.JSONDecodeError:
            print(self.lang.get('pkg_config_corrupt'))
            self.config = {"repo_url": DEFAULT_API_URL}
            self._save_config()
        
        self.api_url = self.config.get("repo_url", DEFAULT_API_URL)

    def _save_config(self):
        """Menyimpan data config saat ini ke config.json."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(self.lang.get('pkg_config_save_error', e=e))

    def set_repo(self, url=None):
        """Mengatur URL repository baru atau mereset ke default."""
        if url is None:
            self.config["repo_url"] = DEFAULT_API_URL
            print(self.lang.get('pkg_repo_reset', url=DEFAULT_API_URL))
        else:
            if not url.endswith('/'):
                url += '/'
            self.config["repo_url"] = url
            print(self.lang.get('pkg_repo_changed', url=url))
        
        self._save_config()
        self._load_config() 
        print(self.lang.get('pkg_run_update'))

    def load(self):
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(self.lang.get('pkg_installed_corrupt'))
            return {} 

    def save(self, data):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    def load_repo_cache(self):
        try:
            with open(self.repo_cache, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(self.lang.get('pkg_cache_corrupt'))
            return {}

    def save_repo_cache(self, data):
        with open(self.repo_cache, "w") as f:
            json.dump(data, f, indent=4)

    def update_repo(self):
        print(self.lang.get('pkg_updating', url=self.api_url))
        try:
            if "api.github.com" in self.api_url:
                print(self.lang.get('pkg_mode_github'))
                res = requests.get(self.api_url, headers=self.headers, timeout=10)
                if res.status_code != 200:
                    raise Exception(self.lang.get('pkg_github_api_error', code=res.status_code))
                
                repo_data = {}
                for pkg in res.json():
                    if pkg["name"].endswith(".json"):
                        repo_data[pkg["name"].replace(".json", "")] = pkg["url"]
            
            else:
                print(self.lang.get('pkg_mode_mirror'))
                index_url = self.api_url + "index.json"
                
                print(self.lang.get('pkg_fetching_index', url=index_url))
                res = requests.get(index_url, headers=self.headers, timeout=10)
                if res.status_code != 200:
                    raise Exception(self.lang.get('pkg_mirror_api_error', code=res.status_code))
                
                repo_data = res.json()
                if not isinstance(repo_data, dict):
                    raise Exception(self.lang.get('pkg_mirror_not_dict'))
            
            self.save_repo_cache(repo_data)
            print(self.lang.get('pkg_update_success', count=len(repo_data)))
            return True

        except Exception as e:
            print(self.lang.get('pkg_update_error', url=self.api_url, e=e))
            
            if self.api_url != DEFAULT_API_URL:
                print(self.lang.get('pkg_fallback_default'))
                try:
                    res_default = requests.get(DEFAULT_API_URL, headers=self.headers, timeout=10)
                    if res_default.status_code == 200:
                        repo_data = {}
                        for pkg in res_default.json():
                            if pkg["name"].endswith(".json"):
                                repo_data[pkg["name"].replace(".json", "")] = pkg["url"] 
                        self.save_repo_cache(repo_data)
                        print(self.lang.get('pkg_fallback_success', count=len(repo_data)))
                        return True
                    else:
                        print(self.lang.get('pkg_fallback_fail', code=res_default.status_code))
                        return False
                except Exception as e_default:
                    print(self.lang.get('pkg_fallback_fatal', e=e_default))
                    return False
            else:
                return False

    def _parse_commands_from_data(self, data):
        """
        FIX: Fungsi ini 'menormalkan' data command.
        Dia akan cari '**default**' atau 'default' dan mengubahnya
        menjadi '__default__' secara otomatis.
        """
        if "command" in data:
            return {"__default__": data["command"]}
        
        elif "commands" in data and isinstance(data["commands"], dict):
            cmds = data["commands"].copy() 
            
            if "**default**" in cmds:
                print(self.lang.get('pkg_command_parse_info_1'))
                cmds["__default__"] = cmds.pop("**default**")
            elif "default" in cmds and "__default__" not in cmds:
                print(self.lang.get('pkg_command_parse_info_2'))
                cmds["__default__"] = cmds.pop("default")
                
            return cmds 
        
        return {} 

    def _get_package_data_from_api(self, api_url):
        """Mengambil dan mem-parse data paket dari API GitHub ATAU Simple Mirror."""
        try:
            res = requests.get(api_url, headers=self.headers, timeout=10)
            if res.status_code != 200:
                print(self.lang.get('pkg_fetch_http_error', code=res.status_code))
                return None

            if "api.github.com" in api_url:
                print(self.lang.get('pkg_fetch_mode_github'))
                res_json = res.json()
                if res_json.get("encoding") != "base64":
                    print(self.lang.get('pkg_fetch_not_base64'))
                    return None
                
                content_base64 = res_json.get("content", "")
                decoded_content = base64.b64decode(content_base64).decode("utf-8")
                
                print(self.lang.get('pkg_fetch_applying_fix'))
                safe_text = re.sub(r'\\(?![\"\\/bfnrtu])', r'\\\\', decoded_content)
            
            else:
                print(self.lang.get('pkg_fetch_mode_mirror'))
                safe_text = res.text
            
            data = json.loads(safe_text)
            return data

        except json.JSONDecodeError as e: 
            print(self.lang.get('pkg_fetch_parse_error', e=e))
            return None
        except Exception as e:
            print(self.lang.get('pkg_fetch_process_error', e=e))
            return None

    def install(self, name):
        repo_cache = self.load_repo_cache()
        api_url = repo_cache.get(name)

        if not api_url:
            print(self.lang.get('pkg_not_in_cache', name=name))
            return self.load() 

        print(self.lang.get('pkg_getting_info', name=name))
        data = self._get_package_data_from_api(api_url) 
        if not data:
            return self.load() 

        print(f"\n{self.lang.get('pkg_detail_title')}")
        print(self.lang.get('pkg_detail_name', name=data.get('name', name)))
        print(self.lang.get('pkg_detail_version', version=data.get('version', 'N/A')))
        print(self.lang.get('pkg_detail_author', author=data.get('author', 'Unknown')))
        print(self.lang.get('pkg_detail_desc', desc=data.get('desc', 'N/A')))
        print(self.lang.get('pkg_detail_footer'))
        
        try:
            confirm = input(self.lang.get('pkg_confirm_install')).strip().lower()
        except EOFError:
            confirm = "n" 
            print()

        if confirm not in ["y", "yes", ""]:
            print(self.lang.get('pkg_install_cancelled'))
            return self.load() 

        progress_bar(self.lang.get('pkg_installing', name=name), 0.5) 
        installed = self.load()

        commands = self._parse_commands_from_data(data)

        installed[name] = {
            "version": data.get("version", "1.0"),
            "commands": commands, 
            "description": data.get("desc", ""),
            "author": data.get("author", "Unknown")
        }

        self.save(installed)
        version_str = data.get('version', '1.0')
        print(self.lang.get('pkg_install_success', name=name, version=version_str))
        return installed 

    def remove(self, name):
        installed = self.load()
        if name not in installed:
            print(self.lang.get('pkg_not_installed', name=name))
            return installed 

        try:
            confirm_text = self.lang.get('pkg_confirm_remove', name=name)
            confirm = input(confirm_text).strip().lower()
        except EOFError:
            confirm = "n"
            print()

        if confirm not in ["y", "yes", ""]:
            print(self.lang.get('pkg_remove_cancelled'))
            return installed 
            
        del installed[name]
        self.save(installed)
        print(self.lang.get('pkg_remove_success', name=name))
        return installed 

    def list_installed(self):
        installed = self.load()
        if not installed:
            print(self.lang.get('pkg_list_empty'))
            return

        print(f"\n{self.lang.get('pkg_list_title')}")
        for name, info in installed.items():
            commands = ", ".join(info["commands"].keys()) if info["commands"] else "-"
            print(self.lang.get('pkg_list_item', name=name, version=info['version'], commands=commands))

    def upgrade_all(self):
        print(self.lang.get('pkg_upgrade_checking'))
        
        if not self.update_repo():
            print(self.lang.get('pkg_upgrade_fail_update'))
            return

        installed = self.load()
        repo_cache = self.load_repo_cache()
        
        if not installed:
            print(self.lang.get('pkg_upgrade_empty'))
            return

        upgraded_count = 0
        uptodate_count = 0

        print(self.lang.get('pkg_upgrade_check_installed'))
        for name, info in installed.items():
            api_url = repo_cache.get(name)
            current_ver = info.get("version", "0.0")

            if not api_url:
                print(self.lang.get('pkg_upgrade_not_in_repo', name=name))
                continue

            try:
                data = self._get_package_data_from_api(api_url) 
                if not data:
                    print(self.lang.get('pkg_upgrade_error_process', name=name))
                    continue

                new_ver = data.get("version")
                if not new_ver:
                    print(self.lang.get('pkg_upgrade_no_version', name=name))
                    continue
                
                if new_ver != current_ver:
                    print(self.lang.get('pkg_upgrading_from', name=name, current_ver=current_ver, new_ver=new_ver))
                    commands = self._parse_commands_from_data(data)
                    
                    installed[name]["version"] = new_ver
                    installed[name]["commands"] = commands
                    installed[name]["description"] = data.get("desc", "")
                    installed[name]["author"] = data.get("author", "Unknown")
                    upgraded_count += 1
                else:
                    print(self.lang.get('pkg_up_to_date', name=name, current_ver=current_ver, new_ver=new_ver))
                    uptodate_count += 1
            
            except Exception as e:
                 print(self.lang.get('pkg_upgrade_error_skip', name=name, e=e))

        self.save(installed)
        print(f"\n{self.lang.get('pkg_upgrade_complete')}")
        print(self.lang.get('pkg_upgrade_summary', upgraded_count=upgraded_count, uptodate_count=uptodate_count))

    def search(self, keyword):
        """Mencari paket di repo cache."""
        repo_cache = self.load_repo_cache()
        if not repo_cache:
            print(self.lang.get('pkg_search_empty_cache'))
            return

        print(self.lang.get('pkg_searching', keyword=keyword))
        found = 0
        for name in repo_cache.keys():
            if keyword.lower() in name.lower():
                print(self.lang.get('pkg_search_item', name=name))
                found += 1
        
        if found == 0:
            print(self.lang.get('pkg_search_not_found'))

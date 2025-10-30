import os
import json
import re
import requests
import time
import base64
from core.ui import progress_bar

DEFAULT_API_URL = "https://api.github.com/repos/muhammadzili/termz-package/contents/packages"

class PackageManager:
    def __init__(self):
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
                print("Membuat file config.json default...")
                self.config = {"repo_url": DEFAULT_API_URL}
                self._save_config()
            else:
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Peringatan: file config.json rusak. Mereset ke default.")
            self.config = {"repo_url": DEFAULT_API_URL}
            self._save_config()
        
        self.api_url = self.config.get("repo_url", DEFAULT_API_URL)

    def _save_config(self):
        """Menyimpan data config saat ini ke config.json."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"❌ Error saat menyimpan config.json: {e}")

    def set_repo(self, url=None):
        """Mengatur URL repository baru atau mereset ke default."""
        if url is None:
            self.config["repo_url"] = DEFAULT_API_URL
            print(f"✅ Repository direset ke default:\n   {DEFAULT_API_URL}")
        else:
            if not url.endswith('/'):
                url += '/'
            self.config["repo_url"] = url
            print(f"✅ Repository URL diubah menjadi:\n   {url}")
        
        self._save_config()
        self._load_config() 
        print("   Jalankan 'pkg update' untuk menyinkronkan daftar paket.")

    def load(self):
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Peringatan: file installed.json rusak. Membuat file baru.")
            return {} 

    def save(self, data):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    def load_repo_cache(self):
        try:
            with open(self.repo_cache, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Peringatan: file repo_cache.json rusak. Membuat file baru.")
            return {}

    def save_repo_cache(self, data):
        with open(self.repo_cache, "w") as f:
            json.dump(data, f, indent=4)

    def update_repo(self):
        print(f"🔄 Updating package list from {self.api_url}...")
        try:
            if "api.github.com" in self.api_url:
                print("   (Mode: GitHub API)")
                res = requests.get(self.api_url, headers=self.headers, timeout=10)
                if res.status_code != 200:
                    raise Exception(f"GitHub API returned HTTP {res.status_code}")
                
                repo_data = {}
                for pkg in res.json():
                    if pkg["name"].endswith(".json"):
                        repo_data[pkg["name"].replace(".json", "")] = pkg["url"]
            
            else:
                print("   (Mode: Simple Mirror)")
                index_url = self.api_url + "index.json"
                
                print(f"   Fetching index: {index_url}")
                res = requests.get(index_url, headers=self.headers, timeout=10)
                if res.status_code != 200:
                    raise Exception(f"Simple Mirror returned HTTP {res.status_code} for index.json")
                
                repo_data = res.json()
                if not isinstance(repo_data, dict):
                    raise Exception("Simple Mirror index.json bukan sebuah JSON object (dictionary).")
            
            self.save_repo_cache(repo_data)
            print(f"✅ Repository updated. {len(repo_data)} packages available.")
            return True

        except Exception as e:
            print(f"❌ Error updating repo from {self.api_url}: {e}")
            
            if self.api_url != DEFAULT_API_URL:
                print(f"⚠️ Mencoba kembali (fallback) ke repository default...")
                try:
                    res_default = requests.get(DEFAULT_API_URL, headers=self.headers, timeout=10)
                    if res_default.status_code == 200:
                        repo_data = {}
                        for pkg in res_default.json():
                            if pkg["name"].endswith(".json"):
                                repo_data[pkg["name"].replace(".json", "")] = pkg["url"] 
                        self.save_repo_cache(repo_data)
                        print(f"✅ Repository default berhasil dimuat. {len(repo_data)} packages available.")
                        return True
                    else:
                        print(f"❌ Gagal mengambil dari repo default (HTTP {res_default.status_code}).")
                        return False
                except Exception as e_default:
                    print(f"❌ Error fatal: Repo default juga gagal: {e_default}")
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
                print("   (Info: Mendeteksi '**default**', mengonversi ke '__default__')")
                cmds["__default__"] = cmds.pop("**default**")
            elif "default" in cmds and "__default__" not in cmds:
                print("   (Info: Mendeteksi 'default', mengonversi ke '__default__')")
                cmds["__default__"] = cmds.pop("default")
                
            return cmds 
        
        return {} 

    def _get_package_data_from_api(self, api_url):
        """Mengambil dan mem-parse data paket dari API GitHub ATAU Simple Mirror."""
        try:
            res = requests.get(api_url, headers=self.headers, timeout=10)
            if res.status_code != 200:
                print(f"Failed to fetch package data (HTTP {res.status_code}).")
                return None

            if "api.github.com" in api_url:
                print("   (Fetching mode: GitHub API)")
                res_json = res.json()
                if res_json.get("encoding") != "base64":
                    print("Error: Encoding file bukan base64.")
                    return None
                
                content_base64 = res_json.get("content", "")
                decoded_content = base64.b64decode(content_base64).decode("utf-8")
                
                # FIX BACKSLASH (\033 etc.) HANYA UNTUK GITHUB
                print("   (Applying backslash fix for GitHub content...)")
                safe_text = re.sub(r'\\(?![\"\\/bfnrtu])', r'\\\\', decoded_content)
            
            else:
                print("   (Fetching mode: Simple Mirror)")
                safe_text = res.text
            
            data = json.loads(safe_text)
            return data

        except json.JSONDecodeError as e: 
            print(f"Error parsing package data: {e}") 
            return None
        except Exception as e:
            print(f"Error processing package data: {e}")
            return None

    def install(self, name):
        repo_cache = self.load_repo_cache()
        api_url = repo_cache.get(name)

        if not api_url:
            print(f"⚠️ Package '{name}' not found in cache. Coba 'pkg update' dulu.")
            return self.load() 

        print(f"Mencari info paket '{name}'...")
        data = self._get_package_data_from_api(api_url) 
        if not data:
            return self.load() 

        print("\n--- Detail Paket ---")
        print(f"Nama    : {data.get('name', name)}")
        print(f"Versi   : {data.get('version', 'N/A')}")
        print(f"Author  : {data.get('author', 'Unknown')}")
        print(f"Deskripsi: {data.get('desc', 'N/A')}")
        print("--------------------")
        
        try:
            confirm = input("Lanjutkan instalasi? [Y/n] ").strip().lower()
        except EOFError:
            confirm = "n" 
            print()

        if confirm not in ["y", "yes", ""]:
            print("Instalasi dibatalkan.")
            return self.load() 

        progress_bar(f"Installing '{name}'", 0.5) 
        installed = self.load()

        commands = self._parse_commands_from_data(data)

        installed[name] = {
            "version": data.get("version", "1.0"),
            "commands": commands, 
            "description": data.get("desc", ""),
            "author": data.get("author", "Unknown")
        }

        self.save(installed)
        print(f"✅ Successfully installed '{name}' v{data.get('version', '1.0')}!")
        return installed 

    def remove(self, name):
        installed = self.load()
        if name not in installed:
            print(f"❌ Package '{name}' not found in installed list.")
            return installed 

        print(f"Anda yakin ingin menghapus '{name}'?")
        try:
            confirm = input("Lanjutkan? [Y/n] ").strip().lower()
        except EOFError:
            confirm = "n"
            print()

        if confirm not in ["y", "yes", ""]:
            print("Penghapusan dibatalkan.")
            return installed 
            
        del installed[name]
        self.save(installed)
        print(f"🗑️ Removed package '{name}'.")
        return installed 

    def list_installed(self):
        installed = self.load()
        if not installed:
            print("No packages installed yet.")
            return

        print("\nInstalled Packages:")
        for name, info in installed.items():
            commands = ", ".join(info["commands"].keys()) if info["commands"] else "-"
            print(f" - {name} v{info['version']} | commands: {commands}")

    def upgrade_all(self):
        print("⬆️ Checking for package upgrades...")
        
        if not self.update_repo():
            print("⚠️ Gagal update repo, proses upgrade dibatalkan.")
            return

        installed = self.load()
        repo_cache = self.load_repo_cache()
        
        if not installed:
            print("Tidak ada paket terinstall untuk di-upgrade.")
            return

        upgraded_count = 0
        uptodate_count = 0

        print("--- Memeriksa paket terinstall ---")
        for name, info in installed.items():
            api_url = repo_cache.get(name)
            current_ver = info.get("version", "0.0")

            if not api_url:
                print(f"⚠️ '{name}' tidak lagi ada di repo. Skipping.")
                continue

            try:
                data = self._get_package_data_from_api(api_url) 
                if not data:
                    print(f"❌ Error processing package '{name}'. Skipping.")
                    continue

                new_ver = data.get("version")
                if not new_ver:
                    print(f"⚠️ Paket '{name}' di repo tidak punya versi. Skipping.")
                    continue
                
                if new_ver != current_ver:
                    print(f"📦 Upgrading '{name}' from {current_ver} → {new_ver}")
                    commands = self._parse_commands_from_data(data)
                    
                    installed[name]["version"] = new_ver
                    installed[name]["commands"] = commands
                    installed[name]["description"] = data.get("desc", "")
                    installed[name]["author"] = data.get("author", "Unknown")
                    upgraded_count += 1
                else:
                    print(f"✅ '{name}' (v{current_ver}) is already up to date. (Repo version: {new_ver})")
                    uptodate_count += 1
            
            except Exception as e:
                 print(f"❌ Error processing '{name}': {e}. Skipping.")

        self.save(installed)
        print("\n🎉 Upgrade complete!")
        print(f"Upgraded: {upgraded_count}, Up-to-date: {uptodate_count}")

    def search(self, keyword):
        """Mencari paket di repo cache."""
        repo_cache = self.load_repo_cache()
        if not repo_cache:
            print("Cache repo kosong. Jalankan 'pkg update' dulu.")
            return

        print(f"Mencari '{keyword}' di repo...")
        found = 0
        for name in repo_cache.keys():
            if keyword.lower() in name.lower():
                print(f" - {name}")
                found += 1
        
        if found == 0:
            print("Tidak ada paket yang ditemukan.")


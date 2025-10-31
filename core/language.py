import json
import os
import glob

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LANGUAGE_DIR = os.path.join(ROOT_DIR, 'language')
SANDBOX_DATA_DIR = "data" 
SETTING_FILE = os.path.join(SANDBOX_DATA_DIR, "lan.json")

DEFAULT_LANG = "id"
FALLBACK_LANG = "en"

class LanguageManager:
    def __init__(self):
        self.strings = {}
        self.available_languages = {} 
        self.current_lang = DEFAULT_LANG
        
        self._discover_languages()
        self.load_language_setting()
        self.load_language_file()

    def _discover_languages(self):
        """Mencari file .json di direktori language/"""
        self.available_languages = {}
        try:
            for filepath in glob.glob(os.path.join(LANGUAGE_DIR, "*.json")):
                lang_code = os.path.basename(filepath).replace('.json', '')
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        lang_name = data.get("__lang_name__", lang_code)
                        self.available_languages[lang_code] = lang_name
                except Exception:
                    if lang_code not in self.available_languages:
                         self.available_languages[lang_code] = lang_code
        except Exception as e:
            print(f"[Language] Error discovering languages: {e}")
            
        if FALLBACK_LANG not in self.available_languages:
            print(f"[Language] Peringatan: Fallback language '{FALLBACK_LANG}.json' tidak ditemukan!")
            self.available_languages[FALLBACK_LANG] = "English (Fallback)"
            
        if DEFAULT_LANG not in self.available_languages:
             self.available_languages[DEFAULT_LANG] = "Indonesia (Default)"


    def load_language_setting(self):
        """Memuat setelan bahasa dari data/lan.json (di dalam sandbox)"""
        try:
            if os.path.exists(SETTING_FILE):
                with open(SETTING_FILE, 'r') as f:
                    settings = json.load(f)
                    self.current_lang = settings.get("lang", DEFAULT_LANG)
            else:
                self.current_lang = DEFAULT_LANG
                self.save_language_setting()
        except Exception:
            self.current_lang = DEFAULT_LANG

    def save_language_setting(self):
        """Menyimpan setelan bahasa ke data/lan.json"""
        try:
            os.makedirs(SANDBOX_DATA_DIR, exist_ok=True)
            with open(SETTING_FILE, 'w') as f:
                json.dump({"lang": self.current_lang}, f, indent=4)
        except Exception as e:
            print(f"Gagal menyimpan setelan bahasa: {e}")
    
    def load_language_file(self):
        """Memuat file bahasa, dengan fallback ke English."""
        self.strings = {}
        
        fallback_path = os.path.join(LANGUAGE_DIR, f"{FALLBACK_LANG}.json")
        try:
            with open(fallback_path, 'r', encoding='utf-8') as f:
                self.strings = json.load(f)
        except Exception as e:
            print(f"Peringatan: Gagal memuat file bahasa fallback {FALLBACK_LANG}.json: {e}")
            self.strings = {"generic_error": "Error", "unknown_command": "Unknown command."}

        if self.current_lang != FALLBACK_LANG:
            current_lang_path = os.path.join(LANGUAGE_DIR, f"{self.current_lang}.json")
            try:
                with open(current_lang_path, 'r', encoding='utf-8') as f:
                    lang_data = json.load(f)
                    self.strings.update(lang_data)
            except Exception as e:
                print(f"Peringatan: Gagal memuat file bahasa {self.current_lang}.json: {e}. Menggunakan fallback.")
                self.current_lang = FALLBACK_LANG 
    def set_language(self, lang_code):
        """Mengganti bahasa dan menyimpannya."""
        if lang_code in self.available_languages:
            self.current_lang = lang_code
            self.save_language_setting()
            self.load_language_file()
            return True, self.available_languages[lang_code]
        else:
            return False, lang_code

    def get(self, key, **kwargs):
        """Mengambil string berdasarkan key dan memformatnya."""
        message = self.strings.get(key, key) 
        try:
            return message.format(**kwargs)
        except KeyError as e:
            print(f"[Language] Missing format key {e} in '{key}'")
            return message

    def get_available_languages(self):
        """Mengembalikan dict { 'id': 'Indonesia', ... }"""
        return self.available_languages

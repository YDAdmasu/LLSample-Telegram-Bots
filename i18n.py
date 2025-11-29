import gettext
import os
import json
from threading import Lock

# Directory containing the locales folder
BASE_DIR = os.path.dirname(__file__)
LOCALES_DIR = os.path.join(BASE_DIR, "locales")

# File to persist user language preferences (per chat id)
DATA_DIR = os.path.join(BASE_DIR, "data")
USER_LANG_FILE = os.path.join(DATA_DIR, "user_langs.json")

_lock = Lock()


class I18nManager:
    """Manage gettext translations and simple user-language persistence.

    Usage:
      manager = I18nManager()
      t = manager.get_translator('am')
      t('Welcome!')
    Or for per-user language:
      manager.set_user_lang(chat_id, 'om')
      manager.gettext_for_user(chat_id, 'Welcome!')
    """

    def __init__(self, domain="messages", locales_dir=LOCALES_DIR, default_lang="en"):
        self.domain = domain
        self.locales_dir = locales_dir
        self.default_lang = default_lang
        self._cache = {}
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(USER_LANG_FILE):
            with open(USER_LANG_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def get_translator(self, lang_code: str):
        """Return a translation object with gettext() and ngettext().

        Falls back to the default language if translation not available.
        """
        lang_code = (lang_code or "").lower()
        if not lang_code:
            lang_code = self.default_lang
        if lang_code in self._cache:
            return self._cache[lang_code]

        try:
            trans = gettext.translation(self.domain, localedir=self.locales_dir, languages=[lang_code], fallback=True)
        except Exception:
            trans = gettext.translation(self.domain, localedir=self.locales_dir, languages=[self.default_lang], fallback=True)

        self._cache[lang_code] = trans
        return trans

    def gettext(self, lang_code: str, message: str, **kwargs):
        t = self.get_translator(lang_code).gettext
        result = t(message)
        if kwargs:
            try:
                return result.format(**kwargs)
            except Exception:
                return result
        return result

    def ngettext(self, lang_code: str, singular: str, plural: str, n: int, **kwargs):
        t = self.get_translator(lang_code).ngettext
        result = t(singular, plural, n)
        if kwargs:
            try:
                return result.format(**kwargs)
            except Exception:
                return result
        return result

    # --- simple user preference persistence ---
    def _load_user_langs(self):
        with _lock:
            try:
                with open(USER_LANG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}

    def _save_user_langs(self, mapping):
        with _lock:
            with open(USER_LANG_FILE, "w", encoding="utf-8") as f:
                json.dump(mapping, f, ensure_ascii=False, indent=2)

    def set_user_lang(self, chat_id: str, lang_code: str):
        mapping = self._load_user_langs()
        mapping[str(chat_id)] = lang_code
        self._save_user_langs(mapping)

    def get_user_lang(self, chat_id: str):
        mapping = self._load_user_langs()
        return mapping.get(str(chat_id), self.default_lang)

    def gettext_for_user(self, chat_id: str, message: str, **kwargs):
        lang = self.get_user_lang(chat_id)
        return self.gettext(lang, message, **kwargs)


# module-level manager to import and reuse
manager = I18nManager()

def set_user_lang(chat_id, lang_code):
    manager.set_user_lang(chat_id, lang_code)

def get_user_lang(chat_id):
    return manager.get_user_lang(chat_id)

def gettext_for_user(chat_id, message, **kwargs):
    return manager.gettext_for_user(chat_id, message, **kwargs)

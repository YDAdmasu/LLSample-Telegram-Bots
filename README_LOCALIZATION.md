**Localization Structure**

- **`locales/`**: top-level folder containing one directory per language code.
- **`<lang>/LC_MESSAGES/messages.po`**: gettext PO file (source English msgids). Compiler produces `messages.mo`.

Example layout:

```
locales/
  en/LC_MESSAGES/messages.po
  am/LC_MESSAGES/messages.po
  om/LC_MESSAGES/messages.po
```

**Why gettext?**
- Standard tooling for pluralization and translator workflows.
- Works well with Python `gettext` module.

**Files added**
- `i18n.py`: small manager to load translations and persist per-user language preference in `data/user_langs.json`.
- `scripts/compile_translations.py`: compile `.po` → `.mo` using `polib`.
- `requirements.txt`: lists required packages for the tooling.

**Quick start (Windows PowerShell)**

Install requirements and compile translations:

```powershell
python -m pip install -r requirements.txt
python scripts/compile_translations.py
```

**Using in your bot (example)**
- Import `i18n` and use `gettext_for_user(chat_id, "Welcome!")` to get translated strings.
- Use `set_user_lang(chat_id, 'am')` to change a user's language.

See `i18n.py` for functions and `locales/` for example `.po` files.

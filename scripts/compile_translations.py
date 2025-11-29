"""Compile all .po files under `locales/` to .mo files using polib.

Run:
  python -m pip install -r requirements.txt
  python scripts/compile_translations.py

This will write .mo files next to each .po.
"""
import os
import glob
import polib

ROOT = os.path.dirname(os.path.dirname(__file__))
LOCALES = os.path.join(ROOT, "locales")


def compile_all():
    pattern = os.path.join(LOCALES, "*", "LC_MESSAGES", "*.po")
    for po_path in glob.glob(pattern):
        try:
            mo_path = os.path.splitext(po_path)[0] + ".mo"
            po = polib.pofile(po_path)
            po.save_as_mofile(mo_path)
            print(f"Compiled: {po_path} -> {mo_path}")
        except Exception as e:
            print(f"Failed to compile {po_path}: {e}")


if __name__ == "__main__":
    compile_all()

#!/usr/bin/env python3
import os
import unicodedata

ROOT = os.path.abspath(".")
SKIP_DIRS = {".git", ".idea", ".vscode", "__pycache__"}

def to_nfc(name: str) -> str:
    return unicodedata.normalize("NFC", name)

def main():
    # Walk bottom-up so children are renamed before parents
    for dirpath, dirnames, filenames in os.walk(ROOT, topdown=False):
        # Skip special dirs
        rel = os.path.relpath(dirpath, ROOT)
        if any(part in SKIP_DIRS for part in rel.split(os.sep)):
            continue

        # Directories
        for dirname in dirnames:
            if dirname in SKIP_DIRS:
                continue
            old_path = os.path.join(dirpath, dirname)
            new_name = to_nfc(dirname)
            new_path = os.path.join(dirpath, new_name)
            if new_path != old_path:
                if os.path.exists(new_path) and not os.path.samefile(old_path, new_path):
                    print(f"SKIP (collision): {old_path} -> {new_path}")
                else:
                    # If exists but samefile, or doesn't exist, we rename.
                    # On macOS, simple rename might be no-op if FS thinks they are same.
                    # Use temp intermediate to be safe.
                    temp_path = new_path + f".tmp_{os.getpid()}"
                    try:
                        os.rename(old_path, temp_path)
                        os.rename(temp_path, new_path)
                        print(f"REN DIR: {old_path} -> {new_path}")
                    except OSError as e:
                        print(f"ERR: {old_path} -> {new_path}: {e}")

        # Files
        for filename in filenames:
            old_path = os.path.join(dirpath, filename)
            new_name = to_nfc(filename)
            new_path = os.path.join(dirpath, new_name)
            if new_path != old_path:
                if os.path.exists(new_path) and not os.path.samefile(old_path, new_path):
                    print(f"SKIP (collision): {old_path} -> {new_path}")
                else:
                    # Use temp intermediate to force FS to update the directory entry bytes
                    temp_path = new_path + f".tmp_{os.getpid()}"
                    try:
                        os.rename(old_path, temp_path)
                        os.rename(temp_path, new_path)
                        print(f"REN FILE: {old_path} -> {new_path}")
                    except OSError as e:
                        print(f"ERR: {old_path} -> {new_path}: {e}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Print filepaths in a directory and show their Unicode normalization form.
"""
import os
import unicodedata

SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}


def check_normalization(path: str) -> tuple[str, list[str]]:
    """
    Check each path component's normalization form.
    Returns (overall_form, details) where details lists non-ASCII components.
    """
    parts = path.replace("\\", "/").split("/")
    forms = []
    
    for part in parts:
        if not part:
            continue
        is_nfc = unicodedata.is_normalized("NFC", part)
        is_nfd = unicodedata.is_normalized("NFD", part)
        if is_nfc and is_nfd:
            forms.append(("ASCII", part))
        elif is_nfc:
            forms.append(("NFC", part))
        elif is_nfd:
            forms.append(("NFD", part))
        else:
            forms.append(("Mixed", part))
    
    # Determine overall form
    non_ascii = [(f, p) for f, p in forms if f != "ASCII"]
    if not non_ascii:
        return "ASCII", []
    
    unique_forms = set(f for f, _ in non_ascii)
    if len(unique_forms) == 1:
        return unique_forms.pop(), non_ascii
    else:
        return "Mixed", non_ascii


def main():
    directory = input("Enter root path to scan [.]: ").strip() or "."
    
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory")
        return
    
    print(f"\nScanning: {os.path.abspath(directory)}\n")
    print(f"{'Form':<6} | Path")
    print("-" * 80)
    
    for root, dirs, files in os.walk(directory):
        # Skip hidden/unwanted directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for name in dirs + files:
            path = os.path.join(root, name)
            rel_path = os.path.relpath(path, directory)
            form, details = check_normalization(rel_path)
            
            if details:
                detail_str = ", ".join(f"{p}={f}" for f, p in details)
                print(f"{form:<6} | {rel_path}")
                print(f"       |   └─ {detail_str}")
            else:
                print(f"{form:<6} | {rel_path}")


if __name__ == "__main__":
    main()


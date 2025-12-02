#!/usr/bin/env python3
import pathlib
import subprocess
import sys
import unicodedata

def main() -> None:
    repo_str = input("Enter the absolute path to the Git repository root: ").strip()
    if not repo_str:
        sys.exit("Path is required.")
    repo = pathlib.Path(repo_str).resolve()

    try:
        raw = subprocess.check_output(["git", "-C", str(repo), "ls-files", "-z"])
    except subprocess.CalledProcessError as exc:
        sys.exit(f"git ls-files failed: {exc}")

    paths = [p for p in raw.decode("utf-8").split("\0") if p]
    # Rename deepest paths first to avoid clobbering parent folders mid-walk.
    paths.sort(key=lambda p: p.count("/"), reverse=True)

    renamed = False
    seen_targets = set()

    for rel in paths:
        nfc_rel = unicodedata.normalize("NFC", rel)
        if nfc_rel == rel:
            continue

        if nfc_rel in seen_targets or (repo / nfc_rel).exists():
            sys.exit(f"Refusing to rename: {rel} -> {nfc_rel} would collide with an existing path")

        src = repo / rel
        dst = repo / nfc_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)
        print(f"Renamed: {rel} -> {nfc_rel}")
        renamed = True
        seen_targets.add(nfc_rel)

    if not renamed:
        print("All tracked paths already NFC-normalized.")
    else:
        print("Done. Review `git status`, test, then commit the renames.")

if __name__ == "__main__":
    main()
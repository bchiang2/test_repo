"""
Demonstrate that two strings can look identical but differ in Unicode normalization.
"""
import unicodedata

# Same visual text, different byte representations
nfc = "해양수산부"                          # NFC: Composed (1 codepoint per syllable)
nfd = unicodedata.normalize("NFD", nfc)   # NFD: Decomposed (2-3 codepoints per syllable)

print(f'NFC: "{nfc}"')
print(f'NFD: "{nfd}"')
print(f"Look the same? {nfc} == {nfd} visually")
print()
print(f"But: nfc == nfd → {nfc == nfd}")
print(f"     len(nfc)={len(nfc)}, len(nfd)={len(nfd)}")
print(f"     bytes(nfc)={len(nfc.encode())}B, bytes(nfd)={len(nfd.encode())}B")
print()
print("Codepoints:")
print(f"  NFC: {[f'U+{ord(c):04X}' for c in nfc]}")
print(f"  NFD: {[f'U+{ord(c):04X}' for c in nfd]}")
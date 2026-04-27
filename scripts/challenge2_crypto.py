"""Defi 2 - Chiffre de Vigenere.

Genere/verifie le fichier assets/secret.enc.
La cle (VIGENERE_KEY = SOPHIE) est obtenue lors du defi 1.

Usage:
  python challenge2_crypto.py encrypt
  python challenge2_crypto.py decrypt SOPHIE
"""
import sys
from pathlib import Path

from common import FLAG2, VIGENERE_KEY, STEGO_PASSPHRASE

ASSETS = Path(__file__).resolve().parent.parent / "assets"
ENC_PATH = ASSETS / "secret.enc"

PLAINTEXT = (
    f"Bravo, vous avez casse Vigenere. {FLAG2}. "
    f"Prochaine etape: une carte postale numerique (assets/carte_postale.png) "
    f"contient un message cache par steganographie LSB. "
    f"La passphrase pour l'extraire est: {STEGO_PASSPHRASE}."
)


def vigenere(text: str, key: str, encrypt: bool = True) -> str:
    out = []
    key = key.upper()
    j = 0
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            shift = ord(key[j % len(key)]) - ord("A")
            if not encrypt:
                shift = -shift
            out.append(chr((ord(ch) - base + shift) % 26 + base))
            j += 1
        else:
            out.append(ch)
    return "".join(out)


def encrypt_to_file():
    ASSETS.mkdir(exist_ok=True)
    cipher = vigenere(PLAINTEXT, VIGENERE_KEY, encrypt=True)
    ENC_PATH.write_text(cipher, encoding="utf-8")
    print(f"[OK] Ecrit {ENC_PATH} ({len(cipher)} octets)")


def decrypt_from_file(key: str):
    cipher = ENC_PATH.read_text(encoding="utf-8")
    print(vigenere(cipher, key, encrypt=False))


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "encrypt":
        encrypt_to_file()
    elif len(sys.argv) >= 3 and sys.argv[1] == "decrypt":
        decrypt_from_file(sys.argv[2])
    else:
        print(__doc__)

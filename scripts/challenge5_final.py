"""Defi 5 - Tresor chiffre AES-256-GCM.

Le mot de passe AES est donne par le serveur du defi 4. Le tresor
contient le FLAG_FINAL qui valide la reussite de l'escape game.

Usage:
  python challenge5_final.py encrypt
  python challenge5_final.py decrypt <password>
"""
import base64
import json
import sys
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from common import FLAG_FINAL, AES_PASSWORD

ASSETS = Path(__file__).resolve().parent.parent / "assets"
TREASURE = ASSETS / "tresor.aes"

PLAINTEXT = (
    f"=========================================\n"
    f"  TRESOR FINAL - Escape Game Cyber PFE\n"
    f"=========================================\n\n"
    f"Felicitations ! Vous avez traverse les 5 defis :\n"
    f"  1. Injection SQL\n"
    f"  2. Chiffre de Vigenere\n"
    f"  3. Steganographie LSB\n"
    f"  4. Service reseau authentifie\n"
    f"  5. Dechiffrement AES-256-GCM\n\n"
    f"FLAG FINAL: {FLAG_FINAL}\n"
)


def _derive(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)
    return kdf.derive(password.encode())


def encrypt(password: str = AES_PASSWORD):
    ASSETS.mkdir(exist_ok=True)
    salt = b"PFE-L3B-G3-2026!"
    nonce = b"\x00" * 12
    key = _derive(password, salt)
    ct = AESGCM(key).encrypt(nonce, PLAINTEXT.encode(), None)
    blob = {
        "alg": "AES-256-GCM",
        "kdf": "scrypt(n=16384,r=8,p=1)",
        "salt_b64": base64.b64encode(salt).decode(),
        "nonce_b64": base64.b64encode(nonce).decode(),
        "ciphertext_b64": base64.b64encode(ct).decode(),
    }
    TREASURE.write_text(json.dumps(blob, indent=2), encoding="utf-8")
    print(f"[OK] Tresor chiffre ecrit: {TREASURE}")


def decrypt(password: str):
    blob = json.loads(TREASURE.read_text(encoding="utf-8"))
    salt = base64.b64decode(blob["salt_b64"])
    nonce = base64.b64decode(blob["nonce_b64"])
    ct = base64.b64decode(blob["ciphertext_b64"])
    key = _derive(password, salt)
    pt = AESGCM(key).decrypt(nonce, ct, None)
    print(pt.decode())


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "encrypt":
        encrypt()
    elif len(sys.argv) >= 3 and sys.argv[1] == "decrypt":
        decrypt(sys.argv[2])
    else:
        print(__doc__)

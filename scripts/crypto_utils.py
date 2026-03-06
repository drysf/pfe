# -*- coding: utf-8 -*-
"""
Utilitaires cryptographie - Défi 3
Génère flag.enc avec OpenSSL (AES-256-CBC)
"""
import subprocess
import os

PLAINTEXT_FLAG = "CTF{DEFI3_CRYPTO_CAESAR}"
OUTPUT_FILE = "flag.enc"
# Clé de chiffrement volontairement faible (défi pédagogique)
PASSWORD = "escape123"

def generate_encrypted_flag():
    """Chiffre le flag avec OpenSSL AES-256-CBC."""
    cmd = [
        "openssl", "enc", "-aes-256-cbc",
        "-pbkdf2",
        "-in", "/dev/stdin",
        "-out", OUTPUT_FILE,
        "-pass", f"pass:{PASSWORD}"
    ]
    result = subprocess.run(cmd, input=PLAINTEXT_FLAG.encode(), capture_output=True)
    if result.returncode == 0:
        print(f"[+] {OUTPUT_FILE} généré avec succès.")
        print(f"[*] Commande de déchiffrement pour les joueurs :")
        print(f"    openssl enc -d -aes-256-cbc -pbkdf2 -in {OUTPUT_FILE} -pass pass:???")
    else:
        print(f"[-] Erreur : {result.stderr.decode()}")

if __name__ == '__main__':
    generate_encrypted_flag()

"""Constantes partagees entre les defis de l'escape game.

Chaque defi expose un FLAG et un indice (HINT) qui mene au defi suivant.
Le scenario: Sophie Dupont (s.dupont@mega-corp.local) a ete compromise,
l'equipe doit reconstituer la chaine d'attaque pour atteindre le tresor.
"""

FLAG1 = "FLAG{M41L_P1R4T3_SQL1}"
FLAG2 = "FLAG{C35AR_3T_V1G3N3R3_S0NT_M0RTS}"
FLAG3 = "FLAG{P1X3LS_QU1_PARL3NT}"
FLAG4 = "FLAG{S0CK3T_M4ST3R_2026}"
FLAG_FINAL = "FLAG{ESC4P3_G4M3_PFE_L3B_G3_W1N}"

VIGENERE_KEY = "SOPHIE"

STEGO_PASSPHRASE = "pixels2026"

SOCKET_HOST = "127.0.0.1"
SOCKET_PORT = 4242
SOCKET_TOKEN = "TOKEN-LSB-OK"

AES_PASSWORD = "k1ng_0f_th3_h1ll"

CHAIN = [
    ("1 - Web / SQL Injection", "http://127.0.0.1:5000/mail"),
    ("2 - Cryptographie Vigenere", "assets/secret.enc"),
    ("3 - Steganographie LSB", "assets/carte_postale.png"),
    ("4 - Socket reseau", f"nc {SOCKET_HOST} {SOCKET_PORT}"),
    ("5 - Tresor chiffre AES", "assets/tresor.aes"),
]

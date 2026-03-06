# -*- coding: utf-8 -*-
"""
Défi 5 - Serveur réseau (nc localhost 1337)
PFE L3B Groupe 3 — Younes Beouch
"""
import socket
import threading

FLAG = "CTF{DEFI5_NETWORK_RECON}"
SECRET_PORT = 1337
BANNER = b"""
=== Escape Game Cyber - Defi 5 ===
Bienvenue sur le serveur reseau.
Trouvez le bon mot de passe pour obtenir le flag.
Mot de passe : """

def handle_client(conn, addr):
    try:
        conn.sendall(BANNER)
        data = conn.recv(1024).decode('utf-8', errors='ignore').strip()
        if data == "letmein":
            conn.sendall(f"\n✅ FLAG : {FLAG}\n".encode())
        else:
            conn.sendall(b"\n❌ Mauvais mot de passe.\n")
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', SECRET_PORT))
        s.listen(5)
        print(f"[*] Serveur réseau défi 5 en écoute sur le port {SECRET_PORT}")
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.daemon = True
            t.start()

if __name__ == '__main__':
    start_server()

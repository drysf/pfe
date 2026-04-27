"""Defi 4 - Service TCP avec authentification.

Le serveur ecoute sur SOCKET_HOST:SOCKET_PORT. Il attend une commande
'AUTH <token>' (token recupere via la steganographie au defi 3) et
renvoie le FLAG4 ainsi que la cle AES du defi final.

Usage:
  python challenge4_socket.py serve
  python challenge4_socket.py client AUTH TOKEN-LSB-OK
"""
import socket
import socketserver
import sys
import threading

from common import (
    FLAG4,
    SOCKET_HOST,
    SOCKET_PORT,
    SOCKET_TOKEN,
    AES_PASSWORD,
)

BANNER = (
    "+--------------------------------------------------+\n"
    "|  MegaCorp - Backdoor Service v0.3 (PROD)         |\n"
    "|  Commandes: HELP | AUTH <token> | QUIT           |\n"
    "+--------------------------------------------------+\n"
)


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write(BANNER.encode())
        self.wfile.write(b"> ")
        for raw in self.rfile:
            line = raw.decode(errors="replace").strip()
            if not line:
                self.wfile.write(b"> ")
                continue
            if line.upper() == "QUIT":
                self.wfile.write(b"bye.\n")
                return
            if line.upper() == "HELP":
                self.wfile.write(
                    b"commandes: AUTH <token>, QUIT.\n"
                    b"indice: le token a ete cache dans une carte postale.\n> "
                )
                continue
            if line.upper().startswith("AUTH "):
                token = line.split(" ", 1)[1].strip()
                if token == SOCKET_TOKEN:
                    msg = (
                        f"\n[+] Authentification reussie.\n"
                        f"[+] {FLAG4}\n"
                        f"[+] Mot de passe AES pour le tresor final: {AES_PASSWORD}\n"
                        f"[+] Le tresor est dans assets/tresor.aes (defi 5).\n"
                        f"[+] Outil: python challenge5_final.py decrypt {AES_PASSWORD}\n"
                    )
                    self.wfile.write(msg.encode())
                    return
                self.wfile.write(b"[-] Token invalide.\n> ")
                continue
            self.wfile.write(b"[-] Commande inconnue (HELP).\n> ")


class ReusableServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


def serve(host: str = SOCKET_HOST, port: int = SOCKET_PORT):
    with ReusableServer((host, port), Handler) as srv:
        print(f"[OK] Serveur en ecoute sur {host}:{port}")
        srv.serve_forever()


def serve_in_thread():
    srv = ReusableServer((SOCKET_HOST, SOCKET_PORT), Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv


def client(command: str) -> str:
    with socket.create_connection((SOCKET_HOST, SOCKET_PORT), timeout=5) as s:
        s.sendall((command + "\n").encode())
        chunks = []
        s.settimeout(2)
        try:
            while True:
                data = s.recv(4096)
                if not data:
                    break
                chunks.append(data)
        except socket.timeout:
            pass
        return b"".join(chunks).decode(errors="replace")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "serve":
        serve()
    elif len(sys.argv) >= 2 and sys.argv[1] == "client":
        cmd = " ".join(sys.argv[2:]) or "HELP"
        print(client(cmd))
    else:
        print(__doc__)

"""Lance simultanement le serveur web (defi 1) et le serveur TCP (defi 4).

Usage:  python orchestrator.py
"""
import threading
import time

import app as escape_app
import challenge4_socket


def run_web():
    escape_app.app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


def main():
    t_web = threading.Thread(target=run_web, daemon=True)
    t_web.start()
    challenge4_socket.serve_in_thread()
    print("[OK] Web   : http://127.0.0.1:5000/mail")
    print("[OK] Socket: nc 127.0.0.1 4242")
    print("Ctrl+C pour quitter.")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\nArret.")


if __name__ == "__main__":
    main()

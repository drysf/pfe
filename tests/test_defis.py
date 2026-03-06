# -*- coding: utf-8 -*-
"""
Tests d'intégration - Escape Game Cyber
PFE L3B Groupe 3 — Ryan Hassani
"""
import unittest
import requests
import socket
import subprocess
import sys
import os

BASE_URL = "http://localhost:5000"


class TestDefi1Login(unittest.TestCase):
    """Tests Défi 1 — Authentification mot de passe faible"""

    def test_page_accessible(self):
        r = requests.get(f"{BASE_URL}/login", timeout=5)
        self.assertEqual(r.status_code, 200)

    def test_mauvais_mdp(self):
        r = requests.post(f"{BASE_URL}/login",
                          data={"username": "admin", "password": "wrong"},
                          timeout=5)
        self.assertIn("Mauvais", r.text)

    def test_bon_mdp(self):
        r = requests.post(f"{BASE_URL}/login",
                          data={"username": "admin", "password": "password123"},
                          timeout=5)
        self.assertIn("CTF{DEFI1", r.text)


class TestDefi2SQLi(unittest.TestCase):
    """Tests Défi 2 — Injection SQL"""

    def test_recherche_normale(self):
        r = requests.post(f"{BASE_URL}/search",
                          data={"term": "bob"}, timeout=5)
        self.assertEqual(r.status_code, 200)

    def test_injection_sql(self):
        r = requests.post(f"{BASE_URL}/search",
                          data={"term": "' OR 1=1 --"},
                          timeout=5)
        self.assertIn("CTF{DEFI2", r.text)


class TestDefi5Reseau(unittest.TestCase):
    """Tests Défi 5 — Serveur réseau"""

    def test_connexion_port_1337(self):
        try:
            s = socket.create_connection(("localhost", 1337), timeout=5)
            banner = s.recv(1024).decode('utf-8', errors='ignore')
            self.assertIn("Escape Game", banner)
            s.close()
        except ConnectionRefusedError:
            self.skipTest("Serveur réseau non démarré (normal hors VM)")

    def test_bon_mot_de_passe_reseau(self):
        try:
            s = socket.create_connection(("localhost", 1337), timeout=5)
            s.recv(1024)  # banner
            s.sendall(b"letmein\n")
            response = s.recv(1024).decode('utf-8', errors='ignore')
            self.assertIn("CTF{DEFI5", response)
            s.close()
        except ConnectionRefusedError:
            self.skipTest("Serveur réseau non démarré (normal hors VM)")


if __name__ == '__main__':
    print("=== Tests Escape Game Cyber - Ryan Hassani ===")
    unittest.main(verbosity=2)

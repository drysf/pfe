"""Tests d'integration pour les 5 defis de l'escape game.

Lance: pytest -v depuis la racine du projet.
"""
import time
from pathlib import Path

import pytest

import challenge1_web
import challenge2_crypto
import challenge3_stego
import challenge4_socket
import challenge5_final
from common import (
    AES_PASSWORD,
    FLAG1,
    FLAG2,
    FLAG3,
    FLAG4,
    FLAG_FINAL,
    SOCKET_TOKEN,
    STEGO_PASSPHRASE,
    VIGENERE_KEY,
)

ASSETS = Path(__file__).resolve().parent.parent / "assets"


@pytest.fixture(scope="session", autouse=True)
def assets_ready():
    challenge2_crypto.encrypt_to_file()
    challenge3_stego.generate()
    challenge5_final.encrypt()
    yield


# --- Defi 1 : SQLi -----------------------------------------------------------

@pytest.fixture
def web_client():
    challenge1_web.app.config["TESTING"] = True
    return challenge1_web.app.test_client()


def test_mail_page_contient_indice(web_client):
    r = web_client.get("/mail")
    assert r.status_code == 200
    assert b"s.dupont" in r.data


def test_login_legitime_donne_flag1(web_client):
    r = web_client.post("/", data={"username": "s.dupont", "password": "mdp_super_complexe_inconnu"})
    assert FLAG1.encode() in r.data


def test_sqli_donne_flag1(web_client):
    # Payload classique : commenter le test du mot de passe.
    r = web_client.post("/", data={"username": "' OR '1'='1' --", "password": "x"})
    assert FLAG1.encode() in r.data


def test_login_invalide_refuse(web_client):
    r = web_client.post("/", data={"username": "alice", "password": "bob"})
    assert FLAG1.encode() not in r.data


# --- Defi 2 : Vigenere -------------------------------------------------------

def test_vigenere_roundtrip():
    msg = "Hello, MegaCorp 2026!"
    cipher = challenge2_crypto.vigenere(msg, VIGENERE_KEY, encrypt=True)
    assert cipher != msg
    assert challenge2_crypto.vigenere(cipher, VIGENERE_KEY, encrypt=False) == msg


def test_secret_enc_dechiffre_donne_flag2():
    cipher = (ASSETS / "secret.enc").read_text(encoding="utf-8")
    plain = challenge2_crypto.vigenere(cipher, VIGENERE_KEY, encrypt=False)
    assert FLAG2 in plain
    assert STEGO_PASSPHRASE in plain


# --- Defi 3 : Steganographie LSB --------------------------------------------

def test_extraction_stego_donne_flag3():
    msg = challenge3_stego.extract(ASSETS / "carte_postale.png")
    assert FLAG3 in msg
    assert SOCKET_TOKEN in msg


# --- Defi 4 : Socket TCP -----------------------------------------------------

@pytest.fixture(scope="module")
def tcp_server():
    srv = challenge4_socket.serve_in_thread()
    time.sleep(0.2)
    yield srv
    srv.shutdown()
    srv.server_close()


def test_help_repond(tcp_server):
    out = challenge4_socket.client("HELP")
    assert "AUTH" in out


def test_token_invalide(tcp_server):
    out = challenge4_socket.client("AUTH wrongtoken")
    assert "invalide" in out.lower()


def test_token_valide_donne_flag4_et_password(tcp_server):
    out = challenge4_socket.client(f"AUTH {SOCKET_TOKEN}")
    assert FLAG4 in out
    assert AES_PASSWORD in out


# --- Defi 5 : AES-256-GCM ----------------------------------------------------

def test_dechiffrement_aes_donne_flag_final(capsys):
    challenge5_final.decrypt(AES_PASSWORD)
    out = capsys.readouterr().out
    assert FLAG_FINAL in out


def test_mauvais_password_echoue():
    with pytest.raises(Exception):
        challenge5_final.decrypt("mauvais_password")


# --- Chaine complete ---------------------------------------------------------

def test_chaine_complete_de_bout_en_bout(web_client, tcp_server, capsys):
    # 1. SQLi
    r = web_client.post("/", data={"username": "' OR '1'='1' --", "password": "x"})
    assert FLAG1.encode() in r.data and VIGENERE_KEY.encode() in r.data
    # 2. Vigenere
    plain = challenge2_crypto.vigenere(
        (ASSETS / "secret.enc").read_text(encoding="utf-8"),
        VIGENERE_KEY,
        encrypt=False,
    )
    assert FLAG2 in plain
    # 3. Stego
    msg = challenge3_stego.extract(ASSETS / "carte_postale.png")
    assert FLAG3 in msg and SOCKET_TOKEN in msg
    # 4. Socket
    out = challenge4_socket.client(f"AUTH {SOCKET_TOKEN}")
    assert FLAG4 in out and AES_PASSWORD in out
    # 5. AES
    challenge5_final.decrypt(AES_PASSWORD)
    captured = capsys.readouterr().out
    assert FLAG_FINAL in captured

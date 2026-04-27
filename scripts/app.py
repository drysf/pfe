"""Application web unifiee de l'escape game (5 chambres).

Chaque defi est une 'chambre'. Une fois resolue, un bouton
'Passer a la chambre suivante' apparait.

Demarrer:  python app.py
Acces:     http://127.0.0.1:5000/
"""
import sqlite3
from pathlib import Path

from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string

import challenge2_crypto
import challenge3_stego
import challenge5_final
from common import (
    AES_PASSWORD,
    FLAG1, FLAG2, FLAG3, FLAG4, FLAG_FINAL,
    SOCKET_TOKEN, STEGO_PASSPHRASE, VIGENERE_KEY,
)

ASSETS = Path(__file__).resolve().parent.parent / "assets"

app = Flask(__name__)


# --- Layout commun ----------------------------------------------------------

LAYOUT = """
<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<title>Escape Game Cyber - {{ title }}</title>
<style>
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', Arial, sans-serif; background:#0f172a;
       color:#e2e8f0; margin:0; min-height:100vh; }
header { background:#020617; padding:18px 32px; border-bottom:1px solid #1e293b;
         display:flex; align-items:center; justify-content:space-between; }
header h1 { margin:0; color:#38bdf8; font-size:18px; letter-spacing:1px; }
.progress { display:flex; gap:6px; }
.dot { width:30px; height:6px; border-radius:3px; background:#1e293b; }
.dot.done { background:#10b981; }
.dot.current { background:#38bdf8; box-shadow:0 0 12px #38bdf8; }
main { max-width:760px; margin:40px auto; padding:0 24px; }
.card { background:#1e293b; border:1px solid #334155; border-radius:14px;
        padding:32px; box-shadow:0 14px 40px rgba(0,0,0,.5); }
h2 { margin-top:0; color:#38bdf8; }
h3 { color:#a5f3fc; margin-top:28px; }
label { display:block; margin:14px 0 6px; color:#94a3b8; font-size:14px; }
input, textarea { width:100%; padding:12px; border-radius:8px;
        border:1px solid #475569; background:#0f172a; color:#e2e8f0;
        font-family:inherit; font-size:15px; }
textarea { font-family: 'JetBrains Mono', 'Courier New', monospace; min-height:140px; }
button, .btn { background:#38bdf8; color:#0f172a; padding:12px 22px;
         border:0; border-radius:8px; font-weight:700; cursor:pointer;
         font-size:15px; text-decoration:none; display:inline-block; margin-top:14px; }
button:hover, .btn:hover { background:#7dd3fc; }
.btn-next { background:#10b981; color:#022c22; padding:14px 28px; font-size:16px; }
.btn-next:hover { background:#34d399; }
.flag { background:#022c22; border:1px dashed #10b981; padding:14px 18px;
        border-radius:8px; font-family:monospace; color:#34d399;
        font-size:16px; margin:18px 0; }
.error { color:#f87171; padding:10px 14px; background:#450a0a;
         border-radius:8px; margin:12px 0; }
.hint { color:#94a3b8; font-style:italic; font-size:14px;
        background:#0f172a; padding:12px 14px; border-left:3px solid #38bdf8;
        border-radius:4px; margin:14px 0; }
.code { font-family: monospace; background:#0f172a; padding:2px 8px;
        border-radius:4px; color:#a5f3fc; }
pre { background:#0f172a; padding:14px; border-radius:8px; overflow-x:auto;
      color:#cbd5e1; }
img { max-width:100%; border-radius:8px; margin:14px 0;
      border:2px solid #334155; }
.terminal { background:#000; color:#10b981; padding:18px;
            border-radius:8px; font-family:monospace; min-height:160px;
            white-space:pre-wrap; font-size:14px; }
a { color:#38bdf8; }
footer { text-align:center; color:#475569; padding:30px; font-size:13px; }
</style></head>
<body>
<header>
  <h1>ESCAPE GAME CYBER - PFE L3B G3</h1>
  <div class="progress">
    {% for i in range(1, 6) %}
      <div class="dot {% if i < room %}done{% elif i == room %}current{% endif %}"></div>
    {% endfor %}
  </div>
</header>
<main>{{ body|safe }}</main>
<footer>Chambre {{ room }} / 5</footer>
</body></html>
"""


def page(title, room, body):
    return render_template_string(LAYOUT, title=title, room=room, body=body)


def next_button(next_room: int, label: str = "Passer a la chambre suivante"):
    return (
        f'<a class="btn btn-next" href="/room{next_room}">{label} -&gt;</a>'
    )


# --- Accueil ----------------------------------------------------------------

@app.route("/")
def home():
    body = """
    <div class="card">
      <h2>Bienvenue agent.</h2>
      <p>Sophie Dupont, employee de MegaCorp, vient d'etre piratee.
         Cinq epreuves t'attendent. Chaque chambre debloque la suivante.</p>
      <p>Domaines couverts : <b>Web, Cryptographie, Steganographie,
         Reseau, Crypto symetrique</b>.</p>
      <a class="btn btn-next" href="/room1">Entrer dans la chambre 1 -&gt;</a>
    </div>
    """
    return page("Accueil", 0, body)


# --- Chambre 1 : SQL Injection ---------------------------------------------

def init_db():
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("CREATE TABLE users (username TEXT, password TEXT)")
    c.execute("INSERT INTO users VALUES ('s.dupont', 'mdp_super_complexe_inconnu')")
    return conn


@app.route("/room1", methods=["GET", "POST"])
def room1():
    message = ""
    success = False
    if request.method == "POST":
        u = request.form.get("username", "")
        p = request.form.get("password", "")
        try:
            c = init_db().cursor()
            c.execute(f"SELECT * FROM users WHERE username = '{u}' AND password = '{p}'")
            if c.fetchone():
                success = True
            else:
                message = "Identifiants incorrects."
        except sqlite3.Error as e:
            message = f"Erreur SQL : {e}"

    if success:
        body = f"""
        <div class="card">
          <h2>Chambre 1 - Reussie</h2>
          <p>Bravo, tu as exploite l'injection SQL.</p>
          <div class="flag">{FLAG1}</div>
          <h3>Indice pour la chambre 2</h3>
          <p>Un fichier <span class="code">assets/secret.enc</span> a ete
             chiffre avec <b>Vigenere</b>. La cle est le prenom de la victime
             en MAJUSCULES : <span class="code">{VIGENERE_KEY}</span>.</p>
          {next_button(2)}
        </div>
        """
        return page("Chambre 1", 1, body)

    body = f"""
    <div class="card">
      <h2>Chambre 1 - Boite mail interceptee</h2>
      <div class="hint">
        <b>De :</b> it-support@mega-corp.local<br>
        <b>A  :</b> s.dupont@mega-corp.local<br>
        Ton compte admin est reactive. Identifiant : <b>s.dupont</b>.
        Le mot de passe te sera donne de vive voix.
      </div>
      <p>Connecte-toi au portail. Astuce : le code source de cette page
         contient la requete SQL utilisee.</p>
      <!-- DEBUG: SELECT * FROM users WHERE username='?' AND password='?' -->
      {f'<div class="error">{message}</div>' if message else ''}
      <form method="POST">
        <label>Utilisateur</label>
        <input type="text" name="username" autocomplete="off">
        <label>Mot de passe</label>
        <input type="password" name="password">
        <button type="submit">Se connecter</button>
      </form>
    </div>
    """
    return page("Chambre 1", 1, body)


# --- Chambre 2 : Vigenere ---------------------------------------------------

@app.route("/room2", methods=["GET", "POST"])
def room2():
    cipher = (ASSETS / "secret.enc").read_text(encoding="utf-8")
    message = ""
    plaintext = ""
    success = False
    if request.method == "POST":
        key = request.form.get("key", "").strip().upper()
        if not key:
            message = "Donne la cle Vigenere."
        else:
            plaintext = challenge2_crypto.vigenere(cipher, key, encrypt=False)
            if FLAG2 in plaintext:
                success = True
            else:
                message = "Mauvaise cle, le texte reste illisible."

    if success:
        body = f"""
        <div class="card">
          <h2>Chambre 2 - Reussie</h2>
          <div class="flag">{FLAG2}</div>
          <h3>Texte dechiffre</h3>
          <pre>{plaintext}</pre>
          <h3>Indice pour la chambre 3</h3>
          <p>Une carte postale t'attend. Passphrase :
             <span class="code">{STEGO_PASSPHRASE}</span></p>
          {next_button(3)}
        </div>
        """
        return page("Chambre 2", 2, body)

    body = f"""
    <div class="card">
      <h2>Chambre 2 - Cryptographie Vigenere</h2>
      <p>Voici le contenu de <span class="code">assets/secret.enc</span> :</p>
      <pre>{cipher}</pre>
      <div class="hint">Le chiffre de Vigenere decale chaque lettre selon
         une cle repetee. La cle a ete revelee a la chambre precedente.</div>
      {f'<div class="error">{message}</div>' if message else ''}
      <form method="POST">
        <label>Cle Vigenere</label>
        <input type="text" name="key" placeholder="MAJUSCULES" autocomplete="off">
        <button type="submit">Dechiffrer</button>
      </form>
      {f'<h3>Tentative</h3><pre>{plaintext}</pre>' if plaintext else ''}
    </div>
    """
    return page("Chambre 2", 2, body)


# --- Chambre 3 : Steganographie LSB ----------------------------------------

@app.route("/assets/<path:fname>")
def assets_static(fname):
    return send_from_directory(ASSETS, fname)


@app.route("/room3", methods=["GET", "POST"])
def room3():
    message = ""
    success = False
    extracted = ""
    if request.method == "POST":
        action = request.form.get("action", "")
        if action == "extract":
            extracted = challenge3_stego.extract(ASSETS / "carte_postale.png")
            if SOCKET_TOKEN in extracted:
                success = True
        else:
            answer = request.form.get("token", "").strip()
            if answer == SOCKET_TOKEN:
                success = True
                extracted = challenge3_stego.extract(ASSETS / "carte_postale.png")
            else:
                message = "Token incorrect."

    if success:
        body = f"""
        <div class="card">
          <h2>Chambre 3 - Reussie</h2>
          <div class="flag">{FLAG3}</div>
          <h3>Message cache extrait</h3>
          <pre>{extracted}</pre>
          <h3>Indice pour la chambre 4</h3>
          <p>Un service reseau ecoute. Token a envoyer :
             <span class="code">{SOCKET_TOKEN}</span></p>
          {next_button(4)}
        </div>
        """
        return page("Chambre 3", 3, body)

    body = f"""
    <div class="card">
      <h2>Chambre 3 - Steganographie LSB</h2>
      <p>Sophie t'a envoye une carte postale. Elle parait innocente,
         mais ses pixels cachent un message (technique LSB - Least
         Significant Bit sur les canaux RGB).</p>
      <img src="/assets/carte_postale.png" alt="carte postale">
      <div class="hint">Outils possibles : un script LSB Python, ou
         <span class="code">.venv/bin/python scripts/challenge3_stego.py
         extract assets/carte_postale.png</span></div>
      {f'<div class="error">{message}</div>' if message else ''}
      <form method="POST">
        <input type="hidden" name="action" value="extract">
        <button type="submit">Extraire le message (auto)</button>
      </form>
      <form method="POST" style="margin-top:20px">
        <label>Ou colle ici le token trouve dans le message</label>
        <input type="text" name="token" autocomplete="off">
        <button type="submit">Valider</button>
      </form>
    </div>
    """
    return page("Chambre 3", 3, body)


# --- Chambre 4 : Service reseau (terminal simule) --------------------------

@app.route("/room4", methods=["GET", "POST"])
def room4():
    transcript = (
        "+--------------------------------------------------+\n"
        "|  MegaCorp - Backdoor Service v0.3 (PROD)         |\n"
        "|  Commandes: HELP | AUTH <token> | QUIT           |\n"
        "+--------------------------------------------------+\n"
        "> "
    )
    success = False
    cmd = ""
    if request.method == "POST":
        cmd = request.form.get("cmd", "").strip()
        transcript += cmd + "\n"
        up = cmd.upper()
        if up == "HELP":
            transcript += "commandes: AUTH <token>, QUIT.\n> "
        elif up == "QUIT":
            transcript += "bye.\n"
        elif up.startswith("AUTH "):
            token = cmd.split(" ", 1)[1].strip()
            if token == SOCKET_TOKEN:
                transcript += (
                    f"\n[+] Authentification reussie.\n"
                    f"[+] {FLAG4}\n"
                    f"[+] Mot de passe AES : {AES_PASSWORD}\n"
                )
                success = True
            else:
                transcript += "[-] Token invalide.\n> "
        else:
            transcript += "[-] Commande inconnue (HELP).\n> "

    body = f"""
    <div class="card">
      <h2>Chambre 4 - Service reseau TCP</h2>
      <p>Un serveur ecoute sur <span class="code">127.0.0.1:4242</span>.
         Tu peux y acceder via netcat (<span class="code">nc 127.0.0.1
         4242</span>) ou directement ici dans le terminal simule.</p>
      <div class="hint">Astuce : tape <span class="code">HELP</span>
         puis <span class="code">AUTH &lt;token&gt;</span> avec le token
         trouve dans la carte postale.</div>
      <div class="terminal">{transcript}</div>
      <form method="POST" style="margin-top:14px">
        <label>Commande</label>
        <input type="text" name="cmd" autocomplete="off"
               placeholder="HELP ou AUTH <token>" autofocus>
        <button type="submit">Envoyer</button>
      </form>
      {next_button(5) if success else ''}
    </div>
    """
    return page("Chambre 4", 4, body)


# --- Chambre 5 : AES-256-GCM -----------------------------------------------

@app.route("/room5", methods=["GET", "POST"])
def room5():
    message = ""
    success = False
    plaintext = ""
    if request.method == "POST":
        pwd = request.form.get("password", "").strip()
        try:
            import base64, json
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            blob = json.loads((ASSETS / "tresor.aes").read_text(encoding="utf-8"))
            salt = base64.b64decode(blob["salt_b64"])
            nonce = base64.b64decode(blob["nonce_b64"])
            ct = base64.b64decode(blob["ciphertext_b64"])
            key = challenge5_final._derive(pwd, salt)
            plaintext = AESGCM(key).decrypt(nonce, ct, None).decode()
            success = FLAG_FINAL in plaintext
        except Exception:
            message = "Mauvais mot de passe (l'authentification AES-GCM a echoue)."

    if success:
        body = f"""
        <div class="card">
          <h2>Chambre 5 - TRESOR DECOUVERT</h2>
          <div class="flag">{FLAG_FINAL}</div>
          <pre>{plaintext}</pre>
          <a class="btn btn-next" href="/win">Voir l'ecran de victoire -&gt;</a>
        </div>
        """
        return page("Chambre 5", 5, body)

    body = f"""
    <div class="card">
      <h2>Chambre 5 - Tresor chiffre AES-256-GCM</h2>
      <p>Le fichier <span class="code">assets/tresor.aes</span> est protege
         par AES-256-GCM avec une cle derivee par scrypt.</p>
      <div class="hint">Le mot de passe a ete revele a la chambre 4.</div>
      {f'<div class="error">{message}</div>' if message else ''}
      <form method="POST">
        <label>Mot de passe AES</label>
        <input type="password" name="password" autocomplete="off">
        <button type="submit">Dechiffrer le tresor</button>
      </form>
    </div>
    """
    return page("Chambre 5", 5, body)


@app.route("/win")
def win():
    body = f"""
    <div class="card" style="text-align:center">
      <h2 style="font-size:32px">VICTOIRE !</h2>
      <p>Tu as resolu les 5 chambres de l'Escape Game Cyber.</p>
      <div class="flag" style="font-size:18px">{FLAG_FINAL}</div>
      <h3>Tes 5 flags</h3>
      <pre>{FLAG1}
{FLAG2}
{FLAG3}
{FLAG4}
{FLAG_FINAL}</pre>
      <a class="btn" href="/">Recommencer</a>
    </div>
    """
    return page("Victoire", 5, body)


if __name__ == "__main__":
    # Genere les artefacts s'ils n'existent pas.
    if not (ASSETS / "secret.enc").exists():
        challenge2_crypto.encrypt_to_file()
    if not (ASSETS / "carte_postale.png").exists():
        challenge3_stego.generate()
    if not (ASSETS / "tresor.aes").exists():
        challenge5_final.encrypt()
    print("[OK] Escape Game pret : http://127.0.0.1:5000/")
    app.run(host="0.0.0.0", port=5000, debug=False)

"""Defi 1 - Faux portail mail + portail admin vulnerable a l'injection SQL.

Demarrer:  python challenge1_web.py
Acces:     http://127.0.0.1:5000/mail

Solution attendue: payload SQLi  ' OR '1'='1  dans le champ utilisateur.
La page de succes contient FLAG1 et l'indice menant au defi 2.
"""
from flask import Flask, request, render_template_string
import sqlite3

from common import FLAG1, VIGENERE_KEY

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("CREATE TABLE users (username TEXT, password TEXT, note TEXT)")
    c.execute(
        "INSERT INTO users VALUES ('s.dupont', 'mdp_super_complexe_inconnu', 'compte legitime')"
    )
    c.execute(
        "INSERT INTO users VALUES ('attaquant', 'p4ssword!', 'porte derobee laissee par l intrus')"
    )
    return conn


BASE_CSS = """
<style>
body { font-family: 'Segoe UI', Arial, sans-serif; background:#0f172a; color:#e2e8f0; margin:0; padding:40px; }
.card { max-width:640px; margin:auto; background:#1e293b; border:1px solid #334155;
        border-radius:12px; padding:32px; box-shadow:0 10px 30px rgba(0,0,0,.4); }
h1,h2 { color:#38bdf8; margin-top:0; }
input { width:100%; padding:10px; margin:6px 0 16px; border-radius:6px;
        border:1px solid #475569; background:#0f172a; color:#e2e8f0; box-sizing:border-box; }
button { background:#38bdf8; color:#0f172a; padding:10px 20px; border:0;
         border-radius:6px; font-weight:600; cursor:pointer; }
.flag { background:#022c22; border:1px dashed #10b981; padding:14px; border-radius:8px;
        font-family:monospace; color:#34d399; }
.error { color:#f87171; }
a { color:#38bdf8; }
hr { border:0; border-top:1px solid #334155; }
</style>
"""


@app.route("/mail")
def mail():
    return BASE_CSS + """
    <div class="card">
      <h2>MailBox - Message intercepte</h2>
      <p><b>De :</b> it-support@mega-corp.local<br>
         <b>A  :</b> s.dupont@mega-corp.local<br>
         <b>Objet :</b> Reactivation acces administrateur</p>
      <hr>
      <p>Bonjour Sophie,</p>
      <p>Ton compte sur le portail d'administration vient d'etre reactive.
         Identifiant: <b>s.dupont</b>. Le mot de passe te sera communique
         de vive voix.</p>
      <p>L'equipe IT.</p>
      <hr>
      <p><i>(Indice cache dans le code source de cette page...)</i></p>
      <!-- DEBUG: requete brute => SELECT * FROM users WHERE username='?' AND password='?' -->
      <a href="/">Aller au portail d'administration -&gt;</a>
    </div>
    """


@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        conn = init_db()
        c = conn.cursor()
        # Vulnerabilite volontaire: concatenation directe dans la requete.
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        try:
            c.execute(query)
            user = c.fetchone()
            if user:
                return BASE_CSS + f"""
                <div class="card">
                  <h1>Acces autorise</h1>
                  <p>Bienvenue dans la console d'administration.</p>
                  <p class="flag">{FLAG1}</p>
                  <hr>
                  <h2>Indice pour le defi 2</h2>
                  <p>Un fichier <code>assets/secret.enc</code> a ete laisse sur
                     le serveur. Il a ete chiffre avec un <b>chiffre de Vigenere</b>.
                     La cle est le <b>prenom</b> de la victime, en MAJUSCULES.</p>
                  <p>(verification: cle = <code>{VIGENERE_KEY}</code>)</p>
                </div>
                """
            message = "Identifiants incorrects."
        except sqlite3.Error as e:
            message = f"Erreur SQL : {e}"

    return BASE_CSS + render_template_string("""
    <div class="card">
      <h2>Portail d'Administration - MegaCorp</h2>
      <p class="error">{{ message }}</p>
      <form method="POST">
        <label>Utilisateur</label>
        <input type="text" name="username" autocomplete="off">
        <label>Mot de passe</label>
        <input type="password" name="password">
        <button type="submit">Se connecter</button>
      </form>
    </div>
    """, message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# --- Page d'accueil ---
@app.route('/')
def index():
    return render_template_string('''
    <h1>🕵️ Escape Game Cyber</h1>
    <h2>Choisissez votre défi :</h2>
    <ul>
        <li><a href="/login">Défi 1 - Mot de passe faible</a></li>
        <li><a href="/search">Défi 2 - Injection SQL</a></li>
        <li><a href="/crypto">Défi 3 - Cryptographie</a></li>
        <li><a href="/stego">Défi 4 - Stéganographie</a></li>
        <li>Défi 5 - Réseau : <code>nc localhost 1337</code></li>
    </ul>
    ''')

# --- Défi 1 : Mot de passe faible ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        # Mot de passe volontairement faible (défi pédagogique)
        if username == 'admin' and password == 'password123':
            message = '✅ FLAG : CTF{DEFI1_WEAK_PASSWORD}'
        else:
            message = '❌ Mauvais identifiants. Indice : compte administrateur courant...'
    return render_template_string('''
    <h2>Défi 1 - Authentification</h2>
    <form method="POST">
        Utilisateur : <input name="username"><br>
        Mot de passe : <input type="password" name="password"><br>
        <input type="submit" value="Connexion">
    </form>
    <p>{{ message }}</p>
    ''', message=message)

# --- Défi 2 : Injection SQL ---
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    query_display = ''
    if request.method == 'POST':
        search_term = request.form.get('term', '')
        query_display = search_term
        try:
            conn = sqlite3.connect(':memory:')
            c = conn.cursor()
            c.execute("CREATE TABLE users (id INTEGER, name TEXT, secret TEXT)")
            c.execute("INSERT INTO users VALUES (1, 'alice', 'CTF{DEFI2_SQL_INJECTION}')")
            c.execute("INSERT INTO users VALUES (2, 'bob', 'rien ici')")
            # Vulnérabilité SQLi intentionnelle (défi pédagogique)
            raw_query = f"SELECT name, secret FROM users WHERE name = '{search_term}'"
            c.execute(raw_query)
            results = c.fetchall()
            conn.close()
        except Exception as e:
            results = [('Erreur SQL', str(e))]
    return render_template_string('''
    <h2>Défi 2 - Injection SQL</h2>
    <form method="POST">
        Rechercher un utilisateur : <input name="term">
        <input type="submit" value="Chercher">
    </form>
    <p>Résultats pour "{{ query }}" :</p>
    <ul>{% for r in results %}<li>{{ r }}</li>{% endfor %}</ul>
    ''', results=results, query=query_display)

# --- Défi 3 : Cryptographie (placeholder) ---
@app.route('/crypto')
def crypto():
    return render_template_string('''
    <h2>Défi 3 - Cryptographie</h2>
    <p>Déchiffrez le fichier <code>flag.enc</code> pour obtenir le flag.</p>
    <p><em>Défi en cours de développement...</em></p>
    ''')

# --- Défi 4 : Stéganographie (placeholder) ---
@app.route('/stego')
def stego():
    return render_template_string('''
    <h2>Défi 4 - Stéganographie</h2>
    <p>Analysez l'image <code>secret.png</code> pour y trouver le message caché.</p>
    <p><em>Défi en cours de développement...</em></p>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

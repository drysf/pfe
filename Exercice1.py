from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute("CREATE TABLE users (username TEXT, password TEXT)")
    # L'identifiant correspond maintenant à celui du mail
    c.execute("INSERT INTO users VALUES ('s.dupont', 'mdp_super_complexe_inconnu')") 
    return conn

# 1. La fausse boîte mail (Le point de départ)
@app.route('/mail')
def mail():
    html = """
    <div style="font-family: Arial; padding: 20px;">
        <h2>MailBox - Message intercepté</h2>
        <div style="border: 2px solid #333; padding: 15px; background-color: #f9f9f9; width: 500px;">
            <p><b>De :</b> it-support@mega-corp.local</p>
            <p><b>À :</b> s.dupont@mega-corp.local</p>
            <p><b>Sujet :</b> Nouveaux accès administrateur</p>
            <hr>
            <p>Bonjour Sophie,</p>
            <p>Ton compte pour le portail d'administration est actif. Ton identifiant de connexion est : <b>s.dupont</b>.</p>
            <p>Le mot de passe t'a été envoyé séparément sur ton téléphone pro. Ne le perds pas.</p>
            <p>L'équipe IT.</p>
        </div>
        <br>
        <a href="/">-> Aller vers le portail d'administration</a>
    </div>
    """
    return html

# 2. Le portail d'administration vulnérable
@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        conn = init_db()
        c = conn.cursor()
        
        requete = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        try:
            c.execute(requete)
            user = c.fetchone()
            
            if user:
                return f"<h1 style='color:green;'>Accès Autorisé !</h1><p><b>FLAG{{M41L_P1R4T3_SQL1}}</b></p>"
            else:
                message = "Identifiants incorrects."
        except sqlite3.Error as e:
            message = f"Erreur SQL : {e}"

    html = """
    <div style="font-family: Arial; padding: 20px;">
        <h2>Portail d'Administration</h2>
        <p style="color:red;">{{ message }}</p>
        <form method="POST">
            Utilisateur: <input type="text" name="username"><br><br>
            Mot de passe: <input type="password" name="password"><br><br>
            <input type="submit" value="Se connecter">
        </form>
    </div>
    """
    return render_template_string(html, message=message)

if __name__ == '__main__':
    app.run(debug=True)
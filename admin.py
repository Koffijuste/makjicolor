# --- Ajoute ces imports ---
from flask import Flask, session, redirect, url_for, request, flash, render_template_string
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import check_password_hash, generate_password_hash
import os
from dotenv import load_dotenv
from models import Produit, Utilisateur, db

load_dotenv()

# Récupérer les identifiants admin depuis .env
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

if not ADMIN_USERNAME or not ADMIN_PASSWORD:
    raise ValueError("❌ ADMIN_USERNAME et ADMIN_PASSWORD doivent être définis dans .env")

# Hachage optionnel (recommandé)
# Pour l'utiliser : génère le hash une fois, puis stocke-le dans .env
ADMIN_PASSWORD_HASH = generate_password_hash(ADMIN_PASSWORD)

# --- Vue d'index sécurisée ---
class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return session.get('admin_logged_in') is True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login'))

# --- Modèle sécurisé ---
class SecureModelView(ModelView):
    def is_accessible(self):
        return session.get('admin_logged_in') is True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login'))

class ProduitAdminView(SecureModelView):
    column_list = ['id', 'nom', 'categorie', 'prix', 'dimensions', 'materiau']
    form_columns = ['nom', 'categorie', 'prix', 'dimensions', 'materiau', 'description', 'image_url']
    form_widget_args = {
        'description': {'rows': 3, 'style': 'width: 100%'}
    }

class UtilisateurAdminView(SecureModelView):
    form_columns = ['email', 'numero']
    column_list = ['id', 'email', 'numero']

 # Optionnel : afficher une vignette dans la liste
    def _list_thumbnail(view, context, model, name):
        if not model.image_url:
            return ''
        url = model.image_url
        if not url.startswith(('http://', 'https://')):
            url = url_for('static', filename=url, _external=True)
        return f'<img src="{url}" style="width:60px; height:auto;">'
    
    column_formatters = {
        'image_url': _list_thumbnail
    }

# --- Route de login dédiée à l'admin ---
def init_admin_auth(app):
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Vérification simple (ou avec hash)
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                session['admin_logged_in'] = True
                return redirect('/admin')
            else:
                flash('Identifiants incorrects.', 'error')
        
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Connexion Admin</title>
            <style>
                body { font-family: Arial, sans-serif; background: #f5f5f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .login-box { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 320px; }
                .login-box h2 { text-align: center; margin-bottom: 20px; color: #333; }
                .login-box input { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                .login-box button { width: 100%; padding: 10px; background: #d4af37; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px; }
                .login-box button:hover { background: #b8860b; }
                .error { color: #d32f2f; text-align: center; margin-top: 10px; }
            </style>
        </head>
        <body>
            <div class="login-box">
                <h2>🔐 Admin Login</h2>
                <form method="POST">
                    <input type="text" name="username" placeholder="Nom d'utilisateur" required>
                    <input type="password" name="password" placeholder="Mot de passe" required>
                    <button type="submit">Se connecter</button>
                </form>
                {% with messages = get_flashed_messages() %}
                    {% if messages %}
                        <div class="error">{{ messages[0] }}</div>
                    {% endif %}
                {% endwith %}
            </div>
        </body>
        </html>
        ''')

    @app.route('/admin/logout')
    def admin_logout():
        session.pop('admin_logged_in', None)
        return redirect('/admin/login')

# --- Initialisation de Flask-Admin ---
def init_admin(app):
    admin = Admin(
        app,
        name='MAKJICOLOR Admin',
        index_view=SecureAdminIndexView()
    )
    admin.add_view(ProduitAdminView(Produit, db.session, endpoint='produits_admin'))
    admin.add_view(UtilisateurAdminView(Utilisateur, db.session, endpoint='utilisateurs_admin'))
    init_admin_auth(app)
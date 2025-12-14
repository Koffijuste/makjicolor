from flask import (
    session, redirect, url_for, request,
    flash, render_template_string
)
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import check_password_hash
import os
from dotenv import load_dotenv

from models import Produit, Utilisateur, db

load_dotenv()

# ==============================
# CONFIG ADMIN (.env)
# ==============================
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

if not ADMIN_USERNAME or not ADMIN_PASSWORD_HASH:
    raise RuntimeError(
        "❌ ADMIN_USERNAME et ADMIN_PASSWORD_HASH doivent être définis"
    )

# ==============================
# INSTANCE UNIQUE FLASK-ADMIN
# ==============================
admin = Admin(
    name="maxime",
    template_mode="bootstrap4"
)

# ==============================
# VUE INDEX SÉCURISÉE
# ==============================
class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return session.get("admin_logged_in") is True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin_login"))

# ==============================
# BASE VIEW SÉCURISÉE
# ==============================
class SecureModelView(ModelView):
    def is_accessible(self):
        return session.get("admin_logged_in") is True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin_login"))

# ==============================
# VUES ADMIN
# ==============================
class ProduitAdminView(SecureModelView):
    column_list = ["id", "nom", "categorie", "prix", "dimensions", "materiau"]
    form_columns = [
        "nom", "categorie", "prix",
        "dimensions", "materiau",
        "description", "image_url"
    ]
    form_widget_args = {
        "description": {"rows": 3, "style": "width: 100%;"}
    }

class UtilisateurAdminView(SecureModelView):
    column_list = ["id", "email", "numero"]
    form_columns = ["email", "numero"]

# ==============================
# AUTH ADMIN (LOGIN / LOGOUT)
# ==============================
def init_admin_auth(app):

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if (
                username == ADMIN_USERNAME
                and check_password_hash(ADMIN_PASSWORD_HASH, password)
            ):
                session["admin_logged_in"] = True
                return redirect("/admin")
            else:
                flash("Identifiants incorrects.", "error")

        return render_template_string("""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Admin Login</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f5f5f5;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .login-box {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    width: 320px;
                    box-shadow: 0 4px 12px rgba(0,0,0,.1);
                }
                .login-box h2 {
                    text-align: center;
                }
                .login-box input {
                    width: 100%;
                    padding: 10px;
                    margin: 8px 0;
                }
                .login-box button {
                    width: 100%;
                    padding: 10px;
                    background: #d4af37;
                    border: none;
                    color: white;
                    font-size: 16px;
                    cursor: pointer;
                }
                .error {
                    color: #c62828;
                    text-align: center;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <div class="login-box">
                <h2>🔐 Admin</h2>
                <form method="POST">
                    <input name="username" placeholder="Utilisateur" required>
                    <input type="password" name="password" placeholder="Mot de passe" required>
                    <button type="submit">Connexion</button>
                </form>
                {% with messages = get_flashed_messages() %}
                    {% if messages %}
                        <div class="error">{{ messages[0] }}</div>
                    {% endif %}
                {% endwith %}
            </div>
        </body>
        </html>
        """)

    @app.route("/admin/logout")
    def admin_logout():
        session.pop("admin_logged_in", None)
        return redirect("/admin/login")

# ==============================
# INIT ADMIN (APPEL UNIQUE)
# ==============================
def init_admin(app):

    if not app.secret_key:
        raise RuntimeError("❌ SECRET_KEY requis pour Flask-Admin")

    admin.init_app(
        app,
        index_view=SecureAdminIndexView()
    )

    admin.add_view(
        ProduitAdminView(Produit, db.session, endpoint="produits_admin")
    )
    admin.add_view(
        UtilisateurAdminView(Utilisateur, db.session, endpoint="utilisateurs_admin")
    )

    init_admin_auth(app)

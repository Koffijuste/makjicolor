# __init__.py
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from models import db, Utilisateur, Produit, Panier, Commande, CommandeProduit
import os
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Base de données
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    else:
        database_url = 'sqlite:///../instance/makjicolor.db'

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # === Initialisation des extensions ===
    db.init_app(app)

    migrate.init_app(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Utilisateur.query.get(int(user_id))

    # === Flask-Admin ===
    from admin import init_admin
    init_admin(app)

    # === Context processors ===
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}  # <-- corrigé

    @app.context_processor
    def inject_data():
        dark_mode = session.get('dark_mode', False)
        nb_articles = 0
        if current_user.is_authenticated:
            nb_articles = Panier.query.filter_by(utilisateur_id=current_user.id).count()
        return dict(dark_mode=dark_mode, nb_articles=nb_articles)

    # === Enregistrer les routes ===
    from routes import main  # Vérifie le nom du blueprint
    app.register_blueprint(main)

    return app

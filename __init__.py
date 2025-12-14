# __init__.py
from datetime import datetime
from flask import Flask, render_template, session
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from models import db, Utilisateur, Panier
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Initialiser les extensions globalement
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # === Clé secrète ===
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    if not app.config['SECRET_KEY']:
        raise ValueError("❌ La variable SECRET_KEY est manquante. Définissez-la dans Render ou .env.")

     # === Base de données ===
    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        # Convertit postgres:// → postgresql+psycopg://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)

        # Convertit postgresql:// → postgresql+psycopg://
        elif database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

        elif database_url.startswith("mysql://"):
            database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)
            
        elif database_url.startswith("sqlite://") and database_url == "sqlite://":
            database_url = "sqlite:///../instance/makjicolor.db"

        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Développement local : SQLite
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/makjicolor.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # === Initialisation des extensions ===
    db.init_app(app)
    migrate.init_app(app, db)

    # === Flask-Login ===
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Utilisateur.query.get(int(user_id))

    # === Flask-Admin (sécurisé) ===
    try:
        from admin import init_admin
        init_admin(app)
    except ImportError:
        pass  # Optionnel en production

    # === Context processors ===
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow}

    @app.context_processor
    def inject_data():
        dark_mode = session.get('dark_mode', False)
        nb_articles = 0
        if current_user.is_authenticated:
            nb_articles = Panier.query.filter_by(utilisateur_id=current_user.id).count()
        return dict(dark_mode=dark_mode, nb_articles=nb_articles)

    # === Gestion des erreurs ===
    @app.errorhandler(500)
    def internal_error(e):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    # === Création des tables au démarrage ===
    with app.app_context():
        db.create_all()

    # === Routes ===
    from routes import main
    app.register_blueprint(main)

    return app
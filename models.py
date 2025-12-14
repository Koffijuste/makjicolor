from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ========================
# Utilisateur
# ========================
class Utilisateur(UserMixin, db.Model):
    __tablename__ = "utilisateurs"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(200), nullable=False)  # Stocke le hash sécurisé
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    commandes = db.relationship('Commande', backref='utilisateur', lazy=True)
    panier_items = db.relationship('Panier', backref='utilisateur', lazy=True)

    # Méthodes pour le mot de passe
    def set_mot_de_passe(self, mot_de_passe_clair: str):
        self.mot_de_passe_hash = generate_password_hash(mot_de_passe_clair)

    def check_mot_de_passe(self, mot_de_passe_clair: str) -> bool:
        return check_password_hash(self.mot_de_passe_hash, mot_de_passe_clair)


# ========================
# Produit
# ========================
class Produit(db.Model):
    __tablename__ = "produits"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    categorie = db.Column(db.String(50))
    prix = db.Column(db.Float, nullable=False)
    dimensions = db.Column(db.String(50))
    materiau = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))

# ========================
# Panier
# ========================
class Panier(db.Model):
    __tablename__ = "paniers"

    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=False)
    quantite = db.Column(db.Integer, default=0)

    produit = db.relationship('Produit', backref='paniers')


# ========================
# Commande
# ========================
class Commande(db.Model):
    __tablename__ = "commandes"

    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    statut = db.Column(db.String(20), default='en attente')  # en attente, confirmée, livrée

    items = db.relationship('CommandeProduit', backref='commande', lazy=True)


# ========================
# CommandeProduit
# ========================
class CommandeProduit(db.Model):
    __tablename__ = "commande_produits"

    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commandes.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_unitaire = db.Column(db.Float, nullable=False)

    produit = db.relationship('Produit', backref='commandes_items')

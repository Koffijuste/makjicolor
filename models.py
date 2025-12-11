from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Utilisateur(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(100), nullable=False)  # En production : hasher avec bcrypt
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    commandes = db.relationship('Commande', backref='utilisateur', lazy=True)
    panier_items = db.relationship('Panier', backref='utilisateur', lazy=True)

class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    categorie = db.Column(db.String(50))
    prix = db.Column(db.Float, nullable=False)
    dimensions = db.Column(db.String(50))
    materiau = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))

class Panier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    quantite = db.Column(db.Integer, default=0)

    produit = db.relationship('Produit', backref='paniers')

class Commande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    statut = db.Column(db.String(20), default='en attente')  # en attente, confirmée, livrée

    items = db.relationship('CommandeProduit', backref='commande', lazy=True)

class CommandeProduit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_unitaire = db.Column(db.Float, nullable=False)

    produit = db.relationship('Produit', backref='commandes_items')
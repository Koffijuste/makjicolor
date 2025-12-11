# seed.py
import os
import sys

# Ajoute le dossier racine au chemin Python pour importer l'appli
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Produit

# Liste des produits de démo (identique à ce que tu utilises)
PRODUITS_DEMO = [
    # --- PEINTURE À EAU ---
    {"nom": "Sofap Acrylic Pro", "prix": 12000, "dimensions": "10 L", "materiau": "Acrylique (Eau)", "description": "Peinture polyvalente intérieur/extérieur, très couvrante et durable.", "image_url": "img/Eurocolor.jpg", "categorie": "Peinture à Eau"},
    {"nom": "Colormat Latex Mate", "prix": 8500, "dimensions": "5 L", "materiau": "Latex Mat", "description": "Finition mate pour murs intérieurs, anti-reflets et facile à appliquer.", "image_url": "img/samara.jpg", "categorie": "Peinture à Eau"},
    {"nom": "Sika WallCoat", "prix": 14000, "dimensions": "10 L", "materiau": "Acrylique Premium", "description": "Résistance maximale à l’humidité et à la moisissure. Idéal salles d’eau.", "image_url": "img/sika_wallcoat.jpg", "categorie": "Peinture à Eau"},
    {"nom": "Tollens Acrylic White", "prix": 9000, "dimensions": "5 L", "materiau": "Acrylique Mat", "description": "Blanc profond longue durée pour plafonds et murs.", "image_url": "img/tollens_acry_white.jpg", "categorie": "Peinture à Eau"},
    {"nom": "DecoPlus Satiné", "prix": 13000, "dimensions": "5 L", "materiau": "Acrylique Satinée", "description": "Aspect satiné premium, idéal pour salons et chambres.", "image_url": "img/decoplus_satine.jpg", "categorie": "Peinture à Eau"},

    # --- PEINTURE À HUILE ---
    {"nom": "Sofap Glycéro Brillant", "prix": 11000, "dimensions": "4 L", "materiau": "Huile Glycéro", "description": "Brillance intense, très résistante. Idéale portes et fenêtres.", "image_url": "img/sofap_glycero.jpg", "categorie": "Peinture à Huile"},
    {"nom": "Tollens OilPro", "prix": 13500, "dimensions": "5 L", "materiau": "Glycéro Extérieure", "description": "Excellente résistance au soleil et intempéries.", "image_url": "img/tollens_oilpro.jpg", "categorie": "Peinture à Huile"},
    {"nom": "Colormat Huile Satin", "prix": 12500, "dimensions": "4 L", "materiau": "Glycéro Satinée", "description": "Durabilité et aspect satiné élégant. Pour boiseries.", "image_url": "img/colormat_huile.jpg", "categorie": "Peinture à Huile"},
    {"nom": "Valéso Glycéro Pro", "prix": 15000, "dimensions": "5 L", "materiau": "Huile Professionnelle", "description": "Très haute résistance chimique. Parfait pour zones industrielles.", "image_url": "img/valeso_glycero.jpg", "categorie": "Peinture à Huile"},
    {"nom": "MakjiMetal Protect", "prix": 16000, "dimensions": "4 L", "materiau": "Huile Anti-Rouille", "description": "Peinture idéale pour portails, barrières et structures métalliques.", "image_url": "img/makji_metal.jpg", "categorie": "Peinture à Huile"},

    # --- VERNIS ---
    {"nom": "Vernis Bois Premium", "prix": 7500, "dimensions": "1 L", "materiau": "Vernis PU", "description": "Protection longue durée pour meubles et boiseries.", "image_url": "img/vernis_bois.jpg", "categorie": "Vernis"},
    {"nom": "Vernis Marin", "prix": 12000, "dimensions": "1 L", "materiau": "Polyuréthane Marin", "description": "Ultra résistant à l’eau salée et climat humide.", "image_url": "img/vernis_marin.jpg", "categorie": "Vernis"},
    {"nom": "Vernis Parquet Brillant", "prix": 14000, "dimensions": "2 L", "materiau": "PU Brillant", "description": "Met en valeur les parquets avec une couche brillante solide.", "image_url": "img/vernis_parquet.jpg", "categorie": "Vernis"},

    # --- ACCESSOIRES ---
    {"nom": "Rouleau Pro 25cm", "prix": 3000, "dimensions": "25 cm", "materiau": "Fibre Premium", "description": "Pour peintures murs et plafonds. Application uniforme.", "image_url": "img/rouleau_25.jpg", "categorie": "Accessoire"},
    {"nom": "Pinceau Plat 50mm", "prix": 1500, "dimensions": "50 mm", "materiau": "Poils Synthétiques", "description": "Parfait pour finitions et retouches.", "image_url": "img/pinceau_50.jpg", "categorie": "Accessoire"},
    {"nom": "Bâche de Protection", "prix": 2000, "dimensions": "4 × 5 m", "materiau": "PVC Léger", "description": "Protège sols et meubles pendant les travaux.", "image_url": "img/bache.jpg", "categorie": "Accessoire"},
    {"nom": "Ruban de Masquage Pro", "prix": 1000, "dimensions": "25 m", "materiau": "Adhésif", "description": "Pour des bordures nettes sans bavures.", "image_url": "img/ruban.jpg", "categorie": "Accessoire"},
    {"nom": "Bac à Peinture Ergonomique", "prix": 2500, "dimensions": "18 cm", "materiau": "Plastique ABS", "description": "Pratique pour rouleaux et applications rapides.", "image_url": "img/bac.jpg", "categorie": "Accessoire"},
    {"nom": "Grille d’Essorage Métal", "prix": 2000, "dimensions": "20 cm", "materiau": "Acier", "description": "À accrocher sur le seau pour enlever l’excès de peinture.", "image_url": "img/grille.jpg", "categorie": "Accessoire"},

    # --- PEINTURES DÉCORATIVES ---
    {"nom": "Effet Marbré Or", "prix": 18000, "dimensions": "2 L", "materiau": "Acrylique Décoratif", "description": "Crée un effet marbre luxueux sur murs et meubles.", "image_url": "img/marbre_or.jpg", "categorie": "Peinture Décorative"},
    {"nom": "Béton Ciré Pro", "prix": 22000, "dimensions": "5 kg", "materiau": "Enduit Décoratif", "description": "Revêtement lisse et minéral pour sols et murs.", "image_url": "img/beton_cire.jpg", "categorie": "Peinture Décorative"},

    # --- PEINTURES ÉTANCHES ---
    {"nom": "HydroBlock Extérieur", "prix": 16000, "dimensions": "10 L", "materiau": "Acrylique Étanche", "description": "Imperméabilise façades et murs extérieurs.", "image_url": "img/hydroblock.jpg", "categorie": "Peinture Étanche"},

    # --- ÉPOXY SOLS ---
    {"nom": "Époxy Sol Garage", "prix": 35000, "dimensions": "20 kg", "materiau": "Résine Époxy Bicomposant", "description": "Revêtement ultra-résistant pour sols industriels.", "image_url": "img/epoxy_sol.jpg", "categorie": "Époxy Sol"},

    # --- AUTRES ---
    {"nom": "Nettoyant Après Travaux", "prix": 4500, "dimensions": "1 L", "materiau": "Nettoyant Professionnel", "description": "Élimine taches de peinture, colle et résidus.", "image_url": "img/nettoyant.jpg", "categorie": "Autres"},
]

def seed_db():
    with app.app_context():
        db.create_all()
        # Ajouter uniquement les produits manquants (recommandé)
        noms_existants = {p.nom for p in Produit.query.with_entities(Produit.nom).all()}
        ajoutes = 0
        for p_data in PRODUITS_DEMO:
            if p_data["nom"] not in noms_existants:
                produit = Produit(**p_data)
                db.session.add(produit)
                ajoutes += 1
        
        db.session.commit()
        print(f"✅ {ajoutes} nouveaux produits ajoutés à la base.")

if __name__ == "__main__":
    seed_db()
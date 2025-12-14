from flask import Blueprint, app, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from flask import Response
from flask_login import current_user, login_user, logout_user, login_required
from models import db, Utilisateur, Produit, Panier, Commande, CommandeProduit
import os
import urllib.parse

main = Blueprint('main', __name__)

# --- Routes ---
@main.route("/")
def portail():
    return render_template("portail.html", page_class="page-portail")

@main.route("/MAKJICOLOR-Shop")
def accueil():
    produits = Produit.query.all()
    return render_template("index.html", produits=produits, page_class="page-accueil")

@main.route("/histoire")
def histoire():
    return render_template("histoire.html" , page_class="page-histoire")

@main.route("/mentions-legales")
def mentions_legales():
    return render_template("mentions-legales.html", page_class="page-mentions-legales")

@main.route("/politique-confidentialite")
def politique_confidentialite():
    return render_template("politique-confidentialite.html", page_class="page-politique-confidentialite")

@main.route("/conditions-vente")
def conditions_vente():
    return render_template("conditions-vente.html", page_class="page-conditions-vente")

@main.route("/support-client")
def support_client():
    return render_template("support-client.html", page_class="page-support-client")

@main.route("/prestations")
def prestations():
    return render_template("prestations.html", page_class="page-prestations")

@main.route('/produit/<int:produit_id>')
def fiche_produit(produit_id):
    produit = Produit.query.get_or_404(produit_id)
    return render_template('fiche_produit.html', produit=produit)

@main.route("/legal")
def legal():
    return render_template("legal.html", page_class="page-legal")

@main.route("/recherche")
def recherche():
    query = request.args.get("q", "").strip()
    if query:
        produits = Produit.query.filter(
            Produit.nom.ilike(f"%{query}%") |
            Produit.categorie.ilike(f"%{query}%") |
            Produit.materiau.ilike(f"%{query}%")
        ).all()
    else:
        produits = []
    return render_template("recherche.html", produits=produits, query=query)

@main.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Envoie d'email avec Flask-Mail ou autre
        flash("Message envoyé avec succès !", "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html", page_class="page-contact")

@main.route("/account")
@login_required
def account():
    return render_template("account.html", user=current_user, page_class="page-account")

@main.route("/blog")
def blog():
    return render_template("blog.html", page_class="page-blog")

@main.route('/sitemap.xml')
def sitemap():
    pages = [
        url_for('main.portail', _external=True),
        url_for('main.accueil', _external=True),
        url_for('main.produits', _external=True),
        url_for('main.histoire', _external=True),
        url_for('main.contact', _external=True),
        url_for('main.prestations', _external=True),
    ]
    # Ajouter toutes les pages produits
    produits = Produit.query.all()
    for p in produits:
        pages.append(url_for('main.fiche_produit', produit_id=p.id, _external=True))
    
    sitemap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''
    for url in pages:
        sitemap_xml += f"\n  <url><loc>{url}</loc></url>"
    sitemap_xml += "\n</urlset>"
    
    return Response(sitemap_xml, mimetype='application/xml')

@main.route("/debug")
def debug():
    produits = Produit.query.all()
    return f"<h1>{len(produits)} produits trouvés</h1>" + \
           "<br>".join([f"{p.nom} - {p.categorie}" for p in produits])

@main.route("/modifier-quantite", methods=["POST"])
@login_required
def modifier_quantite():
    produit_id = request.form.get("produit_id", type=int)
    action = request.form.get("action")
    if not produit_id or action not in ["augmenter", "diminuer"]:
        flash("Requête invalide.", "error")
        return redirect(url_for('main.panier'))
    else:
        item = Panier.query.filter_by(
            utilisateur_id=current_user.id,
            produit_id=produit_id
        ).first()
        if not item:
            flash("Article non trouvé dans le panier.", "error")
            return redirect(url_for('main.panier'))
        if action == "augmenter":
            item.quantite += 1
        elif action == "diminuer":
            if item.quantite >= 1:
                item.quantite -= 1
            else:
                db.session.delete(item)
        db.session.commit()
    return redirect(url_for('main.panier'))


@main.route("/supprimer-panier/<int:produit_id>")
@login_required
def supprimer_panier(produit_id):
    # Supprime la ligne du panier où produit_id = X et utilisateur = Y
    Panier.query.filter_by(
        utilisateur_id=current_user.id,
        produit_id=produit_id
    ).delete()
    db.session.commit()
    flash("Article supprimé.", "info")
    return redirect(url_for('main.panier'))
 
@main.route('/update-shipping', methods=['POST'])
@login_required
def update_shipping():
    country = request.form.get('country')
    if country not in ['CIV', 'INTL']:
        country = 'CIV'
    
    # Stocker dans la session
    session['shipping_country'] = country
    return redirect(url_for('main.panier'))

@main.route("/produits")
@main.route("/produits/<categorie>")
def produits(categorie=None):
    mapping = {
        "interieur": ["Peinture à Eau", "Peinture à Huile"],
        "exterieur": ["Peinture Étanche", "Peinture Décorative"],
        "accessoires": ["Accessoire"],
        "vernis": ["Vernis", "Époxy Sol"],
        "decoratif": ["Peinture Décorative"],
        "etanche": ["Peinture Étanche"],
        "epoxy": ["Époxy Sol"],
        "autres": ["Autres"]
    }
    
    if categorie:
        cats = mapping.get(categorie)
        produits = Produit.query.filter(Produit.categorie.in_(cats)).all() if cats else []
    else:
        cat = request.args.get("cat")
        if cat == "interieur":
            produits = Produit.query.filter(Produit.categorie.in_(["Peinture à Eau", "Peinture à Huile"])).all()
        elif cat == "exterieur":
            produits = Produit.query.filter_by(categorie="Peinture Extérieure").all()
        elif cat == "vernis":
            produits = Produit.query.filter_by(categorie="Vernis").all()
        elif cat == "accessoires":
            produits = Produit.query.filter_by(categorie="Accessoire").all()
        elif cat == "decoratif":
            produits = Produit.query.filter_by(categorie="Peinture Décorative").all()
        elif cat == "etanche":
            produits = Produit.query.filter_by(categorie="Peinture Étanche").all()
        elif cat == "epoxy":
            produits = Produit.query.filter_by(categorie="Époxy Sol").all()
        elif cat == "autres":
            produits = Produit.query.filter_by(categorie="Autres").all()
        else:
            produits = Produit.query.all()

    return render_template("produits.html", produits=produits, categorie_active=categorie, page_class="page-produits")

@main.route("/panier")
@login_required
def panier():
    items = Panier.query.filter_by(utilisateur_id=current_user.id).all()
    total = sum(item.produit.prix * item.quantite for item in items)
    # Récupérer la zone de livraison
    shipping_country = session.get('shipping_country', 'CIV')

    # Définir les frais
    shipping = 2000 if shipping_country == 'CIV' else 7500

    # Calculer total avec livraison
    total_with_shipping = total + shipping

    return render_template(
        "panier.html",
        panier=items,
        total=total,
        shipping=shipping,
        shipping_country=shipping_country,
        total_with_shipping=total_with_shipping,  # ← à utiliser dans WhatsApp
        page_class="page-panier"
    )

@main.route("/ajouter-panier", methods=["POST"])
@login_required
def ajouter_panier():
    produit_id = request.form.get("produit_id", type=int)
    produit = Produit.query.get(produit_id)

    if 'shipping_country' not in session:
        session['shipping_country'] = 'CIV'  # ou détecter par IP (plus avancé)

    if not produit:
        flash("Produit non trouvé.", "error")
        return redirect(url_for("main.produits"))

    # Ajouter au panier (via session ou modèle Panier)
    item = Panier.query.filter_by(utilisateur_id=current_user.id, produit_id=produit_id).first()
    if item:
        item.quantite += 1
    else:
        item = Panier(utilisateur_id=current_user.id, produit_id=produit_id, quantite=1)
        db.session.add(item)
    db.session.commit()
    
    flash(f"{produit.nom} ajouté au panier !", "success")
    return redirect(url_for("main.fiche_produit", produit_id=produit_id))

@main.route("/paiement")
@login_required
def paiement():
    # 1. Récupérer le panier
    items = Panier.query.filter_by(utilisateur_id=current_user.id).all()
    if not items:
        flash("Panier vide.", "error")
        return redirect(url_for("main.panier"))

    # 2. Calculer les totaux
    total = sum(item.produit.prix * item.quantite for item in items)
    shipping_country = session.get('shipping_country', 'CIV')
    shipping = 2000 if shipping_country == 'CIV' else 7500
    total_with_shipping = total + shipping

    # 3. Générer le message — propre, sans doublon
    lignes = [
        "📦 *NOUVELLE COMMANDE — MAKJICOLOR*",
        "",
        f"👤 *Téléphone* : {current_user.numero}",
        f"📧 *Email* : {current_user.email}",
        "",
        "🛍️ *Articles commandés* :"
    ]

    for item in items:
        line = f"• {item.produit.nom} × {item.quantite}"
        img_url = item.produit.image_url
        if img_url and isinstance(img_url, str):
            img_url = img_url.strip()
            if img_url.startswith(('http://', 'https://')) and any(img_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                line += f"\n  📷 {img_url}"
        lignes.append(line)

    lignes.extend([
        "",
        f"💰 *Sous-total* : {total:,.0f} FCFA",
        f"🚚 *Livraison* : {shipping:,.0f} FCFA ({ 'Côte d’Ivoire' if shipping_country == 'CIV' else 'International' })",
        f"*TOTAL À PAYER* : {total_with_shipping:,.0f} FCFA",
        "",
        "🙏 Merci pour votre commande ! Veuillez confirmer."
    ])

    message = "\n".join(lignes)
    
    # 4. Vider le panier AVANT redirection (critique !)
    Panier.query.filter_by(utilisateur_id=current_user.id).delete()
    db.session.commit()  # ← commit ici pour garantir la suppression

    # 5. Rediriger vers WhatsApp
    numero = os.environ.get("WHATSAPP_NUMBER", "2250711066021")
    url = f"https://wa.me/{numero}?text={urllib.parse.quote(message)}"
    return redirect(url)

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        pwd = request.form["password"]

        user = Utilisateur.query.filter_by(email=email).first()  # cherche juste par email
        if user and user.check_mot_de_passe(pwd):  # vérifie le mot de passe hashé
            from flask_login import login_user
            login_user(user)
            return redirect(url_for("main.panier"))  # ou la page de ton choix
        flash("Email ou mot de passe incorrect.", "error")

    return render_template("login.html", page_class="page-login")


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        numero = request.form["numero"]
        pwd1 = request.form["password"]
        pwd2 = request.form["confirm_password"]
        if pwd1 != pwd2:
            flash("Les mots de passe ne correspondent pas.", "error")
        elif Utilisateur.query.filter_by(email=email).first() or Utilisateur.query.filter_by(numero=numero).first():
            flash("Cet email ou numéro est déjà utilisé.", "error")
        else:
            user = Utilisateur(email=email, numero=numero)
            user.set_mot_de_passe(pwd1)
            db.session.add(user)
            db.session.commit()
            from flask_login import login_user
            login_user(user)
            return redirect(url_for("main.login"))
    return render_template("register.html", page_class="page-register")

@main.route('/logout')
@login_required
def logout():
    from flask_login import logout_user
    logout_user()
    flash("Déconnexion réussie.", "info")
    return redirect(url_for('main.portail'))


# --- Context Processor ---
@main.app_context_processor
def inject_data():
    dark_mode = session.get('dark_mode', False)
    nb_articles = 0
    if current_user.is_authenticated:
        nb_articles = Panier.query.filter_by(utilisateur_id=current_user.id).count()
    return dict(dark_mode=dark_mode, nb_articles=nb_articles)

@main.route("/toggle-dark-mode")
def toggle_dark_mode():
    session['dark_mode'] = not session.get('dark_mode', False)
    return redirect(request.referrer or url_for("accueil"))
# (Ajoute aussi : contact, account, prestations, recherche, legal, 404, toggle-dark-mode, etc.)
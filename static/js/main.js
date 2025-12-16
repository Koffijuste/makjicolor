// === DONNÉES PRODUITS ===
const products = [
  {
    id: 1,
    name: "Forêt Enchantée",
    price: 299,
    dimensions: "80 × 100 cm",
    material: "Toile sur châssis en pin",
    description: "Une immersion totale dans la forêt luxuriante du matin, où la lumière perce à travers les feuillages. Peinte à l’huile avec des pigments naturels.",
    img: "https://images.unsplash.com/photo-1501084817091-a4f3d220886e?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"
  },
  {
    id: 2,
    name: "Coucher de Soleil sur la Mer",
    price: 349,
    dimensions: "100 × 120 cm",
    material: "Toile coton premium",
    description: "Un moment suspendu entre ciel et mer, capturé dans des tons chauds et vibrants. Chaque vague est peinte avec passion.",
    img: "https://images.unsplash.com/photo-1543857778-c4a1a569e7bd?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"
  },
  {
    id: 3,
    name: "Rêverie Urbaine",
    price: 249,
    dimensions: "70 × 90 cm",
    material: "Toile sur châssis en chêne",
    description: "L’âme de la ville la nuit, entre néons et silhouettes. Une œuvre contemporaine qui dialogue avec l’architecture moderne.",
    img: "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"
  },
  {
    id: 4,
    name: "Éclat de Printemps",
    price: 399,
    dimensions: "90 × 110 cm",
    material: "Toile coton bio",
    description: "Une explosion florale douce et joyeuse, peinte pendant la saison des cerisiers en fleurs à Kyoto.",
    img: "https://images.unsplash.com/photo-1579540425814-2e7f1e6a4f5c?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"
  }
];

// === PANIER ===
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// === DOM ===
const productsGrid = document.getElementById('products-grid');
const productModal = document.getElementById('product-modal');
const modalBody = document.getElementById('modal-body');
const modalClose = document.getElementById('modal-close');
const modalOverlay = document.getElementById('modal-overlay');
const cartModal = document.getElementById('cart-modal');
const cartOverlay = document.getElementById('cart-overlay');
const cartBtn = document.getElementById('cart-btn');
const closeCart = document.getElementById('close-cart');
const cartItems = document.getElementById('cart-items');
const cartTotal = document.getElementById('cart-total');
const checkoutBtn = document.getElementById('checkout-btn');
const email = document.getElementById('email');
const numero = document.getElementById('numero')

// Regex 

const Email_Regex = /^[a-zA-Z0-9]+@[a-zA-Z0-9]+/.[a-zA-Z](2,)$/;
const Num_Regex = /^(?:\+225|0)[1-9](?:[ .-]?\d(2))(4)$/

// === Afficher les produits ===
products.forEach(product => {
  const card = document.createElement('div');
  card.className = 'product-card';
  card.innerHTML = `
    <img src="${product.img}" alt="${product.name}" class="product-img">
    <div class="product-info">
      <h3 class="product-title">${product.name}</h3>
      <p class="product-price">${product.price} €</p>
    </div>
  `;
  card.addEventListener('click', () => openProductModal(product));
  productsGrid.appendChild(card);
});

// === Modal Produit ===
function openProductModal(product) {
  modalBody.innerHTML = `
    <div class="product-modal-content">
      <img src="${product.img}" alt="${product.name}" class="product-modal-image">
      <div class="product-modal-details">
        <h2>${product.name}</h2>
        <p class="product-price">${product.price} €</p>
        <p><strong>Dimensions :</strong> ${product.dimensions}</p>
        <p><strong>Support :</strong> ${product.material}</p>
        <p>${product.description}</p>
        <button class="btn add-to-cart-btn" data-id="${product.id}">Ajouter au panier</button>
      </div>
    </div>
  `;
  productModal.classList.add('open');
  document.body.style.overflow = 'hidden';
  
  // Ajouter au panier depuis modal
  modalBody.querySelector('.add-to-cart-btn').addEventListener('click', () => {
    addToCart(product);
  });
}

modalClose.addEventListener('click', () => closeModals());
modalOverlay.addEventListener('click', () => closeModals());
cartOverlay.addEventListener('click', () => closeModals());


function closeModals() {
  productModal.classList.remove('open');
  cartModal.classList.remove('open');
  document.body.style.overflow = '';
}

// === Ajout au panier ===
function addToCart(product) {
  const existing = cart.find(item => item.id === product.id);
  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({ ...product, quantity: 1 });
  }
  localStorage.setItem('cart', JSON.stringify(cart));
  updateCartUI();
  closeModals();
}

// === UI Panier ===
function updateCartUI() {
  const count = cart.reduce((sum, item) => sum + item.quantity, 0);
  document.querySelector('.cart-count').textContent = count;
}

cartBtn.addEventListener('click', () => {
  renderCart();
  cartModal.classList.add('open');
  document.body.style.overflow = 'hidden';
});

closeCart.addEventListener('click', () => {
  cartModal.classList.remove('open');
  document.body.style.overflow = '';
});

function renderCart() {
  if (cart.length === 0) {
    cartItems.innerHTML = '<p>Votre panier est vide.</p>';
    cartTotal.textContent = 'Total : 0 FCFA';
    return;
  }

  cartItems.innerHTML = '';
  let total = 0;
  cart.forEach(item => {
    const itemTotal = item.price * item.quantity;
    total += itemTotal;
    const div = document.createElement('div');
    div.className = 'cart-item';
    div.innerHTML = `
      <div>
        <strong>${item.name}</strong> × ${item.quantity}
      </div>
      <div>${itemTotal} FCFA</div>
    `;
    cartItems.appendChild(div);
  });
  cartTotal.textContent = `Total : ${total} FCFA`;
}

// === Checkout ===
checkoutBtn.addEventListener('click', () => {
  alert('✅ Commande validée avec succès !\nMerci pour votre confiance.');
  cart = [];
  localStorage.setItem('cart', JSON.stringify(cart));
  updateCartUI();
  renderCart();
  cartModal.classList.remove('open');
  document.body.style.overflow = '';
});

// === Story Toggle ===
const toggleStory = document.getElementById('toggle-story');
const storyBody = document.getElementById('story-body');

toggleStory.addEventListener('click', () => {
  const isExpanded = toggleStory.getAttribute('aria-expanded') === 'true';
  if (isExpanded) {
    storyBody.style.height = '0px';
    storyBody.classList.remove('visible');
    setTimeout(() => storyBody.setAttribute('aria-hidden', 'true'), 500);
    toggleStory.setAttribute('aria-expanded', 'false');
    toggleStory.innerHTML = `<span>Découvrir notre histoire</span>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="6,9 12,15 18,9"></polyline></svg>`;
  } else {
    storyBody.setAttribute('aria-hidden', 'false');
    storyBody.style.height = storyBody.scrollHeight + 'px';
    setTimeout(() => storyBody.classList.add('visible'), 10);
    toggleStory.setAttribute('aria-expanded', 'true');
    toggleStory.innerHTML = `<span>Fermer</span>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="6,18 12,12 18,18"></polyline></svg>`;
  }
});

// === Slider Hero (auto + manuel) ===
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const dotsContainer = document.getElementById('slider-dots');

// Créer les dots
slides.forEach((_, i) => {
  const dot = document.createElement('span');
  dot.addEventListener('click', () => goToSlide(i));
  dotsContainer.appendChild(dot);
});
updateDots();

function goToSlide(index) {
  slides.forEach(slide => slide.classList.remove('active'));
  slides[index].classList.add('active');
  currentSlide = index;
  updateDots();
}

function updateDots() {
  document.querySelectorAll('.slider-dots span').forEach((dot, i) => {
    dot.classList.toggle('active', i === currentSlide);
  });
}

// Auto-avance
setInterval(() => {
  currentSlide = (currentSlide + 1) % slides.length;
  goToSlide(currentSlide);
}, 6000);

// === Menu mobile ===
document.getElementById('menu-toggle').addEventListener('click', () => {
  document.querySelector('.nav').classList.toggle('active');
});

// === Init ===
updateCartUI();

// Afficher le loader lors de la soumission de formulaire ou clic sur "Payer"
document.addEventListener('DOMContentLoaded', () => {
  // Pour les liens vers /paiement
  const paymentLinks = document.querySelectorAll('a[href$="/paiement"]');
  paymentLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      showLoader();
      // Rediriger après un court délai pour la fluidité
      setTimeout(() => {
        window.location.href = link.href;
      }, 300);
    });
  });

  // Optionnel : soumission de formulaire (ex: contact)
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', showLoader);
  }
});

function showLoader() {
  const loader = document.createElement('div');
  loader.className = 'loader-overlay';
  loader.innerHTML = '<div class="loader"></div>';
  document.body.appendChild(loader);
  setTimeout(() => loader.classList.add('active'), 10);
}

// Masquer le loader au chargement de la page (utile après redirection)
window.addEventListener('load', () => {
  const loader = document.querySelector('.loader-overlay');
  if (loader) {
    loader.classList.remove('active');
    setTimeout(() => loader.remove(), 300);
  }
});
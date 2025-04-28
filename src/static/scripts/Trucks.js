document.addEventListener('DOMContentLoaded', () => {
    const productContainer = document.getElementById('product-container');
    const cartItemsContainer = document.getElementById('cartItemsContainer');
    const cartCountElement = document.getElementById('cartCount');
    const cartSidebar = document.getElementById('cartSidebar');
    const cartOverlay = document.getElementById('cartOverlay');
    const cartContent = cartSidebar.querySelector('#cartContent'); 
    const emptyCartMessage = cartContent.querySelector('.empty-cart'); 
    const cartTotalSection = document.getElementById('cartTotalSection');
    const cartTotalAmountElement = document.getElementById('cartTotalAmount');
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton'); 
    const suggestionsContainer = document.getElementById('search-suggestions');
  
    document.addEventListener("DOMContentLoaded", function () {
        const dropbtn = document.querySelector(".dropbtn");
        const dropdown = document.querySelector(".dropdown-content");
        dropbtn.addEventListener("click", function (e) {
            e.preventDefault();
            dropdown.classList.toggle("show");
        });
        // Close dropdown if clicking outside
        window.addEventListener("click", function (e) {
            if (!e.target.matches('.dropbtn')) {
                if (dropdown.classList.contains('show')) {
                    dropdown.classList.remove('show');
                }
            }
        });
    });
    let cart = []; 
    let allProducts = []; 
  // --- Sample Product Data ---
  const productsData = [
      { id: 'bike001', name: 'Truck Door', price: 450.00, image: '32.jpg', description: 'Truck Door Made Of Steel And Aluminum.' },
      { id: 'bike002', name: 'Cargo Box', price: 320.50, image: '33.jpg', description: 'It is Mounted On A Truck chassis And Used To Transport Goods.' },
      { id: 'bike003', name: 'Truck Engine', price: 780.00, image: '34.jpg', description: 'Kia K2700 Truck Engine/Commercial Truck/Sudan.' },
      { id: 'bike004', name: 'Air Compressor', price: 150.00, image: '35.jpg', description: 'Air Compressor, 42 Pieces, German Made.' },
      { id: 'bike005', name: 'Htruck Cabin', price: 1200.00, image: '36.jpg', description: 'Used In: Isuzu, Hino, Mitsubishi Fuso And Other Trucks.' },
      { id: 'bike006', name: 'Truck Protector', price: 550.75, image: '37.jpg', description: 'Protect The Truck Grille From Shocks And Collisions.' },
      { id: 'bike007', name: 'Bosch Injector', price: 410.00, image: '38.jpg', description: 'Original Bosch injector for Komatsu /Cummins4.5-4.9-QSL.' },
      { id: 'bike008', name: 'Truck Battery', price: 680.00, image: '39.jpg', description: 'German-made Batteries, Sizes Available.' } ,
      { id: 'bike009', name: 'Transmission Valve', price: 695.00, image: '40.jpg', description: 'Renault/Volvo Automatic Transmission Valve.' },
      { id: 'bike010', name: 'Taillights', price: 695.00, image: '41.jpg', description: 'Mercedes MP4/MP5 High Quality Taillights.' },
      { id: 'bike011', name: 'Double Disco', price: 695.00, image: '42.jpg', description: 'Mercedes double disco spacer crew quality.' },
      { id: 'bike012', name: 'Air Filter', price: 695.00, image: '43.jpg', description: 'Mercedes Actros MP2 / MP3 Air Filter Original Brand Quality.' },
      { id: 'bike013', name: 'Truck Crane', price: 695.00, image: '44.jpg', description: 'Crane 30 ton - 50 ton, German made.' },
      { id: 'bike014', name: 'Truck Wheel', price: 695.00, image: '46.png', description: 'There Are Different Designs Depending On The Type Of Truck.' },
      { id: 'bike015', name: 'Truck Door Handle', price: 695.00, image: '47.jpg', description: 'Left Side Truck Door Handle Best Quality.' } // Slightly different name/price
  ];

    function initializeProducts() {
        allProducts = productsData; 
        renderProducts(allProducts); 
    }
  
    function renderProducts(productsToRender) {
        if (!productContainer) {
            console.error("Product container not found!");
            return;
        }
        productContainer.innerHTML = '';
  
        if (!productsToRender || productsToRender.length === 0) {
             productContainer.innerHTML = '<p>No products available at the moment.</p>';
             return;
        }
  
        productsToRender.forEach(product => {
            const productElement = document.createElement('div');
            productElement.classList.add('product');
            productElement.setAttribute('data-product-id', product.id); 
  
            const imageSrc = product.image ? `site/img/${product.image}` : 'site/img/placeholder.png'; 
            const priceDisplay = typeof product.price === 'number' ? `${product.price.toFixed(2)} DA` : 'N/A';
  
            productElement.innerHTML = `
                <img src="${imageSrc}" alt="${product.name}" onerror="this.onerror=null; this.src='site/img/placeholder.png';">
                <h2>${product.name}</h2>
                <p>${product.description || ''}</p>
                <div class="price">${priceDisplay}</div>
                <button class="buy-btn" data-id="${product.id}">Add to Cart</button>
            `;
            const addToCartButton = productElement.querySelector('.buy-btn');
            if (addToCartButton) {
                addToCartButton.addEventListener('click', (event) => {
                    const productId = event.target.dataset.id;
                    const productToAdd = allProducts.find(p => p.id === productId);
                    if (productToAdd) {
                         const item = {
                            id: productToAdd.id,
                            name: productToAdd.name,
                            price: productToAdd.price,
                            image: productToAdd.image, 
                            quantity: 1
                        };
                        addToCart(item);
                         event.target.textContent = 'Added!';
                         event.target.disabled = true;
                         event.target.style.backgroundColor = '#28a745';
                         setTimeout(() => {
                            event.target.textContent = 'Add to Cart';
                            event.target.style.backgroundColor = '#da042a';
                            event.target.disabled = false;
                        }, 1000);
                    } else {
                        console.error("Product not found for ID:", productId);
                    }
                });
            }
  
            productContainer.appendChild(productElement);
        });
    }
    function addToCart(itemToAdd) {
        const existingItemIndex = cart.findIndex(item => item.id === itemToAdd.id);
        let itemWasAddedOrIncreased = false;
        let idToHighlight = null;
  
        if (existingItemIndex > -1) {
            cart[existingItemIndex].quantity += 1; 
            itemWasAddedOrIncreased = true;
            idToHighlight = cart[existingItemIndex].id;
        } else {
            const price = typeof itemToAdd.price === 'number' ? itemToAdd.price : 0;
            const newItem = { ...itemToAdd, price: price, quantity: 1 };
            cart.push(newItem);
            itemWasAddedOrIncreased = true;
            idToHighlight = newItem.id;
        }
  
        saveCartToLocalStorage();
        updateCartDisplay(idToHighlight); 
        if (itemWasAddedOrIncreased && cartSidebar && !cartSidebar.classList.contains('active')) {
        }
    }

    function updateCartDisplay(highlightItemId = null) { 
        if (!cartItemsContainer || !cartCountElement || !cartSidebar || !cartTotalSection || !cartTotalAmountElement || !emptyCartMessage || !cartContent) {
            if (!cartCountElement) console.error("Cart count element missing!");
            console.error("One or more critical cart elements are missing!");
            return;
        }
  
        const totalQuantity = cart.reduce((total, item) => total + (item.quantity || 0), 0);
        cartCountElement.textContent = totalQuantity;
        cartItemsContainer.innerHTML = ''; 
  
        if (cart.length === 0) {
            emptyCartMessage.style.display = 'block';
            cartContent.style.justifyContent = 'center'; 
            cartItemsContainer.style.display = 'none';
            cartTotalSection.style.display = 'none';
        } else {
            emptyCartMessage.style.display = 'none';
            cartContent.style.justifyContent = 'flex-start'; 
            cartItemsContainer.style.display = 'block';
            cartTotalSection.style.display = 'block';
  
            let currentTotal = 0;
            let elementToHighlight = null;
  
            cart.forEach((item, index) => {
                const itemPrice = typeof item.price === 'number' ? item.price : 0;
                const itemQuantity = typeof item.quantity === 'number' ? item.quantity : 0;
                const itemTotal = itemPrice * itemQuantity;
                currentTotal += itemTotal;
  
                const cartItemElement = document.createElement('div');
                cartItemElement.classList.add('cart-item');
                cartItemElement.setAttribute('data-item-id', item.id); 
  
                const itemImageSrc = item.image ? `site/img/${item.image}` : 'site/img/placeholder.png'; 
  
                cartItemElement.innerHTML = `
                    <img src="${itemImageSrc}" alt="${item.name || 'Product'}" onerror="this.onerror=null; this.src='site/img/placeholder.png';">
                    <div class="item-details-container">
                        <span class="item-name">${item.name || 'Unknown Item'}</span>
                        <div class="item-details">
                            <span>Qty:
                                <button class="quantity-change" data-index="${index}" data-change="-1" aria-label="Decrease quantity">-</button>
                                ${itemQuantity}
                                <button class="quantity-change" data-index="${index}" data-change="1" aria-label="Increase quantity">+</button>
                            </span>
                            <span class="item-price">${itemTotal.toFixed(2)} DA</span>
                        </div>
                    </div>
                    <button class="remove-item-btn" data-index="${index}" aria-label="Remove item">×</button>
                `;
                const removeButton = cartItemElement.querySelector('.remove-item-btn');
                if (removeButton) {
                     removeButton.addEventListener('click', (event) => {
                        const itemIndex = parseInt(event.currentTarget.dataset.index);
                        if (!isNaN(itemIndex)) {
                            removeItemFromCart(itemIndex);
                        }
                     });
                }
                const quantityButtons = cartItemElement.querySelectorAll('.quantity-change');
                quantityButtons.forEach(button => {
                    button.addEventListener('click', (event) => {
                        const itemIndex = parseInt(event.currentTarget.dataset.index);
                        const change = parseInt(event.currentTarget.dataset.change);
                        if (!isNaN(itemIndex) && !isNaN(change)) {
                            changeItemQuantity(itemIndex, change);
                        }
                    });
                });
  
                cartItemsContainer.appendChild(cartItemElement);
                if (item.id === highlightItemId) {
                    elementToHighlight = cartItemElement; 
                }
            });
            cartTotalAmountElement.textContent = `${currentTotal.toFixed(2)} DA`;
            if (elementToHighlight) {
                elementToHighlight.classList.add('highlight');
                 elementToHighlight.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                setTimeout(() => {
                    if (elementToHighlight) { 
                       elementToHighlight.classList.remove('highlight');
                    }
                }, 1500); 
            }
        }
    }
     function changeItemQuantity(index, change) {
         if (cart[index]) {
            const currentQuantity = cart[index].quantity || 0;
            const newQuantity = currentQuantity + change;
            let idToHighlight = null;
  
            if (newQuantity <= 0) {
                removeItemFromCart(index);
            } else {
                cart[index].quantity = newQuantity;
                 if (change > 0) { 
                     idToHighlight = cart[index].id;
                 }
                saveCartToLocalStorage();
                updateCartDisplay(idToHighlight);
            }
         } else {
             console.error("Attempted to change quantity for non-existent item at index:", index);
         }
     }
    function removeItemFromCart(index) {
        if (index >= 0 && index < cart.length) {
            cart.splice(index, 1);
            saveCartToLocalStorage();
            updateCartDisplay(); 
        } else {
            console.error("Attempted to remove item with invalid index:", index);
        }
    }
    window.toggleCart = function() {
        if (!cartSidebar || !cartOverlay) {
            console.error("Cart sidebar or overlay element not found.");
            return;
        }
        const isActive = cartSidebar.classList.contains('active');
        if (isActive) {
             cartSidebar.classList.remove('active');
             cartOverlay.classList.remove('active');
             const cartIcon = document.querySelector('.cart a');
             if (cartIcon) cartIcon.focus();
        } else {
             updateCartDisplay(); 
             cartSidebar.classList.add('active');
             cartOverlay.classList.add('active');
             const closeButton = cartSidebar.querySelector('.close-btn');
             if (closeButton) {
                 closeButton.focus();
             } else {
                 cartSidebar.focus();
             }
        }
    }
    window.goToShop = function() {
        if (cartSidebar && cartSidebar.classList.contains('active')) {
            toggleCart();
        }
        productContainer?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    window.proceedToCheckout = function() {
         console.log("Proceeding to checkout with items:", JSON.parse(JSON.stringify(cart)));
         if (cart.length === 0) {
             alert("سلة التسوق فارغة. الرجاء إضافة منتجات للمتابعة."); 
             return;
         }
         const totalAmountText = cartTotalAmountElement ? cartTotalAmountElement.textContent : 'N/A';
          alert(`جاري الانتقال إلى الدفع بـ ${cart.length} نوع(أنواع) من المنتجات. الإجمالي: ${totalAmountText}`); 
          window.location.href = "checkout.html";
    }
    function saveCartToLocalStorage() {
        try {
            localStorage.setItem('shoppingCart_bikes', JSON.stringify(cart));
        } catch (e) {
            console.error("Could not save cart to local storage:", e);
        }
    }
  
    function loadCartFromLocalStorage() {
        try {
            const savedCart = localStorage.getItem('shoppingCart_bikes');
            if (savedCart) {
                const parsedCart = JSON.parse(savedCart);
                if (Array.isArray(parsedCart)) {
                     cart = parsedCart.filter(item => item && typeof item.id !== 'undefined' && typeof item.quantity === 'number');
                } else { cart = []; }
            } else { cart = []; }
        } catch (e) {
             console.error("Could not load or parse cart from local storage:", e);
             cart = [];
        }
    }
    function showSuggestions(searchTerm) {
        if (!suggestionsContainer || !allProducts) return;
  
        suggestionsContainer.innerHTML = '';
        if (!searchTerm) {
            suggestionsContainer.style.display = 'none';
            return;
        }
  
        const lowerSearchTerm = searchTerm.toLowerCase();
        const filteredProducts = allProducts.filter(product =>
            (product.name && product.name.toLowerCase().includes(lowerSearchTerm)) ||
            (product.description && product.description.toLowerCase().includes(lowerSearchTerm))
        ).slice(0, 7);
  
        if (filteredProducts.length > 0) {
            filteredProducts.forEach(product => {
                const itemElement = document.createElement('div');
                itemElement.classList.add('suggestion-item');
                const nameHtml = product.name.replace(
                    new RegExp(`(${searchTerm})`, 'gi'),
                    '<strong>$1</strong>'
                );
                itemElement.innerHTML = nameHtml; 
  
                itemElement.setAttribute('data-id', product.id);
                itemElement.addEventListener('click', () => {
                    const productElement = productContainer.querySelector(`.product[data-product-id="${product.id}"]`);
                    if (productElement) {
                        productElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
                         productElement.style.transition = 'outline 0.1s ease-in-out';
                         productElement.style.outline = '2px solid red';
                         setTimeout(() => {
                             productElement.style.outline = 'none';
                         }, 1500);
                    }
                    searchInput.value = product.name;
                    suggestionsContainer.style.display = 'none';
                });
                suggestionsContainer.appendChild(itemElement);
            });
            suggestionsContainer.style.display = 'block';
        } else {
            suggestionsContainer.style.display = 'none'; 
        }
    }
    if (searchInput && suggestionsContainer) {
        searchInput.addEventListener('input', () => {
            showSuggestions(searchInput.value.trim());
        });
  
        document.addEventListener('click', (event) => {
             if (!searchInput.contains(event.target) && !suggestionsContainer.contains(event.target)) {
                 suggestionsContainer.style.display = 'none';
             }
         });
          searchInput.addEventListener('keydown', (event) => {
               if (event.key === 'Escape') {
                  suggestionsContainer.style.display = 'none';
              }
          });
    }
      const performSearch = () => {
         const searchTerm = searchInput ? searchInput.value.trim().toLowerCase() : '';
          suggestionsContainer.style.display = 'none'; 
         if (!searchTerm) {
            renderProducts(allProducts);
            return;
         }
         const filtered = allProducts.filter(p =>
              (p.name && p.name.toLowerCase().includes(searchTerm)) ||
              (p.description && p.description.toLowerCase().includes(searchTerm))
         );
          renderProducts(filtered); 
          if (filtered.length === 0) {
               productContainer.innerHTML = `<p>No products found matching "${searchInput.value}".</p>`;
          }
          console.log(`Performing explicit search for: ${searchTerm}`);
    };
  
    if (searchButton) {
        searchButton.addEventListener('click', performSearch);
    }
    if (searchInput) {
         searchInput.addEventListener('keypress', (event) => {
             if (event.key === 'Enter') {
                  event.preventDefault();
                 performSearch();
             }
         });
    }
  
  
    // --- Initial Setup ---
    loadCartFromLocalStorage();
    initializeProducts();     
    updateCartDisplay();     
  
    // --- Global Event Listeners ---
     document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && cartSidebar && cartSidebar.classList.contains('active')) {
            toggleCart();
        }
    });
  
  });
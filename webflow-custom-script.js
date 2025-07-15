/* 
JAVASCRIPT PERSONALIZADO PARA WEBFLOW
Copiar este código en la sección "Custom Code" > "Before </body> tag" de Webflow
*/

<script>
// Configuración de la aplicación
const CONFIG = {
    // IMPORTANTE: Actualizar esta URL con la URL real de tu backend
    BACKEND_URL: 'http://localhost:5000', // URL del backend local para desarrollo
    API_ENDPOINTS: {
        PRODUCTS: '/api/agilpay/products',
        CREATE_PAYMENT: '/api/agilpay/create-payment'
    }
};

// Estado global de la aplicación
let products = [];
let cart = [];

// Inicialización cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando tienda Agilpay...');
    loadProducts();
    initializeEventListeners();
});

// Cargar productos desde el backend
async function loadProducts() {
    try {
        showLoadingProducts(true);
        
        const response = await fetch(CONFIG.BACKEND_URL + CONFIG.API_ENDPOINTS.PRODUCTS, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const responseData = await response.json();
        
        if (responseData.success) {
            products = responseData.data;
            console.log('Productos cargados:', products.length);
            renderProducts();
        } else {
            throw new Error(responseData.error || 'Error desconocido del servidor');
        }
        
    } catch (error) {
        console.error('Error cargando productos:', error);
        showError('No se pudieron cargar los productos. Por favor, verifica la conexión con el servidor.');
        showLoadingProducts(false);
    }
}

// Mostrar/ocultar indicador de carga de productos
function showLoadingProducts(show) {
    const loadingElement = document.querySelector('.loading-products');
    if (loadingElement) {
        loadingElement.style.display = show ? 'block' : 'none';
    }
}

// Renderizar productos en la interfaz
function renderProducts() {
    const grid = document.getElementById('products-grid');
    if (!grid) {
        console.error('Elemento products-grid no encontrado');
        return;
    }
    
    showLoadingProducts(false);
    grid.innerHTML = '';

    if (products.length === 0) {
        grid.innerHTML = '<p class="text-center">No hay productos disponibles en este momento.</p>';
        return;
    }

    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        productCard.innerHTML = `
            <img src="${product.image}" alt="${product.name}" class="product-image" 
                 onerror="this.src='https://via.placeholder.com/300x200?text=Imagen+No+Disponible'">
            <div class="product-info">
                <h3 class="product-name">${escapeHtml(product.name)}</h3>
                <p class="product-description">${escapeHtml(product.description)}</p>
                <div class="product-price">$${product.price.toFixed(2)}</div>
                <div class="quantity-controls">
                    <button type="button" class="quantity-btn" onclick="changeQuantity(${product.id}, -1)" aria-label="Disminuir cantidad">-</button>
                    <input type="number" class="quantity-input" id="qty-${product.id}" value="1" min="1" max="10" aria-label="Cantidad">
                    <button type="button" class="quantity-btn" onclick="changeQuantity(${product.id}, 1)" aria-label="Aumentar cantidad">+</button>
                </div>
                <button class="add-to-cart-btn" onclick="addToCart(${product.id})" aria-label="Agregar ${escapeHtml(product.name)} al carrito">
                    Agregar al Carrito
                </button>
            </div>
        `;
        grid.appendChild(productCard);
    });
}

// Función para escapar HTML y prevenir XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Cambiar cantidad de producto
function changeQuantity(productId, change) {
    const input = document.getElementById(`qty-${productId}`);
    if (!input) return;
    
    let newValue = parseInt(input.value) + change;
    if (newValue < 1) newValue = 1;
    if (newValue > 10) newValue = 10;
    input.value = newValue;
}

// Agregar producto al carrito
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) {
        showError('Producto no encontrado');
        return;
    }
    
    const quantityInput = document.getElementById(`qty-${productId}`);
    const quantity = quantityInput ? parseInt(quantityInput.value) : 1;
    
    if (quantity < 1 || quantity > 10) {
        showError('Cantidad inválida');
        return;
    }
    
    const existingItem = cart.find(item => item.id === productId);
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({
            id: productId,
            name: product.name,
            price: product.price,
            quantity: quantity
        });
    }
    
    renderCart();
    showNotification(`${product.name} agregado al carrito`);
    
    // Resetear cantidad a 1
    if (quantityInput) {
        quantityInput.value = 1;
    }
}

// Remover producto del carrito
function removeFromCart(productId) {
    const itemIndex = cart.findIndex(item => item.id === productId);
    if (itemIndex > -1) {
        const removedItem = cart[itemIndex];
        cart.splice(itemIndex, 1);
        renderCart();
        showNotification(`${removedItem.name} eliminado del carrito`);
    }
}

// Renderizar carrito
function renderCart() {
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    const checkoutForm = document.getElementById('checkout-form');

    if (!cartItems) return;

    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="empty-cart">Tu carrito está vacío</p>';
        if (cartTotal) cartTotal.style.display = 'none';
        if (checkoutForm) checkoutForm.style.display = 'none';
        return;
    }

    let total = 0;
    cartItems.innerHTML = '';

    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;

        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        cartItem.innerHTML = `
            <div class="cart-item-info">
                <div class="cart-item-name">${escapeHtml(item.name)}</div>
                <div class="cart-item-details">Cantidad: ${item.quantity} × $${item.price.toFixed(2)}</div>
            </div>
            <div class="cart-item-price">
                $${itemTotal.toFixed(2)}
                <button onclick="removeFromCart(${item.id})" class="remove-btn" aria-label="Eliminar ${escapeHtml(item.name)} del carrito">✕</button>
            </div>
        `;
        cartItems.appendChild(cartItem);
    });

    if (cartTotal) {
        cartTotal.innerHTML = `Total: $${total.toFixed(2)}`;
        cartTotal.style.display = 'block';
    }
    
    if (checkoutForm) {
        checkoutForm.style.display = 'block';
    }
}

// Procesar pago
async function processPayment(customerData) {
    try {
        showLoading(true);
        
        const paymentData = {
            customer_name: customerData.name,
            customer_email: customerData.email,
            customer_address: customerData.address,
            items: cart.map(item => ({
                name: item.name,
                price: item.price,
                quantity: item.quantity
            })),
            success_url: window.location.origin + '/success',
            return_url: window.location.origin
        };

        console.log('Enviando datos de pago:', paymentData);

        const response = await fetch(CONFIG.BACKEND_URL + CONFIG.API_ENDPOINTS.CREATE_PAYMENT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(paymentData)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `Error HTTP: ${response.status}`);
        }

        const result = await response.json();
        console.log('Respuesta del backend:', result);

        if (result.success) {
            // Crear formulario para envío a Agilpay
            const form = document.getElementById('agilpay-form') || document.createElement('form');
            form.id = 'agilpay-form';
            form.method = 'post';
            form.action = result.payment_url;
            form.style.display = 'none';
            form.innerHTML = '';

            // Agregar campos del formulario
            Object.keys(result.payment_data).forEach(key => {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = key;
                input.value = result.payment_data[key];
                form.appendChild(input);
            });

            // Asegurar que el formulario esté en el DOM
            if (!document.getElementById('agilpay-form')) {
                document.body.appendChild(form);
            }

            console.log('Redirigiendo a Agilpay...');
            
            // Pequeño delay para mostrar el mensaje de procesamiento
            setTimeout(() => {
                form.submit();
            }, 1000);
            
        } else {
            throw new Error(result.error || 'Error desconocido del servidor');
        }

    } catch (error) {
        console.error('Error procesando pago:', error);
        showError('Error procesando el pago: ' + error.message);
        showLoading(false);
    }
}

// Mostrar/ocultar indicador de carga
function showLoading(show) {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = show ? 'flex' : 'none';
    }
}

// Mostrar notificación de éxito
function showNotification(message) {
    const notification = document.getElementById('notification');
    const messageElement = document.getElementById('notification-message');
    
    if (notification && messageElement) {
        messageElement.textContent = message;
        notification.className = 'notification';
        notification.style.display = 'flex';
        
        // Auto-ocultar después de 3 segundos
        setTimeout(() => {
            hideNotification();
        }, 3000);
    } else {
        // Fallback si no existe el elemento de notificación
        console.log('Notificación:', message);
    }
}

// Mostrar notificación de error
function showError(message) {
    const notification = document.getElementById('notification');
    const messageElement = document.getElementById('notification-message');
    
    if (notification && messageElement) {
        messageElement.textContent = message;
        notification.className = 'notification error';
        notification.style.display = 'flex';
        
        // Auto-ocultar después de 5 segundos para errores
        setTimeout(() => {
            hideNotification();
        }, 5000);
    } else {
        // Fallback
        alert(message);
    }
}

// Ocultar notificación
function hideNotification() {
    const notification = document.getElementById('notification');
    if (notification) {
        notification.style.display = 'none';
    }
}

// Validar email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Inicializar event listeners
function initializeEventListeners() {
    const paymentForm = document.getElementById('payment-form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (cart.length === 0) {
                showError('Tu carrito está vacío');
                return;
            }

            const customerName = document.getElementById('customer-name')?.value?.trim();
            const customerEmail = document.getElementById('customer-email')?.value?.trim();
            const customerAddress = document.getElementById('customer-address')?.value?.trim();

            // Validaciones
            if (!customerName || customerName.length < 2) {
                showError('Por favor ingresa un nombre válido (mínimo 2 caracteres)');
                return;
            }

            if (!customerEmail || !isValidEmail(customerEmail)) {
                showError('Por favor ingresa un correo electrónico válido');
                return;
            }

            if (!customerAddress || customerAddress.length < 5) {
                showError('Por favor ingresa una dirección válida (mínimo 5 caracteres)');
                return;
            }

            const customerData = {
                name: customerName,
                email: customerEmail,
                address: customerAddress
            };

            processPayment(customerData);
        });
    }

    // Event listener para inputs de cantidad
    document.addEventListener('input', function(e) {
        if (e.target.classList.contains('quantity-input')) {
            const value = parseInt(e.target.value);
            if (value < 1) e.target.value = 1;
            if (value > 10) e.target.value = 10;
        }
    });

    // Event listener para tecla Enter en inputs de cantidad
    document.addEventListener('keypress', function(e) {
        if (e.target.classList.contains('quantity-input') && e.key === 'Enter') {
            e.preventDefault();
            const productId = e.target.id.replace('qty-', '');
            addToCart(parseInt(productId));
        }
    });
}

// Función para debugging (solo en desarrollo)
function debugInfo() {
    console.log('Estado actual de la aplicación:');
    console.log('Productos:', products);
    console.log('Carrito:', cart);
    console.log('Configuración:', CONFIG);
}

// Exponer funciones globalmente para uso en HTML
window.changeQuantity = changeQuantity;
window.addToCart = addToCart;
window.removeFromCart = removeFromCart;
window.hideNotification = hideNotification;
window.debugInfo = debugInfo;

// Manejo de errores globales
window.addEventListener('error', function(e) {
    console.error('Error global:', e.error);
    showError('Ha ocurrido un error inesperado. Por favor, recarga la página.');
});

// Manejo de promesas rechazadas
window.addEventListener('unhandledrejection', function(e) {
    console.error('Promesa rechazada:', e.reason);
    showError('Error de conexión. Por favor, verifica tu conexión a internet.');
});

console.log('Script de tienda Agilpay cargado correctamente');
</script>


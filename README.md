[file name] README_ES.md  
[file content begin]  
# Implementation Guide: Agilpay Gateway Integration in Webflow  

**Author:** Javier Sanchez
**Date:** July 15, 2025  
**Version:** 1.0  

## Executive Summary  

This guide provides a comprehensive implementation for integrating the Agilpay payment gateway into websites developed with Webflow. The solution includes a Flask backend that handles communication with Agilpay and a responsive frontend that can be deployed directly in Webflow.  

The integration allows secure payment processing using Agilpay's test credentials, with support for multiple products, a dynamic shopping cart, and fully functional checkout forms.  

## Table of Contents  

1. [Introduction](#introduction)  
2. [Solution Architecture](#solution-architecture)  
3. [Prerequisites](#prerequisites)  
4. [Backend Configuration](#backend-configuration)  
5. [Webflow Implementation](#webflow-implementation)  
6. [Agilpay Configuration](#agilpay-configuration)  
7. [Testing and Validation](#testing-and-validation)  
8. [Production Deployment](#production-deployment)  
9. [Maintenance and Monitoring](#maintenance-and-monitoring)  
10. [Troubleshooting](#troubleshooting)  
11. [References](#references)  

## Introduction  

Agilpay Gateway is a payment processing platform that enables merchants to securely accept credit card, debit card, and ACH payments. Integrating with Webflow presents unique challenges due to the platform's limitations regarding server-side logic and backend processing.  

Webflow is a visual web design platform that allows the creation of responsive websites without writing code. However, for complex integrations like payment gateways that require OAuth2 authentication and secure handling of sensitive data, a hybrid solution combining Webflow's design capabilities with a custom backend is necessary.  

This guide presents a complete solution using a Flask backend to handle communication with Agilpay, while the frontend is implemented directly in Webflow using custom HTML, CSS, and JavaScript. This architecture ensures transaction security while maintaining the design flexibility Webflow offers.  

The solution includes five example products demonstrating different use cases, from basic to premium, with a fully functional shopping cart and an optimized checkout process for user experience.  

## Solution Architecture  

The Agilpay-Webflow integration architecture is based on a clear separation between frontend and backend, with each component having specific, well-defined responsibilities.  

### Key Components  

**Frontend (Webflow):**  
The frontend runs entirely in the user's browser and is built using HTML5, CSS3, and vanilla JavaScript. This component is responsible for visual presentation, user interaction, and shopping cart management. The design is fully responsive and automatically adapts to different screen sizes, from mobile devices to desktop displays.  

The frontend includes a dynamic product catalog loaded from the backend via AJAX calls. Each product contains detailed information such as name, description, price, and image. Users can add products to the cart, adjust quantities, and proceed to checkout intuitively.  

**Backend (Flask):**  
The backend is implemented in Python using the Flask framework, providing a solid and scalable foundation for server operations. This component handles secure communication with Agilpay's servers, including obtaining JWT tokens and constructing payment requests.  

The backend exposes a RESTful API consumed by the frontend to fetch product information and process payments. All sensitive credentials and authentication logic remain on the server, ensuring confidential information is never exposed to the client browser.  

**Agilpay Gateway:**  
Agilpay acts as the external payment processor handling all financial transactions. Communication with Agilpay occurs through two main endpoints: one for OAuth2 authentication and another for payment processing.  

### Data Flow  

The application's data flow follows a well-defined pattern ensuring transaction security and integrity:  

1. **Initial Load:** When the user visits the website, the frontend makes an AJAX request to the backend to fetch the list of available products. This information is displayed in a visually appealing interface allowing users to explore available options.  

2. **Cart Management:** When users add products to the cart, all logic is handled client-side using JavaScript. This provides a smooth and responsive user experience, as no server communication is required for basic cart operations.  

3. **Checkout Process:** When the user proceeds to payment, the frontend collects all necessary information (customer data and cart contents) and sends it to the backend via a secure POST request.  

4. **Agilpay Authentication:** The backend uses configured credentials to obtain a JWT token from Agilpay. This process includes transaction-specific details such as order ID, customer ID, and total amount.  

5. **Payment Request Construction:** Once the token is obtained, the backend builds the complete payment request according to Agilpay's specifications, including all product details, customer information, and return URLs.  

6. **Redirect to Agilpay:** The backend returns all necessary data to the frontend to create an HTML form automatically submitted to Agilpay's servers, redirecting the user to the secure payment page.  

7. **Payment Processing:** Agilpay handles all payment processing, including card validation, transaction authorization, and communication with issuing banks.  

8. **Response and Confirmation:** Once payment is complete, Agilpay redirects the user back to the website using configured URLs, providing transaction status information.  

### Security Considerations  

The architecture implements multiple security layers to protect both customer data and system integrity:  

**Separation of Responsibilities:** Sensitive credentials and authentication logic remain exclusively on the backend, protected by server security measures.  

**Encrypted Communication:** All inter-component communications use HTTPS to ensure data is transmitted securely and cannot be intercepted by third parties.  

**Data Validation:** Both frontend and backend implement data validation to ensure only valid, well-formed requests are processed.  

**Session Tokens:** JWT tokens obtained from Agilpay have limited lifespans and are used only for the specific transaction, minimizing unauthorized use risks.  

## Prerequisites  

Before starting implementation, ensure all technical and configuration prerequisites are met for the integration to function correctly.  

### Technical Requirements  

**Web Server:** A web server capable of running Python applications is required. This can be a dedicated server, VPS (Virtual Private Server), or cloud hosting service like AWS, Google Cloud Platform, or DigitalOcean. The server must have internet access to communicate with Agilpay's services.  

**Python 3.7 or Higher:** The backend application is developed in Python and requires version 3.7 or higher. The latest stable Python version is recommended for compatibility and security.  

**SSL Certificate:** A valid SSL certificate for the backend domain is essential for security and because Agilpay requires all callback URLs to use HTTPS.  

**Custom Domain:** A dedicated domain or subdomain for the backend is needed, configured to point to the server running the Flask application.  

### Agilpay Credentials  

To use Agilpay's services, obtain the following credentials from the provider:  

**Client ID:** Unique identifier assigned by Agilpay for the application. For testing, use "API-001".  

**Client Secret:** Secret key associated with the Client ID. For testing, the value is "Dynapay".  

**Merchant Key:** Merchant key identifying the specific account. For testing, use "TEST-001".  

**Service URLs:** Agilpay provides different URLs for test and production environments:  
- Sandbox Token URL: https://sandbox-webapi.agilpay.net/oauth/paymenttoken  
- Sandbox Payment URL: https://sandbox-webpay.agilpay.net/Payment  
- Production Token URL: https://webapi.agilpay.net/oauth/paymenttoken  
- Production Payment URL: https://webpay.agilpay.net/Payment  

### Development Tools  

**Code Editor:** Use a modern code editor like Visual Studio Code, PyCharm, or Sublime Text for easier development and debugging.  

**Git Client:** To manage source code and facilitate deployment, having Git installed and configured is recommended.  

**Testing Tools:** For integration validation, tools like Postman or curl are useful for API testing.  

## Backend Configuration  

Backend configuration is a critical process establishing the foundation for the entire integration. Below are all necessary steps to correctly configure the Flask server.  

### Environment Setup  

The first step is preparing the development environment on the server, including installing Python, creating a virtual environment, and installing required dependencies.  

**Virtual Environment Creation:**  
```bash  
python3 -m venv agilpay-backend  
cd agilpay-backend  
source bin/activate  # On Linux/Mac  
# or  
Scripts\activate  # On Windows  
```  

Using a virtual environment is a recommended practice to isolate project dependencies and avoid conflicts with other Python applications on the system.  

**Dependency Installation:**  
```bash  
pip install flask requests python-dotenv  
```  

These dependencies provide basic required functionalities:  
- Flask: Python web framework  
- Requests: HTTP request library  
- Python-dotenv: For managing environment variables  

### Project Structure  

Code organization is fundamental for maintaining a scalable and maintainable project. The recommended structure is:  

```  
agilpay-backend/  
├── src/  
│   ├── routes/  
│   │   ├── __init__.py  
│   │   └── agilpay.py  
│   ├── static/  
│   │   └── index.html  
│   ├── models/  
│   │   └── __init__.py  
│   └── main.py  
├── requirements.txt  
├── .env  
└── README.md  
```  

This structure clearly separates different code responsibilities, facilitating maintenance and future scalability.  

### Environment Variable Configuration  

To maintain credential security, using environment variables is essential. Create a `.env` file in the project root with:  

```  
AGILPAY_CLIENT_ID=API-001  
AGILPAY_CLIENT_SECRET=Dynapay  
AGILPAY_MERCHANT_KEY=TEST-001  
AGILPAY_TOKEN_URL=https://sandbox-webapi.agilpay.net/oauth/paymenttoken  
AGILPAY_PAYMENT_URL=https://sandbox-webpay.agilpay.net/Payment  
FLASK_ENV=development  
FLASK_DEBUG=True  
```  

Never include the `.env` file in version control to avoid exposing sensitive credentials.  

### Backend Code Implementation  

The main `main.py` file configures the Flask application and registers necessary routes:  

```python  
import os  
from flask import Flask, send_from_directory  
from flask_cors import CORS  
from src.routes.agilpay import agilpay_bp  

app = Flask(__name__, static_folder='src/static')  
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')  

# Enable CORS to allow requests from Webflow  
CORS(app)  

# Register blueprints  
app.register_blueprint(agilpay_bp, url_prefix='/api/agilpay')  

@app.route('/')  
def serve_frontend():  
    return send_from_directory(app.static_folder, 'index.html')  

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000, debug=True)  
```  

CORS configuration is essential to allow frontend hosted on Webflow to communicate with the backend.  

### Agilpay Route Implementation  

The `src/routes/agilpay.py` file contains all Agilpay-specific integration logic:  

```python  
from flask import Blueprint, request, jsonify  
import requests  
import json  
import uuid  
import os  

agilpay_bp = Blueprint('agilpay', __name__)  

# Configuration from environment variables  
AGILPAY_CONFIG = {  
    'client_id': os.environ.get('AGILPAY_CLIENT_ID'),  
    'client_secret': os.environ.get('AGILPAY_CLIENT_SECRET'),  
    'merchant_key': os.environ.get('AGILPAY_MERCHANT_KEY'),  
    'token_url': os.environ.get('AGILPAY_TOKEN_URL'),  
    'payment_url': os.environ.get('AGILPAY_PAYMENT_URL')  
}  

def get_oauth_token(order_id, customer_id, amount):  
    """Obtains JWT token from Agilpay"""  
    try:  
        payload = {  
            'grant_type': 'client_credentials',  
            'client_id': AGILPAY_CONFIG['client_id'],  
            'client_secret': AGILPAY_CONFIG['client_secret'],  
            'orderId': order_id,  
            'customerId': customer_id,  
            'amount': amount  
        }  
          
        headers = {'Content-Type': 'application/json'}  
          
        response = requests.post(  
            AGILPAY_CONFIG['token_url'],  
            data=json.dumps(payload),  
            headers=headers,  
            timeout=30  
        )  
          
        if response.status_code == 200:  
            data = response.json()  
            return data.get('access_token')  
        else:  
            print(f"Error obtaining token: {response.status_code} - {response.text}")  
            return None  
              
    except Exception as e:  
        print(f"Exception obtaining token: {str(e)}")  
        return None  
```  

This function handles OAuth2 authentication with Agilpay, including appropriate error and timeout handling.  

### Product Configuration  

To demonstrate functionality, an endpoint returning a sample product list is included:  

```python  
@agilpay_bp.route('/products', methods=['GET'])  
def get_products():  
    """Returns available product list"""  
    products = [  
        {  
            'id': 1,  
            'name': 'Premium Product A',  
            'description': 'Detailed description of premium product A',  
            'price': 99.99,  
            'image': 'https://via.placeholder.com/300x200?text=Product+A'  
        },  
        {  
            'id': 2,  
            'name': 'Standard Product B',  
            'description': 'Detailed description of standard product B',  
            'price': 59.99,  
            'image': 'https://via.placeholder.com/300x200?text=Product+B'  
        },  
        # ... more products  
    ]  
      
    return jsonify(products)  
```  

In a real implementation, this information would come from a database or inventory management system.  

## Webflow Implementation  

Webflow implementation requires careful integration of custom code within the platform. Webflow allows adding custom HTML, CSS, and JavaScript through embedded code elements, page settings, and site settings.  

### Initial Webflow Configuration  

**Accessing Configuration Panel:**  
To begin implementation, access the site configuration panel in Webflow by navigating to project settings and selecting the "Custom Code" tab. This section allows adding code that will run on all site pages or specific pages.  

**Backend URL Configuration:**  
Before implementing frontend code, correctly configure backend URLs. These URLs must be updated in the JavaScript code to reflect the actual backend server location.  

### HTML Structure for Webflow  

HTML code should use native Webflow elements where possible, supplemented with custom code when necessary. The recommended structure includes:  

**Product Section:**  
```html  
<div class="products-section">  
    <div class="container">  
        <h2 class="section-title">Our Products</h2>  
        <div class="products-grid" id="products-grid">  
            <!-- Products will load dynamically -->  
        </div>  
    </div>  
</div>  
```  

This structure uses CSS classes that can be styled directly in Webflow's visual designer, maintaining platform design flexibility.  

**Cart Section:**  
```html  
<div class="cart-section">  
    <div class="container">  
        <h3 class="cart-title">Shopping Cart</h3>  
        <div id="cart-items">  
            <p class="empty-cart">Your cart is empty</p>  
        </div>  
        <div class="cart-total" id="cart-total" style="display: none;">  
            Total: $0.00  
        </div>  
    </div>  
</div>  
```  

**Checkout Form:**  
```html  
<div class="checkout-form" id="checkout-form" style="display: none;">  
    <div class="container">  
        <h3 class="form-title">Billing Information</h3>  
        <form id="payment-form">  
            <div class="form-group">  
                <label class="form-label" for="customer-name">Full Name *</label>  
                <input type="text" id="customer-name" class="form-input" required>  
            </div>  
            <div class="form-group">  
                <label class="form-label" for="customer-email">Email *</label>  
                <input type="email" id="customer-email" class="form-input" required>  
            </div>  
            <div class="form-group">  
                <label class="form-label" for="customer-address">Address *</label>  
                <input type="text" id="customer-address" class="form-input" required>  
            </div>  
            <button type="submit" class="checkout-btn" id="checkout-btn">  
                Proceed to Payment with Agilpay  
            </button>  
        </form>  
    </div>  
</div>  
```  

### Custom CSS Styles  

Custom CSS should be added in the site's "Custom Code" section in Webflow. These styles complement the visual design created in the designer and provide specific functionality needed for the store:  

```css  
/* Base store styles */  
.products-grid {  
    display: grid;  
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));  
    gap: 2rem;  
    margin-bottom: 3rem;  
}  

.product-card {  
    background: white;  
    border-radius: 12px;  
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  
    overflow: hidden;  
    transition: transform 0.3s ease, box-shadow 0.3s ease;  
}  

.product-card:hover {  
    transform: translateY(-5px);  
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);  
}  

.product-image {  
    width: 100%;  
    height: 200px;  
    object-fit: cover;  
}  

.product-info {  
    padding: 1.5rem;  
}  

.product-name {  
    font-size: 1.3rem;  
    font-weight: 600;  
    margin-bottom: 0.5rem;  
    color: #333;  
}  

.product-price {  
    font-size: 1.5rem;  
    font-weight: 700;  
    color: #667eea;  
    margin-bottom: 1rem;  
}  

.quantity-controls {  
    display: flex;  
    align-items: center;  
    gap: 0.5rem;  
    margin-bottom: 1rem;  
}  

.quantity-btn {  
    background: #667eea;  
    color: white;  
    border: none;  
    width: 30px;  
    height: 30px;  
    border-radius: 50%;  
    cursor: pointer;  
    font-size: 1rem;  
    display: flex;  
    align-items: center;  
    justify-content: center;  
}  

.add-to-cart-btn {  
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);  
    color: white;  
    border: none;  
    padding: 0.75rem 1.5rem;  
    border-radius: 8px;  
    cursor: pointer;  
    font-size: 1rem;  
    font-weight: 600;  
    width: 100%;  
    transition: opacity 0.3s ease;  
}  

/* Cart styles */  
.cart-section {  
    background: white;  
    border-radius: 12px;  
    padding: 2rem;  
    margin: 2rem 0;  
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  
}  

.cart-item {  
    display: flex;  
    justify-content: space-between;  
    align-items: center;  
    padding: 1rem 0;  
    border-bottom: 1px solid #eee;  
}  

.cart-total {  
    font-size: 1.3rem;  
    font-weight: 700;  
    text-align: right;  
    margin-top: 1rem;  
    color: #667eea;  
}  

/* Form styles */  
.checkout-form {  
    background: white;  
    border-radius: 12px;  
    padding: 2rem;  
    margin: 2rem 0;  
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  
}  

.form-group {  
    margin-bottom: 1.5rem;  
}  

.form-label {  
    display: block;  
    margin-bottom: 0.5rem;  
    font-weight: 600;  
    color: #333;  
}  

.form-input {  
    width: 100%;  
    padding: 0.75rem;  
    border: 1px solid #ddd;  
    border-radius: 8px;  
    font-size: 1rem;  
}  

.form-input:focus {  
    outline: none;  
    border-color: #667eea;  
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);  
}  

.checkout-btn {  
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);  
    color: white;  
    border: none;  
    padding: 1rem 2rem;  
    border-radius: 8px;  
    cursor: pointer;  
    font-size: 1.1rem;  
    font-weight: 600;  
    width: 100%;  
    transition: opacity 0.3s ease;  
}  

/* Responsive styles */  
@media (max-width: 768px) {  
    .products-grid {  
        grid-template-columns: 1fr;  
    }  
      
    .cart-item {  
        flex-direction: column;  
        align-items: flex-start;  
        gap: 0.5rem;  
    }  
}  
```  

### JavaScript Functionality  

The JavaScript code is the core of the store's functionality. It should be added in the "Before </body> tag" section in site settings to ensure it runs after all HTML content loads:  

```javascript  
// Application configuration  
const CONFIG = {  
    BACKEND_URL: 'https://your-backend.com', // Update with actual backend URL  
    API_ENDPOINTS: {  
        PRODUCTS: '/api/agilpay/products',  
        CREATE_PAYMENT: '/api/agilpay/create-payment'  
    }  
};  

// Application state  
let products = [];  
let cart = [];  

// Initialization on page load  
document.addEventListener('DOMContentLoaded', function() {  
    loadProducts();  
    initializeEventListeners();  
});  

// Load products from backend  
async function loadProducts() {  
    try {  
        const response = await fetch(CONFIG.BACKEND_URL + CONFIG.API_ENDPOINTS.PRODUCTS);  
        if (!response.ok) {  
            throw new Error('Error loading products');  
        }  
        products = await response.json();  
        renderProducts();  
    } catch (error) {  
        console.error('Error loading products:', error);  
        showError('Could not load products. Please try again later.');  
    }  
}  

// Render products in the interface  
function renderProducts() {  
    const grid = document.getElementById('products-grid');  
    if (!grid) return;  
      
    grid.innerHTML = '';  

    products.forEach(product => {  
        const productCard = document.createElement('div');  
        productCard.className = 'product-card';  
        productCard.innerHTML = `  
            <img src="${product.image}" alt="${product.name}" class="product-image">  
            <div class="product-info">  
                <h3 class="product-name">${product.name}</h3>  
                <p class="product-description">${product.description}</p>  
                <div class="product-price">$${product.price.toFixed(2)}</div>  
                <div class="quantity-controls">  
                    <button type="button" class="quantity-btn" onclick="changeQuantity(${product.id}, -1)">-</button>  
                    <input type="number" class="quantity-input" id="qty-${product.id}" value="1" min="1" max="10">  
                    <button type="button" class="quantity-btn" onclick="changeQuantity(${product.id}, 1)">+</button>  
                </div>  
                <button class="add-to-cart-btn" onclick="addToCart(${product.id})">  
                    Add to Cart  
                </button>  
            </div>  
        `;  
        grid.appendChild(productCard);  
    });  
}  

// Shopping cart management  
function addToCart(productId) {  
    const product = products.find(p => p.id === productId);  
    if (!product) return;  
      
    const quantity = parseInt(document.getElementById(`qty-${productId}`).value);  
      
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
    showNotification('Product added to cart');  
}  

function renderCart() {  
    const cartItems = document.getElementById('cart-items');  
    const cartTotal = document.getElementById('cart-total');  
    const checkoutForm = document.getElementById('checkout-form');  

    if (!cartItems) return;  

    if (cart.length === 0) {  
        cartItems.innerHTML = '<p class="empty-cart">Your cart is empty</p>';  
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
            <div>  
                <strong>${item.name}</strong><br>  
                Quantity: ${item.quantity} × $${item.price.toFixed(2)}  
            </div>  
            <div>  
                $${itemTotal.toFixed(2)}  
                <button onclick="removeFromCart(${item.id})" style="margin-left: 10px; color: red; background: none; border: none; cursor: pointer;">✕</button>  
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

// Payment processing  
async function processPayment(customerData) {  
    try {  
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

        const response = await fetch(CONFIG.BACKEND_URL + CONFIG.API_ENDPOINTS.CREATE_PAYMENT, {  
            method: 'POST',  
            headers: {  
                'Content-Type': 'application/json'  
            },  
            body: JSON.stringify(paymentData)  
        });  

        if (!response.ok) {  
            throw new Error('Server response error');  
        }  

        const result = await response.json();  

        if (result.success) {  
            // Create form for submission to Agilpay  
            const form = document.createElement('form');  
            form.method = 'post';  
            form.action = result.payment_url;  
            form.style.display = 'none';  

            // Add form fields  
            Object.keys(result.payment_data).forEach(key => {  
                const input = document.createElement('input');  
                input.type = 'hidden';  
                input.name = key;  
                input.value = result.payment_data[key];  
                form.appendChild(input);  
            });  

            document.body.appendChild(form);  
            form.submit();  
        } else {  
            throw new Error(result.error || 'Unknown error');  
        }  

    } catch (error) {  
        console.error('Error processing payment:', error);  
        showError('Payment processing error: ' + error.message);  
    }  
}  

// Helper functions  
function showError(message) {  
    alert(message); // In a real implementation, use a more elegant notification system  
}  

function showNotification(message) {  
    // Implement notification system  
    console.log(message);  
}  

// Initialize event listeners  
function initializeEventListeners() {  
    const paymentForm = document.getElementById('payment-form');  
    if (paymentForm) {  
        paymentForm.addEventListener('submit', function(e) {  
            e.preventDefault();  
              
            if (cart.length === 0) {  
                showError('Your cart is empty');  
                return;  
            }  

            const customerData = {  
                name: document.getElementById('customer-name').value,  
                email: document.getElementById('customer-email').value,  
                address: document.getElementById('customer-address').value  
            };  

            if (!customerData.name || !customerData.email || !customerData.address) {  
                showError('Please complete all required fields');  
                return;  
            }  

            processPayment(customerData);  
        });  
    }  
}  
```  

### Webflow Element Configuration  

**Embedded Code Elements:**  
To implement specific store sections, use "Embed" elements in Webflow. These allow inserting custom HTML directly into the visual design.  

**ID and Class Configuration:**  
Ensure HTML elements in Webflow have correct IDs and classes matching the JavaScript code. This can be done using the element configuration panel in the visual designer.  

**Responsive Design:**  
Webflow automatically handles many responsive design aspects, but testing functionality across different screen sizes is important to ensure optimal user experience on all devices.  

## Agilpay Configuration  

Proper Agilpay configuration is fundamental for secure and effective communication with the payment gateway. This section details all aspects needed to establish secure communication with Agilpay.  

### Test Credentials  

For development and testing environments, Agilpay provides specific credentials allowing transaction simulation without processing real payments. Test credentials used in this implementation are:  

**Client ID:** API-001  
**Client Secret:** Dynapay  
**Merchant Key:** TEST-001  

These credentials are configured to work exclusively with Agilpay's sandbox servers and will not process real transactions. Never use these credentials in production.  

### Service URLs  

Agilpay maintains separate environments for development and production, each with its own service URLs:  

**Sandbox Environment (Testing):**  
- Token URL: https://sandbox-webapi.agilpay.net/oauth/paymenttoken  
- Payment URL: https://sandbox-webpay.agilpay.net/Payment  

**Production Environment:**  
- Token URL: https://webapi.agilpay.net/oauth/paymenttoken  
- Payment URL: https://webpay.agilpay.net/Payment  

### Webhook Configuration  

To receive transaction status notifications, webhooks must be configured in the Agilpay account. These allow Agilpay to automatically notify the system when a transaction completes, a payment is rejected, or any other relevant event occurs.  

The webhook endpoint must be implemented in the backend and configured in Agilpay's admin panel. An example implementation would be:  

```python  
@agilpay_bp.route('/webhook', methods=['POST'])  
def handle_webhook():  
    """Handles Agilpay webhook notifications"""  
    try:  
        data = request.get_json()  
          
        # Validate webhook authenticity  
        if not validate_webhook_signature(data):  
            return jsonify({'error': 'Invalid signature'}), 401  
          
        # Process notification based on event type  
        event_type = data.get('event_type')  
          
        if event_type == 'payment_completed':  
            handle_payment_completed(data)  
        elif event_type == 'payment_failed':  
            handle_payment_failed(data)  
          
        return jsonify({'status': 'received'}), 200  
          
    except Exception as e:  
        print(f"Error processing webhook: {str(e)}")  
        return jsonify({'error': 'Internal server error'}), 500  
```  

## Testing and Validation  

A thorough testing process is essential to ensure the integration works correctly in all possible scenarios. This section describes different test types that should be performed.  

### Functionality Testing  

**Product Catalog Tests:**  
Verify products load correctly from the backend and display in the user interface with all necessary information (name, description, price, image).  

**Shopping Cart Tests:**  
Validate users can add products to the cart, modify quantities, remove products, and that the total calculates correctly in real-time.  

**Checkout Form Tests:**  
Ensure field validation works correctly, appropriate error messages display for invalid data, and the form submits correctly when all fields are complete.  

**Agilpay Integration Tests:**  
Verify the backend can successfully obtain JWT tokens, payment requests are built correctly according to Agilpay specifications, and redirection to the payment gateway works without issues.  

### Security Testing  

**Data Validation:**  
Test the system correctly handles malformed or malicious data, including SQL injection, XSS (Cross-Site Scripting), and other common attack vectors.  

**Authentication and Authorization:**  
Verify Agilpay credentials remain secure on the backend and are never exposed to the client, and JWT tokens are handled correctly with appropriate expiration times.  

**Secure Communication:**  
Ensure all communications use HTTPS and sensitive data is transmitted encrypted.  

### Performance Testing  

**Product Loading:**  
Measure response time for loading the product list and optimize if necessary.  

**Payment Processing:**  
Evaluate total time from user form submission to redirection to Agilpay.  

**Concurrency Handling:**  
Test system behavior when multiple users perform transactions simultaneously.  

### Compatibility Testing  

**Web Browsers:**  
Verify the application works correctly in popular browsers (Chrome, Firefox, Safari, Edge) and different versions.  

**Mobile Devices:**  
Test functionality on mobile devices and tablets to ensure optimal user experience across all platforms.  

**Screen Resolutions:**  
Validate responsive design works correctly across different resolutions and screen orientations.  

## Production Deployment  

Production deployment requires additional security, performance, and reliability considerations. This section provides a complete guide for moving the integration to a production environment.  

### Production Environment Preparation  

**Production Server:**  
Select a reliable hosting provider offering high availability, automatic backups, and technical support. Recommended options include AWS, Google Cloud Platform, DigitalOcean, or Heroku.  

**SSL Configuration:**  
Obtain and install a valid SSL certificate for the backend domain. This is mandatory for communication with Agilpay and essential for customer data security.  

**Production Environment Variables:**  
Update environment variables to use Agilpay production credentials and configure the Flask environment for production:  

```  
FLASK_ENV=production  
FLASK_DEBUG=False  
AGILPAY_CLIENT_ID=[Actual production credential]  
AGILPAY_CLIENT_SECRET=[Actual production credential]  
AGILPAY_MERCHANT_KEY=[Actual production credential]  
AGILPAY_TOKEN_URL=https://webapi.agilpay.net/oauth/paymenttoken  
AGILPAY_PAYMENT_URL=https://webpay.agilpay.net/Payment  
```  

### Web Server Configuration  

**WSGI Server:**  
For production, using a WSGI server like Gunicorn is recommended instead of Flask's development server:  

```bash  
pip install gunicorn  
gunicorn --bind 0.0.0.0:5000 --workers 4 src.main:app  
```  

**Reverse Proxy:**  
Configure a reverse proxy like Nginx to handle HTTP requests and provide additional functionalities like compression, caching, and load balancing.  

**Monitoring and Logs:**  
Implement a monitoring system to track application performance and configure detailed logs to facilitate troubleshooting.  

### Webflow Updates  

**Backend URLs:**  
Update all backend URL references in Webflow's JavaScript code to point to the production server.  

**CORS Configuration:**  
Ensure the backend is configured to accept requests from Webflow's production domain.  

**Integration Testing:**  
Perform complete integration tests in the production environment before making the site public.  

## Maintenance and Monitoring  

Proactive maintenance is essential for ensuring continuous and secure integration operation. This section describes best practices for long-term maintenance.  

### Performance Monitoring  

**Key Metrics:**  
Establish metrics to monitor application performance, including API response times, transaction success rates, and service availability.  

**Automatic Alerts:**  
Configure alerts to automatically notify when issues are detected, such as Agilpay communication errors, high response times, or server failures.  

**Log Analysis:**  
Implement a log analysis system to identify patterns, detect potential issues, and optimize performance.  

### Security Updates  

**Dependencies:**  
Keep all Python dependencies updated to include the latest security fixes:  

```bash  
pip list --outdated  
pip install --upgrade [package_name]  
```  

**SSL Certificates:**  
Monitor SSL certificate expiration dates and renew them before they expire.  

**Credentials:**  
Regularly rotate access credentials and maintain a record of all changes.  

### Backups and Recovery  

**Code Backup:**  
Maintain source code in a version control system like Git, with regular backups in multiple locations.  

**Configuration Backup:**  
Perform regular backups of server configuration and environment variables.  

**Recovery Plan:**  
Develop and regularly test a disaster recovery plan enabling quick service restoration in case of failures.  

## Troubleshooting  

This section provides solutions for common issues that may arise during integration implementation and operation.  

### Authentication Issues  

**Error: "Invalid client credentials"**  
This error indicates Agilpay credentials are invalid or misconfigured.  

*Solution:*  
- Verify environment variable credentials exactly match those provided by Agilpay  
- Ensure correct credentials are used for the environment (sandbox vs production)  
- Check if credentials have expired  

**Error: "Token expired"**  
Agilpay JWT tokens have limited lifespans and may expire.  

*Solution:*  
- Implement logic to automatically renew tokens upon expiration  
- Verify server time is correctly synchronized  
- Reduce time between token acquisition and use  

### Connectivity Issues  

**Error: "Connection timeout"**  
Network issues can cause timeouts in Agilpay requests.  

*Solution:*  
- Verify server internet connectivity  
- Increase HTTP request timeout  
- Implement automatic retries with exponential backoff  

**Error: "CORS policy"**  
CORS issues may prevent Webflow from communicating with the backend.  

*Solution:*  
- Verify CORS is enabled in the backend  
- Ensure Webflow's domain is included in allowed origins  
- Check required headers are correctly configured  

### Data Issues  

**Error: "Invalid payment data"**  
Agilpay may reject requests with malformed data.  

*Solution:*  
- Validate all data before sending to Agilpay  
- Verify amounts are in correct format (decimal numbers)  
- Ensure all required fields are present  

**Error: "Product not found"**  
Product loading errors may indicate backend API issues.  

*Solution:*  
- Verify the products endpoint is functioning correctly  
- Check server logs for specific errors  
- Validate product data structure is correct  

## References  

[1] Official Agilpay Gateway Documentation: https://agilisa.atlassian.net/wiki/spaces/DOCUMENTAT/pages/38273121/Payment+Request  

[2] Agilpay WooCommerce Example Repository: https://github.com/agilisa-technologies/woocommerce  

[3] Webflow Custom Code Documentation: https://university.webflow.com/lesson/custom-code-in-the-head-and-body-tags  

[4] Flask Documentation: https://flask.palletsprojects.com/  

[5] Requests Library Documentation: https://docs.python-requests.org/  

[6] OAuth 2.0 RFC: https://tools.ietf.org/html/rfc6749  

[7] CORS Documentation: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS  

[8] JavaScript Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API  

---  

**Note:** This documentation is based on specifications and examples provided by Agilisa Technologies. For production credentials and additional technical support, contact the Agilpay team directly.  

**Author:** Javier Sanchez  
**Last Updated:** July 15, 2025  
**Document Version:** 1.0  
[file content end]
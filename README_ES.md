# Guía de Implementación: Integración de Agilpay Gateway en Webflow

**Autor:** Javier Sanchez
**Fecha:** 15 de Julio, 2025  
**Versión:** 1.0

## Resumen Ejecutivo

Esta guía proporciona una implementación completa para integrar el gateway de pago Agilpay en sitios web desarrollados con Webflow. La solución incluye un backend en Flask que maneja la comunicación con Agilpay y un frontend responsivo que puede ser implementado directamente en Webflow.

La integración permite procesar pagos de manera segura utilizando las credenciales de prueba de Agilpay, con soporte para múltiples productos, carrito de compras dinámico y formularios de checkout completamente funcionales.

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura de la Solución](#arquitectura-de-la-solución)
3. [Requisitos Previos](#requisitos-previos)
4. [Configuración del Backend](#configuración-del-backend)
5. [Implementación en Webflow](#implementación-en-webflow)
6. [Configuración de Agilpay](#configuración-de-agilpay)
7. [Pruebas y Validación](#pruebas-y-validación)
8. [Despliegue en Producción](#despliegue-en-producción)
9. [Mantenimiento y Monitoreo](#mantenimiento-y-monitoreo)
10. [Solución de Problemas](#solución-de-problemas)
11. [Referencias](#referencias)




## Introducción

Agilpay Gateway es una plataforma de procesamiento de pagos que permite a los comerciantes aceptar pagos con tarjetas de crédito, débito y ACH de manera segura. La integración con Webflow presenta desafíos únicos debido a las limitaciones de la plataforma en cuanto a lógica de servidor y procesamiento backend.

Webflow es una plataforma de diseño web visual que permite crear sitios web responsivos sin necesidad de escribir código. Sin embargo, para integraciones complejas como gateways de pago que requieren autenticación OAuth2 y manejo seguro de datos sensibles, es necesario implementar una solución híbrida que combine las capacidades de diseño de Webflow con un backend personalizado.

Esta guía presenta una solución completa que utiliza un backend en Flask para manejar la comunicación con Agilpay, mientras que el frontend se implementa directamente en Webflow utilizando HTML, CSS y JavaScript personalizados. Esta arquitectura garantiza la seguridad de las transacciones mientras mantiene la flexibilidad de diseño que ofrece Webflow.

La solución incluye cinco productos de ejemplo que demuestran diferentes casos de uso, desde productos básicos hasta premium, con un carrito de compras completamente funcional y un proceso de checkout optimizado para la experiencia del usuario.

## Arquitectura de la Solución

La arquitectura de la integración Agilpay-Webflow se basa en una separación clara entre el frontend y el backend, donde cada componente tiene responsabilidades específicas y bien definidas.

### Componentes Principales

**Frontend (Webflow):**
El frontend se ejecuta completamente en el navegador del usuario y está construido utilizando HTML5, CSS3 y JavaScript vanilla. Este componente es responsable de la presentación visual, la interacción del usuario y la gestión del carrito de compras. El diseño es completamente responsivo y se adapta automáticamente a diferentes tamaños de pantalla, desde dispositivos móviles hasta pantallas de escritorio.

El frontend incluye un catálogo de productos dinámico que se carga desde el backend mediante llamadas AJAX. Cada producto incluye información detallada como nombre, descripción, precio e imagen. Los usuarios pueden agregar productos al carrito, modificar cantidades y proceder al checkout de manera intuitiva.

**Backend (Flask):**
El backend está implementado en Python utilizando el framework Flask, que proporciona una base sólida y escalable para manejar las operaciones del servidor. Este componente es responsable de la comunicación segura con los servidores de Agilpay, incluyendo la obtención de tokens JWT y la construcción de solicitudes de pago.

El backend expone una API RESTful que el frontend consume para obtener información de productos y procesar pagos. Todas las credenciales sensibles y la lógica de autenticación se mantienen en el servidor, garantizando que la información confidencial nunca se exponga al navegador del cliente.

**Gateway Agilpay:**
Agilpay actúa como el procesador de pagos externo que maneja todas las transacciones financieras. La comunicación con Agilpay se realiza mediante dos endpoints principales: uno para la autenticación OAuth2 y otro para el procesamiento de pagos.

### Flujo de Datos

El flujo de datos en la aplicación sigue un patrón bien definido que garantiza la seguridad y la integridad de las transacciones:

1. **Carga Inicial:** Cuando el usuario visita el sitio web, el frontend realiza una solicitud AJAX al backend para obtener la lista de productos disponibles. Esta información se presenta en una interfaz visual atractiva que permite al usuario explorar las opciones disponibles.

2. **Gestión del Carrito:** Cuando el usuario agrega productos al carrito, toda la lógica se maneja en el lado del cliente utilizando JavaScript. Esto proporciona una experiencia de usuario fluida y responsiva, ya que no requiere comunicación con el servidor para operaciones básicas del carrito.

3. **Proceso de Checkout:** Cuando el usuario decide proceder al pago, el frontend recopila toda la información necesaria (datos del cliente y contenido del carrito) y la envía al backend mediante una solicitud POST segura.

4. **Autenticación con Agilpay:** El backend utiliza las credenciales configuradas para obtener un token JWT de Agilpay. Este proceso incluye información específica de la transacción como el ID de la orden, el ID del cliente y el monto total.

5. **Construcción de la Solicitud de Pago:** Una vez obtenido el token, el backend construye la solicitud de pago completa según las especificaciones de Agilpay, incluyendo todos los detalles de los productos, información del cliente y URLs de retorno.

6. **Redirección a Agilpay:** El backend devuelve al frontend todos los datos necesarios para crear un formulario HTML que se envía automáticamente a los servidores de Agilpay, redirigiendo al usuario a la página de pago segura.

7. **Procesamiento del Pago:** Agilpay maneja todo el procesamiento del pago, incluyendo la validación de tarjetas, autorización de transacciones y comunicación con los bancos emisores.

8. **Respuesta y Confirmación:** Una vez completado el pago, Agilpay redirige al usuario de vuelta al sitio web utilizando las URLs configuradas, proporcionando información sobre el estado de la transacción.

### Consideraciones de Seguridad

La arquitectura implementa múltiples capas de seguridad para proteger tanto los datos del cliente como la integridad del sistema:

**Separación de Responsabilidades:** Las credenciales sensibles y la lógica de autenticación se mantienen exclusivamente en el backend, donde están protegidas por las medidas de seguridad del servidor.

**Comunicación Encriptada:** Todas las comunicaciones entre componentes utilizan HTTPS para garantizar que los datos se transmitan de manera segura y no puedan ser interceptados por terceros.

**Validación de Datos:** Tanto el frontend como el backend implementan validación de datos para garantizar que solo se procesen solicitudes válidas y bien formadas.

**Tokens de Sesión:** Los tokens JWT obtenidos de Agilpay tienen una duración limitada y se utilizan únicamente para la transacción específica, minimizando el riesgo de uso no autorizado.


## Requisitos Previos

Antes de comenzar con la implementación, es necesario asegurar que se cumplan todos los requisitos técnicos y de configuración necesarios para el correcto funcionamiento de la integración.

### Requisitos Técnicos

**Servidor Web:** Se requiere un servidor web capaz de ejecutar aplicaciones Python. Esto puede ser un servidor dedicado, un VPS (Virtual Private Server), o un servicio de hosting en la nube como AWS, Google Cloud Platform, o DigitalOcean. El servidor debe tener acceso a internet para comunicarse con los servicios de Agilpay.

**Python 3.7 o Superior:** La aplicación backend está desarrollada en Python y requiere una versión 3.7 o superior. Se recomienda utilizar la versión más reciente estable de Python para garantizar compatibilidad y seguridad.

**Certificado SSL:** Es fundamental contar con un certificado SSL válido para el dominio donde se alojará el backend. Esto es necesario tanto por razones de seguridad como porque Agilpay requiere que todas las URLs de callback utilicen HTTPS.

**Dominio Personalizado:** Se necesita un dominio o subdominio dedicado para el backend. Este dominio debe estar configurado para apuntar al servidor donde se ejecutará la aplicación Flask.

### Credenciales de Agilpay

Para utilizar los servicios de Agilpay, es necesario obtener las siguientes credenciales del proveedor:

**Client ID:** Identificador único asignado por Agilpay para la aplicación. En el entorno de pruebas, se utiliza "API-001".

**Client Secret:** Clave secreta asociada al Client ID. Para pruebas, el valor es "Dynapay".

**Merchant Key:** Clave del comerciante que identifica la cuenta específica. En pruebas se utiliza "TEST-001".

**URLs de Servicio:** Agilpay proporciona diferentes URLs para los entornos de prueba y producción:
- Sandbox Token URL: https://sandbox-webapi.agilpay.net/oauth/paymenttoken
- Sandbox Payment URL: https://sandbox-webpay.agilpay.net/Payment
- Production Token URL: https://webapi.agilpay.net/oauth/paymenttoken
- Production Payment URL: https://webpay.agilpay.net/Payment

### Herramientas de Desarrollo

**Editor de Código:** Se recomienda utilizar un editor de código moderno como Visual Studio Code, PyCharm, o Sublime Text para facilitar el desarrollo y la depuración.

**Cliente Git:** Para gestionar el código fuente y facilitar el despliegue, es recomendable tener Git instalado y configurado.

**Herramientas de Prueba:** Para validar la integración, es útil contar con herramientas como Postman o curl para realizar pruebas de API.

## Configuración del Backend

La configuración del backend es un proceso crítico que establece la base para toda la integración. A continuación se detallan todos los pasos necesarios para configurar correctamente el servidor Flask.

### Instalación del Entorno

El primer paso es preparar el entorno de desarrollo en el servidor. Esto incluye la instalación de Python, la creación de un entorno virtual y la instalación de las dependencias necesarias.

**Creación del Entorno Virtual:**
```bash
python3 -m venv agilpay-backend
cd agilpay-backend
source bin/activate  # En Linux/Mac
# o
Scripts\activate  # En Windows
```

La utilización de un entorno virtual es una práctica recomendada que permite aislar las dependencias del proyecto y evitar conflictos con otras aplicaciones Python instaladas en el sistema.

**Instalación de Dependencias:**
```bash
pip install flask requests python-dotenv
```

Estas dependencias proporcionan las funcionalidades básicas necesarias:
- Flask: Framework web para Python
- Requests: Biblioteca para realizar solicitudes HTTP
- Python-dotenv: Para gestionar variables de entorno

### Estructura del Proyecto

La organización del código es fundamental para mantener un proyecto escalable y fácil de mantener. La estructura recomendada es la siguiente:

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

Esta estructura separa claramente las diferentes responsabilidades del código, facilitando el mantenimiento y la escalabilidad futura.

### Configuración de Variables de Entorno

Para mantener la seguridad de las credenciales, es esencial utilizar variables de entorno. Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
AGILPAY_CLIENT_ID=API-001
AGILPAY_CLIENT_SECRET=Dynapay
AGILPAY_MERCHANT_KEY=TEST-001
AGILPAY_TOKEN_URL=https://sandbox-webapi.agilpay.net/oauth/paymenttoken
AGILPAY_PAYMENT_URL=https://sandbox-webpay.agilpay.net/Payment
FLASK_ENV=development
FLASK_DEBUG=True
```

Es importante nunca incluir el archivo `.env` en el control de versiones para evitar exponer credenciales sensibles.

### Implementación del Código Backend

El archivo principal `main.py` configura la aplicación Flask y registra las rutas necesarias:

```python
import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from src.routes.agilpay import agilpay_bp

app = Flask(__name__, static_folder='src/static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Habilitar CORS para permitir solicitudes desde Webflow
CORS(app)

# Registrar blueprints
app.register_blueprint(agilpay_bp, url_prefix='/api/agilpay')

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

La configuración de CORS es esencial para permitir que el frontend alojado en Webflow pueda comunicarse con el backend.

### Implementación de las Rutas de Agilpay

El archivo `src/routes/agilpay.py` contiene toda la lógica específica para la integración con Agilpay:

```python
from flask import Blueprint, request, jsonify
import requests
import json
import uuid
import os

agilpay_bp = Blueprint('agilpay', __name__)

# Configuración desde variables de entorno
AGILPAY_CONFIG = {
    'client_id': os.environ.get('AGILPAY_CLIENT_ID'),
    'client_secret': os.environ.get('AGILPAY_CLIENT_SECRET'),
    'merchant_key': os.environ.get('AGILPAY_MERCHANT_KEY'),
    'token_url': os.environ.get('AGILPAY_TOKEN_URL'),
    'payment_url': os.environ.get('AGILPAY_PAYMENT_URL')
}

def get_oauth_token(order_id, customer_id, amount):
    """Obtiene el token JWT de Agilpay"""
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
            print(f"Error obteniendo token: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Excepción obteniendo token: {str(e)}")
        return None
```

Esta función maneja la autenticación OAuth2 con Agilpay, incluyendo el manejo de errores y timeouts apropiados.

### Configuración de Productos

Para demostrar la funcionalidad, se incluye un endpoint que devuelve una lista de productos de ejemplo:

```python
@agilpay_bp.route('/products', methods=['GET'])
def get_products():
    """Devuelve la lista de productos disponibles"""
    products = [
        {
            'id': 1,
            'name': 'Producto Premium A',
            'description': 'Descripción detallada del producto premium A',
            'price': 99.99,
            'image': 'https://via.placeholder.com/300x200?text=Producto+A'
        },
        {
            'id': 2,
            'name': 'Producto Estándar B',
            'description': 'Descripción detallada del producto estándar B',
            'price': 59.99,
            'image': 'https://via.placeholder.com/300x200?text=Producto+B'
        },
        # ... más productos
    ]
    
    return jsonify(products)
```

En una implementación real, esta información se obtendría de una base de datos o sistema de gestión de inventario.


## Implementación en Webflow

La implementación en Webflow requiere la integración cuidadosa de código personalizado dentro de la plataforma. Webflow permite agregar código HTML, CSS y JavaScript personalizado a través de varias opciones, incluyendo elementos de código embebido, configuraciones de página y configuraciones del sitio.

### Configuración Inicial en Webflow

**Acceso al Panel de Configuración:**
Para comenzar la implementación, es necesario acceder al panel de configuración del sitio en Webflow. Esto se hace navegando a la configuración del proyecto y seleccionando la pestaña "Custom Code". Esta sección permite agregar código que se ejecutará en todas las páginas del sitio o en páginas específicas.

**Configuración de URLs del Backend:**
Antes de implementar el código frontend, es crucial configurar correctamente las URLs que apuntarán al backend. Estas URLs deben actualizarse en el código JavaScript para reflejar la ubicación real del servidor backend.

### Estructura HTML para Webflow

El código HTML debe organizarse utilizando los elementos nativos de Webflow siempre que sea posible, complementándolos con código personalizado cuando sea necesario. La estructura recomendada incluye:

**Sección de Productos:**
```html
<div class="products-section">
    <div class="container">
        <h2 class="section-title">Nuestros Productos</h2>
        <div class="products-grid" id="products-grid">
            <!-- Los productos se cargarán dinámicamente -->
        </div>
    </div>
</div>
```

Esta estructura utiliza clases CSS que pueden ser estilizadas directamente en el diseñador visual de Webflow, manteniendo la flexibilidad de diseño que caracteriza a la plataforma.

**Sección del Carrito:**
```html
<div class="cart-section">
    <div class="container">
        <h3 class="cart-title">Carrito de Compras</h3>
        <div id="cart-items">
            <p class="empty-cart">Tu carrito está vacío</p>
        </div>
        <div class="cart-total" id="cart-total" style="display: none;">
            Total: $0.00
        </div>
    </div>
</div>
```

**Formulario de Checkout:**
```html
<div class="checkout-form" id="checkout-form" style="display: none;">
    <div class="container">
        <h3 class="form-title">Información de Facturación</h3>
        <form id="payment-form">
            <div class="form-group">
                <label class="form-label" for="customer-name">Nombre Completo *</label>
                <input type="text" id="customer-name" class="form-input" required>
            </div>
            <div class="form-group">
                <label class="form-label" for="customer-email">Correo Electrónico *</label>
                <input type="email" id="customer-email" class="form-input" required>
            </div>
            <div class="form-group">
                <label class="form-label" for="customer-address">Dirección *</label>
                <input type="text" id="customer-address" class="form-input" required>
            </div>
            <button type="submit" class="checkout-btn" id="checkout-btn">
                Proceder al Pago con Agilpay
            </button>
        </form>
    </div>
</div>
```

### Estilos CSS Personalizados

Los estilos CSS deben agregarse en la sección "Custom Code" del sitio en Webflow. Estos estilos complementan el diseño visual creado en el diseñador y proporcionan la funcionalidad específica necesaria para la tienda:

```css
/* Estilos base para la tienda */
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

/* Estilos para el carrito */
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

/* Estilos para el formulario */
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

/* Estilos responsivos */
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

### JavaScript para la Funcionalidad

El código JavaScript es el corazón de la funcionalidad de la tienda. Debe agregarse en la sección "Before </body> tag" en la configuración del sitio para asegurar que se ejecute después de que se cargue todo el contenido HTML:

```javascript
// Configuración de la aplicación
const CONFIG = {
    BACKEND_URL: 'https://tu-backend.com', // Actualizar con la URL real del backend
    API_ENDPOINTS: {
        PRODUCTS: '/api/agilpay/products',
        CREATE_PAYMENT: '/api/agilpay/create-payment'
    }
};

// Estado de la aplicación
let products = [];
let cart = [];

// Inicialización cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
    initializeEventListeners();
});

// Cargar productos desde el backend
async function loadProducts() {
    try {
        const response = await fetch(CONFIG.BACKEND_URL + CONFIG.API_ENDPOINTS.PRODUCTS);
        if (!response.ok) {
            throw new Error('Error al cargar productos');
        }
        products = await response.json();
        renderProducts();
    } catch (error) {
        console.error('Error cargando productos:', error);
        showError('No se pudieron cargar los productos. Por favor, intenta más tarde.');
    }
}

// Renderizar productos en la interfaz
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
                    Agregar al Carrito
                </button>
            </div>
        `;
        grid.appendChild(productCard);
    });
}

// Gestión del carrito de compras
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
    showNotification('Producto agregado al carrito');
}

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
            <div>
                <strong>${item.name}</strong><br>
                Cantidad: ${item.quantity} × $${item.price.toFixed(2)}
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

// Procesamiento del pago
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
            throw new Error('Error en la respuesta del servidor');
        }

        const result = await response.json();

        if (result.success) {
            // Crear formulario para envío a Agilpay
            const form = document.createElement('form');
            form.method = 'post';
            form.action = result.payment_url;
            form.style.display = 'none';

            // Agregar campos del formulario
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
            throw new Error(result.error || 'Error desconocido');
        }

    } catch (error) {
        console.error('Error procesando pago:', error);
        showError('Error procesando el pago: ' + error.message);
    }
}

// Funciones auxiliares
function showError(message) {
    alert(message); // En una implementación real, usar un sistema de notificaciones más elegante
}

function showNotification(message) {
    // Implementar sistema de notificaciones
    console.log(message);
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

            const customerData = {
                name: document.getElementById('customer-name').value,
                email: document.getElementById('customer-email').value,
                address: document.getElementById('customer-address').value
            };

            if (!customerData.name || !customerData.email || !customerData.address) {
                showError('Por favor completa todos los campos requeridos');
                return;
            }

            processPayment(customerData);
        });
    }
}
```

### Configuración de Elementos en Webflow

**Elementos de Código Embebido:**
Para implementar secciones específicas de la tienda, utiliza elementos de "Embed" en Webflow. Estos elementos permiten insertar código HTML personalizado directamente en el diseño visual.

**Configuración de IDs y Clases:**
Es crucial asegurar que los elementos HTML en Webflow tengan los IDs y clases correctos que coincidan con el código JavaScript. Esto se puede hacer utilizando el panel de configuración de elementos en el diseñador visual.

**Responsive Design:**
Webflow maneja automáticamente muchos aspectos del diseño responsivo, pero es importante probar la funcionalidad en diferentes tamaños de pantalla para asegurar que la experiencia del usuario sea óptima en todos los dispositivos.


## Configuración de Agilpay

La configuración correcta de Agilpay es fundamental para el funcionamiento de la integración. Esta sección detalla todos los aspectos necesarios para establecer una comunicación segura y efectiva con el gateway de pago.

### Credenciales de Prueba

Para el entorno de desarrollo y pruebas, Agilpay proporciona credenciales específicas que permiten simular transacciones sin procesar pagos reales. Las credenciales de prueba utilizadas en esta implementación son:

**Client ID:** API-001  
**Client Secret:** Dynapay  
**Merchant Key:** TEST-001

Estas credenciales están configuradas para funcionar exclusivamente con los servidores sandbox de Agilpay y no procesarán transacciones reales. Es importante nunca utilizar estas credenciales en un entorno de producción.

### URLs de Servicio

Agilpay mantiene entornos separados para desarrollo y producción, cada uno con sus propias URLs de servicio:

**Entorno Sandbox (Pruebas):**
- Token URL: https://sandbox-webapi.agilpay.net/oauth/paymenttoken
- Payment URL: https://sandbox-webpay.agilpay.net/Payment

**Entorno Producción:**
- Token URL: https://webapi.agilpay.net/oauth/paymenttoken
- Payment URL: https://webpay.agilpay.net/Payment

### Configuración de Webhooks

Para recibir notificaciones sobre el estado de las transacciones, es necesario configurar webhooks en la cuenta de Agilpay. Estos webhooks permiten que Agilpay notifique automáticamente al sistema cuando se completa una transacción, se rechaza un pago, o ocurre cualquier otro evento relevante.

El endpoint para recibir webhooks debe implementarse en el backend y configurarse en el panel de administración de Agilpay. Un ejemplo de implementación sería:

```python
@agilpay_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    """Maneja las notificaciones de webhook de Agilpay"""
    try:
        data = request.get_json()
        
        # Validar la autenticidad del webhook
        if not validate_webhook_signature(data):
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Procesar la notificación según el tipo de evento
        event_type = data.get('event_type')
        
        if event_type == 'payment_completed':
            handle_payment_completed(data)
        elif event_type == 'payment_failed':
            handle_payment_failed(data)
        
        return jsonify({'status': 'received'}), 200
        
    except Exception as e:
        print(f"Error procesando webhook: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
```

## Pruebas y Validación

Un proceso de pruebas exhaustivo es esencial para garantizar que la integración funcione correctamente en todos los escenarios posibles. Esta sección describe las diferentes tipos de pruebas que deben realizarse.

### Pruebas de Funcionalidad

**Pruebas del Catálogo de Productos:**
Verificar que los productos se cargan correctamente desde el backend y se muestran en la interfaz de usuario con toda la información necesaria (nombre, descripción, precio, imagen).

**Pruebas del Carrito de Compras:**
Validar que los usuarios pueden agregar productos al carrito, modificar cantidades, eliminar productos y que el total se calcula correctamente en tiempo real.

**Pruebas del Formulario de Checkout:**
Asegurar que la validación de campos funciona correctamente, que se muestran mensajes de error apropiados para datos inválidos, y que el formulario se envía correctamente cuando todos los campos están completos.

**Pruebas de Integración con Agilpay:**
Verificar que el backend puede obtener tokens JWT exitosamente, que las solicitudes de pago se construyen correctamente según las especificaciones de Agilpay, y que la redirección al gateway de pago funciona sin problemas.

### Pruebas de Seguridad

**Validación de Datos:**
Probar que el sistema maneja correctamente datos malformados o maliciosos, incluyendo intentos de inyección SQL, XSS (Cross-Site Scripting), y otros vectores de ataque comunes.

**Autenticación y Autorización:**
Verificar que las credenciales de Agilpay se mantienen seguras en el backend y nunca se exponen al cliente, y que los tokens JWT se manejan correctamente con tiempos de expiración apropiados.

**Comunicación Segura:**
Asegurar que todas las comunicaciones utilizan HTTPS y que los datos sensibles se transmiten de manera encriptada.

### Pruebas de Rendimiento

**Carga de Productos:**
Medir el tiempo de respuesta para cargar la lista de productos y optimizar si es necesario.

**Procesamiento de Pagos:**
Evaluar el tiempo total desde que el usuario envía el formulario hasta que es redirigido a Agilpay.

**Manejo de Concurrencia:**
Probar el comportamiento del sistema cuando múltiples usuarios realizan transacciones simultáneamente.

### Pruebas de Compatibilidad

**Navegadores Web:**
Verificar que la aplicación funciona correctamente en los navegadores más populares (Chrome, Firefox, Safari, Edge) y en diferentes versiones.

**Dispositivos Móviles:**
Probar la funcionalidad en dispositivos móviles y tablets para asegurar que la experiencia del usuario sea óptima en todas las plataformas.

**Resoluciones de Pantalla:**
Validar que el diseño responsivo funciona correctamente en diferentes resoluciones y orientaciones de pantalla.

## Despliegue en Producción

El despliegue en producción requiere consideraciones adicionales de seguridad, rendimiento y confiabilidad. Esta sección proporciona una guía completa para llevar la integración a un entorno de producción.

### Preparación del Entorno de Producción

**Servidor de Producción:**
Seleccionar un proveedor de hosting confiable que ofrezca alta disponibilidad, backups automáticos y soporte técnico. Opciones recomendadas incluyen AWS, Google Cloud Platform, DigitalOcean, o Heroku.

**Configuración de SSL:**
Obtener e instalar un certificado SSL válido para el dominio del backend. Esto es obligatorio para la comunicación con Agilpay y esencial para la seguridad de los datos del cliente.

**Variables de Entorno de Producción:**
Actualizar las variables de entorno para utilizar las credenciales de producción de Agilpay y configurar el entorno Flask para producción:

```
FLASK_ENV=production
FLASK_DEBUG=False
AGILPAY_CLIENT_ID=[Credencial real de producción]
AGILPAY_CLIENT_SECRET=[Credencial real de producción]
AGILPAY_MERCHANT_KEY=[Credencial real de producción]
AGILPAY_TOKEN_URL=https://webapi.agilpay.net/oauth/paymenttoken
AGILPAY_PAYMENT_URL=https://webpay.agilpay.net/Payment
```

### Configuración del Servidor Web

**Servidor WSGI:**
Para producción, es recomendable utilizar un servidor WSGI como Gunicorn en lugar del servidor de desarrollo de Flask:

```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 src.main:app
```

**Proxy Reverso:**
Configurar un proxy reverso como Nginx para manejar las solicitudes HTTP y proporcionar funcionalidades adicionales como compresión, cache y balanceador de carga.

**Monitoreo y Logs:**
Implementar un sistema de monitoreo para rastrear el rendimiento de la aplicación y configurar logs detallados para facilitar la depuración de problemas.

### Actualización de Webflow

**URLs del Backend:**
Actualizar todas las referencias a URLs del backend en el código JavaScript de Webflow para apuntar al servidor de producción.

**Configuración de CORS:**
Asegurar que el backend esté configurado para aceptar solicitudes desde el dominio de producción de Webflow.

**Pruebas de Integración:**
Realizar pruebas completas de la integración en el entorno de producción antes de hacer el sitio público.

## Mantenimiento y Monitoreo

Un mantenimiento proactivo es esencial para garantizar el funcionamiento continuo y seguro de la integración. Esta sección describe las mejores prácticas para el mantenimiento a largo plazo.

### Monitoreo de Rendimiento

**Métricas Clave:**
Establecer métricas para monitorear el rendimiento de la aplicación, incluyendo tiempo de respuesta de APIs, tasa de éxito de transacciones, y disponibilidad del servicio.

**Alertas Automáticas:**
Configurar alertas que notifiquen automáticamente cuando se detecten problemas, como errores en la comunicación con Agilpay, tiempos de respuesta elevados, o fallos del servidor.

**Análisis de Logs:**
Implementar un sistema de análisis de logs para identificar patrones, detectar problemas potenciales y optimizar el rendimiento.

### Actualizaciones de Seguridad

**Dependencias:**
Mantener todas las dependencias de Python actualizadas para incluir las últimas correcciones de seguridad:

```bash
pip list --outdated
pip install --upgrade [package_name]
```

**Certificados SSL:**
Monitorear la fecha de expiración de los certificados SSL y renovarlos antes de que expiren.

**Credenciales:**
Rotar regularmente las credenciales de acceso y mantener un registro de todos los cambios.

### Backups y Recuperación

**Backup de Código:**
Mantener el código fuente en un sistema de control de versiones como Git, con backups regulares en múltiples ubicaciones.

**Backup de Configuración:**
Realizar backups regulares de la configuración del servidor y las variables de entorno.

**Plan de Recuperación:**
Desarrollar y probar regularmente un plan de recuperación ante desastres que permita restaurar el servicio rápidamente en caso de fallos.

## Solución de Problemas

Esta sección proporciona soluciones para los problemas más comunes que pueden surgir durante la implementación y operación de la integración.

### Problemas de Autenticación

**Error: "Invalid client credentials"**
Este error indica que las credenciales de Agilpay no son válidas o están mal configuradas.

*Solución:*
- Verificar que las credenciales en las variables de entorno coincidan exactamente con las proporcionadas por Agilpay
- Asegurar que se están utilizando las credenciales correctas para el entorno (sandbox vs producción)
- Verificar que las credenciales no hayan expirado

**Error: "Token expired"**
Los tokens JWT de Agilpay tienen una duración limitada y pueden expirar.

*Solución:*
- Implementar lógica para renovar automáticamente los tokens cuando expiren
- Verificar que la hora del servidor esté sincronizada correctamente
- Reducir el tiempo entre la obtención del token y su uso

### Problemas de Conectividad

**Error: "Connection timeout"**
Problemas de red pueden causar timeouts en las solicitudes a Agilpay.

*Solución:*
- Verificar la conectividad a internet del servidor
- Aumentar el timeout en las solicitudes HTTP
- Implementar reintentos automáticos con backoff exponencial

**Error: "CORS policy"**
Problemas de CORS pueden impedir que Webflow se comunique con el backend.

*Solución:*
- Verificar que CORS esté habilitado en el backend
- Asegurar que el dominio de Webflow esté incluido en la lista de orígenes permitidos
- Verificar que los headers necesarios estén configurados correctamente

### Problemas de Datos

**Error: "Invalid payment data"**
Agilpay puede rechazar solicitudes con datos mal formados.

*Solución:*
- Validar todos los datos antes de enviarlos a Agilpay
- Verificar que los montos estén en el formato correcto (números decimales)
- Asegurar que todos los campos requeridos estén presentes

**Error: "Product not found"**
Errores al cargar productos pueden indicar problemas con la API del backend.

*Solución:*
- Verificar que el endpoint de productos esté funcionando correctamente
- Revisar los logs del servidor para identificar errores específicos
- Validar que la estructura de datos de los productos sea correcta

## Referencias

[1] Documentación oficial de Agilpay Gateway: https://agilisa.atlassian.net/wiki/spaces/DOCUMENTAT/pages/38273121/Payment+Request

[2] Repositorio de ejemplo WooCommerce Agilpay: https://github.com/agilisa-technologies/woocommerce

[3] Documentación de Webflow Custom Code: https://university.webflow.com/lesson/custom-code-in-the-head-and-body-tags

[4] Flask Documentation: https://flask.palletsprojects.com/

[5] Requests Library Documentation: https://docs.python-requests.org/

[6] OAuth 2.0 RFC: https://tools.ietf.org/html/rfc6749

[7] CORS Documentation: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

[8] JavaScript Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

---

**Nota:** Esta documentación está basada en las especificaciones y ejemplos proporcionados por Agilisa Technologies. Para obtener las credenciales de producción y soporte técnico adicional, contacte directamente con el equipo de Agilpay.

**Autor:** Javier Sanchez
**Última actualización:** 15 de Julio, 2025  
**Versión del documento:** 1.0


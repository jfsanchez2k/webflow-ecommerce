from flask import Blueprint, request, jsonify
import requests
import json
import uuid

agilpay_bp = Blueprint('agilpay', __name__)

# Configuración de Agilpay (credenciales de prueba)
AGILPAY_CONFIG = {
    'client_id': 'API-001',
    'client_secret': 'Dynapay',
    'merchant_key': 'TEST-001',
    'token_url': 'https://sandbox-webapi.agilpay.net/oauth/paymenttoken',
    'payment_url': 'https://sandbox-webpay.agilpay.net/Payment'
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
        
        headers = {
            'Content-Type': 'application/json'
        }
        
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

@agilpay_bp.route('/create-payment', methods=['POST'])
def create_payment():
    """Crea una solicitud de pago con Agilpay"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['customer_name', 'customer_email', 'customer_address', 'items']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        # Generar ID único para la orden
        order_id = str(uuid.uuid4())
        
        # Calcular el total
        total_amount = 0
        items = []
        for item in data['items']:
            item_total = float(item['price']) * int(item['quantity'])
            total_amount += item_total
            items.append({
                'Description': item['name'],
                'Quantity': str(item['quantity']),
                'Amount': item_total,
                'Tax': 0
            })
        
        # Obtener token JWT
        token = get_oauth_token(order_id, data['customer_email'], total_amount)
        if not token:
            return jsonify({'error': 'No se pudo obtener el token de autenticación'}), 500
        
        # Preparar detalles del pago
        payment_details = {
            'MerchantKey': AGILPAY_CONFIG['merchant_key'],
            'Service': order_id,
            'MerchantName': 'Webflow Store',
            'Description': f'Orden {order_id}',
            'Amount': total_amount,
            'Tax': 0,
            'Currency': '840',  # USD
            'Items': items
        }
        
        # Preparar datos para el formulario de Agilpay
        agilpay_data = {
            'SiteId': AGILPAY_CONFIG['client_id'],
            'UserId': data['customer_email'],
            'Names': data['customer_name'],
            'Email': data['customer_email'],
            'Address': data['customer_address'],
            'Detail': json.dumps({'Payments': [payment_details]}),
            'SuccessURL': data.get('success_url', 'https://example.com/success'),
            'ReturnURL': data.get('return_url', 'https://example.com/return'),
            'token': token,
            'NoHeader': '2'  # Modo iframe
        }
        
        return jsonify({
            'success': True,
            'payment_url': AGILPAY_CONFIG['payment_url'],
            'payment_data': agilpay_data,
            'order_id': order_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@agilpay_bp.route('/payment-response', methods=['POST'])
def payment_response():
    """Maneja la respuesta de Agilpay después del pago"""
    try:
        # Aquí se procesaría la respuesta de Agilpay
        # Por ahora, simplemente registramos los datos recibidos
        data = request.form.to_dict()
        print(f"Respuesta de Agilpay: {data}")
        
        # En una implementación real, aquí se validaría la respuesta
        # y se actualizaría el estado de la orden en la base de datos
        
        return jsonify({'status': 'received'})
        
    except Exception as e:
        return jsonify({'error': f'Error procesando respuesta: {str(e)}'}), 500

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
        {
            'id': 3,
            'name': 'Producto Básico C',
            'description': 'Descripción detallada del producto básico C',
            'price': 29.99,
            'image': 'https://via.placeholder.com/300x200?text=Producto+C'
        },
        {
            'id': 4,
            'name': 'Producto Deluxe D',
            'description': 'Descripción detallada del producto deluxe D',
            'price': 149.99,
            'image': 'https://via.placeholder.com/300x200?text=Producto+D'
        },
        {
            'id': 5,
            'name': 'Producto Especial E',
            'description': 'Descripción detallada del producto especial E',
            'price': 79.99,
            'image': 'https://via.placeholder.com/300x200?text=Producto+E'
        }
    ]
    
    return jsonify(products)


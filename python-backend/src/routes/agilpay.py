from flask import Blueprint, request, jsonify
import requests
import json
import uuid
import logging
import os

agilpay_bp = Blueprint('agilpay', __name__)
logger = logging.getLogger(__name__)

# Configuración de Agilpay (credenciales de prueba)
AGILPAY_CONFIG = {
    'client_id': os.environ.get('AGILPAY_CLIENT_ID', 'API-001'),
    'client_secret': os.environ.get('AGILPAY_CLIENT_SECRET', 'Dynapay'),
    'merchant_key': os.environ.get('AGILPAY_MERCHANT_KEY', 'TEST-001'),
    'token_url': os.environ.get('AGILPAY_TOKEN_URL', 'https://sandbox-webapi.agilpay.net/oauth/paymenttoken'),
    'payment_url': os.environ.get('AGILPAY_PAYMENT_URL', 'https://sandbox-webpay.agilpay.net/Payment')
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
        
        logger.info(f"Solicitando token para orden {order_id}")
        
        response = requests.post(
            AGILPAY_CONFIG['token_url'],
            data=json.dumps(payload),
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            if token:
                logger.info(f"Token obtenido exitosamente para orden {order_id}")
                return token
            else:
                logger.error(f"Token no encontrado en respuesta para orden {order_id}")
                return None
        else:
            logger.error(f"Error obteniendo token: {response.status_code} - {response.text}")
            return None
            
    except requests.RequestException as e:
        logger.error(f"Error de conexión obteniendo token: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Excepción obteniendo token: {str(e)}")
        return None

@agilpay_bp.route('/create-payment', methods=['POST'])
def create_payment():
    """Crea una solicitud de pago con Agilpay"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se enviaron datos'
            }), 400
        
        # Validar datos requeridos
        required_fields = ['customer_name', 'customer_email', 'customer_address', 'items']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
            }), 400
        
        # Validar items
        if not isinstance(data['items'], list) or len(data['items']) == 0:
            return jsonify({
                'success': False,
                'error': 'Items debe ser una lista no vacía'
            }), 400
        
        # Validar cada item
        for i, item in enumerate(data['items']):
            if not isinstance(item, dict):
                return jsonify({
                    'success': False,
                    'error': f'Item {i+1} debe ser un objeto'
                }), 400
            
            required_item_fields = ['name', 'price', 'quantity']
            missing_item_fields = [field for field in required_item_fields if field not in item]
            
            if missing_item_fields:
                return jsonify({
                    'success': False,
                    'error': f'Item {i+1} falta campos: {", ".join(missing_item_fields)}'
                }), 400
            
            try:
                price = float(item['price'])
                quantity = int(item['quantity'])
                if price <= 0 or quantity <= 0:
                    raise ValueError("Precio y cantidad deben ser positivos")
            except (ValueError, TypeError):
                return jsonify({
                    'success': False,
                    'error': f'Item {i+1} tiene precio o cantidad inválidos'
                }), 400
        
        # Validar email
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['customer_email']):
            return jsonify({
                'success': False,
                'error': 'Email inválido'
            }), 400
        
        # Generar ID único para la orden
        order_id = str(uuid.uuid4())
        logger.info(f"Creando pago para orden {order_id}")
        
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
        
        logger.info(f"Total calculado para orden {order_id}: ${total_amount}")
        
        # Obtener token JWT
        token = get_oauth_token(order_id, data['customer_email'], total_amount)
        if not token:
            return jsonify({
                'success': False,
                'error': 'No se pudo obtener el token de autenticación'
            }), 500
        
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
        
        logger.info(f"Pago creado exitosamente para orden {order_id}")
        
        return jsonify({
            'success': True,
            'payment_url': AGILPAY_CONFIG['payment_url'],
            'payment_data': agilpay_data,
            'order_id': order_id
        })
        
    except Exception as e:
        logger.error(f"Error interno creando pago: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@agilpay_bp.route('/payment-response', methods=['POST'])
def payment_response():
    """Maneja la respuesta de Agilpay después del pago"""
    try:
        # Obtener datos del formulario
        data = request.form.to_dict()
        logger.info(f"Respuesta de Agilpay recibida: {data}")
        
        # En una implementación real, aquí se validaría la respuesta
        # y se actualizaría el estado de la orden en la base de datos
        
        # Validar que se recibieron datos
        if not data:
            logger.warning("Respuesta de Agilpay vacía")
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos'
            }), 400
        
        # Aquí podrías agregar validaciones específicas de Agilpay
        # Por ejemplo, verificar firmas, estados de transacción, etc.
        
        return jsonify({
            'success': True,
            'status': 'received',
            'message': 'Respuesta procesada correctamente'
        })
        
    except Exception as e:
        logger.error(f"Error procesando respuesta de Agilpay: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error procesando respuesta: {str(e)}'
        }), 500

@agilpay_bp.route('/products', methods=['GET'])
def get_products():
    """Devuelve la lista de productos disponibles"""
    try:
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
        
        logger.info(f"Productos solicitados: {len(products)} productos devueltos")
        
        return jsonify({
            'success': True,
            'data': products
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo productos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


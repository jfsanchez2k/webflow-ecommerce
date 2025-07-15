#!/usr/bin/env python3
"""
Script de pruebas básicas para verificar que el backend funciona correctamente
"""

import requests
import json
import sys

# Configuración
BASE_URL = 'http://localhost:5000'
API_BASE = f'{BASE_URL}/api'

def test_products_endpoint():
    """Prueba el endpoint de productos"""
    print("🧪 Probando endpoint de productos...")
    try:
        response = requests.get(f'{API_BASE}/agilpay/products')
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Productos obtenidos: {len(data['data'])} productos")
                return True
            else:
                print(f"❌ Error en respuesta: {data.get('error', 'Error desconocido')}")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_user_crud():
    """Prueba las operaciones CRUD de usuarios"""
    print("🧪 Probando CRUD de usuarios...")
    
    # Crear usuario
    print("  - Creando usuario...")
    user_data = {
        "username": "test_user",
        "email": "test@example.com"
    }
    
    try:
        response = requests.post(f'{API_BASE}/users', json=user_data)
        if response.status_code == 201:
            created_user = response.json()
            if created_user.get('success'):
                user_id = created_user['data']['id']
                print(f"  ✅ Usuario creado con ID: {user_id}")
                
                # Obtener usuario
                print("  - Obteniendo usuario...")
                response = requests.get(f'{API_BASE}/users/{user_id}')
                if response.status_code == 200:
                    user_data = response.json()
                    if user_data.get('success'):
                        print("  ✅ Usuario obtenido correctamente")
                        
                        # Eliminar usuario
                        print("  - Eliminando usuario...")
                        response = requests.delete(f'{API_BASE}/users/{user_id}')
                        if response.status_code == 200:
                            print("  ✅ Usuario eliminado correctamente")
                            return True
                        else:
                            print(f"  ❌ Error eliminando usuario: {response.status_code}")
                            return False
                    else:
                        print(f"  ❌ Error obteniendo usuario: {user_data.get('error')}")
                        return False
                else:
                    print(f"  ❌ Error HTTP obteniendo usuario: {response.status_code}")
                    return False
            else:
                print(f"  ❌ Error en respuesta de creación: {created_user.get('error')}")
                return False
        else:
            print(f"  ❌ Error HTTP creando usuario: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error de conexión: {e}")
        return False

def test_payment_creation():
    """Prueba la creación de un pago"""
    print("🧪 Probando creación de pago...")
    
    payment_data = {
        "customer_name": "Juan Pérez",
        "customer_email": "juan@example.com",
        "customer_address": "Calle 123, Ciudad",
        "items": [
            {
                "name": "Producto de prueba",
                "price": 99.99,
                "quantity": 1
            }
        ]
    }
    
    try:
        response = requests.post(f'{API_BASE}/agilpay/create-payment', json=payment_data)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Pago creado con orden ID: {data['order_id']}")
                return True
            else:
                print(f"❌ Error en respuesta: {data.get('error', 'Error desconocido')}")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Detalles: {error_data}")
            except:
                print(f"   Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas del backend Agilpay...\n")
    
    # Verificar que el servidor está corriendo
    print("🔍 Verificando conexión con el servidor...")
    try:
        response = requests.get(BASE_URL, timeout=5)
        print("✅ Servidor accesible\n")
    except Exception as e:
        print(f"❌ No se puede conectar al servidor: {e}")
        print("   Asegúrate de que el servidor esté corriendo en http://localhost:5000")
        sys.exit(1)
    
    # Ejecutar pruebas
    tests = [
        test_products_endpoint,
        test_user_crud,
        test_payment_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    # Mostrar resultados
    print("📊 Resultados de las pruebas:")
    print(f"   Pasadas: {passed}/{total}")
    print(f"   Fallidas: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron!")
        sys.exit(0)
    else:
        print("⚠️  Algunas pruebas fallaron")
        sys.exit(1)

if __name__ == "__main__":
    main()

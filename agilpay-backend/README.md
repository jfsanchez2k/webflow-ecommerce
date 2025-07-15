# Agilpay Backend - Python Flask

Backend para integración con el sistema de pagos Agilpay, desarrollado con Flask.

## 🚀 Características

- **Flask** - Framework web ligero y flexible
- **SQLAlchemy** - ORM para manejo de base de datos
- **Flask-CORS** - Manejo de CORS para integración con frontend
- **SQLite** - Base de datos ligera y portátil
- **Logging** - Sistema de logs estructurado
- **Validación robusta** - Validación de datos de entrada
- **Manejo de errores** - Respuestas de error consistentes

## 📁 Estructura del Proyecto

```
agilpay-backend/
├── src/
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── models/
│   │   └── user.py          # Modelo de usuario
│   ├── routes/
│   │   ├── agilpay.py       # Endpoints de Agilpay
│   │   └── user.py          # Endpoints de usuarios
│   ├── static/              # Archivos estáticos
│   └── database/            # Base de datos SQLite
├── requirements.txt         # Dependencias de Python
├── start.bat               # Script de inicio para Windows
├── start.sh                # Script de inicio para Linux/Mac
└── .env.example            # Ejemplo de configuración
```

## 🔌 Endpoints de la API

### Productos
- `GET /api/agilpay/products` - Obtiene la lista de productos

### Pagos con Agilpay
- `POST /api/agilpay/create-payment` - Crea una solicitud de pago
- `POST /api/agilpay/payment-response` - Maneja respuestas de Agilpay

### Gestión de Usuarios
- `GET /api/users` - Lista todos los usuarios
- `POST /api/users` - Crea un nuevo usuario
- `GET /api/users/{id}` - Obtiene un usuario específico
- `PUT /api/users/{id}` - Actualiza un usuario
- `DELETE /api/users/{id}` - Elimina un usuario

## 🛠️ Instalación y Ejecución

### Opción 1: Ejecución Rápida (Recomendada)

#### Windows:
```bash
start.bat
```

#### Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

### Opción 2: Instalación Manual

#### Prerrequisitos
- Python 3.8+ instalado
- pip (incluido con Python)

#### Pasos de instalación

1. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

2. **Activar entorno virtual**
   
   Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno** (opcional)
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

5. **Ejecutar la aplicación**
   ```bash
   cd src
   python main.py
   ```

6. **Acceder a la aplicación**
   - API: `http://localhost:5000`

## 🔧 Configuración

### Variables de Entorno
Puedes configurar las siguientes variables de entorno:

```bash
# Configuración general
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database/app.db

# Agilpay
AGILPAY_CLIENT_ID=API-001
AGILPAY_CLIENT_SECRET=Dynapay
AGILPAY_MERCHANT_KEY=TEST-001
AGILPAY_TOKEN_URL=https://sandbox-webapi.agilpay.net/oauth/paymenttoken
AGILPAY_PAYMENT_URL=https://sandbox-webpay.agilpay.net/Payment

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### Base de Datos
La aplicación usa SQLite por defecto. La base de datos se crea automáticamente en `src/database/app.db`.

## 📚 Uso de la API

### Crear un pago
```bash
curl -X POST http://localhost:5000/api/agilpay/create-payment \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Juan Pérez",
    "customer_email": "juan@example.com",
    "customer_address": "Calle 123, Ciudad",
    "items": [
      {
        "name": "Producto A",
        "price": 99.99,
        "quantity": 1
      }
    ]
  }'
```

### Obtener productos
```bash
curl http://localhost:5000/api/agilpay/products
```

### Crear usuario
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario123",
    "email": "usuario@example.com"
  }'
```

## ✅ Mejoras Implementadas

### Validación Robusta

- ✅ Validación de campos requeridos
- ✅ Validación de formato de email
- ✅ Validación de tipos de datos
- ✅ Validación de rangos numéricos

### Manejo de Errores

- ✅ Respuestas de error consistentes
- ✅ Códigos de estado HTTP apropiados
- ✅ Logging de errores detallado
- ✅ Manejo de excepciones de base de datos

### Seguridad

- ✅ CORS configurado correctamente
- ✅ Validación de entrada sanitizada
- ✅ Variables de entorno para configuración sensible
- ✅ Timeouts en peticiones HTTP

### Funcionalidad

- ✅ Logging estructurado
- ✅ Respuestas JSON consistentes
- ✅ Manejo de transacciones de BD
- ✅ Configuración de entorno flexible

## 🧪 Testing

Para probar los endpoints:

```bash
# Instalar herramientas de testing (opcional)
pip install pytest requests

# Ejecutar pruebas manuales
python -c "
import requests
response = requests.get('http://localhost:5000/api/agilpay/products')
print(response.json())
"
```

## 🔧 Desarrollo

### Estructura de Respuestas

Todas las respuestas siguen este formato:

```json
{
  "success": true,
  "data": {...},
  "error": null,
  "message": "Opcional"
}
```

### Logging

Los logs se escriben en la consola con el formato:
```
2025-01-15 10:30:45 - module_name - INFO - Mensaje
```

## 🚀 Producción

Para despliegue en producción:

1. Configurar variables de entorno apropiadas
2. Usar un servidor WSGI como Gunicorn:

   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 main:app
   ```

3. Configurar proxy reverso (nginx)
4. Usar base de datos más robusta (PostgreSQL)

## 📝 Logs y Monitoreo

Los logs incluyen:

- Solicitudes de token a Agilpay
- Creación de pagos
- Errores de validación
- Errores de base de datos
- Operaciones CRUD de usuarios

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la misma licencia que el proyecto principal.

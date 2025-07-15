# Agilpay Backend - C# ASP.NET Core

Este proyecto es una versión equivalente en C# del backend Python original, desarrollado con ASP.NET Core para la integración con el sistema de pagos Agilpay.

## 🚀 Características

- **ASP.NET Core 8.0** - Framework web moderno y de alto rendimiento
- **Entity Framework Core** - ORM para manejo de base de datos
- **SQLite** - Base de datos ligera y portátil
- **Swagger/OpenAPI** - Documentación automática de la API
- **Arquitectura limpia** - Separación de responsabilidades en capas
- **Inyección de dependencias** - Patrón IoC integrado
- **Logging estructurado** - Sistema de logs robusto

## 📁 Estructura del Proyecto

```
csharp-backend/
├── Controllers/           # Controladores de API
│   ├── AgilpayController.cs
│   └── UsersController.cs
├── Data/                 # Contexto de base de datos
│   └── ApplicationDbContext.cs
├── Models/               # Modelos de datos
│   ├── User.cs
│   ├── Product.cs
│   ├── PaymentRequest.cs
│   └── PaymentResponse.cs
├── Services/             # Lógica de negocio
│   ├── IAgilpayService.cs
│   └── AgilpayService.cs
├── wwwroot/              # Archivos estáticos
│   └── index.html
├── database/             # Base de datos SQLite
├── Program.cs            # Punto de entrada
├── appsettings.json      # Configuración
└── AgilpayBackend.csproj # Archivo de proyecto
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

### Prerrequisitos
- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)

### Pasos de instalación

1. **Clonar y navegar al directorio**
   ```bash
   cd csharp-backend
   ```

2. **Restaurar dependencias**
   ```bash
   dotnet restore
   ```

3. **Ejecutar la aplicación**
   ```bash
   dotnet run
   ```

4. **Acceder a la aplicación**
   - API: `https://localhost:5001` o `http://localhost:5000`
   - Documentación Swagger: `https://localhost:5001/swagger`

## 📚 Documentación de la API

Una vez que la aplicación esté ejecutándose, puedes acceder a la documentación interactiva de Swagger en:
- `https://localhost:5001/swagger`

## 🔧 Configuración

### Base de Datos
La aplicación usa SQLite por defecto. La base de datos se crea automáticamente en el directorio `database/app.db`.

### Agilpay
Las credenciales de Agilpay están configuradas en `AgilpayService.cs`:
- Client ID: `API-001`
- Client Secret: `Dynapay`
- Merchant Key: `TEST-001`
- Token URL: `https://sandbox-webapi.agilpay.net/oauth/paymenttoken`
- Payment URL: `https://sandbox-webpay.agilpay.net/Payment`

### CORS
CORS está habilitado para todos los orígenes en modo desarrollo. Para producción, configura políticas específicas.

## 🔍 Diferencias con la versión Python

### Ventajas de la versión C#:
- **Tipado fuerte** - Mayor seguridad en tiempo de compilación
- **Performance** - ASP.NET Core es más rápido que Flask
- **Async/Await nativo** - Mejor manejo de operaciones asíncronas
- **Inyección de dependencias** - Patrón IoC integrado
- **Middleware pipeline** - Procesamiento de requests más flexible
- **Swagger integrado** - Documentación automática
- **Logging estructurado** - Sistema de logs más robusto

### Equivalencias:
- **Flask Blueprints** → **ASP.NET Core Controllers**
- **SQLAlchemy** → **Entity Framework Core**
- **Flask-CORS** → **CORS Middleware**
- **Python requests** → **HttpClient**
- **Python dictionaries** → **C# DTOs/Models**

## 🧪 Testing

Para ejecutar pruebas (cuando estén implementadas):
```bash
dotnet test
```

## 📦 Compilación para Producción

Para compilar una versión optimizada:
```bash
dotnet publish -c Release -o ./publish
```

## 🔒 Seguridad

- Validación de modelos automática
- Sanitización de entrada
- Headers de seguridad configurables
- Autenticación y autorización escalable

## 📝 Logs

Los logs se escriben en la consola por defecto. Para producción, configura providers adicionales en `appsettings.json`.

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la misma licencia que el proyecto original.

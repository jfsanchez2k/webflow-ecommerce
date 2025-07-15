# Instrucciones de Desarrollo

## Configuración del Entorno de Desarrollo

### Visual Studio / Visual Studio Code
1. Instala la extensión de C# para tu editor
2. Instala .NET 8.0 SDK
3. Abre el proyecto desde la carpeta `csharp-backend`

### Comandos útiles

```bash
# Restaurar paquetes
dotnet restore

# Compilar
dotnet build

# Ejecutar
dotnet run

# Ejecutar con recarga automática
dotnet watch run

# Crear migración (si usas migraciones)
dotnet ef migrations add InitialCreate

# Aplicar migraciones
dotnet ef database update
```

## Variables de Entorno

Puedes configurar las siguientes variables en `appsettings.Development.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Data Source=database/app.db"
  },
  "Agilpay": {
    "ClientId": "API-001",
    "ClientSecret": "Dynapay",
    "MerchantKey": "TEST-001",
    "TokenUrl": "https://sandbox-webapi.agilpay.net/oauth/paymenttoken",
    "PaymentUrl": "https://sandbox-webpay.agilpay.net/Payment"
  }
}
```

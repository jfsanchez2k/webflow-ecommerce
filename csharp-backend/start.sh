#!/bin/bash

echo "Iniciando Agilpay Backend - C#..."
echo

# Verificar si .NET está instalado
if ! command -v dotnet &> /dev/null; then
    echo "Error: .NET SDK no está instalado."
    echo "Por favor instala .NET 8.0 SDK desde: https://dotnet.microsoft.com/download/dotnet/8.0"
    exit 1
fi

echo "✓ .NET SDK detectado"
echo

# Restaurar dependencias
echo "Restaurando dependencias..."
if ! dotnet restore; then
    echo "Error restaurando dependencias"
    exit 1
fi

echo "✓ Dependencias restauradas"
echo

# Crear directorio de base de datos si no existe
mkdir -p database

echo "✓ Directorio de base de datos verificado"
echo

# Ejecutar la aplicación
echo "Iniciando servidor..."
echo "La aplicación estará disponible en:"
echo "  - HTTP:  http://localhost:5000"
echo "  - HTTPS: https://localhost:5001"
echo "  - Swagger: https://localhost:5001/swagger"
echo
echo "Presiona Ctrl+C para detener el servidor"
echo

dotnet run

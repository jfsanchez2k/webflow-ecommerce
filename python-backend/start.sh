#!/bin/bash

echo "Iniciando Agilpay Backend - Python Flask..."
echo

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 no está instalado."
    echo "Por favor instala Python3 desde: https://python.org"
    exit 1
fi

echo "✓ Python3 detectado"
echo

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error creando entorno virtual"
        exit 1
    fi
    echo "✓ Entorno virtual creado"
else
    echo "✓ Entorno virtual existente"
fi

echo

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error instalando dependencias"
    exit 1
fi

echo "✓ Dependencias instaladas"
echo

# Crear directorio de base de datos si no existe
mkdir -p src/database

echo "✓ Directorio de base de datos verificado"
echo

# Ejecutar la aplicación
echo "Iniciando servidor Flask..."
echo "La aplicación estará disponible en: http://localhost:5000"
echo
echo "Presiona Ctrl+C para detener el servidor"
echo

cd src
python main.py

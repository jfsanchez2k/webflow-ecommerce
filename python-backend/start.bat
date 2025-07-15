@echo off
echo Iniciando Agilpay Backend - Python Flask...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no está instalado o no está en el PATH
    echo Por favor instala Python desde: https://python.org
    pause
    exit /b 1
)

echo ✓ Python detectado
echo.

REM Crear entorno virtual si no existe
if not exist "venv\" (
    echo Creando entorno virtual...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error creando entorno virtual
        pause
        exit /b 1
    )
    echo ✓ Entorno virtual creado
) else (
    echo ✓ Entorno virtual existente
)

echo.

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error instalando dependencias
    pause
    exit /b 1
)

echo ✓ Dependencias instaladas
echo.

REM Crear directorio de base de datos si no existe
if not exist "src\database\" mkdir src\database

echo ✓ Directorio de base de datos verificado
echo.

REM Ejecutar la aplicación
echo Iniciando servidor Flask...
echo La aplicación estará disponible en: http://localhost:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

cd src
python main.py

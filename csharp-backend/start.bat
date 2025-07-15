@echo off
echo Iniciando Agilpay Backend - C#...
echo.

REM Verificar si .NET está instalado
dotnet --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: .NET SDK no está instalado.
    echo Por favor instala .NET 8.0 SDK desde: https://dotnet.microsoft.com/download/dotnet/8.0
    pause
    exit /b 1
)

echo ✓ .NET SDK detectado
echo.

REM Restaurar dependencias
echo Restaurando dependencias...
dotnet restore
if %ERRORLEVEL% neq 0 (
    echo Error restaurando dependencias
    pause
    exit /b 1
)

echo ✓ Dependencias restauradas
echo.

REM Crear directorio de base de datos si no existe
if not exist "database" mkdir database

echo ✓ Directorio de base de datos verificado
echo.

REM Ejecutar la aplicación
echo Iniciando servidor...
echo La aplicación estará disponible en:
echo   - HTTP:  http://localhost:5000
echo   - HTTPS: https://localhost:5001
echo   - Swagger: https://localhost:5001/swagger
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

dotnet run

pause

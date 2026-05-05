#!/bin/bash
# Script de instalación rápida para el Sistema de Alertas de Autos Eléctricos Cuba

set -e

echo "⚡ Instalando Sistema de Alertas de Autos Eléctricos Cuba..."
echo ""

# Check Python version
python3 --version || { echo "❌ Python 3 no está instalado"; exit 1; }

# Install dependencies
echo "📦 Instalando dependencias..."
pip3 install -r requirements.txt

# Create .env if not exists
if [ ! -f .env ]; then
    echo "📝 Creando archivo de configuración .env..."
    cp .env.example .env
    echo "✅ .env creado. Edítalo con tus credenciales de correo."
else
    echo "ℹ️  .env ya existe, no se sobrescribió."
fi

# Create temp directory
mkdir -p /tmp/cuba_ev_alerts

echo ""
echo "✅ Instalación completada."
echo ""
echo "Próximos pasos:"
echo "1. Edita .env con tus credenciales de Gmail (App Password)"
echo "2. Ejecuta: python3 main.py --test"
echo "3. Programa en cron para ejecución cada hora:"
echo "   crontab -e"
echo "   0 * * * * cd $(pwd) && python3 main.py >> /tmp/cuba_ev_cron.log 2>&1"

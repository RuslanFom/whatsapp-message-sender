# Sender di Messaggi WhatsApp

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Questo progetto automatizza l'invio di messaggi WhatsApp a una lista di clienti utilizzando un'API esterna.

## 📁 Struttura del Progetto

```
$whatsapp-sender/
│
├── # app.py
├── # config.py
├── # clients.xlsx
├── # requirements.txt
└── # venv/
---

## 🚀 Funzionalità

- Validazione del token di accesso
- Invio di messaggi WhatsApp personalizzati
- Lettura dei dati dei clienti da un file Excel
- Gestione degli errori e logging dettagliato

## 🛠️ Installazione

1. Clona il repository:
   ```
   git clone https://github.com/tuousername/whatsapp-sender.git
   ```

2. Entra nella directory del progetto:
   ```
   cd whatsapp-sender
   ```

3. Crea un ambiente virtuale:
   ```
   python -m venv venv
   ```

4. Attiva l'ambiente virtuale:
   - Su Windows: `venv\Scripts\activate`
   - Su Unix o MacOS: `source venv/bin/activate`

5. Installa le dipendenze:
   ```
   pip install -r requirements.txt
   ```

## ⚙️ Configurazione

1. Apri `config.py` e inserisci i tuoi dati:

   ```python
   ACCESS_TOKEN = "il_tuo_token_di_accesso"
   TEMPLATE_ID = "il_tuo_template_id"
   HOST = "https://api.example.com/"
   EXCEL_FILE_PATH = "percorso/del/tuo/file.xlsx"
   ```

2. Prepara il file Excel `clients.xlsx` con i dati dei clienti.

## 🖥️ Utilizzo

Esegui lo script principale:


python app.py


## 📝 File Principali

### app.py

Contiene la logica principale dell'applicazione:

- `validate_token(token)`: Valida il token di accesso
- `send_whatsapp_message(phone, full_name)`: Invia un messaggio WhatsApp
- `read_clients_from_excel(file_path)`: Legge i dati dei clienti da Excel
- `send_messages_to_clients(clients, message_type)`: Gestisce l'invio di messaggi in massa

### config.py

Contiene le configurazioni dell'applicazione.

## ⚠️ Note Importanti

- Assicurati di avere l'autorizzazione per inviare messaggi ai numeri di telefono dei clienti.
- Il numero del mittente deve essere configurato e approvato nell'account WhatsApp Business.



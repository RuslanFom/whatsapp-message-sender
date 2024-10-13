from config import ACCESS_TOKEN, TEMPLATE_ID, HOST, EXCEL_FILE_PATH

import requests
import json
import sys
import pandas as pd
import logging

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Valida il token di accesso con l'API
def validate_token(token):
    url = f"{HOST}Api/ValidateToken"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        # Invia una richiesta POST per validare il token
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Solleva un'eccezione per codici di stato non riusciti
        logger.info(f"Codice di stato: {response.status_code}")
        logger.info(f"Risposta API: {response.text}")
        
        if response.status_code == 200:
            logger.info("Token valido.")
            return True
        else:
            logger.warning(f"Token non valido. Codice di stato: {response.status_code}")
            return False
    except requests.RequestException as e:
        logger.error(f"Errore durante la validazione del token: {e}")
        return False
    except json.JSONDecodeError:
        logger.error("Errore durante l'analisi della risposta JSON.")
        return False

# Invia un messaggio WhatsApp a un cliente.  
def send_whatsapp_message(phone, full_name):
    url = f"{HOST}Api/Message/Send"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    first_name = full_name.split()[0]  # Prendiamo solo il nome dal nome completo
    
    payload = {
        "Sender": "+39xxxxxxxxxx",  # Sostituire con il numero del mittente
        "Receiver": phone,
        "Body": "{{1}}", 
        "Medias": [],
        "TemplateId": TEMPLATE_ID,
        "TemplateParameters": [
            {
                "Name": "firstName",
                "Value": first_name
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()


# Legge i dati dei clienti da un file Excel.
def read_clients_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        clients = []
        for _, row in df.iterrows():
            clients.append({
                "phone": f"+39{row['phone']}",  # Aggiungiamo il prefisso del paese
                "name": f"{row['first_name']} {row['last_name']}"
            })
        try:
            logger.info(f"Letti con successo {len(clients)} clienti dal file {file_path}")
        except Exception as e:
            logger.error(f"Errore durante la stampa del numero di clienti: {e}")
        return clients
    except Exception as e:
        logger.error(f"Errore durante la lettura del file {file_path}: {e}")
        return []

# Invia messaggi a una lista di clienti
def send_messages_to_clients(clients, message_type):
    logger.info(f"Invio messaggi {message_type}:")
    for client in clients:
        result = send_whatsapp_message(client["phone"], client["name"])
        logger.info(f"Messaggio inviato a {client['name']}: {result}")


# Dati dei clienti
clients = [
    {"phone": "+393485422909", "name": "Marco Lembo"},
    {"phone": "+393206299891", "name": "Dario Panzeri"}
]

# Prima validiamo il token
if not validate_token(ACCESS_TOKEN):
    logger.error("Errore: token di accesso non valido.")
    sys.exit(1)

# Se il token è valido, inviamo messaggi a MARCO e DARIO
send_messages_to_clients(clients, "clienti dall'elenco")

# Leggiamo i dati dei clienti dal file Excel
excel_clients = read_clients_from_excel(EXCEL_FILE_PATH)

# Inviamo messaggi ai clienti dal file Excel
send_messages_to_clients(excel_clients, "clienti dal file Excel")

logger.info("Esecuzione del programma completata.")
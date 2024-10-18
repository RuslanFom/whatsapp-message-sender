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
            logger.error(f"Token non valido. Codice di stato: {response.status_code}")
            return False
    except requests.RequestException as e:
        logger.error(f"Errore durante la validazione del token: {e}")
        return False
    except json.JSONDecodeError:
        logger.error("Errore durante l'analisi della risposta JSON.")
        return False

# Invia un messaggio WhatsApp a un cliente
def send_whatsapp_message(phone, full_name):
    url = f"{HOST}Api/Outbound/SendTemplateMessages/{TEMPLATE_ID}"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    first_name = full_name.split()[0]  # Prende solo il nome dal nome completo
    
    payload = [{
        "MobileNumber": phone,
        "var1": first_name
    }]
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Legge i dati dei clienti da un file Excel e invia messaggi
def send_messages_from_excel(file_path, batch_name):
    import os
    if not os.path.exists(file_path):
        logger.error(f"File non trovato: {file_path}")
        return {"Success": False, "ErrorMessage": "File Excel non trovato"}
    
    url = f"{HOST}Api/Outbound/SendTemplateMessages/{TEMPLATE_ID}"
    params = {
        "batchName": batch_name,
        # "scheduleTime": "2023-10-13T14:00:00"
    }
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        df = pd.read_excel(file_path)
        required_columns = ['phone', 'firstName', 'lastName']
        
        if not all(column in df.columns for column in required_columns):
            missing_columns = [col for col in required_columns if col not in df.columns]
            logger.error(f"Colonne mancanti nel file Excel: {', '.join(missing_columns)}")
            return {"Success": False, "ErrorMessage": "Formato del file Excel non valido"}
        
        batch_data = []
        for _, row in df.iterrows():
            batch_data.append({
                "MobileNumber": row['phone'],
                "firstName": row['firstName'],
                "lastName": row['lastName']
            })
        
        response = requests.post(url, headers=headers, json=batch_data, params=params)
        logger.info(f"Codice di stato della risposta: {response.status_code}")
        logger.info(f"Testo della risposta: {response.text}")
        result = response.json()
        
        if result.get("Success"):
            logger.info(f"Invio batch riuscito. BatchId: {result.get('BatchId')}, Messaggi inviati: {result.get('NewMessages')}")
        else:
            logger.error(f"Errore nell'invio dei messaggi: {result.get('ErrorMessage')}")
        
        return result
    except Exception as e:
        logger.error(f"Errore durante l'elaborazione del file Excel: {e}")
        return {"Success": False, "ErrorMessage": str(e)}

# Invia messaggi a una lista di clienti
def send_messages_to_clients(clients, message_type):
    logger.info(f"Invio messaggi {message_type}:")
    url = f"{HOST}Api/Outbound/SendTemplateMessages/{TEMPLATE_ID}"
    
    # Prepara i dati per l'invio in massa
    batch_data = []
    for client in clients:
        first_name = client["name"].split()[0]
        batch_data.append({
            "MobileNumber": client["phone"],
            "firstName": first_name
        })
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    response = requests.post(url, headers=headers, json=batch_data)
    result = response.json()
    
    logger.info(f"Risultato invio batch: {result}")
    
    if result.get("Success"):
        logger.info(f"Inviati con successo {result.get('NewMessages')} messaggi.")
    else:
        logger.error(f"Errore nell'invio dei messaggi: {result.get('ErrorMessage')}")

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

# Invia messaggi a una lista di clienti dal file Excel
result = send_messages_from_excel(EXCEL_FILE_PATH, "Invio_Clienti_Excel")
logger.info(f"Risultato dell'invio: {result}")

logger.info("Esecuzione del programma completata.")

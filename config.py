import os

# Token di accesso per l'API
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "jnWEQwIu-TdUIFGkw-tlC9s5mg-nsi1cSlm-WBmV8iJH-r0RqHuRk-H2vUywZn-aPrxnRsb")

# ID del template per i messaggi WhatsApp
TEMPLATE_ID = os.getenv("TEMPLATE_ID", "118")

# Nome del tenant
TENANT = os.getenv("TENANT", "phonetica")

# URL di base per l'API
HOST = os.getenv("HOST", f"https://witiop.intoowit.it/{TENANT}/")

# Percorso del file Excel contenente i dati dei clienti
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH", "clients.xlsx")

# Verifica che tutte le variabili di configurazione siano impostate
assert all([ACCESS_TOKEN, TEMPLATE_ID, TENANT, HOST, EXCEL_FILE_PATH]), "Configurazione incompleta. Controlla le variabili d'ambiente o il file config.py."
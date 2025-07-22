from firebase_admin import credentials, firestore, initialize_app
import os
from dotenv import load_dotenv
import json
load_dotenv()

#---------------------------------- Adatbézishoz kapcsolódás ----------------------------------
# JSON betöltése környezeti változóból
firebase_json_str = os.getenv("FIREBASE_KEY_JSON")

# Dictté alakítás
firebase_cred_dict = json.loads(firebase_json_str)

# Inicializálás dict alapján (nem fájl alapján!)
cred = credentials.Certificate(firebase_cred_dict)

initialize_app(cred)

db = firestore.client()
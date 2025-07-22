import os
import json
import base64
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()

try:
    app = firebase_admin.get_app()  # ha már létezik, csak használjuk
except ValueError:
    # --- Inicializálás csak egyszer ---
    b64 = os.getenv("FIREBASE_CRED_B64")        # ajánlott: base64-elt JSON
    json_str = os.getenv("FIREBASE_KEY_JSON")   # fallback: nyers (egy soros!) JSON
    path = os.getenv("FIREBASE_KEY_PATH")       # fallback: fájl útvonal

    if b64:
        cred_dict = json.loads(base64.b64decode(b64).decode("utf-8"))
        cred = credentials.Certificate(cred_dict)
    elif json_str:
        cred_dict = json.loads(json_str)
        cred = credentials.Certificate(cred_dict)
    elif path:
        cred = credentials.Certificate(path)
    else:
        raise RuntimeError(
            "Hiányzik a Firebase hitelesítés. Adj meg FIREBASE_CRED_B64 vagy "
            "FIREBASE_KEY_JSON vagy FIREBASE_KEY_PATH változót."
        )

    app = firebase_admin.initialize_app(cred)

db = firestore.client(app)

from firebase_admin import credentials, firestore, initialize_app
import os
from dotenv import load_dotenv

load_dotenv()

#---------------------------------- Adatbézishoz kapcsolódás ----------------------------------
firebase_key = os.path.abspath(os.path.join(os.path.dirname(__file__), "../gymdatabase-129e2-firebase-adminsdk-fbsvc-f4d145d2ff.json"))

cred = credentials.Certificate(firebase_key)
initialize_app(cred)

db = firestore.client()
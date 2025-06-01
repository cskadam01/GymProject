from firebase_admin import credentials, firestore, initialize_app
import os
from dotenv import load_dotenv

load_dotenv()


firebase_key = os.getenv("FIREBASE_KEY_PATH")

cred = credentials.Certificate(firebase_key)
initialize_app(cred)

db = firestore.client()
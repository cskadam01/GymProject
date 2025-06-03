from fastapi import FastAPI
from src.endpoints import users
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from src.endpoints import exercise



from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# ----------Cors Beállítások----------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # vagy a saját domained
    allow_credentials=True,  # ⬅⬅⬅ FONTOS: kell a sütikhez!
    allow_methods=["*"],
    allow_headers=["*"],
)



# ----------Endpoint fileok csatolása----------
app.include_router(users.router)
app.include_router(exercise.router)





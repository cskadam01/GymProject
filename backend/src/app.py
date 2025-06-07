import firebase_admin
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, firestore
from src.endpoints import diary, exercise, users

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
app.include_router(diary.router)

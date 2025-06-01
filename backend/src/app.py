from fastapi import FastAPI
from src.models import Base, engine
from src.endpoints import users
import sys
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv



from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # vagy a saját domained
    allow_credentials=True,  # ⬅⬅⬅ FONTOS: kell a sütikhez!
    allow_methods=["*"],
    allow_headers=["*"],
)



Base.metadata.create_all(bind=engine)



app.include_router(users.router)





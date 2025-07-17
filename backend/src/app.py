from fastapi import FastAPI
from src.endpoints import users, exercise, diary
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv




from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# ----------Cors Beállítások----------

app.add_middleware(
    CORSMiddleware,
        allow_origins=[
        "https://gymdatabase-129e2.web.app"
    ],
  # vagy a saját domained
    allow_credentials=True,  # ⬅⬅⬅ FONTOS: kell a sütikhez!
    allow_methods=["*"],
    allow_headers=["*"],
)



# ----------Endpoint fileok csatolása----------
app.include_router(users.router)
app.include_router(exercise.router)
app.include_router(diary.router)






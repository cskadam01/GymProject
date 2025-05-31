from fastapi import FastAPI
from src.models import Base, engine
from src.endpoints import users
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)


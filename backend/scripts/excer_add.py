import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from src.firebase import db
import pandas as pd
from datetime import datetime
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

name = input("name ")
desc = input("desc ")
muscle = input("muscle: Láb, Váll, Mell, Tricepsz, Bicepsz, Hát ")
e_type = input("e_type ")

def excer_add():
    

    data = {
        "exer_description" : desc,
        "exer_name" : name,
        "muscle" : muscle,
        "type" : e_type,
        "creation" : SERVER_TIMESTAMP
        

    }

    db.collection("exercise").add(data)

if __name__ == "__main__":
    excer_add()
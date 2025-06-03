from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from src.firebase import db
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

router = APIRouter(
    prefix="/exercise",
    tags=["Exercise"]
)


class AddExercise(BaseModel):
    name:str
    description:str
    muscle:str
    e_type:str




@router.get("/get-all-exercise")
def get_all_exercise():
    try:
        docs = db.collection("exercise").get()
        exercises = []

        for i in docs:
            data = i.to_dict()
            exercises.append(data)

        return exercises
        


    except Exception as e: 
        raise HTTPException(status_code=400, detail=f"Hiba: {e}")

@router.post("/add-new-exercise")
def add_new_exercise(e : AddExercise):


    try:
        exercise = {
            "exer_name" : e.name,
            "exer_description" : e.description,
            "type" : e.e_type,
            "muscle": e.muscle,
            "creation": SERVER_TIMESTAMP
        }
        
        db.collection("exercise").add(exercise)
        return {"message" : f"{e.name} Sikeresen hozzáadva!"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Hiba: {e}")

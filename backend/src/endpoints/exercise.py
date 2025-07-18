from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from src.firebase import db
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from src.token import get_current_user
from google.cloud import firestore

router = APIRouter(
    prefix="/exercise",
    tags=["Exercise"]
)


class AddExercise(BaseModel):
    name:str
    description:str
    muscle:str
    e_type:str

class ExerId(BaseModel):
    exerciseID : str


#------------------- ITT TALÁLHATÓAK A FELADATOKKAL KAPCSOLATOS ENDPOINTOK -------------------------


       
    


@router.get("/get-all-exercise")
def get_all_exercise(current_user: dict = Depends(get_current_user)):
    try:
        # 1. Összes feladat lekérése
        docs = db.collection("exercise").get()
        exercises = []

        # 2. Felhasználó dokumentum lekérdezése
        user_docs = db.collection("users").where("name", "==", current_user["name"]).limit(1).get()
        if not user_docs:
            raise HTTPException(status_code=404, detail="Felhasználó nem található")

        # 3. Elmentett gyakorlatok listája
        saved = user_docs[0].to_dict().get("saved_exercises", [])

        # 4. Végigmegyünk az összes feladaton, és megnézzük, el van-e mentve
        for i in docs:
            data = i.to_dict() #minden json objektumot doc-á alakítunk és betesszük a data változóba
            data["id"] = i.id # a data "id" kulcshoz hozzá rendeljük a firebase id-t mivel ez alapból nincs benne
            data["saved"] = data["id"] in saved # ami benne van a saved feladatokban azokat hozzá tesszük a "saved kulcshoz" 
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
    


@router.get("/exer/{id}")
def get_exercise(id: str):
    print("KERESÉS:", id)
    doc_ref = db.collection("exercise").document(id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Nincs ilyen feladat")
    

    return doc.to_dict()

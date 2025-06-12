from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from src.firebase import db
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from src.token import get_current_user
from google.cloud import firestore

router = APIRouter(
    prefix="/diary",
    tags=["Diary"]
)


class NewSave(BaseModel):
    exer_id: str
    exerName: str
    weight: int
    reps: int
   


@router.get("/user-diary")
def get_saved_exer(current_user: dict = Depends(get_current_user)):
        
    try:
        saves = []

        docs = db.collection("users").where("name", "==", current_user["name"]).limit(1).get()


        saved_ids = docs[0].to_dict().get("saved_exercises", [])


        for exercise_id in saved_ids:
            doc = db.collection("exercise").document(exercise_id).get()
            if doc.exists:
                data = doc.to_dict()
                data["id"] = doc.id
                saves.append(data)

        return saves
    
    except Exception as e:
        print(f"Hiba {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"valami hiba lépett fel a lekérdezéskor: {e}")
    

@router.post("/add-new-record")
def add_new_record(task : NewSave, current_user : dict = Depends(get_current_user)):
    try:
        data = {
            "user" : current_user["name"],
            "task_id" : task.exer_id,
            "exer_name": task.exerName,
            "rep" : task.reps,
            "weight": task.weight,
            "date": SERVER_TIMESTAMP
        }

        db.collection("diary_entries").add(data)

        return {"message" : "Sikeres naplózás"}
    

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Szett rögzítése sikertelen {e}")



@router.get("/by-exercise")
def get_diary_entries_by_exercise(exercise_id: str = Query(...), current_user : dict = Depends(get_current_user)):

    saved_reps = db.collection("diary_entries").where("task_id", "==", exercise_id).where("user", "==", current_user["name"])
    docs = list(saved_reps.stream())

    if not docs:
        raise HTTPException(status_code=404, detail="Nincs ilyen feladatod naplózva.")
    
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

@router.get("/is-authorized")
def is_exercise_authorized(exercise_id: str = Query(...), current_user: dict = Depends(get_current_user)):
    if exercise_id in current_user.get("urls", []):
        return {"authorized": True}
    return {"authorized": False}


    








    

     




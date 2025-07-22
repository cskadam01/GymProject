from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from firebase import db
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from jwt_token import get_current_user
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

class ExerId(BaseModel):
    exerciseID : str



@router.get("/user-diary")
def get_saved_exer(current_user: dict = Depends(get_current_user)):
    try:
        user_doc = db.collection("users").document(current_user["name"]).get()
        user = user_doc.to_dict()
        saved_ids = user.get("saved_exercises", [])

        doc_refs = [db.collection("exercise").document(doc_id) for doc_id in saved_ids]
        docs = db.get_all(doc_refs)

        saves = []
        for doc in docs:
            if doc.exists:
                data = doc.to_dict()
                data["id"] = doc.id
                saves.append(data)

        return saves

    except Exception as e:
        print(f"Hiba {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"valami hiba lépett fel a lekérdezéskor: {e}")

    

@router.post("/save-to-diary")


def save_to_diary(exer : ExerId, current_user: dict = Depends(get_current_user)):
    try:
        print("EXER ID:", exer.exerciseID)
        print("USER NAME:", current_user["name"])

        user_doc = db.collection("users").document(current_user["name"]).get()
        



        user_ref = user_doc.reference #referencel megszerezzük hogy a gettel melyik objektumot kértük le

        user_ref.update({
                "saved_exercises": firestore.ArrayUnion([exer.exerciseID])   #feladat arrayhez való apendálás a feladat idjét
            })
        
        return{"success" : "Feladat hozzá adva a naplóhoz"}

    except Exception as e:
        print("Hiba Firestore frissítésnél:", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Naplózás sikertelen: {e}")
    

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
    
    saves = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        saves.append(data)

    # ✅ rendezés az eredeti datetime alapján (mert data["date"] az)
    saves.sort(key=lambda x: x["date"])

# 🕒 csak ezután formázod stringgé

      
    
    return saves
    
#------------------- ITT TALÁLHATÓAK A NAPLÓZÁSSAL KAPCSOLATOS ENDPOINTOK -------------------------



@router.get("/is-authorized")
def is_exercise_authorized(exercise_id: str = Query(...), #A Querry miatt kötelező paraméter lesz
                           current_user: dict = Depends(get_current_user)):
    
    
    user_doc = db.collection("users").document(current_user["name"]).get()
    user = user_doc.to_dict()
    saved_ids =user.get("saved_exercises", [])

    if exercise_id in saved_ids: #Megnézzük hogy a frontendről érkezett id benne van e a felhasználó által mentett idk listájában
            return {"authorized": True}
    return {"authorized": False}
    
    
@router.delete("/delete/{entry_id}")
def delete_diary_entry(entry_id: str, current_user: dict = Depends(get_current_user)):
    try:
        # Lekérdezzük a bejegyzést
        doc_ref = db.collection("diary_entries").document(entry_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="Naplóbejegyzés nem található")

        # Ellenőrizzük, hogy a bejegyzés a jelenlegi felhasználóhoz tartozik-e
        if doc.to_dict().get("user") != current_user["name"]:
            raise HTTPException(status_code=403, detail="Nincs jogosultságod ezt törölni")

        # Törlés
        doc_ref.delete()
        return {"message": "Sikeresen törölve"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Törlés sikertelen: {e}")


    








    

     




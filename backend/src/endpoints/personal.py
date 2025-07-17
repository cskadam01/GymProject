from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from src.token import get_current_user
from src.firebase import db
from typing import Optional



router = APIRouter(
    prefix="/personal",
    tags=["presonal"]
)

class PersonalMeasurements(BaseModel):
    body_weight: Optional[float]  # kg
    height: Optional[float]       # cm
    body_fat: Optional[float]     # %
    biceps: Optional[float]       # cm
    hips: Optional[float]         # cm
    waist: Optional[float]        # cm
    upper_arm: Optional[float]    # cm
    forearm: Optional[float]      # cm
    shoulders: Optional[float]    # cm
    chest: Optional[float]        # cm
    abs: Optional[float]          # cm
    thigh: Optional[float]        # cm
    calf: Optional[float]         # cm
    neck: Optional[float]         # cm
    wrist: Optional[float]        # cm



@router.post("/add-measurements")
def add_measurements(measure : PersonalMeasurements, current_user : dict = Depends(get_current_user)):
    try:  
        data = measure.dict()
        filterd_data = {
            "name" : current_user["name"]

        }

        for key, mes in data.items():
            if mes not in (0, None):
                filterd_data[key] = mes

        db.collection("measurements").add(filterd_data)
        return {"message" : "Sikeres naplózás"}
    
    except Exception as e :
        return{"error" : f"Nem várt hiba történt, késöbb próbáld újra {e}"}


@router.get("/get-measurements")
def get_measurements( current_user : dict = Depends(get_current_user)):

    measure_saves = db.collection("measurements").where("name", "==", current_user["name"]).get()
    if not measure_saves:
        return{"Message" : "Még nincsenek mentett mértékek"}
    

    measures = []
    for doc in measure_saves:
        measures.append(doc.to_dict())

    return{"measurements" : measures}






    






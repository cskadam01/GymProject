from src.firebase import db
from src.schemas.personal import PersonalMeasurements


def add_measurements(measure: PersonalMeasurements, username: str):
    data = measure.model_dump()
    filtered_data = {"name": username}

    for key, mes in data.items():
        if mes not in (0, None):
            filtered_data[key] = mes

    db.collection("measurements").add(filtered_data)
    return {"message": "Sikeres naplózás"}


def get_measurements(username: str):
    measure_saves = db.collection("measurements").where("name", "==", username).get()
    if not measure_saves:
        return {"Message": "Még nincsenek mentett mértékek"}

    measures = []
    for doc in measure_saves:
        measures.append(doc.to_dict())

    return {"measurements": measures}

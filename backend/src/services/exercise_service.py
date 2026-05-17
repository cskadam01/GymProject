from fastapi import HTTPException
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

from src.firebase import db
from src.schemas.exercise import AddExercise


def get_all_exercises_for_user(username: str):
    docs = db.collection("exercise").get()
    exercises = []

    user_doc = db.collection("users").document(username).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")

    user = user_doc.to_dict()
    saved = user.get("saved_exercises", [])

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        data["saved"] = data["id"] in saved
        exercises.append(data)

    return exercises


def add_exercise(exercise_data: AddExercise, username: str):
    exercise = {
        "exer_name": exercise_data.name,
        "exer_description": exercise_data.description,
        "type": exercise_data.e_type,
        "muscle": exercise_data.muscle,
        "created_by": username,
        "creation": SERVER_TIMESTAMP,
    }

    db.collection("exercise").add(exercise)
    return {"message": f"{exercise_data.name} Sikeresen hozzáadva!"}


def get_exercise_by_id(exercise_id: str):
    doc_ref = db.collection("exercise").document(exercise_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Nincs ilyen feladat")

    return doc.to_dict()

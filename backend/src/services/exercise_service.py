from fastapi import HTTPException
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

from src.firebase import db
from src.schemas.exercise import AddExercise


def get_all_exercises_for_user(username: str, limit: int = 20, cursor: int | None = None):
    offset = cursor or 0
    page_size = min(max(limit, 1), 50)
    docs = (
        db.collection("exercise")
        .order_by("exer_name")
        .offset(offset)
        .limit(page_size + 1)
        .stream()
    )
    exercises = []

    user_doc = db.collection("users").document(username).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")

    user = user_doc.to_dict()
    saved = user.get("saved_exercises", [])

    docs_list = list(docs)
    page_docs = docs_list[:page_size]

    for doc in page_docs:
        data = doc.to_dict()
        data["id"] = doc.id
        data["saved"] = data["id"] in saved
        exercises.append(data)

    has_more = len(docs_list) > page_size

    return {
        "items": exercises,
        "next_cursor": offset + len(page_docs) if has_more else None,
        "has_more": has_more,
    }


def add_exercise(exercise_data: AddExercise, username: str):
    exercise = {
        "exer_name": exercise_data.name,
        "exer_description": exercise_data.description,
        "type": exercise_data.e_type,
        "muscle": exercise_data.muscle,
        "created_by": username,
        "creation": SERVER_TIMESTAMP,
    }

    if exercise_data.e_type == "Gép" and exercise_data.machine_brand:
        exercise["machine_brand"] = exercise_data.machine_brand

    db.collection("exercise").add(exercise)
    return {"message": f"{exercise_data.name} Sikeresen hozzáadva!"}


def get_exercise_by_id(exercise_id: str):
    doc_ref = db.collection("exercise").document(exercise_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Nincs ilyen feladat")

    return doc.to_dict()

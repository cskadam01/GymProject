from fastapi import HTTPException
from google.cloud import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

from src.firebase import db
from src.schemas.diary import ExerId, NewSave


def _get_user(username: str):
    user_doc = db.collection("users").document(username).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")
    return user_doc


def _get_exercise(exercise_id: str):
    exercise_doc = db.collection("exercise").document(exercise_id).get()
    if not exercise_doc.exists:
        raise HTTPException(status_code=404, detail="Feladat nem található")
    return exercise_doc


def _require_saved_exercise(username: str, exercise_id: str):
    user_doc = _get_user(username)
    user = user_doc.to_dict()
    saved_ids = user.get("saved_exercises", [])
    if exercise_id not in saved_ids:
        raise HTTPException(status_code=403, detail="Nincs jogosultságod ehhez a feladathoz")
    return user_doc


def get_saved_exercises(username: str):
    user_doc = _get_user(username)
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


def save_exercise_to_diary(exercise: ExerId, username: str):
    _get_exercise(exercise.exerciseID)
    user_doc = _get_user(username)
    user_ref = user_doc.reference

    user_ref.update({"saved_exercises": firestore.ArrayUnion([exercise.exerciseID])})
    return {"success": "Feladat hozzá adva a naplóhoz"}


def add_diary_record(task: NewSave, username: str):
    _require_saved_exercise(username, task.exer_id)
    exercise_doc = _get_exercise(task.exer_id)
    exercise = exercise_doc.to_dict()

    data = {
        "user": username,
        "task_id": task.exer_id,
        "exer_name": exercise.get("exer_name", task.exerName),
        "rep": task.reps,
        "weight": task.weight,
        "date": SERVER_TIMESTAMP,
    }

    db.collection("diary_entries").add(data)
    return {"message": "Sikeres naplózás"}


def get_entries_by_exercise(exercise_id: str, username: str):
    saved_reps = (
        db.collection("diary_entries")
        .where("task_id", "==", exercise_id)
        .where("user", "==", username)
    )
    docs = list(saved_reps.stream())

    if not docs:
        raise HTTPException(status_code=404, detail="Nincs ilyen feladatod naplózva.")

    saves = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        saves.append(data)

    saves.sort(key=lambda x: x["date"])
    return saves


def is_exercise_authorized(exercise_id: str, username: str):
    user_doc = _get_user(username)
    user = user_doc.to_dict()
    saved_ids = user.get("saved_exercises", [])

    return {"authorized": exercise_id in saved_ids}


def delete_diary_entry(entry_id: str, username: str):
    doc_ref = db.collection("diary_entries").document(entry_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Naplóbejegyzés nem található")

    if doc.to_dict().get("user") != username:
        raise HTTPException(status_code=403, detail="Nincs jogosultságod ezt törölni")

    doc_ref.delete()
    return {"message": "Sikeresen törölve"}

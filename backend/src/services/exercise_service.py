from fastapi import HTTPException
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

from src.firebase import db
from src.schemas.exercise import AddExercise


DEFAULT_EXERCISE_CREATOR_ID = "Csadax"
FIRESTORE_BATCH_LIMIT = 450


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
    machine_brand = exercise_data.machine_brand if exercise_data.e_type == "Gép" else None

    if exercise_data.e_type == "Gép" and not machine_brand:
        raise HTTPException(
            status_code=400,
            detail="Gépes feladatnál kötelező megadni a gép márkáját.",
        )

    exercise = {
        "exer_name": exercise_data.name,
        "exer_description": exercise_data.description,
        "type": exercise_data.e_type,
        "muscle": exercise_data.muscle,
        "creator_id": username,
        "created_by": username,
        "creation": SERVER_TIMESTAMP,
    }

    if machine_brand:
        exercise["machine_brand"] = machine_brand

    db.collection("exercise").add(exercise)
    return {"message": f"{exercise_data.name} Sikeresen hozzáadva!"}


def backfill_exercise_creator_ids(default_creator_id: str = DEFAULT_EXERCISE_CREATOR_ID):
    creator_id = default_creator_id.strip()

    if not creator_id:
        raise HTTPException(status_code=400, detail="Hiányzó creator id.")

    batch = db.batch()
    pending_writes = 0
    skipped = 0
    updated = 0

    for doc in db.collection("exercise").stream():
        data = doc.to_dict() or {}

        if data.get("creator_id"):
            skipped += 1
            continue

        batch.update(doc.reference, {"creator_id": creator_id})
        pending_writes += 1
        updated += 1

        if pending_writes >= FIRESTORE_BATCH_LIMIT:
            batch.commit()
            batch = db.batch()
            pending_writes = 0

    if pending_writes:
        batch.commit()

    return {
        "creator_id": creator_id,
        "message": "Feladat creator id backfill kész.",
        "skipped": skipped,
        "updated": updated,
    }


def get_exercise_by_id(exercise_id: str):
    doc_ref = db.collection("exercise").document(exercise_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Nincs ilyen feladat")

    return doc.to_dict()
from fastapi import HTTPException
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

from src.firebase import db
from src.schemas.workout_plan import CreateWorkoutPlan, UpdateWorkoutPlan


COLLECTION_NAME = "workout_plans"


def _get_user(username: str):
    user_doc = db.collection("users").document(username).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")

    return user_doc


def _get_saved_exercise_ids(username: str) -> set[str]:
    user_doc = _get_user(username)
    user = user_doc.to_dict() or {}

    return set(user.get("saved_exercises", []))


def _validate_saved_exercises(username: str, exercise_ids: list[str]):
    saved_ids = _get_saved_exercise_ids(username)
    missing_ids = [
        exercise_id for exercise_id in exercise_ids if exercise_id not in saved_ids
    ]

    if missing_ids:
        raise HTTPException(
            status_code=403,
            detail="Csak a saját naplódban szereplő feladatokat teheted edzéstervbe.",
        )


def _get_plan_for_owner(plan_id: str, username: str):
    doc_ref = db.collection(COLLECTION_NAME).document(plan_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Edzésterv nem található")

    plan = doc.to_dict() or {}
    if plan.get("owner") != username:
        raise HTTPException(
            status_code=403,
            detail="Nincs jogosultságod ehhez az edzéstervhez.",
        )

    return doc_ref, plan


def _serialize_plan(doc):
    plan = doc.to_dict() or {}
    plan["id"] = doc.id

    return plan


def _created_at_sort_value(plan: dict):
    created_at = plan.get("created_at")
    if hasattr(created_at, "timestamp"):
        return created_at.timestamp()

    return 0


def create_workout_plan(plan_data: CreateWorkoutPlan, username: str):
    _validate_saved_exercises(username, plan_data.exercise_ids)

    plan = {
        "name": plan_data.name,
        "owner": username,
        "exercise_ids": plan_data.exercise_ids,
        "created_at": SERVER_TIMESTAMP,
        "updated_at": SERVER_TIMESTAMP,
    }

    _, doc_ref = db.collection(COLLECTION_NAME).add(plan)
    created_doc = doc_ref.get()

    return _serialize_plan(created_doc)


def get_workout_plans(username: str):
    docs = db.collection(COLLECTION_NAME).where("owner", "==", username).stream()
    plans = [_serialize_plan(doc) for doc in docs]

    plans.sort(key=_created_at_sort_value, reverse=True)
    return plans


def get_workout_plan(plan_id: str, username: str):
    doc_ref, _ = _get_plan_for_owner(plan_id, username)

    return _serialize_plan(doc_ref.get())


def update_workout_plan(plan_id: str, plan_data: UpdateWorkoutPlan, username: str):
    doc_ref, _ = _get_plan_for_owner(plan_id, username)
    _validate_saved_exercises(username, plan_data.exercise_ids)

    doc_ref.update(
        {
            "name": plan_data.name,
            "exercise_ids": plan_data.exercise_ids,
            "updated_at": SERVER_TIMESTAMP,
        }
    )

    return _serialize_plan(doc_ref.get())


def delete_workout_plan(plan_id: str, username: str):
    doc_ref, _ = _get_plan_for_owner(plan_id, username)
    doc_ref.delete()

    return {"message": "Edzésterv törölve"}

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from src.jwt_token import get_current_user
from src.rate_limit import enforce_rate_limit
from src.schemas.diary import ExerId, NewSave
from src.services.diary_service import (
    add_diary_record,
    delete_diary_entry as delete_diary_entry_service,
    get_entries_by_exercise,
    get_progress_summary,
    get_saved_exercises,
    is_exercise_authorized as is_exercise_authorized_service,
    save_exercise_to_diary,
)

router = APIRouter(
    prefix="/diary",
    tags=["Diary"],
)


@router.get("/user-diary")
def get_saved_exer(
    limit: int = Query(20, ge=1, le=50),
    cursor: int | None = Query(None, ge=0),
    current_user: dict = Depends(get_current_user),
):
    try:
        return get_saved_exercises(current_user["name"], limit=limit, cursor=cursor)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"valami hiba lépett fel a lekérdezéskor: {e}",
        )


@router.post("/save-to-diary")
def save_to_diary(request: Request, exer: ExerId, current_user: dict = Depends(get_current_user)):
    enforce_rate_limit(
        request,
        "save-exercise-user",
        limit=60,
        window_seconds=3600,
        identifier=current_user["name"].lower(),
    )
    try:
        return save_exercise_to_diary(exer, current_user["name"])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Naplózás sikertelen: {e}")


@router.post("/add-new-record")
def add_new_record(request: Request, task: NewSave, current_user: dict = Depends(get_current_user)):
    enforce_rate_limit(
        request,
        "add-diary-record-user",
        limit=120,
        window_seconds=3600,
        identifier=current_user["name"].lower(),
    )
    try:
        return add_diary_record(task, current_user["name"])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Szett rögzítése sikertelen {e}")


@router.get("/by-exercise")
def get_diary_entries_by_exercise(
    exercise_id: str = Query(...), current_user: dict = Depends(get_current_user)
):
    return get_entries_by_exercise(exercise_id, current_user["name"])


@router.get("/progress-summary")
def get_diary_progress_summary(
    exercise_id: str = Query(...), current_user: dict = Depends(get_current_user)
):
    return get_progress_summary(exercise_id, current_user["name"])


@router.get("/is-authorized")
def is_exercise_authorized(exercise_id: str = Query(...), current_user: dict = Depends(get_current_user)):
    return is_exercise_authorized_service(exercise_id, current_user["name"])


@router.delete("/delete/{entry_id}")
def delete_diary_entry(entry_id: str, current_user: dict = Depends(get_current_user)):
    try:
        return delete_diary_entry_service(entry_id, current_user["name"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Törlés sikertelen: {e}")

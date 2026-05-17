from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from src.jwt_token import get_current_user
from src.rate_limit import enforce_rate_limit
from src.schemas.exercise import AddExercise
from src.services.exercise_service import add_exercise, get_all_exercises_for_user, get_exercise_by_id

router = APIRouter(
    prefix="/exercise",
    tags=["Exercise"],
)


@router.get("/get-all-exercise")
def get_all_exercise(
    limit: int = Query(20, ge=1, le=50),
    cursor: int | None = Query(None, ge=0),
    current_user: dict = Depends(get_current_user),
):
    try:
        return get_all_exercises_for_user(current_user["name"], limit=limit, cursor=cursor)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Hiba: {e}")


@router.post("/add-new-exercise")
def add_new_exercise(request: Request, e: AddExercise, current_user: dict = Depends(get_current_user)):
    enforce_rate_limit(
        request,
        "add-exercise-user",
        limit=20,
        window_seconds=3600,
        identifier=current_user["name"].lower(),
    )
    try:
        return add_exercise(e, current_user["name"])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Hiba: {e}")


@router.get("/exer/{id}")
def get_exercise(id: str, current_user: dict = Depends(get_current_user)):
    return get_exercise_by_id(id)

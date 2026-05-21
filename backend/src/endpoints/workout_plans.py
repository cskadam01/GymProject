from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.jwt_token import get_current_user
from src.rate_limit import enforce_rate_limit
from src.schemas.workout_plan import CreateWorkoutPlan, UpdateWorkoutPlan
from src.services.workout_plan_service import (
    create_workout_plan,
    delete_workout_plan as delete_workout_plan_service,
    get_workout_plan,
    get_workout_plans,
    update_workout_plan,
)

router = APIRouter(
    prefix="/workout-plans",
    tags=["Workout plans"],
)


@router.get("")
def list_workout_plans(current_user: dict = Depends(get_current_user)):
    try:
        return get_workout_plans(current_user["name"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lekérdezés sikertelen: {e}",
        )


@router.get("/{plan_id}")
def get_one_workout_plan(plan_id: str, current_user: dict = Depends(get_current_user)):
    try:
        return get_workout_plan(plan_id, current_user["name"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lekérdezés sikertelen: {e}",
        )


@router.post("")
def create_new_workout_plan(
    request: Request,
    plan: CreateWorkoutPlan,
    current_user: dict = Depends(get_current_user),
):
    enforce_rate_limit(
        request,
        "create-workout-plan-user",
        limit=40,
        window_seconds=3600,
        identifier=current_user["name"].lower(),
    )
    try:
        return create_workout_plan(plan, current_user["name"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Mentés sikertelen: {e}",
        )


@router.put("/{plan_id}")
def update_existing_workout_plan(
    plan_id: str,
    request: Request,
    plan: UpdateWorkoutPlan,
    current_user: dict = Depends(get_current_user),
):
    enforce_rate_limit(
        request,
        "update-workout-plan-user",
        limit=80,
        window_seconds=3600,
        identifier=current_user["name"].lower(),
    )
    try:
        return update_workout_plan(plan_id, plan, current_user["name"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Módosítás sikertelen: {e}",
        )


@router.delete("/{plan_id}")
def delete_existing_workout_plan(
    plan_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        return delete_workout_plan_service(plan_id, current_user["name"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Törlés sikertelen: {e}",
        )

from fastapi import APIRouter, Depends, Request

from src.jwt_token import get_current_user
from src.rate_limit import enforce_rate_limit
from src.schemas.personal import PersonalMeasurements
from src.services.personal_service import add_measurements as add_measurements_service
from src.services.personal_service import get_measurements as get_measurements_service

router = APIRouter(
    prefix="/personal",
    tags=["Personal"],
)


@router.post("/add-measurements")
def add_measurements(request: Request, measure: PersonalMeasurements, current_user: dict = Depends(get_current_user)):
    enforce_rate_limit(
        request,
        "add-measurements-user",
        limit=60,
        window_seconds=3600,
        identifier=current_user["name"].lower(),
    )
    return add_measurements_service(measure, current_user["name"])


@router.get("/get-measurements")
def get_measurements(current_user: dict = Depends(get_current_user)):
    return get_measurements_service(current_user["name"])

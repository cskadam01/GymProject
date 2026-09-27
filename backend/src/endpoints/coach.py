from fastapi import APIRouter, Depends, Request

from src.jwt_token import get_current_user
from src.rate_limit import enforce_rate_limit
from src.schemas.coach import JoinCoach
from src.services.coach_service import create_invite, join_coach, list_clients


router = APIRouter(prefix="/coach", tags=["Coach"])


@router.get("/clients")
def get_clients(current_user: dict = Depends(get_current_user)):
    return list_clients(current_user["name"])


@router.post("/invitations")
def new_invitation(request: Request, current_user: dict = Depends(get_current_user)):
    enforce_rate_limit(request, "coach-invite", limit=20, window_seconds=3600, identifier=current_user["name"].lower())
    return create_invite(current_user["name"])


@router.post("/join")
def accept_invitation(request: Request, payload: JoinCoach, current_user: dict = Depends(get_current_user)):
    enforce_rate_limit(request, "coach-join", limit=10, window_seconds=3600, identifier=current_user["name"].lower())
    return join_coach(payload.code, current_user["name"])

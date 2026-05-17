from fastapi import APIRouter, Depends, Request

from src.jwt_token import get_current_user
from src.rate_limit import enforce_rate_limit
from src.schemas.user import (
    ChangePassword,
    ForgottenPassword,
    GoalValue,
    LoginUser,
    PasswordResetConfirm,
    RefreshRequest,
    RegisterUser,
)
from src.services.user_service import (
    change_user_password,
    confirm_password_reset,
    get_user_profile,
    login_user,
    refresh_access_token,
    register_user,
    send_forgotten_password_email,
    set_user_goal,
)
from src.utils.get_streak import get_streak, get_total_workouts, get_total_workouts_days, get_weekly_prs

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/test-protected")
def test_protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Be vagy jelentkezve, {current_user['name']}!"}


@router.get("/me")
def get_me(
    current_user: dict = Depends(get_current_user),
    streak: int = Depends(get_streak),
    total_workouts: int = Depends(get_total_workouts),
    prs: int = Depends(get_weekly_prs),
    days: set = Depends(get_total_workouts_days),
):
    return get_user_profile(current_user["name"], streak, total_workouts, prs, days)


@router.post("/set-goal")
def set_goal(value: GoalValue, current_user: dict = Depends(get_current_user)):
    return set_user_goal(value, current_user["name"])


@router.post("/login")
def login(request: Request, user: LoginUser):
    enforce_rate_limit(request, "login-ip", limit=10, window_seconds=60)
    enforce_rate_limit(request, "login-user", limit=5, window_seconds=300, identifier=user.name.lower())
    return login_user(user, request)


@router.post("/register")
def register(request: Request, user: RegisterUser):
    enforce_rate_limit(request, "register-ip", limit=5, window_seconds=3600)
    return register_user(user)


@router.post("/forgotten-passoword")
async def forgotten_password(request: Request, user: ForgottenPassword):
    enforce_rate_limit(request, "forgot-password-ip", limit=3, window_seconds=900)
    enforce_rate_limit(
        request,
        "forgot-password-user",
        limit=3,
        window_seconds=3600,
        identifier=user.user_name.lower(),
    )
    return await send_forgotten_password_email(user)


@router.post("/change-password")
def change_password(request: Request, passes: ChangePassword, current_user: dict = Depends(get_current_user)):
    enforce_rate_limit(
        request,
        "change-password-user",
        limit=5,
        window_seconds=900,
        identifier=current_user["name"].lower(),
    )
    return change_user_password(passes, current_user["name"])


@router.post("/reset-password")
def reset_password(request: Request, payload: PasswordResetConfirm):
    enforce_rate_limit(request, "reset-password-ip", limit=5, window_seconds=900)
    return confirm_password_reset(payload)


@router.post("/refresh")
def refresh_tokens(request: Request, payload: RefreshRequest):
    enforce_rate_limit(request, "refresh-ip", limit=30, window_seconds=60)
    return refresh_access_token(payload)

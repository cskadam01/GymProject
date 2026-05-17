import hashlib
import html
import os
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import HTTPException, Request, status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from jose import JWTError, jwt

from src.firebase import db
from src.jwt_token import ALGORITHM, SECRET_KEY, create_access_token, create_refresh_token
from src.rate_limit import get_client_ip
from src.schemas.user import (
    ChangePassword,
    ForgottenPassword,
    GoalValue,
    LoginUser,
    PasswordResetConfirm,
    RefreshRequest,
    RegisterUser,
)


GENERIC_LOGIN_ERROR = "Helytelen felhasználónév vagy jelszó"
GENERIC_RESET_RESPONSE = {
    "success": "Ha létezik ilyen felhasználó, elküldtük a jelszó-visszaállító e-mailt."
}
PASSWORD_RESET_EXPIRES = timedelta(minutes=int(os.getenv("PASSWORD_RESET_EXPIRES_MINUTES", "15")))
DUMMY_PASSWORD_HASH = bcrypt.hashpw(b"dummy-password-for-timing", bcrypt.gensalt()).decode()


def _get_mail_config() -> ConnectionConfig:
    required = [
        "MAIL_USERNAME",
        "MAIL_PASSWORD",
        "MAIL_FROM",
        "MAIL_PORT",
        "MAIL_SERVER",
    ]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise HTTPException(status_code=500, detail="Email küldés nincs konfigurálva.")

    return ConnectionConfig(
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_FROM=os.getenv("MAIL_FROM"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
        MAIL_SERVER=os.getenv("MAIL_SERVER"),
        MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
        MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
        USE_CREDENTIALS=os.getenv("USE_CREDENTIALS") == "True",
    )


def _invalid_credentials():
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=GENERIC_LOGIN_ERROR)


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _revoke_refresh_tokens(username: str) -> None:
    docs = db.collection("refresh-tokens").where("sub", "==", username).where("revoked", "==", False).stream()
    for doc in docs:
        doc.reference.update(
            {
                "revoked": True,
                "revoked_at": datetime.now(timezone.utc).isoformat(),
            }
        )


def get_user_profile(username: str, streak: int, total_workouts: int, prs: int, days):
    user_doc = db.collection("users").document(username).get()
    user = user_doc.to_dict()
    added_exercises = len(user.get("saved_exercises", []))
    days_list = list(days) if days is not None else []

    return {
        "message": "Sikeres azonosítás",
        "user": user["name"],
        "age": user["age"],
        "email": user["email"],
        "exers": added_exercises,
        "streak": streak,
        "total_workouts": total_workouts,
        "weekly_prs": prs,
        "days": days_list,
    }


def set_user_goal(value: GoalValue, username: str):
    db.collection("users").document(username).update({"goal_weight": value.value})
    return {"message": "Cél sikeresen beállítva", "goal_weight": value.value}


def login_user(user: LoginUser, request: Request):
    db_user = db.collection("users").where("name", "==", user.name).get()
    client_ip = get_client_ip(request)
    now = datetime.now(timezone.utc).isoformat()

    if not db_user:
        bcrypt.checkpw(user.password.encode("utf-8"), DUMMY_PASSWORD_HASH.encode("utf-8"))
        db.collection("login-logs").document(f"{now} unknown").set(
            {
                "name": user.name,
                "time": now,
                "ip": client_ip,
                "status": "failed",
                "reason": "invalid_credentials",
            }
        )
        _invalid_credentials()

    user_data = db_user[0].to_dict()
    doc_id = f"{now} {user_data['name']}"

    if not bcrypt.checkpw(user.password.encode("utf-8"), user_data["password"].encode("utf-8")):
        error_data = {
            "name": user_data["name"],
            "time": now,
            "ip": client_ip,
            "status": "failed",
            "reason": "invalid_credentials",
        }
        db.collection("login-logs").document(doc_id).set(error_data)
        _invalid_credentials()

    access_token = create_access_token({"sub": user_data["name"]})
    refresh_token, jti, refresh_exp = create_refresh_token({"sub": user_data["name"]})

    db.collection("refresh-tokens").document(jti).set(
        {
            "jti": jti,
            "sub": user_data["name"],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": refresh_exp.isoformat(),
            "revoked": False,
        }
    )

    data = {
        "name": user_data["name"],
        "time": now,
        "ip": client_ip,
        "status": "success",
    }
    db.collection("login-logs").document(doc_id).set(data)

    return {
        "message": "Sikeres bejelentkezés",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "name": user_data["name"],
        "email": user_data["email"],
    }


def register_user(user: RegisterUser):
    user_ref = db.collection("users").document(user.name)
    if user_ref.get().exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Foglalt felhasználónév")

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    data = {
        "name": user.name,
        "age": user.age,
        "password": hashed_password,
        "email": user.email,
        "saved_exercises": [],
    }

    user_ref.set(data)
    return {"success": f"{user.name} sikeresen regisztrálva"}


async def send_forgotten_password_email(user: ForgottenPassword):
    user_ref = db.collection("users").where("name", "==", user.user_name).get()
    if not user_ref:
        return GENERIC_RESET_RESPONSE

    user_data = user_ref[0].to_dict()
    reset_token = secrets.token_urlsafe(32)
    token_hash = _hash_token(reset_token)
    expires_at = datetime.now(timezone.utc) + PASSWORD_RESET_EXPIRES

    db.collection("password-reset-tokens").document(token_hash).set(
        {
            "sub": user_data["name"],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": expires_at.isoformat(),
            "used_at": None,
        }
    )

    reset_url = os.getenv("PASSWORD_RESET_URL")
    reset_target = f"{reset_url}?token={reset_token}" if reset_url else reset_token
    safe_name = html.escape(user_data["name"])
    safe_target = html.escape(reset_target)

    template = f"""
    <html>
        <body>
            <h1>Kedves {safe_name}!</h1>
            <p>Jelszó-visszaállítást kértél a FluxNote fiókodhoz.</p>
            <p>A visszaállító link/kód 15 percig érvényes:</p>
            <p>{safe_target}</p>
            <p>Ha nem te kérted, hagyd figyelmen kívül ezt az e-mailt.</p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="FluxNote jelszó-visszaállítás",
        recipients=[user_data["email"]],
        body=template,
        subtype="html",
    )

    fm = FastMail(_get_mail_config())
    await fm.send_message(message)
    return GENERIC_RESET_RESPONSE


def change_user_password(passes: ChangePassword, username: str):
    db_user = db.collection("users").where("name", "==", username).get()
    user_ref = db_user[0].to_dict()

    if not bcrypt.checkpw(passes.old_password.encode("utf-8"), user_ref["password"].encode("utf-8")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Helytelen jelszó")

    hashed_password = bcrypt.hashpw(passes.new_password.encode(), bcrypt.gensalt()).decode()
    db.collection("users").document(username).update({"password": hashed_password})
    _revoke_refresh_tokens(username)
    return {"message": "Jelszó sikeresen módosítva"}


def confirm_password_reset(payload: PasswordResetConfirm):
    token_hash = _hash_token(payload.reset_token)
    token_ref = db.collection("password-reset-tokens").document(token_hash)
    token_doc = token_ref.get()

    if not token_doc.exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Érvénytelen vagy lejárt reset token")

    token_data = token_doc.to_dict()
    if token_data.get("used_at"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Érvénytelen vagy lejárt reset token")

    expires_at = datetime.fromisoformat(token_data["expires_at"].replace("Z", "+00:00"))
    if datetime.now(timezone.utc) > expires_at:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Érvénytelen vagy lejárt reset token")

    username = token_data.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Érvénytelen vagy lejárt reset token")

    hashed_password = bcrypt.hashpw(payload.new_password.encode(), bcrypt.gensalt()).decode()
    db.collection("users").document(username).update({"password": hashed_password})
    token_ref.update({"used_at": datetime.now(timezone.utc).isoformat()})
    _revoke_refresh_tokens(username)

    return {"message": "Jelszó sikeresen módosítva"}


def refresh_access_token(payload: RefreshRequest):
    try:
        decoded = jwt.decode(payload.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Érvénytelen vagy lejárt refresh token")

    if decoded.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nem refresh token")

    jti = decoded.get("jti")
    sub = decoded.get("sub")
    if not jti or not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Hiányzó token adatok")

    doc_ref = db.collection("refresh-tokens").document(jti)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ismeretlen refresh token")

    token_row = doc.to_dict()
    if token_row.get("sub") != sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Érvénytelen refresh token")

    if token_row.get("revoked") is True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="A refresh token vissza van vonva")

    expires_at_str = token_row.get("expires_at")
    if expires_at_str:
        expires_at = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
        if datetime.now(timezone.utc) > expires_at:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="A refresh token lejárt (szerver)")

    doc_ref.update(
        {
            "revoked": True,
            "revoked_at": datetime.now(timezone.utc).isoformat(),
        }
    )

    refresh_token, new_jti, refresh_exp = create_refresh_token({"sub": sub})
    db.collection("refresh-tokens").document(new_jti).set(
        {
            "jti": new_jti,
            "sub": sub,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": refresh_exp.isoformat(),
            "revoked": False,
        }
    )

    return {
        "access_token": create_access_token({"sub": sub}),
        "refresh_token": refresh_token,
    }

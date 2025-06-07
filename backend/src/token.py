import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import HTTPException, Request, status
from jose import JWTError, jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# ----------------------Token Generálás----------------------


def create_access_token(data: dict, expires_delta: timedelta = timedelta(days=365)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


# ----------------------Aktuális Bejelentkezett Felhasználó Lekérdezése----------------------


def get_current_user(request: Request):
    token = request.cookies.get("access_token")  # lekéri a kiküldött tokent

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Nincs bejelentkezve"
        )  # ha nincs akkor hibát küld

    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )  # decodolja a tokent és elmenti a payloadba
        username: str = payload.get("sub")  # a payloadból kiolvassuk a felhasználónevet

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Érvénytelen token"
            )  # Ha nincs felhasználónév akkor nem érvénes a token

        return {"name": username}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Érvénytelen vagy lejárt token",
        )

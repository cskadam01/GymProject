import os
import uuid
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import HTTPException, Request, status
from jose import JWTError, jwt


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

if not SECRET_KEY:
    raise RuntimeError("Hiányzik a SECRET_KEY környezeti változó.")

if len(SECRET_KEY) < 32:
    raise RuntimeError("A SECRET_KEY legyen legalább 32 karakter hosszú.")

if ALGORITHM not in {"HS256", "HS384", "HS512"}:
    raise RuntimeError("Nem támogatott JWT algoritmus. Használj HS256/HS384/HS512 értéket.")

#----------------------Token Generálás----------------------

ACCESS_EXPIRES = timedelta(minutes=45)

def create_access_token(data: dict, expires_delta: timedelta = ACCESS_EXPIRES):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({
        "exp": expire,
        "type": "access",
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


#----------------------Aktuális Bejelentkezett Felhasználó Lekérdezése----------------------

def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nincs bejelentkezve"
        )              
    token = auth_header.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")

        if username is None or token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Érvénytelen token"
            )

        return {"name": username}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Érvénytelen vagy lejárt token"
        )
    

REFRESH_EXPIRES = timedelta(days=14)

def create_refresh_token(data: dict, expires_delta: timedelta = REFRESH_EXPIRES):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    jti = str(uuid.uuid4())

    to_encode.update({
        "exp": expire,
        "jti": jti,
        "type": "refresh",
    })

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token, jti, expire

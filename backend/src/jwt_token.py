from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from fastapi import Request, HTTPException, status, Response
from jose import jwt, JWTError
import os
from fastapi.responses import Response



load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

#----------------------Token Generálás----------------------

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=3)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


#----------------------Aktuális Bejelentkezett Felhasználó Lekérdezése----------------------

def get_current_user(request: Request, response: Response):
    auth_header = request.headers.get("Authorization")  #lekéri a kiküldött tokent, amikor ai hívás történik a frontend elküldi a sutit és onnan olvassa ki
    print("Authorization header:", auth_header)


    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nincs bejelentkezve"
        )              
    token = auth_header.split(" ")[1]                          #ha nincs akkor hibát küld

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #decodolja a tokent és elmenti a payloadba
        print("Token payload:", payload)  
        username: str = payload.get("sub")  #a payloadból kiolvassuk a felhasználónevet
        token_time = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)  #lekérjük hogy mennyi idő mire lejár, és átalakítjuk olvasható időre
        now = datetime.now(timezone.utc)  #meghatározzuk a jelenlegi időt

        expire_time = token_time-now  #megkapjuk a hogy hány óra van hátra az életéből, hogy a lejárati dátumot kivonjuk a mostani dátumból


        print("token time: ", token_time)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Érvénytelen token"
            ) #Ha nincs felhasználónév akkor nem érvénes a token


       

       

        return {"name": username}

    except JWTError:
        print("Token decode error:", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Érvénytelen vagy lejárt token"
        )
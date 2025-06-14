from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os
from src.token import create_access_token, get_current_user
from src.firebase import db
from fastapi.responses import Response


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



class LoginUser(BaseModel):
    name: str
    password: str
class RegisterUser(LoginUser):
    email: str
    age: int


    


@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):

    users = db.collection("users").where("name", "==", current_user["name"]).get()

    user = users[0].to_dict()


    addedExer  = addedExer = len(user.get("saved_exercises", []))


    print(current_user)





    return {"message": "Sikeres azonosítás",
            "user": user["name"],
            "age": user["age"],
            "email" : user["email"],
            "exers": addedExer
            }


@router.post("/login")
def login(user: LoginUser, response: Response):
    db_user = db.collection("users").where("name", "==", user.name).get()

    

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Helytelen felhasználónév")
    
    user_data = db_user[0].to_dict()

    print("HASH érték Firestore-ből:", user_data["password"])
    print("Típus:", type(user_data["password"]))
    
    if not bcrypt.checkpw   (user.password.encode("utf-8"),
    user_data["password"].encode("utf-8")):
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Helytelen jelszó")
    
    token = create_access_token({"sub" : user_data["name"]})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600  # opcionális: 1 óra
    )

    print("Firestore-ből kapott hash:", user_data["password"])

    
    return {"message" : "Sikeres bejelentkezés",
            "name" : user_data["name"],
            "email" : user_data["email"] }

    
    

@router.post("/register")
def register(user: RegisterUser):

    user_conflict = db.collection("users").where("name", "==", user.name).get()

    if user_conflict:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Foglalt felhasználónév")
    
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

    data = {
        "name" : user.name,
        "age" : user.age,
        "password": hashed_password,
        "email" : user.email,
        "saved_exercises": []
        
    }

    db.collection("users").add(data)

    return {"success" : f"{user.name} sikeresen regisztrálva"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Sikeres kijelentkezés"}






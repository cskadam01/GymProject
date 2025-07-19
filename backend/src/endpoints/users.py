from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os
from src.jwt_token import create_access_token, get_current_user
from src.firebase import db
from fastapi.responses import Response


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


#------------------- ITT TALÁLHATÓAK AZ AUTENTIKÁCÓ ÉS FELHASZNÁLÓKKAL KAPCSOLATOS ENDPOINTOK -------------------------



class LoginUser(BaseModel):
    name: str
    password: str
class RegisterUser(LoginUser):
    email: str
    age: int


@router.get("/test-protected")
def test_protected_route(current_user: dict = Depends(get_current_user)): #A token. pyból lefuttatjuk a current_user metódust,
    return {"message": f"Be vagy jelentkezve, {current_user['name']}!"}   # a depends azt csuinálja hogy mielött lefutna az api elötte fusson le a current_user
                                                                          # majd a current_user vissza adja dict-ként a nevet
    




@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):

    # a users collectionból lekérjük azt a dokumentumot ahol a name key megegyezik a current user-el
    user_doc = db.collection("users").document(current_user["name"]).get()
    user = user_doc.to_dict()
    # Ha nincs a felhasznűlónak ilyen listája akkor egy öres lista hoszzát kéri le a hibát elkerülve
    # (ez a hiba már nem fordulhat elő, mert alapból üres listával regisztrálnak a tagok, de benne hagyom)
    addedExer  = len(user.get("saved_exercises", []))

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
    
    user_data = db_user[0].to_dict() # Az első eredményt vissza kapjuk és a json filet átalakítjuk python .todict() metódussal hogy tudj
    
    if not bcrypt.checkpw   (user.password.encode("utf-8"), user_data["password"].encode("utf-8")): #aa beírt jelszót titkosítja majd össze hasonlítja a firestoreból kapott haselt jelszóval és ha nem egyezik meg hibát dob
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Helytelen jelszó")
    
    token = create_access_token({"sub" : user_data["name"]}) #itt meghívjuk a token.pyból a create_acess_tokent és beadjuk paraméternek a felhasználó nevét akinek "kiállítjuk"

    return {"message" : "Sikeres bejelentkezés",
            "access_token" : token,
            "name" : user_data["name"],
            "email" : user_data["email"] }

    
    

@router.post("/register")
def register(user: RegisterUser):
    # Megnézzük, van-e már ilyen név (azonos nevű dokumentum = konfliktus)
    user_ref = db.collection("users").document(user.name)
    if user_ref.get().exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Foglalt felhasználónév")

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

    data = {
        "name": user.name,
        "age": user.age,
        "password": hashed_password,
        "email": user.email,
        "saved_exercises": []
    }

    # Dokumentum hozzáadása konkrét névvel
    user_ref.set(data)

    return {"success": f"{user.name} sikeresen regisztrálva"}

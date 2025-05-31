from fastapi import APIRouter, HTTPException, status
from src.models import User, get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os
from src.token import create_access_token

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


    

@router.get("/debug-users")
def debug_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [user.name for user in users]



@router.post("/login")
def user_login(user: LoginUser, db: Session = Depends(get_db)):
    db_user =  db.query(User).filter_by(name = user.name).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Helytelen felhasználónév")
    
    if not bcrypt.checkpw   (user.password.encode("utf-8"),
                             db_user.password.encode("utf-8")):
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Helytelen jelszó")
    
    token = create_access_token({"sub" : db_user.name})
    return {"access_token": token,
            "token_type" : "bearer",
            "name" : db_user.name,
            "email" : db_user.email }

@router.post("/create-user")
def create_user(user : RegisterUser, db:Session = Depends(get_db)):

    


    user_check = db.query(User).filter_by(name = user.name).first()

    if user_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ez a felhasználónév már foglalt")
    
     

    hashed_pass = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode('utf-8')

    new_user = User(name = user.name, password = hashed_pass, age = user.age, email = user.email )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created", "user_id": new_user.id}
    





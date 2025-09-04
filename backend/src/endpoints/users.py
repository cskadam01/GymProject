from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
import bcrypt
from datetime import datetime
import os
from src.jwt_token import create_access_token, get_current_user
from src.firebase import db
from fastapi.responses import Response
from email.message import EmailMessage
import secrets
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import List
from dotenv import load_dotenv

load_dotenv()


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
    USE_CREDENTIALS=os.getenv("USE_CREDENTIALS") == "True"
)

#------------------- ITT TALÁLHATÓAK AZ AUTENTIKÁCÓ ÉS FELHASZNÁLÓKKAL KAPCSOLATOS ENDPOINTOK -------------------------

# class EmailSchema(BaseModel):
#    email: List[EmailStr]

class LoginUser(BaseModel):
    name: str
    password: str
class RegisterUser(LoginUser):
    email: str
    age: int

class ForgottenPassword(BaseModel):
    user_name: str

class ChangePassword(BaseModel):
    old_password: str
    new_password: str

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
def login(user: LoginUser, response: Response, request : Request):
    db_user = db.collection("users").where("name", "==", user.name).get()

    

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Helytelen felhasználónév")
    
    user_data = db_user[0].to_dict() # Az első eredményt vissza kapjuk és a json filet átalakítjuk python .todict() metódussal hogy tudj
    



    client_ip = request.client.host #Kliens ip lekérdezése
    now = datetime.utcnow().isoformat() #pontos idő lekérése
    doc_id = f"{now} {user_data['name']}" #dokumetnum id generálás idő és név alapján



    if not bcrypt.checkpw   (user.password.encode("utf-8"), user_data["password"].encode("utf-8")): #aa beírt jelszót titkosítja majd össze hasonlítja a firestoreból kapott haselt jelszóval és ha nem egyezik meg hibát dob
        error_data = {
            
                "name" : user_data["name"],
                "time" : now,
                "ip" : client_ip,
                "status" : "failed",
                "reason" : "wrong_pass"
            

        }
        db.collection("login-logs").document(doc_id).set(error_data)
        
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Helytelen jelszó")
    token = create_access_token({"sub" : user_data["name"]}) #itt meghívjuk a token.pyból a create_acess_tokent és beadjuk paraméternek a felhasználó nevét akinek "kiállítjuk"

    data = {
        "name" : user_data["name"],
        "time" : now,
        "ip" : client_ip,
        "status" : "success"
    }


    db.collection("login-logs").document(doc_id).set(data) #betesszük a "login-logs" collectionbe az elöbb megadott dokumentumot
    
    print(f"{user_data['name']} bejelentkezett")

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


@router.post("/forgotten-passoword")
async def forgotten_password(user: ForgottenPassword, ):

    #kikeressük a felhasználót név alapján
    user_ref = db.collection("users").where("name", "==", user.user_name).get()
    if not user_ref:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nincs ilyen e-mail című felhasználó")
    
    user_data = user_ref[0].to_dict()

    #generálunk egy új jelszót
    password_length = 13
    new_pass = secrets.token_urlsafe(password_length)

    #leváltjuk az új jelszóra a régit
    hashed_password = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt()).decode()
    db.collection("users").document(user_data["name"]).update({"password": hashed_password})


    #Email megyrása
    template = f"""
    <html>
        <body>
            <h1>Kedves {user_data['name']}!</h1>
            <h3>Úgy tűnik, hogy a FluxNote-on új jelszót kértél!</h3>

            <p>Elküldük az új jelszavad, amit kérünk, hogy bejelentkezés után változtass meg a profilodon!</p>
            <h2>Új jelszavad:</h2>
            <p>{new_pass}</p>
    
            <p>Ha nem te kérted az új jelszót, akkor ezt az e-mailt figyelmen kívül hagyhatod.</p>
        </body>
    </html>

 """
    
    #email küldése
    message = MessageSchema(
       subject="Fastapi-Mail module",
       recipients= [user_data['email']], # List of recipients, as many as you can pass
       body=template,
       subtype="html"
       )


    fm = FastMail(conf)
    await fm.send_message(message)
    return {"success": "Email elküldve"}


@router.post("/change-password")
def change_password(passes : ChangePassword, current_user: dict = Depends(get_current_user)):
    db_user = db.collection("users").where("name", "==", current_user['name']).get()
    use_ref = db_user[0].to_dict()


    if not bcrypt.checkpw   (passes.old_password.encode("utf-8"), use_ref["password"].encode("utf-8")): #aa beírt jelszót titkosítja majd össze hasonlítja a firestoreból kapott haselt jelszóval
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Helytelen jelszó")
    
    hashed_password = bcrypt.hashpw(passes.new_password.encode(), bcrypt.gensalt()).decode()
    
    db.collection("users").document(current_user["name"]).update({"password" : hashed_password})
    



    
    



    
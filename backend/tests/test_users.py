
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app) #Szimulál egy böngészőt/frontendet, de gyors, nem indít valós szervert

def test_login_then_me():
    test_user ={                     # csinálunk egy dict-et amiben úgy teszünk mint ha a login oldalon adta volna meg a felhasznéló az adatokat
        "name" : "Admin",
        "password" : "Admin"
    }

    login_res = client.post("/users/login", json= test_user) # itt elküldjök a post metódusnak probsa az útvonalat és az elöbb létre hozott dictet
    print("Válaszkód:", login_res.status_code) # Lekérdezzük a választ

    token_cookie = login_res.cookies.get("access_token") # A szerver által visszaküldött sütiből lekérdezzük az access_token-t
    
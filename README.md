# Kondi Haladás Napló || Fluxe Note

### Az app célja:
Egy olyan webapp létrehozása amivel könnyedén lehet követni, hogy milyen teljesítményt értünk el konditermi súlyzós edzéseinken.

### Használt technológiák:

Frontend - React
Backend - FastAPI
Adatbázis - FireStore
Védelem | Validáció - JWT



Főbb funkciók

## ✨ Funkciók

- 🔐 Regisztráció / Bejelentkezés JWT-vel
- 📓 Feladatok naplózása
- 🧱 Szettek felvitele naplón belül
- 📊 Grafikonos megjelenítés Chart.js segítségével






## 🐍 Python Backend Virtuális Környezet és Futtatás

```bash
# Lépj be a projekt mappájába
cd projektneved

# Hozd létre a virtuális környezetet
python -m venv venv

Aktiváld a környezetet
# Windows:
venv\Scripts\activateLinux / macOS:
source venv/bin/activate

# Telepítsd a szükséges csomagokat
pip install -r requirements.txt

# Futtatás:
uvicorn src.app:app --reload
```

## React Frontend

```
# Telepítés
npm install

# Futtatás
npm run dev
```


## 👨🏻‍💻 🌨️Új dolgok amiket ezen a projecten keresztűl tanultam

### ⚡️ Fast API
Eddig ez a második összetettebb webapp projectem, előzőhöz flasket használtam, ennek a keretrendszernek viszont sokkal több funkcióját ki tudtam használ
Például:
Beépített swagger ui dokumentáció.
Basemodellek használata így bisztonságosabb kommunikáció frontend-el


### 🔥 Firestore
Eddig nem használtam NoSQL alapú adatbázisokat, hamar belejöttem és sokkal jobban élveztem mint az SQL alapúakat a nagyobb szabadság miatt

### ⚛️ React
Reactot már régebben is használtam, nem is egyszer, viszont ennek a projectnek köszönhetően megint tanultam új dolgokat 
Például:
Proppok Átadása más komponenseknek
Listákkal való dolgozás megszilárdítása .map .filter
ChartJS használata
Mobilefirst desing







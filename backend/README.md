# Backend

Ez a könyvtár tartalmazza a FastAPI alapú szerver kódját.

## Telepítés

```bash
cd backend
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

A futtatáshoz hozz létre egy `.env` fájlt a következő változókkal:

- `FIREBASE_KEY_PATH` – Firebase szolgáltatói kulcs elérési útja
- `SECRET_KEY` – JWT tokenek titka
- `ALGORITHM` – a tokenek kódolásához használt algoritmus
- `DATABASE_URL` – (opcionális) SQLAlchemy adatbázis URL

## Indítás

```bash
uvicorn src.app:app --reload
```

A szerver alapértelmezett címe: `http://localhost:8000`.

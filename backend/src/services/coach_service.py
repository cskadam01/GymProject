import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from google.cloud import firestore

from src.firebase import db


def create_invite(username: str):
    code = secrets.token_urlsafe(18)
    expires = datetime.now(timezone.utc) + timedelta(hours=24)
    db.collection("coach_invites").document(hashlib.sha256(code.encode()).hexdigest()).set({
        "coach": username, "expires_at": expires, "used_by": None,
    })
    return {"code": code, "expires_at": expires.isoformat()}


def join_coach(code: str, username: str):
    ref = db.collection("coach_invites").document(hashlib.sha256(code.encode()).hexdigest())
    transaction = db.transaction()

    @firestore.transactional
    def claim(transaction):
        doc = ref.get(transaction=transaction)
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Érvénytelen meghívókód")
        invite = doc.to_dict() or {}
        expires = invite.get("expires_at")
        if not isinstance(expires, datetime) or expires < datetime.now(timezone.utc) or invite.get("used_by"):
            raise HTTPException(status_code=400, detail="A meghívókód lejárt vagy már felhasználták")
        coach = invite.get("coach")
        if not coach or coach == username:
            raise HTTPException(status_code=400, detail="Ezzel a kóddal nem kapcsolódhatsz")
        coach_doc = db.collection("users").document(coach).get(transaction=transaction)
        client_ref = db.collection("users").document(username)
        client_doc = client_ref.get(transaction=transaction)
        if not coach_doc.exists or not client_doc.exists:
            raise HTTPException(status_code=404, detail="Felhasználó nem található")
        transaction.update(client_ref, {"coach_id": coach})
        transaction.update(ref, {"used_by": username})
        return {"coach": coach}

    return claim(transaction)


def list_clients(username: str):
    local_zone = ZoneInfo("Europe/Budapest")
    today = datetime.now(local_zone).date()
    first_monday = today - timedelta(days=today.weekday(), weeks=25)
    clients = []
    for doc in db.collection("users").where("coach_id", "==", username).limit(50).stream():
        user = doc.to_dict() or {}
        counts: dict[str, int] = {}
        recent = []
        for entry_doc in db.collection("diary_entries").where("user", "==", doc.id).stream():
            entry = entry_doc.to_dict() or {}
            date = entry.get("date")
            if not isinstance(date, datetime):
                continue
            day = date.astimezone(local_zone).date().isoformat()
            if day < first_monday.isoformat() or day > today.isoformat():
                continue
            counts[day] = counts.get(day, 0) + 1
            recent.append({"name": entry.get("exer_name", ""), "weight": entry.get("weight", 0), "reps": entry.get("rep", 0), "date": date.isoformat()})
        recent.sort(key=lambda item: item["date"], reverse=True)
        week_start = today - timedelta(days=today.weekday())
        clients.append({
            "username": doc.id,
            "name": user.get("name", doc.id),
            "last_workout": recent[0]["date"] if recent else None,
            "week_days": sum(day >= week_start.isoformat() for day in counts),
            "active_days": len(counts),
            "activity": counts,
            "recent": recent[:5],
        })
    clients.sort(key=lambda item: item["name"].lower())
    return clients

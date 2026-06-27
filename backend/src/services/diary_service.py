from datetime import datetime, timezone

from fastapi import HTTPException
from google.cloud import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

from src.firebase import db
from src.schemas.diary import ExerId, NewSave


REP_RANGES = [
    {"key": "1", "label": "1 ismétlés", "min": 1, "max": 1},
    {"key": "2-3", "label": "2-3 ismétlés", "min": 2, "max": 3},
    {"key": "4-5", "label": "4-5 ismétlés", "min": 4, "max": 5},
    {"key": "6-7", "label": "6-7 ismétlés", "min": 6, "max": 7},
    {"key": "8-9", "label": "8-9 ismétlés", "min": 8, "max": 9},
    {"key": "10-11", "label": "10-11 ismétlés", "min": 10, "max": 11},
    {"key": "12-13", "label": "12-13 ismétlés", "min": 12, "max": 13},
    {"key": "14", "label": "14 ismétlés", "min": 14, "max": 14},
]


def _get_user(username: str):
    user_doc = db.collection("users").document(username).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")
    return user_doc


def _get_exercise(exercise_id: str):
    exercise_doc = db.collection("exercise").document(exercise_id).get()
    if not exercise_doc.exists:
        raise HTTPException(status_code=404, detail="Feladat nem található")
    return exercise_doc


def _require_saved_exercise(username: str, exercise_id: str):
    user_doc = _get_user(username)
    user = user_doc.to_dict()
    saved_ids = user.get("saved_exercises", [])
    if exercise_id not in saved_ids:
        raise HTTPException(status_code=403, detail="Nincs jogosultságod ehhez a feladathoz")
    return user_doc


def _get_diary_entry_counts(username: str, exercise_ids: list[str]):
    counts = {}

    for exercise_id in exercise_ids:
        entries = (
            db.collection("diary_entries")
            .where("task_id", "==", exercise_id)
            .where("user", "==", username)
            .stream()
        )
        counts[exercise_id] = sum(1 for _ in entries)

    return counts


def get_saved_exercises(username: str, limit: int = 20, cursor: int | None = None):
    offset = cursor or 0
    page_size = min(max(limit, 1), 50)
    user_doc = _get_user(username)
    user = user_doc.to_dict()
    saved_ids = user.get("saved_exercises", [])
    page_ids = saved_ids[offset : offset + page_size]

    if not page_ids:
        return {
            "items": [],
            "next_cursor": None,
            "has_more": False,
        }

    doc_refs = [db.collection("exercise").document(doc_id) for doc_id in page_ids]
    docs = db.get_all(doc_refs)
    diary_entry_counts = _get_diary_entry_counts(username, page_ids)

    saves = []
    for doc in docs:
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            data["diary_entry_count"] = diary_entry_counts.get(doc.id, 0)
            saves.append(data)

    next_offset = offset + len(page_ids)
    has_more = next_offset < len(saved_ids)

    return {
        "items": saves,
        "next_cursor": next_offset if has_more else None,
        "has_more": has_more,
    }


def save_exercise_to_diary(exercise: ExerId, username: str):
    _get_exercise(exercise.exerciseID)
    user_doc = _get_user(username)
    user_ref = user_doc.reference

    user_ref.update({"saved_exercises": firestore.ArrayUnion([exercise.exerciseID])})
    return {"success": "Feladat hozzá adva a naplóhoz"}


def add_diary_record(task: NewSave, username: str):
    _require_saved_exercise(username, task.exer_id)
    exercise_doc = _get_exercise(task.exer_id)
    exercise = exercise_doc.to_dict()

    data = {
        "user": username,
        "task_id": task.exer_id,
        "exer_name": exercise.get("exer_name", task.exerName),
        "rep": task.reps,
        "weight": task.weight,
        "date": SERVER_TIMESTAMP,
    }

    db.collection("diary_entries").add(data)
    return {"message": "Sikeres naplózás"}


def _to_number(value, fallback: float = 0):
    if isinstance(value, (int, float)):
        return value

    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return fallback

    return fallback


def _entry_date(entry: dict):
    value = entry.get("date")

    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)

    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None

        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)

        return parsed.astimezone(timezone.utc)

    return None


def _entry_sort_key(entry: dict):
    date = _entry_date(entry) or datetime.min.replace(tzinfo=timezone.utc)
    return date, str(entry.get("id", ""))


def _entry_month_key(entry: dict):
    date = _entry_date(entry)

    if not date:
        return f"entry-{entry.get('id', '')}"

    return f"{date.year}-{date.month:02d}"


def _entry_month_label(entry: dict):
    date = _entry_date(entry)

    if not date:
        return str(entry.get("date") or entry.get("id") or "Ismeretlen")

    return f"{date.year}-{date.month:02d}"


def _entry_month_sort_value(entry: dict):
    date = _entry_date(entry)

    if not date:
        return _entry_sort_key(entry)[0]

    return datetime(date.year, date.month, 1, tzinfo=timezone.utc)


def _estimate_one_rep_max(entry: dict):
    weight = _to_number(entry.get("weight"))
    reps = _to_number(entry.get("rep"))
    return round(weight * (1 + reps / 30))


def _entry_strength_key(entry: dict):
    return (
        _estimate_one_rep_max(entry),
        _to_number(entry.get("weight")),
        _to_number(entry.get("rep")),
        _entry_sort_key(entry)[0],
    )


def _entry_range(entry: dict):
    reps = _to_number(entry.get("rep"))

    for rep_range in REP_RANGES:
        if rep_range["min"] <= reps <= rep_range["max"]:
            return rep_range

    return None


def _load_entries_by_exercise(exercise_id: str, username: str):
    saved_reps = (
        db.collection("diary_entries")
        .where("task_id", "==", exercise_id)
        .where("user", "==", username)
    )
    docs = list(saved_reps.stream())

    saves = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        saves.append(data)

    saves.sort(key=_entry_sort_key)
    return saves


def _build_personal_records(entries: list[dict]):
    best_by_reps = {}

    for entry in entries:
        reps = int(_to_number(entry.get("rep")))

        if reps <= 0:
            continue

        current_best = best_by_reps.get(reps)
        weight = _to_number(entry.get("weight"))
        is_better = not current_best or weight > _to_number(current_best.get("weight"))
        is_later_tie = (
            current_best
            and weight == _to_number(current_best.get("weight"))
            and _entry_sort_key(entry) > _entry_sort_key(current_best)
        )

        if is_better or is_later_tie:
            best_by_reps[reps] = entry

    rows = []
    for reps, entry in best_by_reps.items():
        rows.append(
            {
                "entry": entry,
                "estimated_one_rep_max": _estimate_one_rep_max(entry),
                "key": f"{reps}-{entry.get('id', '')}",
                "range": {
                    "key": str(reps),
                    "label": f"{reps} ismétlés",
                    "min": reps,
                    "max": reps,
                },
            }
        )

    return sorted(
        rows,
        key=lambda row: (
            row["range"]["min"],
            -_to_number(row["entry"].get("weight")),
        ),
    )


def _build_monthly_overview(entries: list[dict]):
    return [
        {
            "entry": entry,
            "estimated_one_rep_max": _estimate_one_rep_max(entry),
            "key": str(entry.get("id", "")),
            "period_label": str(entry.get("date") or entry.get("id") or "Naplózás"),
        }
        for entry in reversed(entries)
    ]


def _build_yearly_overview(entries: list[dict]):
    best_by_month = {}

    for entry in entries:
        month_key = _entry_month_key(entry)
        current_best = best_by_month.get(month_key)

        if (
            not current_best
            or _entry_strength_key(entry) > _entry_strength_key(current_best)
        ):
            best_by_month[month_key] = entry

    rows = [
        {
            "entry": entry,
            "estimated_one_rep_max": _estimate_one_rep_max(entry),
            "key": _entry_month_key(entry),
            "period_label": _entry_month_label(entry),
            "sort_value": _entry_month_sort_value(entry),
        }
        for entry in best_by_month.values()
    ]
    rows.sort(key=lambda row: row["sort_value"], reverse=True)

    for row in rows:
        row.pop("sort_value", None)

    return rows


def get_entries_by_exercise(exercise_id: str, username: str):
    saves = _load_entries_by_exercise(exercise_id, username)

    if not saves:
        raise HTTPException(status_code=404, detail="Nincs ilyen feladatod naplózva.")

    return saves


def get_progress_summary(exercise_id: str, username: str):
    _require_saved_exercise(username, exercise_id)
    entries = _load_entries_by_exercise(exercise_id, username)

    return {
        "entries": entries,
        "overview": {
            "monthly": _build_monthly_overview(entries),
            "yearly": _build_yearly_overview(entries),
        },
        "personal_records": _build_personal_records(entries),
        "rep_ranges": REP_RANGES,
    }


def is_exercise_authorized(exercise_id: str, username: str):
    user_doc = _get_user(username)
    user = user_doc.to_dict()
    saved_ids = user.get("saved_exercises", [])

    return {"authorized": exercise_id in saved_ids}


def delete_diary_entry(entry_id: str, username: str):
    doc_ref = db.collection("diary_entries").document(entry_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Naplóbejegyzés nem található")

    if doc.to_dict().get("user") != username:
        raise HTTPException(status_code=403, detail="Nincs jogosultságod ezt törölni")

    doc_ref.delete()
    return {"message": "Sikeresen törölve"}

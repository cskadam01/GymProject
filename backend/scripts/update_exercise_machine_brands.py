import argparse
import json
import pathlib
import sys
from typing import Any

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from src.firebase import db


MAX_BATCH_SIZE = 450
MAX_BRAND_LENGTH = 80
MACHINE_TYPE = "Gép"
KNOWN_BRANDS = [
    "Panatta",
    "Hoist",
    "Technogym",
    "Life Fitness",
    "Hammer Strength",
    "Nautilus",
    "Matrix",
]


def _load_mapping(path: str | None) -> dict[str, str]:
    if not path:
        return {}

    with open(path, encoding="utf-8") as mapping_file:
        mapping = json.load(mapping_file)

    if not isinstance(mapping, dict):
        raise ValueError("A mapping fájlnak JSON objektumnak kell lennie.")

    normalized_mapping = {}
    for key, value in mapping.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("A mapping kulcsai és értékei is szövegek legyenek.")

        brand = value.strip()
        if not brand:
            continue
        if len(brand) > MAX_BRAND_LENGTH:
            raise ValueError(f"Túl hosszú márkanév ehhez: {key}")

        normalized_mapping[key.strip()] = brand

    return normalized_mapping


def _infer_brand_from_name(exercise_name: str) -> str | None:
    lower_name = exercise_name.lower()
    for brand in KNOWN_BRANDS:
        if brand.lower() in lower_name:
            return brand

    return None


def _resolve_brand(
    doc_id: str,
    exercise: dict[str, Any],
    mapping: dict[str, str],
    default_brand: str | None,
    infer_from_name: bool,
) -> str | None:
    exercise_name = str(exercise.get("exer_name", "")).strip()

    return (
        mapping.get(doc_id)
        or mapping.get(exercise_name)
        or (_infer_brand_from_name(exercise_name) if infer_from_name else None)
        or default_brand
    )


def _commit_batch(batch, pending_writes: int):
    if pending_writes:
        batch.commit()

    return db.batch(), 0


def update_machine_brands(
    mapping_file: str | None,
    default_brand: str | None,
    infer_from_name: bool,
    commit: bool,
):
    mapping = _load_mapping(mapping_file)
    if default_brand:
        default_brand = default_brand.strip()
        if len(default_brand) > MAX_BRAND_LENGTH:
            raise ValueError(
                "Az alapértelmezett márkanév legfeljebb 80 karakter lehet."
            )

    docs = db.collection("exercise").stream()
    batch = db.batch()
    pending_writes = 0
    changed_count = 0
    skipped_count = 0
    missing_brand_count = 0

    for doc in docs:
        exercise = doc.to_dict() or {}
        if exercise.get("type") != MACHINE_TYPE:
            continue

        current_brand = str(exercise.get("machine_brand", "")).strip()
        if current_brand:
            skipped_count += 1
            continue

        brand = _resolve_brand(
            doc.id, exercise, mapping, default_brand, infer_from_name
        )
        if not brand:
            missing_brand_count += 1
            print(
                "[HIÁNYZIK] "
                f"{doc.id} | {exercise.get('exer_name', 'Névtelen gyakorlat')}"
            )
            continue

        changed_count += 1
        print(
            f"[{'UPDATE' if commit else 'DRY-RUN'}] "
            f"{doc.id} | {exercise.get('exer_name')} -> {brand}"
        )

        if commit:
            batch.update(doc.reference, {"machine_brand": brand})
            pending_writes += 1

            if pending_writes >= MAX_BATCH_SIZE:
                batch, pending_writes = _commit_batch(batch, pending_writes)

    if commit:
        _commit_batch(batch, pending_writes)

    print("")
    print(f"Módosítandó gépes gyakorlat: {changed_count}")
    print(f"Már volt machine_brand mezője: {skipped_count}")
    print(f"Márka nélkül maradt: {missing_brand_count}")
    if not commit:
        print("Ez csak dry-run volt. Valódi íráshoz add hozzá: --commit")


def main():
    parser = argparse.ArgumentParser(
        description="Meglévő gépes gyakorlatok machine_brand mezőjének feltöltése."
    )
    parser.add_argument(
        "--mapping-file",
        help="JSON fájl, ahol a kulcs doc id vagy exer_name, az érték pedig a márkanév.",
    )
    parser.add_argument(
        "--default-brand",
        help="Ezt a márkát kapja minden olyan gépes gyakorlat, ami nincs a mappingben.",
    )
    parser.add_argument(
        "--infer-from-name",
        action="store_true",
        help="A gyakorlat nevében szereplő ismert márkaneveket automatikusan használja.",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Valóban írja is be a változásokat Firestore-ba.",
    )

    args = parser.parse_args()
    update_machine_brands(
        args.mapping_file,
        args.default_brand,
        args.infer_from_name,
        args.commit,
    )


if __name__ == "__main__":
    main()

import sys
import os





def migrate_users_by_name():
    users = db.collection("users").get()

    for doc in users:
        data = doc.to_dict()
        name = data.get("name")

        if name:
            print(f"Migrálás: {doc.id} → {name}")
            # Új dokumentum a név alapján
            db.collection("users").document(name).set(data)
            # Régi dokumentum törlése
            db.collection("users").document(doc.id).delete()
        else:
            print(f"Név hiányzik: {doc.id}")

if __name__ == "__main__":
    migrate_users_by_name()
    print("✅ Migráció kész")
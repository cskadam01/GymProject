import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from src.firebase import db
import pandas as pd




def delete_unused_entries ():
    users = db.collection("users").stream()
    entries = db.collection("diary_entries").stream()



    names = []
    for doc in users:
        data = doc.to_dict()
        if "name" in data:
            names.append(data["name"])


    deleted_entries = []

    for entry in entries:
        data = entry.to_dict()
        data["id"] = entry.id
        if data["user"] not in names:
            deleted_entries.append(f"{data['id']} {data['user']}\n")
            entry.reference.delete()

    print(deleted_entries)

if __name__ == "__main__":
    delete_unused_entries()


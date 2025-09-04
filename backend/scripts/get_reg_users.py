import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from src.firebase import db
import pandas as pd
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d")

def save_users_to_excel():
    users_data = db.collection("users")
    docs = users_data.stream()
    rows = []

    for doc in docs:
        
        data = doc.to_dict()
        data["id"] = doc.id
      

        rows.append({
            "id" : data["id"],
            "name": data.get("name", ""),
            "email": data.get("email", ""),

             


        })
    df = pd.DataFrame(rows)
    df.to_excel(f"{now}felhasznalok.xlsx", index=False)
    
       
if __name__ == "__main__" :
    save_users_to_excel()





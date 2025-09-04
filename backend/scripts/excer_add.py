import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from src.firebase import db
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
import tkinter as tk
from tkinter import messagebox

def submit():
    exer_name = exer_name_var.get()
    exer_desc = exer_desc_var.get()
    exer_muscle = exer_muscle_var.get()
    exer_type = exer_type_var.get()

    if not all([exer_name, exer_desc, exer_muscle, exer_type]):
        messagebox.showerror("Hiba", "Minden mezőt ki kell tölteni!")
        return

    data = {
        "exer_description": exer_desc,
        "exer_name": exer_name,
        "muscle": exer_muscle,
        "type": exer_type,
        "creation": SERVER_TIMESTAMP
    }

    try:
        db.collection("exercise").add(data)
        messagebox.showinfo("Siker", "Gyakorlat hozzáadva!")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Hiba", f"Hiba történt: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Új gyakorlat hozzáadása")

    exer_name_var = tk.StringVar()
    exer_desc_var = tk.StringVar()
    exer_muscle_var = tk.StringVar()
    exer_type_var = tk.StringVar()

    tk.Label(root, text="Név:").grid(row=0, column=0, sticky="e")
    tk.Entry(root, textvariable=exer_name_var).grid(row=0, column=1)

    tk.Label(root, text="Leírás:").grid(row=1, column=0, sticky="e")
    tk.Entry(root, textvariable=exer_desc_var).grid(row=1, column=1)

    tk.Label(root, text="Izomcsoport:").grid(row=2, column=0, sticky="e")
    tk.Entry(root, textvariable=exer_muscle_var).grid(row=2, column=1)

    tk.Label(root, text="Típus:").grid(row=3, column=0, sticky="e")
    tk.Entry(root, textvariable=exer_type_var).grid(row=3, column=1)

    tk.Button(root, text="Mentés", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()


from src.firebase import db
from datetime import datetime, timezone, timedelta,date
from fastapi import Depends
from src.jwt_token import get_current_user





def get_streak(current_user : dict = Depends(get_current_user)):

    weekday = datetime.now().weekday()
    current_time = datetime.now()
    current_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        

    week_start = current_time - timedelta(days=weekday) 
    week_end = week_start + timedelta(days=7)


    data = []
    try:
        query = db.collection("diary_entries").where("user", "==", current_user["name"]).where("date", ">=", week_start).where("date", "<", week_end ).get()
        
        for doc in query:

            data.append(doc.to_dict())

    except Exception as e:
        print("get_streak ERROR:", e)
        raise
        
    streak_days = set()
    
    for entries  in data :
        dates = entries["date"].date()
        streak_days.add(dates)

    return len(streak_days)


def get_total_workouts(current_user : dict = Depends(get_current_user)):
    query = db.collection("diary_entries").where("user", "==", current_user["name"]).get()

    data = []

    for doc in query:
            data.append(doc.to_dict())
    
    days = set()
    for entries  in data :
        dates = entries["date"].date()
        days.add(dates)

    return(len(days))

def get_weekly_prs(current_user : dict = Depends(get_current_user)):
    weekday = datetime.now().weekday()
    current_time = datetime.now()
    current_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        

    week_start = current_time - timedelta(days=weekday) 
    week_end = week_start + timedelta(days=7)



    query = db.collection("diary_entries").where("user", "==", current_user["name"]).where("date", ">=", week_start).where("date", "<", week_end ).get()

    data = []
    for doc in query:
            data.append(doc.to_dict())

    count = 0

    for entry in data:
        if entry["rep"] == 1:
             count += count
    return(count)



from google.cloud import firestore
import sys
import pathlib

# Make sure the backend folder is on the import path so `src.*` works when running this file directly
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from src.firebase import db


def set_weekly_goal(user_id: str, goal):
    user_ref = db.collection("users").document(user_id)
    user_ref.update({"weeklyGoal": goal})


if __name__ == "__main__":
    # Optional quick manual run:
    # python backend/scripts/update_user.py <USER_ID> <GOAL_NUMBER>
    if len(sys.argv) == 3:
        uid = sys.argv[1]
        goal_value = int(sys.argv[2])
        set_weekly_goal(uid, goal_value)
        print("updated", uid, "weeklyGoal =", goal_value)
    else:
        print("usage: python backend/scripts/update_user.py <USER_ID> <GOAL_NUMBER>")
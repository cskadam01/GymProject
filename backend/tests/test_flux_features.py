import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.schemas.diary import NewWorkout
from src.services import diary_service
from src.services import coach_service, user_service
from fastapi import HTTPException


class WorkoutFeatureTests(unittest.TestCase):
    @patch.object(diary_service, "db")
    @patch.object(diary_service, "_get_exercise")
    @patch.object(diary_service, "_require_saved_exercise")
    def test_workout_saves_all_sets_in_one_batch(self, require_saved, get_exercise, db):
        get_exercise.return_value.to_dict.return_value = {"exer_name": "Fekvenyomás"}
        refs = [MagicMock(), MagicMock()]
        db.collection.return_value.document.side_effect = refs
        payload = NewWorkout(exercise_id="exercise-1", sets=[{"weight": 60, "reps": 10}, {"weight": 62.5, "reps": 8}], note="Jól ment")

        result = diary_service.add_workout(payload, "adam")

        require_saved.assert_called_once_with("adam", "exercise-1")
        self.assertEqual(result["sets_saved"], 2)
        self.assertEqual(db.batch.return_value.set.call_count, 2)
        first = db.batch.return_value.set.call_args_list[0].args[1]
        second = db.batch.return_value.set.call_args_list[1].args[1]
        self.assertEqual(first["workout_id"], second["workout_id"])
        self.assertEqual([first["set_index"], second["set_index"]], [0, 1])
        self.assertEqual([first["weight"], second["weight"]], [60, 62.5])
        db.batch.return_value.commit.assert_called_once()

    @patch.object(diary_service, "db")
    def test_activity_counts_sets_per_day_and_returns_recent(self, db):
        now = datetime.now(ZoneInfo("Europe/Budapest"))
        yesterday = now - timedelta(days=1)
        docs = []
        for index, date in enumerate([now, now, yesterday]):
            doc = MagicMock()
            doc.id = f"entry-{index}"
            doc.to_dict.return_value = {"date": date, "task_id": "exercise-1", "exer_name": "Fekvenyomás", "weight": 60, "rep": 10}
            docs.append(doc)
        db.collection.return_value.where.return_value.stream.return_value = docs

        result = diary_service.get_activity("adam", 7)

        self.assertEqual(result["active_days"], 2)
        self.assertEqual(sum(day["sets"] for day in result["days"]), 3)
        today = now.date().isoformat()
        self.assertEqual(next(day["sets"] for day in result["days"] if day["date"] == today), 2)
        self.assertEqual(len(result["recent"]), 3)


class AccessTests(unittest.TestCase):
    @patch.object(coach_service, "db")
    def test_coach_list_only_queries_linked_clients(self, db):
        users = MagicMock()
        users.where.return_value.limit.return_value.stream.return_value = []
        db.collection.return_value = users

        self.assertEqual(coach_service.list_clients("trainer"), [])
        users.where.assert_called_once_with("coach_id", "==", "trainer")

    @patch.object(user_service, "db")
    @patch.object(user_service.jwt, "decode")
    def test_logout_rejects_another_users_refresh_token(self, decode, db):
        decode.return_value = {"type": "refresh", "sub": "someone-else", "jti": "token-1"}
        with self.assertRaises(HTTPException) as error:
            user_service.logout_user("refresh-token", "adam")
        self.assertEqual(error.exception.status_code, 401)
        db.collection.assert_not_called()


if __name__ == "__main__":
    unittest.main()

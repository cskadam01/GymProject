import json

from src.services.exercise_service import (
    DEFAULT_EXERCISE_CREATOR_ID,
    backfill_exercise_creator_ids,
)


if __name__ == "__main__":
    result = backfill_exercise_creator_ids(DEFAULT_EXERCISE_CREATOR_ID)
    print(json.dumps(result, ensure_ascii=False, indent=2))

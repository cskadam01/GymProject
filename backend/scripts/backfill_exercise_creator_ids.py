import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.services.exercise_service import (  # noqa: E402
    DEFAULT_EXERCISE_CREATOR_ID,
    backfill_exercise_creator_ids,
)


if __name__ == "__main__":
    result = backfill_exercise_creator_ids(DEFAULT_EXERCISE_CREATOR_ID)
    print(json.dumps(result, ensure_ascii=False, indent=2))

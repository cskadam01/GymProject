from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints, field_validator


FirestoreId = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)]
WorkoutPlanName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]


class WorkoutPlanBase(BaseModel):
    name: WorkoutPlanName
    exercise_ids: list[FirestoreId] = Field(min_length=1, max_length=80)

    @field_validator("exercise_ids")
    @classmethod
    def exercise_ids_must_be_unique(cls, exercise_ids: list[str]):
        unique_ids = list(dict.fromkeys(exercise_ids))
        if len(unique_ids) != len(exercise_ids):
            raise ValueError("Egy feladat csak egyszer szerepelhet az edzéstervben.")

        return exercise_ids


class CreateWorkoutPlan(WorkoutPlanBase):
    pass


class UpdateWorkoutPlan(WorkoutPlanBase):
    pass

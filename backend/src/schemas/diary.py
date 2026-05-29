from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


FirestoreId = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)]
ExerciseName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]


class NewSave(BaseModel):
    exer_id: FirestoreId
    exerName: ExerciseName
    weight: float = Field(ge=0, le=1000)
    reps: int = Field(ge=1, le=1000)


class ExerId(BaseModel):
    exerciseID: FirestoreId

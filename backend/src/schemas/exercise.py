from typing import Annotated

from pydantic import BaseModel, StringConstraints


FirestoreId = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)]
ShortText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]
Description = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=500)]


class AddExercise(BaseModel):
    name: ShortText
    description: Description
    muscle: ShortText
    e_type: ShortText


class ExerId(BaseModel):
    exerciseID: FirestoreId

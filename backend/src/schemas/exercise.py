from typing import Annotated, Literal

from pydantic import BaseModel, StringConstraints, model_validator


FirestoreId = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)]
ShortText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]
Description = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=500)]
MachineBrand = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]
MuscleGroup = Literal["Mell", "Váll", "Bicepsz", "Tricepsz", "Láb", "Hát"]
ExerciseType = Literal["Gép", "Szabadsúlyt"]


class AddExercise(BaseModel):
    name: ShortText
    description: Description
    muscle: MuscleGroup
    e_type: ExerciseType
    machine_brand: MachineBrand | None = None

    @model_validator(mode="after")
    def machine_brand_is_required_for_machine(self):
        if self.e_type == "Gép" and not self.machine_brand:
            raise ValueError(
                "Gépes feladatnál kötelező megadni a gép márkáját. "
                "Ha nem tudod, használd az Ismeretlen értéket."
            )

        return self


class ExerId(BaseModel):
    exerciseID: FirestoreId
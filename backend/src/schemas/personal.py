from typing import Optional

from pydantic import BaseModel, Field


class PersonalMeasurements(BaseModel):
    body_weight: Optional[float] = Field(default=None, ge=0, le=500)  # kg
    height: Optional[float] = Field(default=None, ge=30, le=300)  # cm
    body_fat: Optional[float] = Field(default=None, ge=0, le=100)  # %
    biceps: Optional[float] = Field(default=None, ge=0, le=200)  # cm
    hips: Optional[float] = Field(default=None, ge=0, le=300)  # cm
    waist: Optional[float] = Field(default=None, ge=0, le=300)  # cm
    upper_arm: Optional[float] = Field(default=None, ge=0, le=200)  # cm
    forearm: Optional[float] = Field(default=None, ge=0, le=200)  # cm
    shoulders: Optional[float] = Field(default=None, ge=0, le=300)  # cm
    chest: Optional[float] = Field(default=None, ge=0, le=300)  # cm
    abs: Optional[float] = Field(default=None, ge=0, le=300)  # cm
    thigh: Optional[float] = Field(default=None, ge=0, le=200)  # cm
    calf: Optional[float] = Field(default=None, ge=0, le=200)  # cm
    neck: Optional[float] = Field(default=None, ge=0, le=100)  # cm
    wrist: Optional[float] = Field(default=None, ge=0, le=100)  # cm

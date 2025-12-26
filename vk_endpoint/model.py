from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
import datetime


class Dkhype(BaseModel):
    et_et: Optional[float] = Field(alias="1.1")
    fem: Optional[float] = Field(alias="5")
    tyve: Optional[float] = Field(alias="20")
    halvtres: Optional[float] = Field(alias="50")

    @field_validator("*", mode="before")
    def empty_strings_to_none(cls, v):
        return None if v == "" else v


class Vandstand(BaseModel):
    varsel: Optional[float]
    et_et: Optional[float] = Field(alias="1.1")
    to: Optional[float] = Field(alias="2")
    fem: Optional[float] = Field(alias="5")
    ti: Optional[float] = Field(alias="10")

    @field_validator("*", mode="before")
    def empty_strings_to_none(cls, v):
        return None if v == "" else v


class Kriterie(BaseModel):
    id: Optional[int] = None
    dkhype: Optional[Dkhype] = None
    vandstand: Optional[Vandstand] = None
    station_id: str = Field(min_length=8, max_length=8)

    @model_validator(mode="before")
    def enforce_station_id_length(cls, values):
        sid = values.get("station_id")
        if sid is None or len(sid) != 8:
            raise ValueError("Invalid station_id length, skipping this record")
        return values


class UploadRequest(BaseModel):
    note: Optional[str]
    sommer: bool
    kriterier: list[Kriterie]


class Upload_get(BaseModel):
    id: int
    Datetime: datetime.date
    note: str | None = None
    sommer: bool

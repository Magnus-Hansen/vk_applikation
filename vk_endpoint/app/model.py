"""Model klasser for backend."""

import datetime

from pydantic import BaseModel, Field, field_validator, model_validator


class Dkhype(BaseModel):
    """Model klasse for nested Dkhype."""

    et_et: float | None = Field(alias="1.1")
    fem: float | None = Field(alias="5")
    tyve: float | None = Field(alias="20")
    halvtres: float | None = Field(alias="50")

    @field_validator("*", mode="before")
    def empty_strings_to_none(cls, v: any) -> any:  # noqa: N805
        """Convert tomme strenge til None før validering."""
        return None if v == "" else v


class Vandstand(BaseModel):
    """Model klasse for nested vandstand."""

    varsel: float | None
    et_et: float | None = Field(alias="1.1")
    to: float | None = Field(alias="2")
    fem: float | None = Field(alias="5")
    ti: float | None = Field(alias="10")

    @field_validator("*", mode="before")
    def empty_strings_to_none(cls, v: any) -> any:  # noqa: N805
        """Convert tomme strenge til None før validering."""
        return None if v == "" else v


id_length = 8


class Kriterie(BaseModel):
    """Model klasse for varslingskriterie."""

    id: int | None = None
    dkhype: Dkhype | None = None
    vandstand: Vandstand | None = None
    station_id: str = Field(min_length=id_length, max_length=id_length)

    @model_validator(mode="before")
    def enforce_station_id_length(cls, values: any) -> dict[str, any]:  # noqa: N805
        """Sikrer at station_id har korrekt længde før model valideres."""
        sid = values.get("station_id")
        if sid is None or len(sid) != id_length:
            msg = "Invalid station_id length, skipping this record"
            raise ValueError(msg)
        return values


class UploadRequest(BaseModel):
    """Model klasse til genereing af ny upload."""

    note: str | None
    sommer: bool
    kriterier: list[Kriterie]


class Upload(BaseModel):
    """Model klasse for uploads."""

    id: int
    Datetime: datetime.date
    note: str | None = None
    sommer: bool

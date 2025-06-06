from datetime import timedelta
from typing import Any
from pydantic import BaseModel
import cuddly_dicts


class CalendarSource(BaseModel):
    uri: str
    transform: dict[str, dict[str, Any]]


class CalendarConfig(BaseModel):
    source: list[CalendarSource]
    transform: dict[str, dict[str, Any]]


class Configuration(BaseModel):
    calendar: dict[str, CalendarConfig]


def deserialise(file: str):
    Configuration.model_validate(cuddly_dicts.kdl_source_to_dict(
        file,
        {
            "seconds": lambda sec: timedelta(seconds=sec),
            "minutes": lambda min: timedelta(minutes=min),
            "hours": lambda hrs: timedelta(hours=hrs),
            "days": lambda days: timedelta(days=days),
            "weeks": lambda wks: timedelta(weeks=wks),
            "months": lambda mths: timedelta(weeks=mths*4)
        }
    ))

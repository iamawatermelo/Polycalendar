from datetime import timedelta
from typing import Any
from kdl.parsefuncs import parse
from kdl.parsing import ParseConfig
from pydantic import BaseModel
import cuddly_dicts


class CalendarSource(BaseModel):
    transform: dict[str, dict[str, Any]]


class CalendarConfig(BaseModel):
    source: dict[str, CalendarSource]
    transform: dict[str, dict[str, Any]]


class Configuration(BaseModel):
    calendar: dict[str, CalendarConfig]


def deserialise(file: str):
    src = cuddly_dicts.kdl_source_to_dict(
        file,
        {
            "seconds": lambda sec, _: timedelta(seconds=sec.value),
            "minutes": lambda min, _: timedelta(minutes=min.value),
            "hours": lambda hrs, _: timedelta(hours=hrs.value),
            "days": lambda days, _: timedelta(days=days.value),
            "weeks": lambda wks, _: timedelta(weeks=wks.value),
            "months": lambda mths, _: timedelta(weeks=mths.value*4)
        }
    )
    
    return Configuration.model_validate(src)

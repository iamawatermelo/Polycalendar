"""
polycalendar/null

Does nothing.
"""

from typing import Any
from ics import Calendar 


async def null_transformer(calendar: Calendar, config: dict[str, Any]):
    pass

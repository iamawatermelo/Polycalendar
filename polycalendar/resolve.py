import ics
import asyncio
import aiohttp
from urllib.parse import urlparse
from polycalendar.config import CalendarConfig


class CalendarResolveException(BaseException):
    pass


async def fetch(session: aiohttp.ClientSession, url: str) -> bytes:
    async with session.get(url, headers={
        "User-Agent": "polycalendar"
    }):
        


async def resolve(calendar: CalendarConfig) -> ics.Calendar:
    async with asyncio.TaskGroup() as tg, aiohttp.ClientSession() as session:
        for source in calendar.source:
            uri = urlparse(source.uri)
            
            match uri.scheme.lower():
                case "http" | "https":
                    tg.create_task(session.get(source.uri))
                case "file":
                    tg.create_task()
                case _:
                    raise CalendarResolveException(f"Invalid URI {uri}")
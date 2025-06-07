from functools import lru_cache
from typing import Any, Protocol
import ics
import asyncio
import aiohttp
from importlib.metadata import entry_points
from aiofiles import open as aopen
from urllib.parse import urlparse
from polycalendar.config import CalendarConfig, CalendarSource
from polycalendar.__about__ import __version__


class CalendarResolveException(BaseException):
    pass


class TransformationPlugin(Protocol):
    async def __call__(self, calendar: ics.Calendar, config: dict[str, Any]):
        ...


@lru_cache
def fetch_plugins() -> dict[str, TransformationPlugin]:
    return {
        f"{entry_point.dist.name}/{entry_point.name}": entry_point.load()
        for entry_point in entry_points(group="polycalendar.transformations")
    }


async def transform(calendar: ics.Calendar, transformations: dict[str, dict[str, Any]]):
    plugins = fetch_plugins()
    
    for plugin, config in transformations.items():
        await plugins[plugin](calendar, config)


async def fetch_and_transform(calendar_uri: str, session: aiohttp.ClientSession, source: CalendarSource) -> ics.Calendar:
    uri = urlparse(calendar_uri)
    source_str: str
    
    match uri.scheme.lower():
        case "http" | "https":
            async with session.get(calendar_uri, headers={
                "User-Agent": f"polycalendar/{__version__}"
            }) as req:
                source_str = await req.text()
        case "file":
            async with aopen(uri.path) as fd:
                source_str = await fd.read()
        case _:
            raise CalendarResolveException(f"Invalid URI {calendar_uri}")
    
    calendar = ics.Calendar(source_str)
    
    await transform(calendar, source.transform)
    
    return calendar


async def resolve(calendar: CalendarConfig) -> ics.Calendar:
    ret = ics.Calendar()
    
    async with asyncio.TaskGroup() as tg, aiohttp.ClientSession() as session:
        tasks = list[asyncio.Task[ics.Calendar]]()
        
        for uri, source in calendar.source.items():
            tasks.append(tg.create_task(fetch_and_transform(uri, session, source)))
        
        async for task in asyncio.as_completed(tasks):
            resolved_calendar = await task
            ret.events |= resolved_calendar.events
    
    return ret
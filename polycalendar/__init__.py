from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route

from polycalendar.config import CalendarConfig, Configuration
from polycalendar.resolve import resolve


def route(config: CalendarConfig):
    async def _inner(*_):
        return Response(
            (await resolve(config)).serialize(),
            media_type="text/calendar"
        )
    
    return _inner


def build_asgi_app(config: Configuration) -> Starlette:
    return Starlette(
        debug=True,
        routes=[
            Route(f"/{name}.ics", route(calendar)) for name, calendar in config.calendar.items()
        ]
    )

from pathlib import Path
from polycalendar import build_asgi_app
from polycalendar.config import deserialise
from polycalendar.resolve import resolve
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
from os import environ
from typer import Typer


app = Typer(
    pretty_exceptions_show_locals=False,
    pretty_exceptions_short=True
)


@app.command("serve")
def run_server(file: Path, bind: str = f"localhost:{environ.get("PORT", 8080)}"):
    config = deserialise(file.read_text())
    server_config = Config()
    server_config.bind = bind
    
    asyncio.run(serve(
        build_asgi_app(config),
        server_config
    ))


@app.command("execute")
def execute(file: Path, output: Path = Path(".")):
    assert output.is_dir()
    config = deserialise(file.read_text())
    
    for name, calendar in config.calendar.items():
        with open(output / f"{name}.ics", "w") as fd:
            resolved_calendar = asyncio.run(resolve(calendar))
            fd.write(resolved_calendar.serialize())


app()
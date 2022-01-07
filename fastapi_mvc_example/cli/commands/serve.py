# -*- coding: utf-8 -*-
"""fastapi-mvc-example CLI serve command."""
from multiprocessing import cpu_count

import click
from fastapi_mvc_example.wsgi import run_wsgi


@click.command()
@click.option(
    "--host",
    help="Host to bind.",
    type=click.STRING,
    default="localhost",
    required=False,
    show_default=True,
)
@click.option(
    "-p",
    "--port",
    help="Port to bind.",
    type=click.INT,
    default=8000,
    required=False,
    show_default=True,
)
@click.option(
    "-w",
    "--workers",
    help="The number of worker processes for handling requests.",
    type=click.IntRange(min=1, max=cpu_count()),
    default=2,
    required=False,
    show_default=True,
)
def serve(**options):
    """fastapi-mvc-example CLI serve command."""
    run_wsgi(
        host=options["host"],
        port=str(options["port"]),
        workers=str(options["workers"]),
    )

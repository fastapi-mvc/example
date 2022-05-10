"""This project was generated with fastapi-mvc."""
import logging

from fastapi_mvc_example.wsgi import ApplicationLoader
from fastapi_mvc_example.version import __version__  # noqa: F401

# initialize logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

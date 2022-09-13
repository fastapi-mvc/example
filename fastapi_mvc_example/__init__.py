"""This project was generated with fastapi-mvc."""
import logging

from fastapi_mvc_example.wsgi import ApplicationLoader
from fastapi_mvc_example.version import __version__

# initialize logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

__all__ = ("ApplicationLoader", "__version__")

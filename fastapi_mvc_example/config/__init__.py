"""Application configuration.

The ``config`` submodule defines configuration for your application, router,
gunicorn, and more.

Resources:
    1. `Pydantic documentation`_
    2. `Gunicorn documentation`_

.. _Pydantic documentation:
    https://pydantic-docs.helpmanual.io/

.. _Gunicorn documentation:
    https://docs.gunicorn.org/en/20.1.0/

"""
from fastapi_mvc_example.config.application import settings
from fastapi_mvc_example.config.redis import redis

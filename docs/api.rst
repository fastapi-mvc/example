API
===

This part of the documentation lists the full API reference of all classes and functions.

WSGI
----

.. autoclass:: fastapi_mvc_example.wsgi.ApplicationLoader
   :members:
   :show-inheritance:

Config
------

.. automodule:: fastapi_mvc_example.config

.. autoclass:: fastapi_mvc_example.config.application.Application
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc_example.config.redis.Redis
   :members:
   :show-inheritance:

.. automodule:: fastapi_mvc_example.config.gunicorn

CLI
---

.. automodule:: fastapi_mvc_example.cli

.. autofunction:: fastapi_mvc_example.cli.cli.cli

.. autofunction:: fastapi_mvc_example.cli.utils.validate_directory

.. autofunction:: fastapi_mvc_example.cli.serve.serve

App
---

.. automodule:: fastapi_mvc_example.app

.. autofunction:: fastapi_mvc_example.app.asgi.on_startup

.. autofunction:: fastapi_mvc_example.app.asgi.on_shutdown

.. autofunction:: fastapi_mvc_example.app.asgi.get_application

.. automodule:: fastapi_mvc_example.app.router

Controllers
~~~~~~~~~~~

.. automodule:: fastapi_mvc_example.app.controllers

.. autofunction:: fastapi_mvc_example.app.controllers.ready.readiness_check

Models
~~~~~~

.. automodule:: fastapi_mvc_example.app.models

Views
~~~~~

.. automodule:: fastapi_mvc_example.app.views

.. autoclass:: fastapi_mvc_example.app.views.error.ErrorModel
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc_example.app.views.error.ErrorResponse
   :members:
   :show-inheritance:

Exceptions
~~~~~~~~~~

.. automodule:: fastapi_mvc_example.app.exceptions

.. autoclass:: fastapi_mvc_example.app.exceptions.http.HTTPException
   :members:
   :show-inheritance:

.. autofunction:: fastapi_mvc_example.app.exceptions.http.http_exception_handler

Utils
~~~~~

.. automodule:: fastapi_mvc_example.app.utils

.. autoclass:: fastapi_mvc_example.app.utils.aiohttp_client.AiohttpClient
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc_example.app.utils.redis.RedisClient
   :members:
   :show-inheritance:

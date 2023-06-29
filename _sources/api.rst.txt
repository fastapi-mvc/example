:tocdepth: 2
API
===

This part of the documentation lists the full API reference of all classes and functions.

WSGI
----

.. autoclass:: example.wsgi.ApplicationLoader
   :members:
   :show-inheritance:

Config
------

.. automodule:: example.config

.. autoclass:: example.config.application.Application
   :members:
   :show-inheritance:

.. autoclass:: example.config.redis.Redis
   :members:
   :show-inheritance:

.. automodule:: example.config.gunicorn

CLI
---

.. automodule:: example.cli

.. autofunction:: example.cli.cli.cli

.. autofunction:: example.cli.utils.validate_directory

.. autofunction:: example.cli.serve.serve

App
---

.. automodule:: example.app

.. autofunction:: example.app.asgi.on_startup

.. autofunction:: example.app.asgi.on_shutdown

.. autofunction:: example.app.asgi.get_application

.. automodule:: example.app.router

Controllers
~~~~~~~~~~~

.. automodule:: example.app.controllers

.. autofunction:: example.app.controllers.ready.readiness_check

Models
~~~~~~

.. automodule:: example.app.models

Views
~~~~~

.. automodule:: example.app.views

.. autoclass:: example.app.views.error.ErrorModel
   :members:
   :show-inheritance:

.. autoclass:: example.app.views.error.ErrorResponse
   :members:
   :show-inheritance:

Exceptions
~~~~~~~~~~

.. automodule:: example.app.exceptions

.. autoclass:: example.app.exceptions.http.HTTPException
   :members:
   :show-inheritance:

.. autofunction:: example.app.exceptions.http.http_exception_handler

Utils
~~~~~

.. automodule:: example.app.utils

.. autoclass:: example.app.utils.aiohttp_client.AiohttpClient
   :members:
   :show-inheritance:

.. autoclass:: example.app.utils.redis.RedisClient
   :members:
   :show-inheritance:

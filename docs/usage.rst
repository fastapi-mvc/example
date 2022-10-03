Usage
=====

CLI
---

This package exposes simple CLI for easier interaction:

.. code-block:: bash

    $ example --help
    Usage: example [OPTIONS] COMMAND [ARGS]...

      Example CLI root.

    Options:
      -v, --verbose  Enable verbose logging.
      --help         Show this message and exit.

    Commands:
      serve  example CLI serve command.
    $ example serve --help
    Usage: example serve [OPTIONS]

      Run production gunicorn (WSGI) server with uvicorn (ASGI) workers.

    Options:
      --bind TEXT                  Host to bind.
      -w, --workers INTEGER RANGE  The number of worker processes for handling
                                   requests.
      -D, --daemon                 Daemonize the Gunicorn process.
      -e, --env TEXT               Set environment variables in the execution
                                   environment.
      --pid PATH                   Specifies the PID file.
      --help                       Show this message and exit.

.. note::
    Maximum number of workers may be different in your case, it's limited to ``multiprocessing.cpu_count()``

WSGI + ASGI production server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run production unicorn + uvicorn (WSGI + ASGI) server you can use project CLI serve command:

.. code-block:: bash
    example serve
    [2022-04-23 20:21:49 +0000] [4769] [INFO] Start gunicorn WSGI with ASGI workers.
    [2022-04-23 20:21:49 +0000] [4769] [INFO] Starting gunicorn 20.1.0
    [2022-04-23 20:21:49 +0000] [4769] [INFO] Listening at: http://127.0.0.1:8000 (4769)
    [2022-04-23 20:21:49 +0000] [4769] [INFO] Using worker: uvicorn.workers.UvicornWorker
    [2022-04-23 20:21:49 +0000] [4769] [INFO] Server is ready. Spawning workers
    [2022-04-23 20:21:49 +0000] [4771] [INFO] Booting worker with pid: 4771
    [2022-04-23 20:21:49 +0000] [4771] [INFO] Worker spawned (pid: 4771)
    [2022-04-23 20:21:49 +0000] [4771] [INFO] Started server process [4771]
    [2022-04-23 20:21:49 +0000] [4771] [INFO] Waiting for application startup.
    [2022-04-23 20:21:49 +0000] [4771] [INFO] Application startup complete.
    [2022-04-23 20:21:49 +0000] [4772] [INFO] Booting worker with pid: 4772
    [2022-04-23 20:21:49 +0000] [4772] [INFO] Worker spawned (pid: 4772)
    [2022-04-23 20:21:49 +0000] [4772] [INFO] Started server process [4772]
    [2022-04-23 20:21:49 +0000] [4772] [INFO] Waiting for application startup.
    [2022-04-23 20:21:49 +0000] [4772] [INFO] Application startup complete.

To confirm it's working:

.. code-block:: bash
    $ curl localhost:8000/api/ready
    {"status":"ok"}

Dockerfile
----------

This project provides Dockerfile for containerized environment.

.. code-block:: bash
    $ make image
    $ podman run -dit --name example -p 8000:8000 example:$(cat TAG)
    f41e5fa7ffd512aea8f1aad1c12157bf1e66f961aeb707f51993e9ac343f7a4b
    $ podman ps
    CONTAINER ID  IMAGE                                 COMMAND               CREATED        STATUS            PORTS                   NAMES
    f41e5fa7ffd5  localhost/example:0.1.0  /usr/bin/fastapi ...  2 seconds ago  Up 3 seconds ago  0.0.0.0:8000->8000/tcp  example
    $ curl localhost:8000/api/ready
    {"status":"ok"}

.. note::
    Replace podman with docker if it's yours containerization engine.

Development
-----------

You can implement your own web routes logic straight away in ``example.controllers`` submodule. For more information please see `FastAPI documentation <https://fastapi.tiangolo.com/tutorial/>`__.

Makefile
~~~~~~~~

Provided Makefile is a starting point for application and infrastructure development:

.. code-block:: bash
    Usage:
      make <target>
      help             Display this help
      image            Build example image
      clean-image      Clean example image
      install          Install example with poetry
      metrics          Run example metrics checks
      unit-test        Run example unit tests
      integration-test  Run example integration tests
      docs             Build example documentation
      dev-env          Start a local Kubernetes cluster using minikube and deploy application
      clean            Remove .cache directory and cached minikube

Utilities
~~~~~~~~~

Available utilities:
* RedisClient ``example.app.utils.redis``
* AiohttpClient ``example.app.utils.aiohttp_client``

They're initialized in ``asgi.py`` on FastAPI startup event handler:

.. code-block:: python
    :emphasize-lines: 11, 13, 25, 27

    async def on_startup():
        """Fastapi startup event handler.

        Creates RedisClient and AiohttpClient session.

        """
        log.debug("Execute FastAPI startup event handler.")
        # Initialize utilities for whole FastAPI application without passing object
        # instances within the logic. Feel free to disable it if you don't need it.
        if settings.USE_REDIS:
            await RedisClient.open_redis_client()

        AiohttpClient.get_aiohttp_client()


    async def on_shutdown():
        """Fastapi shutdown event handler.

        Destroys RedisClient and AiohttpClient session.

        """
        log.debug("Execute FastAPI shutdown event handler.")
        # Gracefully close utilities.
        if settings.USE_REDIS:
            await RedisClient.close_redis_client()

        await AiohttpClient.close_aiohttp_client()

and are available for whole application scope without passing object instances. In order to utilize it just execute classmethods directly.

Example:

.. code-block:: python

    from example.app.utils import RedisClient

    response = RedisClient.get("Key")

Exceptions
~~~~~~~~~~

**HTTPException and handler**

.. literalinclude:: ../example/app/exceptions/http.py
    :language: python

This exception combined with ``http_exception_handler`` method allows you to use it the same manner as you'd use ``FastAPI.HTTPException`` with one difference.
You have freedom to define returned response body, whereas in ``FastAPI.HTTPException`` content is returned under "detail" JSON key.
In this application custom handler is added in ``asgi.py`` while initializing FastAPI application. This is needed in order to handle it globally.

Web Routes
~~~~~~~~~~

All routes documentation is available on:

* ``/`` with Swagger
* ``/redoc`` or ReDoc.


Configuration
-------------

This application provides flexibility of configuration. All significant settings are defined by the environment variables, each with the default value.
Moreover, package CLI allows overriding core ones: host, port, workers. You can modify all other available configuration settings in the gunicorn.conf.py file.

Priority of overriding configuration:

1. cli
2. environment variables
3. ``gunicorn.py``

All application configuration is available in ``example.config`` submodule.

Environment variables
~~~~~~~~~~~~~~~~~~~~~

**Application configuration**

+-----------------------------+--------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+
| Key                         | Default                                                            | Description                                                                                        |
+=============================+====================================================================+====================================================================================================+
| FASTAPI_BIND                | ``"127.0.0.1:8000"``                                               | The socket to bind. A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'. An IP is a valid HOST. |
+-----------------------------+--------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+
| FASTAPI_WORKERS             | ``"2"``                                                            | Number of gunicorn workers (uvicorn.workers.UvicornWorker.                                         |
+-----------------------------+--------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+
| FASTAPI_DEBUG               | ``"True"``                                                         | FastAPI logging level. You should disable this for production.                                     |
+-----------------------------+--------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+
| FASTAPI_PROJECT_NAME        | ``"example"``                                | FastAPI project name.                                                                              |
+-----------------------------+--------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+
| FASTAPI_VERSION             | ``"0.4.0"``                                                        | Application version.                                                                               |
+-----------------------------+--------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+
| FASTAPI_DOCS_URL            | ``"/"``                                                            | Path where swagger ui will be served at.                                                           |
+-----------------------------+--------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+
| FASTAPI_USE_REDIS           | ``"False"``                                                        | Whether or not to use Redis.                                                                       |
+-----------------------------+--------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+
| FASTAPI_GUNICORN_LOG_LEVEL  | ``"info"``                                                         | The granularity of gunicorn log output                                                             |
+-----------------------------+--------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+
| FASTAPI_GUNICORN_LOG_FORMAT | ``'%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'``  | Gunicorn log format                                                                                |
+-----------------------------+--------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+


**Redis configuration**

+-----------------------------+------------------+--------------------------------------------+
| Key                         | Default          | Description                                |
+=============================+==================+============================================+
| FASTAPI_REDIS_HOTS          | ``"127.0.0.1"``  | Redis host.                                |
+-----------------------------+------------------+--------------------------------------------+
| FASTAPI_REDIS_PORT          | ``"6379"``       | Redis port.                                |
+-----------------------------+------------------+--------------------------------------------+
| FASTAPI_REDIS_USERNAME      | ``""``           | Redis username.                            |
+-----------------------------+------------------+--------------------------------------------+
| FASTAPI_REDIS_PASSWORD      | ``""``           | Redis password.                            |
+-----------------------------+------------------+--------------------------------------------+
| FASTAPI_REDIS_USE_SENTINEL  | ``"False"``      | If provided Redis config is for Sentinel.  |
+-----------------------------+------------------+--------------------------------------------+

Gunicorn
~~~~~~~~

`Gunicorn configuration file documentation <https://docs.gunicorn.org/en/latest/settings.html>`__

.. literalinclude:: ../example/config/gunicorn.py
    :language: python

Routes
~~~~~~

Endpoints are defined in ``example.app.router`` submodule. Just simply import your controller and include it to FastAPI router:

.. literalinclude:: ../example/app/router.py
    :language: python

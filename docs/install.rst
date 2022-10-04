Installation
============

Application
-----------

Prerequisites:

* Python 3.8 or later `(How to install python) <https://docs.python-guide.org/starting/installation/>`__
* make
* (optional) curl
* (optional) Poetry `(How to install poetry) <https://python-poetry.org/docs/#installation>`__

To install fastapi-mvc from source first clone the repository and use ``make install`` target:

.. code-block:: bash

    make install

By default ``make install`` target will search first for ``python3`` then ``python`` executable in your ``PATH``.
If needed this can be overridden by ``PYTHON`` environment variable.

.. code-block:: bash

    export PYTHON=/path/to/my/python
    make install

Lastly if Poetry is not found in its default installation directory (${HOME}/.local/share/pypoetry) this target will install it for you.
However, one can always point to existing/customize Poetry installation with `environment variables <https://python-poetry.org/docs/configuration/#using-environment-variables>`__:

.. code-block:: bash

    export POETRY_HOME=/custom/poetry/path
    export POETRY_CACHE_DIR=/custom/poetry/path/cache
    export POETRY_VIRTUALENVS_IN_PROJECT=true
    make install

Or using Poetry directly, should you choose:

.. code-block:: bash

    poetry install

Infrastructure
--------------

Prerequisites:

* make
* gcc
* golang
* minikube version 1.22.0 `(How to install minikube) <https://minikube.sigs.k8s.io/docs/start>`__
* helm version 3.0.0 or higher `(How to install helm) <https://helm.sh/docs/intro/install>`__
* kubectl version 1.16 up to 1.20.8 `(How to install kubectl) <https://kubernetes.io/docs/tasks/tools/install-kubectl-linux>`__
* Container runtime interface.

.. note::
    Makefile dev-env target uses docker for minikube, for other CRI you'll need to modify this line in ``build/dev-env.sh`` ``MINIKUBE_IN_STYLE=0 minikube start --driver=docker 2>/dev/null``

To bootstrap local minikube Kubernetes cluster exposing ``example`` application run:

.. code-block:: bash

    make dev-env

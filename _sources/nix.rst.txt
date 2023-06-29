Using Nix
=========

Installation
------------

Prerequisites:

* Nix 2.8.x or later installed `(How to install Nix) <https://nixos.org/download.html>`__

First `enable Nix flakes <https://nixos.wiki/wiki/Flakes#Enable_flakes>`__ if needed.

Optionally `setup fastapi-mvc Nix binary cache <https://app.cachix.org/cache/fastapi-mvc#pull>`__ to speed up the build process:

.. code-block:: bash

    nix-env -iA cachix -f https://cachix.org/api/v1/install
    cachix use fastapi-mvc

To build default package run:

.. code-block:: bash

    nix build .#default

Or with concrete Python version, should you choose:

.. code-block:: bash

    # Build with Python38
    nix build .#example-py38
    # Build with Python39
    nix build .#example-py39
    # Build with Python310
    nix build .#example-py310

Lastly, to spawn shell for development environment run:

.. code-block:: bash

    nix develop .#default

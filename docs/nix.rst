Using Nix
=========

Installation
------------

Prerequisites:

* Nix 2.8.x or later installed `(How to install Nix) <https://nixos.org/download.html>`__

First configure Nix channel if needed:

.. code-block:: bash

    nix-channel --add https://nixos.org/channels/nixos-22.05
    nix-channel --update

Next install make via Nix:

.. code-block:: bash

    nix-env --install gnumake
    # If you do not want to install make to your profile, one can always use it ad-hoc via nix-shell
    nix-shell -p gnumake

Lastly, use ``make install`` target:

.. code-block:: bash

    make install
    # Or
    nix-shell -p gnumake --run "make install"

Or using Nix directly, should you choose:

.. code-block:: bash

    nix-build -E 'with import <nixpkgs> { overlays = [ (import ./overlay.nix) ]; }; callPackage ./editable.nix {python = pkgs.python310; poetry2nix = pkgs.poetry2nix;}'

{ pkgs ? import <nixpkgs> { }
, python ? "python3"
}:

let
  pythonPackage = builtins.getAttr (python) pkgs;
  poetry = pkgs.poetry.override { python = pythonPackage; };
in
pkgs.mkShell {
  buildInputs = [
    pkgs.gnumake
    pkgs.curl
    pythonPackage
    poetry
  ];
  shellHook = ''
    export POETRY_HOME=${poetry}
    export POETRY_BINARY=${poetry}/bin/poetry
    export POETRY_VIRTUALENVS_IN_PROJECT=true
    unset SOURCE_DATE_EPOCH
  '';
}

#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

POETRY_HOME="${POETRY_HOME:=${HOME}/.local/share/pypoetry}"
POETRY_BINARY="${POETRY_BINARY:=${POETRY_HOME}/venv/bin/poetry}"
echo "[metrics] Run fastapi-mvc-example PEP 8 checks."
"$POETRY_BINARY" run flake8 --select=E,W,I --max-line-length 80 --import-order-style pep8 --statistics --count fastapi_mvc_example
echo "[metrics] Run fastapi-mvc-example PEP 257 checks."
"$POETRY_BINARY" run flake8 --select=D --ignore D301 --statistics --count fastapi_mvc_example
echo "[metrics] Run fastapi-mvc-example pyflakes checks."
"$POETRY_BINARY" run flake8 --select=F --statistics --count fastapi_mvc_example
echo "[metrics] Run fastapi-mvc-example code complexity checks."
"$POETRY_BINARY" run flake8 --select=C901 --statistics --count fastapi_mvc_example
echo "[metrics] Run fastapi-mvc-example open TODO checks."
"$POETRY_BINARY" run flake8 --select=T --statistics --count fastapi_mvc_example tests
echo "[metrics] Run fastapi-mvc-example black checks."
"$POETRY_BINARY" run black -l 80 --check fastapi_mvc_example

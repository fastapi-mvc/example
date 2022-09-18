#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

echo "[integration-test] Run example integration tests."
POETRY_HOME="${POETRY_HOME:=${HOME}/.local/share/pypoetry}"
POETRY_BINARY="${POETRY_BINARY:=${POETRY_HOME}/venv/bin/poetry}"
"$POETRY_BINARY" run pytest tests/integration

POETRY_HOME ?= ${HOME}/.local/share/pypoetry
POETRY_BINARY ?= ${POETRY_HOME}/venv/bin/poetry
POETRY_VERSION ?= 1.2.0

.PHONY: build
build: ## Build example package
	echo "[build] Build example package."
	${POETRY_BINARY} build

.PHONY: install
install:  ## Install example with poetry
	@build/install.sh

.PHONY: image
image:  ## Build example image
	@build/image.sh

.PHONY: metrics
metrics: install ## Run example metrics checks
	echo "[metrics] Run example PEP 8 checks."
	${POETRY_BINARY} run flake8 --select=E,W,I --max-line-length 80 --import-order-style pep8 --statistics --count example
	echo "[metrics] Run example PEP 257 checks."
	${POETRY_BINARY} run flake8 --select=D --ignore D301 --statistics --count example
	echo "[metrics] Run example pyflakes checks."
	${POETRY_BINARY} run flake8 --select=F --statistics --count example
	echo "[metrics] Run example code complexity checks."
	${POETRY_BINARY} run flake8 --select=C901 --statistics --count example
	echo "[metrics] Run example open TODO checks."
	${POETRY_BINARY} run flake8 --select=T --statistics --count example tests
	echo "[metrics] Run example black checks."
	${POETRY_BINARY} run black -l 80 --check example

.PHONY: unit-test
unit-test: install ## Run example unit tests
	echo "[unit-test] Run example unit tests."
	${POETRY_BINARY} run pytest tests/unit

.PHONY: integration-test
integration-test: install ## Run example integration tests
	echo "[unit-test] Run example integration tests."
	${POETRY_BINARY} run pytest tests/integration

.PHONY: test
test: unit-test integration-test ## Run example tests

.PHONY: docs
docs: install ## Build example documentation
	echo "[docs] Build example documentation."
	${POETRY_BINARY} run sphinx-build docs site

.PHONY: dev-env
dev-env: image ## Start a local Kubernetes cluster using minikube and deploy application
	@build/dev-env.sh

.PHONY: clean
clean: ## Remove .cache directory and cached minikube
	minikube delete && rm -rf ~/.cache ~/.minikube


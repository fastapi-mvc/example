PYTHON_NIXPKG ?= python39

.PHONY: build
build:  ## Build example Nix package
	echo "[nix][build] Build example Nix package."
	@nix-build -E 'with import <nixpkgs> { overlays = [ (import ./overlay.nix) ]; }; callPackage ./default.nix {python = pkgs.${PYTHON_NIXPKG}; poetry2nix = pkgs.poetry2nix;}'

.PHONY: install
install:  ## Install example env with Nix
	echo "[nix][install] Install example env with Nix"
	@nix-build -E 'with import <nixpkgs> { overlays = [ (import ./overlay.nix) ]; }; callPackage ./editable.nix {python = pkgs.${PYTHON_NIXPKG}; poetry2nix = pkgs.poetry2nix;}'

.PHONY: image
image:  ## Build example image with Nix
	echo "[nix][image] Build example image with Nix."
	@nix-build image.nix

.PHONY: docs
docs: install  ## Build example documentation
	echo "[docs] Build example documentation."
	result/bin/sphinx-build docs site

.PHONY: metrics
metrics: install  ## Run example metrics checks
	echo "[nix][metrics] Run example PEP 8 checks."
	result/bin/flake8 --select=E,W,I --max-line-length 80 --import-order-style pep8 --statistics --count example
	echo "[nix][metrics] Run example PEP 257 checks."
	result/bin/flake8 --select=D --ignore D301 --statistics --count example
	echo "[nix][metrics] Run example pyflakes checks."
	result/bin/flake8 --select=F --statistics --count example
	echo "[nix][metrics] Run example code complexity checks."
	result/bin/flake8 --select=C901 --statistics --count example
	echo "[nix][metrics] Run example open TODO checks."
	result/bin/flake8 --select=T --statistics --count example tests
	echo "[nix][metrics] Run example black checks."
	result/bin/black -l 80 --check example

.PHONY: unit-test
unit-test: install  ## Run example unit tests
	echo "[nix][unit-test] Run example unit tests."
	result/bin/pytest tests/unit

.PHONY: integration-test
integration-test: install  ## Run example integration tests
	echo "[nix][integration-test] Run example unit tests."
	result/bin/pytest tests/integration

.PHONY: coverage
coverage: install  ## Run example tests coverage
	echo "[nix][coverage] Run example tests coverage."
	result/bin/pytest --cov-config=.coveragerc --cov=example --cov-fail-under=90 --cov-report=xml --cov-report=term-missing tests

.PHONY: test
test: unit-test integration-test coverage  ## Run example tests


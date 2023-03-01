{
  description = "example flake";
  nixConfig.bash-prompt = ''\n\[\033[1;32m\][nix-develop:\w]\$\[\033[0m\] '';

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix?ref=1.39.1";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    {
      overlays.default = nixpkgs.lib.composeManyExtensions [
        poetry2nix.overlay
        (import ./overlay.nix)
        (final: prev: {
          example = prev.callPackage ./default.nix {
            python = final.python3;
            poetry2nix = final.poetry2nix;
          };
          example-dev = prev.callPackage ./editable.nix {
            python = final.python3;
            poetry2nix = final.poetry2nix;
          };
        })
      ];
    } // (flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlays.default ];
        };
      in
      rec {
        packages = {
          default = pkgs.example;
          example-py38 = pkgs.example.override { python = pkgs.python38; };
          example-py39 = pkgs.example.override { python = pkgs.python39; };
          example-py310 = pkgs.example.override { python = pkgs.python310; };
          poetryEnv = pkgs.example-dev;
        } // pkgs.lib.optionalAttrs pkgs.stdenv.isLinux {
          image = pkgs.callPackage ./image.nix {
            inherit pkgs;
            app = pkgs.example;
          };
        };

        apps = {
          example = flake-utils.lib.mkApp { drv = pkgs.example; };
          metrics = {
            type = "app";
            program = toString (pkgs.writeScript "metrics" ''
              export PATH="${pkgs.lib.makeBinPath [
                  pkgs.example-dev
                  pkgs.git
              ]}"
              echo "[nix][metrics] Run example PEP 8 checks."
              flake8 --select=E,W,I --max-line-length 88 --import-order-style pep8 --statistics --count example
              echo "[nix][metrics] Run example PEP 257 checks."
              flake8 --select=D --ignore D301 --statistics --count example
              echo "[nix][metrics] Run example pyflakes checks."
              flake8 --select=F --statistics --count example
              echo "[nix][metrics] Run example code complexity checks."
              flake8 --select=C901 --statistics --count example
              echo "[nix][metrics] Run example open TODO checks."
              flake8 --select=T --statistics --count example tests
              echo "[nix][metrics] Run example black checks."
              black -l 80 --check example
            '');
          };
          docs = {
            type = "app";
            program = toString (pkgs.writeScript "docs" ''
              export PATH="${pkgs.lib.makeBinPath [
                  pkgs.example-dev
                  pkgs.git
              ]}"
              echo "[nix][docs] Build example documentation."
              sphinx-build docs site
            '');
          };
          unit-test = {
            type = "app";
            program = toString (pkgs.writeScript "unit-test" ''
              export PATH="${pkgs.lib.makeBinPath [
                  pkgs.example-dev
                  pkgs.git
              ]}"
              echo "[nix][unit-test] Run example unit tests."
              pytest tests/unit
            '');
          };
          integration-test = {
            type = "app";
            program = toString (pkgs.writeScript "integration-test" ''
              export PATH="${pkgs.lib.makeBinPath [
                  pkgs.example-dev
                  pkgs.git
                  pkgs.coreutils
              ]}"
              echo "[nix][integration-test] Run example unit tests."
              pytest tests/integration
            '');
          };
          coverage = {
            type = "app";
            program = toString (pkgs.writeScript "coverage" ''
              export PATH="${pkgs.lib.makeBinPath [
                  pkgs.example-dev
                  pkgs.git
                  pkgs.coreutils
              ]}"
              echo "[nix][coverage] Run example tests coverage."
              pytest --cov=example --cov-fail-under=90 --cov-report=xml --cov-report=term-missing tests
            '');
          };
          mypy = {
            type = "app";
            program = toString (pkgs.writeScript "mypy" ''
              export PATH="${pkgs.lib.makeBinPath [
                  pkgs.example-dev
                  pkgs.git
              ]}"
              echo "[nix][mypy] Run example mypy checks."
              mypy example
            '');
          };
          test = {
            type = "app";
            program = toString (pkgs.writeScript "test" ''
              ${apps.unit-test.program}
              ${apps.integration-test.program}
            '');
          };
        };

        devShells = {
          default = pkgs.example-dev.env.overrideAttrs (oldAttrs: {
            buildInputs = [
              pkgs.git
              pkgs.poetry
            ];
          });
          poetry = import ./shell.nix { inherit pkgs; };
        };
      }));
}

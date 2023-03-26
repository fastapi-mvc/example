{
  description = "example flake";
  nixConfig = {
    bash-prompt = ''\n\[\033[1;32m\][nix-develop:\w]\$\[\033[0m\] '';
    extra-trusted-public-keys = [
      "fastapi-mvc.cachix.org-1:knQ8Qo41bnhBmOB6Sp0UH10EV76AXW5o69SbAS668Fg="
    ];
    extra-substituters = [
      "https://fastapi-mvc.cachix.org"
    ];
  };

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
    flake-parts.url = "github:hercules-ci/flake-parts";
    poetry2nix = {
      url = "github:nix-community/poetry2nix?ref=1.40.1";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-parts, poetry2nix }@inputs:
    let
      mkApp =
        { drv
        , name ? drv.pname or drv.name
        , exePath ? drv.passthru.exePath or "/bin/${name}"
        }:
        {
          type = "app";
          program = "${drv}${exePath}";
        };
    in
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.flake-parts.flakeModules.easyOverlay
      ];
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      perSystem = { config, self', inputs', pkgs, system, ... }: {
        # Add poetry2nix overrides to nixpkgs
        _module.args.pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlays.poetry2nix ];
        };

        packages =
          let
            mkProject =
              { python ? pkgs.python3
              }:
              pkgs.callPackage ./default.nix {
                inherit python;
                poetry2nix = pkgs.poetry2nix;
                git = pkgs.git;
              };
          in
          {
            default = mkProject { };
            example-py38 = mkProject { python = pkgs.python38; };
            example-py39 = mkProject { python = pkgs.python39; };
            example-py310 = mkProject { python = pkgs.python310; };
            example-py311 = mkProject { python = pkgs.python311; };
            example-dev = pkgs.callPackage ./editable.nix {
              poetry2nix = pkgs.poetry2nix;
              python = pkgs.python3;
            };
          } // pkgs.lib.optionalAttrs pkgs.stdenv.isLinux {
            image = pkgs.callPackage ./image.nix {
              inherit pkgs;
              app = config.packages.default;
            };
          };

        overlayAttrs = {
          inherit (config.packages) default;
        };

        apps = {
          example = mkApp { drv = config.packages; };
          metrics = {
            type = "app";
            program = toString (pkgs.writeScript "metrics" ''
              export PATH="${pkgs.lib.makeBinPath [
                  config.packages.example-dev
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
              black --check example
            '');
          };
          docs = {
            type = "app";
            program = toString (pkgs.writeScript "docs" ''
              export PATH="${pkgs.lib.makeBinPath [
                  config.packages.example-dev
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
                  config.packages.example-dev
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
                  config.packages.example-dev
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
                  config.packages.example-dev
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
                  config.packages.example-dev
                  pkgs.git
              ]}"
              echo "[nix][mypy] Run example mypy checks."
              mypy example
            '');
          };
          test = {
            type = "app";
            program = toString (pkgs.writeScript "test" ''
              ${config.apps.unit-test.program}
              ${config.apps.integration-test.program}
            '');
          };
        };

        devShells = {
          default = config.packages.example-dev.env.overrideAttrs (oldAttrs: {
            buildInputs = [
              pkgs.git
              pkgs.poetry
            ];
          });
          poetry = import ./shell.nix { inherit pkgs; };
        };
      };
      flake = {
        overlays.poetry2nix = nixpkgs.lib.composeManyExtensions [
          poetry2nix.overlay
          (import ./overlay.nix)
        ];
      };
    };
}

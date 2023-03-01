final: prev: {
  # p2n-final & p2n-prev refers to poetry2nix
  poetry2nix = prev.poetry2nix.overrideScope' (p2n-final: p2n-prev: {

    # py-final & py-prev refers to python packages
    defaultPoetryOverrides = p2n-prev.defaultPoetryOverrides.extend (py-final: py-prev: {

      sphinx = py-prev.sphinx.overridePythonAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [ py-final.flit-core ];
      });

      pydantic = py-prev.pydantic.overrideAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [ final.libxcrypt ];
      });

      flake8-todo = py-prev.flake8-todo.overridePythonAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [ py-final.setuptools ];
      });

      pathspec = py-prev.pathspec.overridePythonAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [ py-final.flit-core ];
      });

      pydocstyle = py-prev.pydocstyle.overridePythonAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [ py-final.poetry-core py-final.setuptools ];
      });

      iniconfig = py-prev.iniconfig.overridePythonAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [
          py-final.hatch-vcs
          py-final.hatchling
          py-final.build
          py-final.setuptools-scm
        ];
      });

      plumbum = py-prev.plumbum.overridePythonAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [ py-final.hatch-vcs py-final.hatchling ];
      });

      pyyaml-include = py-prev.pyyaml-include.overridePythonAttrs (old: {
        postPatch = ''
          substituteInPlace setup.py --replace 'setup()' 'setup(version="${old.version}")'
        '';
      });

      fastapi-mvc = py-prev.fastapi-mvc.overridePythonAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [ py-final.poetry ];
      });

    });

  });
}

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

      packaging = py-prev.packaging.overridePythonAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [ py-final.flit-core ];
      });

    });

  });
}

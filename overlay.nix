final: prev: {
  # p2n-final & p2n-prev refers to poetry2nix
  poetry2nix = prev.poetry2nix.overrideScope' (p2n-final: p2n-prev: {

    # py-final & py-prev refers to python packages
    defaultPoetryOverrides = p2n-prev.defaultPoetryOverrides.extend (py-final: py-prev: {

      sphinx = py-prev.sphinx.overridePythonAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [ py-final.flit-core ];
      });

    });

  });
}
{ lib
, python
, poetry2nix
}:

poetry2nix.mkPoetryApplication rec {
  inherit python;

  projectDir = ./.;
  src = ./.;
  pyproject = ./pyproject.toml;
  poetrylock = ./poetry.lock;

  pythonImportsCheck = [ "example" ];

  meta = with lib; {
    homepage = "https://github.com/fastapi-mvc/example";
    description = "This project was generated with fastapi-mvc.";
  };
}

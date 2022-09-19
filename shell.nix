{ pkgs ? import <nixpkgs> { }
, python ? "python3"
}:

let
  app = pkgs.callPackage ./editable.nix {
    python = builtins.getAttr (python) pkgs;
    poetry2nix = pkgs.poetry2nix;
  };
in
app.env.overrideAttrs (oldAttrs: {
  buildInputs = [
    pkgs.gnumake
    pkgs.podman
    pkgs.kubernetes-helm
    pkgs.kubectl
    pkgs.minikube
  ];
})

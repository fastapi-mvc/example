{ pkgs ? import <nixpkgs> {} }:

let
  nonRootShadowSetup = { user, uid, gid ? uid }: with pkgs; [
    (
      writeTextDir "etc/shadow" ''
        root:!x:::::::
        ${user}:!:::::::
      ''
    )
    (
      writeTextDir "etc/passwd" ''
        root:x:0:0::/root:${runtimeShell}
        ${user}:x:${toString uid}:${toString gid}::/home/${user}:
      ''
    )
    (
      writeTextDir "etc/group" ''
        root:x:0:
        ${user}:x:${toString gid}:
      ''
    )
    (
      writeTextDir "etc/gshadow" ''
        root:x::
        ${user}:x::
      ''
    )
  ];

  example = pkgs.callPackage ./default.nix {
    python = pkgs.python39;
    poetry2nix = pkgs.poetry2nix;
  };

  pyEnv = example.dependencyEnv;
in

pkgs.dockerTools.buildImage {
  name = "example";
  tag = "0.1.0";

  contents = [
    pyEnv
  ] ++ nonRootShadowSetup { uid = 999; user = "nonroot"; };

  runAsRoot = ''
    mkdir /tmp
    chmod 777 /tmp
  '';

  config = {
    User = "nonroot";
    Entrypoint = [ "${pyEnv}/bin/example" ];
  };
}

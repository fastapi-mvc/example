{ pkgs ? import <nixpkgs> { }
, app
, name ? "example"
, tag ? "latest"
}:

pkgs.dockerTools.buildImage {
  inherit name tag;

  copyToRoot = pkgs.buildEnv {
    name = "image-root";
    paths = [
      app
      pkgs.cacert
      pkgs.tzdata
    ];
    pathsToLink = [ "/bin" ];
  };

  runAsRoot = ''
    #!${pkgs.runtimeShell}
    ${pkgs.dockerTools.shadowSetup}
    mkdir /tmp
    chmod 777 -R /tmp
    groupadd -r nonroot
    useradd -r -g nonroot nonroot
    mkdir -p /workspace
    chown nonroot:nonroot /workspace
  '';

  config = {
    Env = [
      "SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
      "PYTHONDONTWRITEBYTECODE=1"
      "PYTHONUNBUFFERED=1"
    ];
    User = "nonroot";
    WorkingDir = "/workspace";
    Entrypoint = [ "${app}/bin/example" ];
  };
}

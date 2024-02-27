{
  description = "A flake for the syn data fidelity library";

  inputs = {
    linux-nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
    darwin-nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
  };

  outputs = { self, linux-nixpkgs, darwin-nixpkgs, flake-utils, ... }: let
    pkgs = {
      x86_64-linux = linux-nixpkgs.legacyPackages.x86_64-linux;
      aarch64-darwin = darwin-nixpkgs.legacyPackages.aarch64-darwin;
    };
    mkShell = pkgs: pkgs.mkShell {
      buildInputs = [
        (pkgs.python310Packages.buildPythonPackage {
          pname = "syn_data_fidelity";
          version = "0.0.1";
          src = self;
          nativeBuildInputs = with pkgs.python310Packages; [
            setuptools
          ];
          nativeCheckInputs = with pkgs.python310Packages; [
            pytest
            numpy
            scipy
            polars
          ];
          checkPhase = "pytest tests/ -vvv";
        })
          (with pkgs.python310Packages; [
            numpy
            scipy
            polars
          ])
        ];
    };
  in {
    devShells = {
      x86_64-linux.default = mkShell pkgs.x86_64-linux;
      aarch64-darwin.default = mkShell pkgs.aarch64-darwin;
    };
  };
}

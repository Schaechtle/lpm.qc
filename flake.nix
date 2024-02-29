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
    mkSynDataFidelity = pkgs: (pkgs.python310Packages.buildPythonPackage {
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
          propagatedBuildInputs = (with pkgs.python310Packages; [
            numpy
            scipy
            polars
          ]);
        });
    mkShell = pkgs: pkgs.mkShell {
      buildInputs = [(mkSynDataFidelity pkgs)];
    };
  in {
    devShells = {
      x86_64-linux.default = mkShell pkgs.x86_64-linux;
      aarch64-darwin.default = mkShell pkgs.aarch64-darwin;
    };
    packages = {
      x86_64-linux.default = mkSynDataFidelity pkgs.x86_64-linux;
      aarch64-darwin.default = mkSynDataFidelity pkgs.aarch64-darwin;
    };
    apps = {
      x86_64-linux.default = {
        type = "app";
        program = "${mkSynDataFidelity pkgs.x86_64-linux}/bin/assess-distance";
      };
      aarch64-darwin.default = {
        type = "app";
        program = "${mkSynDataFidelity pkgs.aarch64-darwin}/bin/assess-distance";
      };
      x86_64-linux.assess-statistics = {
        type = "app";
        program = "${mkSynDataFidelity pkgs.x86_64-linux}/bin/assess-statistics";
      };
      aarch64-darwin.assess-statistics = {
        type = "app";
        program = "${mkSynDataFidelity pkgs.aarch64-darwin}/bin/assess-statistics";
      };
    };
  };
}

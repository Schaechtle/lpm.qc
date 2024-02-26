{
  description = "A flake for the syn data fidelity library";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11"; # Adjust this to the desired Nixpkgs channel
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      syn_data_fidelity = pkgs.python310Packages.buildPythonPackage {
        pname = "syn_data_fidelity";
        version = "0.0.1";
        src = self;
        nativeBuildInputs = with pkgs.python310Packages; [
          setuptools
        ];
        dependencies = [
          pkgs.python310Packages.numpy
          pkgs.python310Packages.scipy
          pkgs.python310Packages.polars
        ];
        doCheck= false;
      };
    in {
      devShell = pkgs.mkShell {
        buildInputs = [
          syn_data_fidelity
          pkgs.python310Packages.pytest
          pkgs.python310Packages.numpy
          pkgs.python310Packages.scipy
          pkgs.python310Packages.polars
        ];
      };
    });
}

{
  description = "A flake for the syn data fidelity library";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05"; # Adjust this to the desired Nixpkgs channel
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
        nativeCheckInputs = with pkgs.python310Packages; [
          pytest
          numpy
          scipy
          polars
        ];
        checkPhase = "pytest tests/ -vvv";
      };
    in {
      devShell = pkgs.mkShell {
        buildInputs = [
          syn_data_fidelity
          (with pkgs.python310Packages; [
            numpy
            scipy
            polars
          ])
        ];
      };
    });
}

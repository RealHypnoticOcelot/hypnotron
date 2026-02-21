{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs {inherit system;};

    # This whole expression, and comics.nix, exist because the comics library doesn't exist by default in Nixpkgs
    # as of the time of programming this
    python3 = pkgs.python3.override { 
      self = python3;
      packageOverrides = pyfinal: pyprev: { # Create a package override that makes imports python-pkgs.comics from ./comics.nix
        comics = pyfinal.callPackage ./comics.nix { };
      };
    };
  in
  {
    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        (python3.withPackages (python-pkgs: with python-pkgs; [
          discordpy
          pillow
          pytz
          openai
          geopandas
          matplotlib
          python-dotenv
          comics
        ]))
        ffmpeg
      ];
    };
  };
}
# Run `nix develop` to enter a shell containing python, and run `exit` to leave the shell
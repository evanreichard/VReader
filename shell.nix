{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  packages = with pkgs; [
    nodePackages.tailwindcss
    python311
  ];
}

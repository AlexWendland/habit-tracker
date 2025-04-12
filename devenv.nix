{ pkgs, lib, config, inputs, ... }:

{
  packages = [ 
    pkgs.ruff
    pkgs.mypy
  ];
  # https://devenv.sh/languages/
  languages.javascript = {
    enable = true;
    npm = {
      enable = true;
    };
  };

  languages.python = {
    enable = true;
    uv = {
      enable = true;
    };
  };
}

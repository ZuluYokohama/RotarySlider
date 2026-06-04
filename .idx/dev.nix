# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-23.11"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.venvShellHook
    pkgs.gnumake
    pkgs.gh
  ];

  # Sets environment variables in the workspace
  env = {};

  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "ms-python.python"
      "ms-python.debugpy"
      "charliermarsh.uv"
    ];

    # Enable previews
    previews = {
      enable = true;
      previews = {};
    };

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      onCreate = {
        setup-venv = ''
          python -m venv .venv
          source .venv/bin/activate
          pip install rich mcp
        '';
      };
      # Runs when the workspace is (re)started
      onStart = {
        show-cli = ''
          source .venv/bin/activate
          make help
        '';
      };
    };
  };
}

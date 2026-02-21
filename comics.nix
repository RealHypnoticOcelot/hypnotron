{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  wheel,
  pillow,
  beautifulsoup4,
  ipython,
  python-dateutil,
  requests,
  playwright,
  ...
}:

buildPythonPackage rec {
  pname = "comics";
  version = "0.9.2";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-z7CxOCoQdnqdCvwpgxARy3jGWWP348i+Ouci0toMX9I=";
  };


  # do not run tests
  doCheck = false;

  # For this package, it requires later versions of these dependencies,
  # so we're just replace the requirement with a less strict one
  # This might just break things, though!
  patchPhase = ''
    substituteInPlace \
      pyproject.toml \
      --replace "Pillow>=9.2.0,<12.0.0" "pillow" \
      --replace "ipython>=8.5.0,<9.0.0" "ipython"
    '';

  # specific to buildPythonPackage, see its reference
  pyproject = true;
  build-system = [
    setuptools
    wheel
  ];
  dependencies = [
    pillow
    ipython
    beautifulsoup4
    python-dateutil
    requests
    playwright
  ];
}
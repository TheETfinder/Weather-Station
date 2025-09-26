let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.xmltodict
      python-pkgs.requests-cache
      python-pkgs.datetime
      python-pkgs.retry
      python-pkgs.yfinance
      python-pkgs.pip
      python-pkgs.pandas
      python-pkgs.xmlschema
    ]))
  ];
}


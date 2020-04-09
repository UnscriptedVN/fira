# Fira

Fira is the package that contains the backend code and API code for Unscripted's minigame. Fira is named after Fira Sans, one of the game's characters.


[![MPL](https://img.shields.io/github/license/alicerunsonfedora/fira)](LICENSE.txt)
![Python](https://img.shields.io/badge/python-2.7+-blue.svg)

## Requirements

- Python 2.7+
- Poetry package manager

## Getting started

Fira comes pre-packaged in Unscripted but can be installed outside of the game to work better with IDEs and other Python tools such as Poetry.

### Dependencies

Fira is both a Python 2 and Python 3 package and relies on the TOML Python package. These dependencies will be installed with the package, either from source or from PyPI.

### Quick Start: Install on PyPI

Fira is available on PyPI and can be installed as such:

```
pip install uvn-fira
```

### Install from source

To install Fira from the source code, first clone the repository from GitHub via `git clone`. You'll also need to install [Poetry](https://python-poetry.org). In the root of the source, run the following commands:

```
poetry install
poetry build
```

The resulting wheel files will be available in the `dist` directory.

## License

The Fira package is licensed under the Mozilla Public License v2.0.
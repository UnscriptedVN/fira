# Fira

**Fira** is the main backend and API code for the minigame in [Unscripted](https://unscripted.marquiskurt.net), a visual novel about software development. Fira provides many facets of the minigame, including a public API that players can use to code solutions to the minigame puzzles, a configuration and data generator from level files, and a virtual machine that runs low-level code that the minigame processes. Fira is named after Fira Sans, one of the game's characters.


[![MPL](https://img.shields.io/github/license/alicerunsonfedora/fira)](LICENSE.txt)
![Python](https://img.shields.io/badge/python-2.7+-blue.svg)
[![PyPI version](https://badge.fury.io/py/uvn-fira.svg)](https://pypi.org/project/uvn-fira)

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

## Usage

For players installing this package to solve minigame puzzles, using the Fira package to access the API is relatively straightforward:

```py
from uvn_fira.api import get_level_information, CSPlayer, CSWorld

gp, gw = get_level_information(0,
                               fn_path=renpy.config.savedir + "/minigame",
                               exists=renpy.loadable,
                               load=renpy.exports.file) # type: (CSPlayer, CSWorld)
```

Documentation on the API is located inside of Unscripted by going to **Help &rsaquo; Minigame** or **Settings &rsaquo; Minigame**.

The documentation for the entire package is located at [https://fira.marquiskurt.net](https://fira.marquiskurt.net), which is useful for developers that wish to make custom toolkits that connect to the minigame's virtual machine or for modders that wish to make custom minigame levels.

## Reporting bugs

Bugs and feature requests for Fira can be submitted on YouTrack. [Submit a report &rsaquo;](https://youtrack.marquiskurt.net/youtrack/newIssue?project=FIRA)

## License

The Fira package is licensed under the Mozilla Public License v2.0.
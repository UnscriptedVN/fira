# Fira

Fira is the package that contains the backend code and API code for Unscripted's minigame. Fira is named after Fira Sans, one of the game's characters.


[![MPL](https://img.shields.io/github/license/alicerunsonfedora/fira)](LICENSE.txt)
![Python](https://img.shields.io/badge/python-2.7+-blue.svg)

## Requirements

- Python 2.7
- Poetry package manager
- Ren'Py

## Installing

To install Fira to a Python environment, run `pip install uvn-fira`. For environments in Ren'Py, run `pip install uvn-fira --target game/python-packages`.

## Building from Source

Clone the Fira repository and then run `poetry install` to create a Python virtual environment and install the development dependencies to.

To build the final package, run `poetry build`.

To publish the package to PyPI, run `poetry publish`.

> Note: For any scripts that rely on these functions, make sure you have your Python environment link to the Ren'Py module.

## License

The Fira package is licensed under the Mozilla Public License v2.0.
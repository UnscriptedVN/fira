# Fira
**Fira** is the main backend and API code for the minigame in [Unscripted](https://unscripted.marquiskurt.net), a visual novel about software development. Fira provides many facets of the minigame, including a public API that players can use to code solutions to the minigame puzzles, a configuration and data generator from level files, and a virtual machine that runs low-level code that the minigame processes (NadiaVM). Fira is named after Fira Sans, one of the game's characters.

## Getting started
Fira comes pre-packaged in Unscripted but can be installed outside of the game to work better with IDEs and other Python tools such as Poetry.

## Usage
For players installing this package to solve minigame puzzles, using the Fira package to access the API is relatively straightforward:

```py
from uvn_fira.api import get_level_information, CSPlayer, CSWorld

gp, gw = get_level_information(0,
                               fn_path=renpy.config.savedir + "/minigame",
                               exists=renpy.loadable,
                               load=renpy.exports.file)
```

Documentation on the API is located inside of Unscripted by going to **Help &rsaquo; Minigame** or **Settings &rsaquo; Minigame**.

The documentation for the entire package is located at [https://fira.marquiskurt.net](https://fira.marquiskurt.net), which is useful for developers that wish to make custom toolkits that connect to the minigame's virtual machine or for modders that wish to make custom minigame levels.

## Reporting bugs
Bugs and feature requests for Fira can be submitted on GitHub.

## License
The Fira package is licensed under the Mozilla Public License v2.0.
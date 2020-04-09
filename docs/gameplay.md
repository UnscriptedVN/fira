---
layout: default
title: Gameplay
nav_order: 2
---

# Gameplay
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{: toc}

In the Unscripted minigame, players are tasked with moving Masti, a mastodon, in a virtual environment, collecting coins and reaching the exit. To do so, players must successfully create the correct combination of moves and commands to execute.

![Minigame](/assets/img/hp.png)

## Gameplay Modes

There are two game modes that the minigame offers:

- **Basic mode**, where players click a series of buttons in the right order
- **Advanced mode**, where players write Python scripts that solve the puzzle

The minigame editor will change depending on what mode is used. For the basic mode, the buttons for input and virtual machine translation are present; in the advanced mode, only the world preview is present.

### Basic Mode

In the basic mode, players click a series of buttons provided on the screen that correspond to creating actions that Masti will follow. These buttons are the directional movement commands, the collect button, and the exit button.

Players also get to view what commands will be executed in the minigame's virtual machine, [NadiaVM](./implementation.html#nadiavm). This VM input view, however, does not display all of the VM commands: commands such as `alloc` and `set` are not displayed since the player cannot control these aspects in basic mode.

There are also some limitations of basic mode in the minigame:

- The basic mode does not support control flow or functions, meaning that players will need to click all of the buttons.
- When the player moves, they do _not_ automatically collect coins, meaning that players will need to explicitly tell Masti to collect the coin.
- Players cannot directly edit the virtual machine file (`.nvm`) before the game preview.

### Advanced Mode

![Advanced Mode](/assets/img/advanced.png)

In the advanced mode, players are offered the ability to solve puzzles programmatically using Python or another language that can compile NadiaVM files. The Fira package offers an official API that can be used to write the necessary code. Players do not see a VM input view or any buttons for inputting commands, but rather see the world preview.

> **Note**: The documentation regarding the APIs refer to the official APIs provided by this package. Some functions and utilities may differ in different APIs or implementations.

By default, the advanced mode is disabled; it can be enabled in **Settings &rsaquo; Minigame** by ticking "Enable advanced mode".

There are also some limitations to the official API when using Advanced Mode:

- Players should not use the `player` variable. This conflicts with the game's own player variable. As a workaround, the template files generate starter code that stores the minigame player as `game_player`.
- The Python script must end with the `exit` command. The player's exit command is also responsible for writing  the virtual machine file.
- Some aspects of the minigame may work unexpectedly. The API has been designed with some safety checks but is not a safeguard against Python's quirks.
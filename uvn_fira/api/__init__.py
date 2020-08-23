# coding=utf-8
#
# __init__.py
# Fira API
#
# Created by Marquis Kurt on 04/01/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""The `api` module contains all of the player-facing functions and classes used in the
    Advanced Mode of the Unscripted minigame.

The Unscriped Minigame Application Programming Interface (API) allows players to directly
    manipulate the player's movements and actions while traversing in the minigame world using
    Python. The minigame's logic will handle translating any commands to display at the end of the
    script compilation.

.. WARNING::
   Although most (if not all) of the submodules in the parent package are publicly accessible,
    it is heavily encouraged that players make use of the standard utilities provided with
    the API module.

   The documentation for some components in the core submodule are provided for reference namely,
    `uvn_fira.api.grid.CSWorldGrid` and `uvn_fira.api.vm.CSMinigameWriter`.

## Contents
The `api` module comes with a few submodules that contain function and utilities for multiple
    aspects of the minigame:

- `player` hosts all of the code related to manipulating the player in the minigame.
- `world` hosts all of the code related to viewing and gathering information about the world
    in the minigame.
- `grid` hosts a publicly available version of the internal grid system used for world generation.
- `info` hosts all of the utilities to start writing code for levels.

## Migrating from v1.x

The Fira API v2.x series is not exactly backwards-compatible with previous Fira API versions, nor
    is it backwards-compatible with older NadiaVM language files. The following sections provides
    tips for how to migrate code from the old Fira API version to newer versions. Namely, this will
    affect players that are migrating from the Unscripted Demo or older development builds of the
    game.

### Using `uvn_fira.api.player.CSPlayer`

The following methods are no longer available when using the `uvn_fira.api.player.CSPlayer` object.
    It is recommended to change your code to use the new methods outlined.

- `CSPlayer.exit`: Use `uvn_fira.api.player.CSPlayer.finish` instead.
- `CSPlayer.collect`: Use `uvn_fira.api.player.CSPlayer.toggle` instead.

### Using `uvn_fira.api.world.CSWorld`

The following methods and properties are no longer available when using the
    `uvn_fira.api.world.CSWorld` object. It is recommended to change your code to use the new
    methods and properties outlined.

- `CSWorld.coins`: Use `uvn_fira.api.world.CSWorld.devices` instead.

### Using `uvn_fira.api.info.get_level_information`

In older Fira API versions, `uvn_fira.api.info.get_level_information` was the function used to get
    information about a world, the player, and to write code for the player to follow. This method
    can sometimes cause unexpected results with Python's native features and could potentially
    produce broken virutal machine code.

A new class, `uvn_fira.api.info.MinigameLevel`, attempts to resolve this issue. The class provides
    direct access to the virtual machine writers and allows players to write virtual machine code
    in a clean, elegant way without the abstraction overhead from other methods.
    `uvn_fira.api.info.MinigameLevel` provides support for the `with` keyword and context manager
    in Python, allowing for clean and concise code.

```py
with MinigameLevel(1) as vm, data:
    devices = data.devices().as_list()
    vm.alloc("world_coins", len(devices))
    vm.alloc("inventory", len(devices))
    for device in devices:
        vm.set(device)
        vm.push("world_coins", devices.index(device))
```
"""
from .world import CSWorld
from .grid import CSWorldGrid
from .player import CSPlayer
from .info import MinigameLevel, get_level_information

__version__ = "2.0.0-beta1"

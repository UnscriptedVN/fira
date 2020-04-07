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
    `minigame.api.grid.CSWorldGrid`.

The `api` module comes with a few submodules that contain function and utilities for multiple
    aspects of the minigame:

- `player` hosts all of the code related to manipulating the player in the minigame.
- `world` hosts all of the code related to viewing and gathering information about the world
    in the minigame.
- `grid` hosts a publicly available version of the internal grid system used for world generation.
"""
from .world import CSWorld
from .grid import CSWorldGrid
from .player import CSPlayer
from .info import get_level_information

__version__ = "1.2.0"

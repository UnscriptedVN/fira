# coding=utf-8
#
# __init__.py
# Fira
#
# Created by Marquis Kurt on 03/31/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

"""The `uvn_fira` package contains the API and core modules for the Fira backend.

Fira is the main backend and API code for the minigame in Unscripted, a visual novel about
    software development. Fira provides many facets of the minigame, including a public API that
    players can use to code solutions to the minigame puzzles, a configuration and data generator
    from level files, and a virtual machine that runs low-level code that the minigame processes
    (NadiaVM). Fira is named after Fira Sans, one of the game's characters.
"""
from uvn_fira.api import *
from uvn_fira.core import *

__version__ = "1.3.1"

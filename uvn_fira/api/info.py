# coding=utf-8
#
# info.py
# Fira API - Info
#
# Created by Marquis Kurt on 04/04/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""The info submodule contains the utilities to get the world and player information for a given
    level."""
import renpy                            #pylint:disable=import-error
from .player import CSPlayer
from .world import CSWorld
from ..core import CSWorldConfigReader
from ..core import CSNadiaVMWriter

def get_level_information(level):
    """Create a world and player based on a game level.

    Arguments:
        level (int): The level number as indicated by the minigame.

    Returns:
        info (tuple): A tuple containing the `minigame.api.player.CSPlayer` object and the
            `minigame.api.world.CSWorld` object
    """
    w_info = CSWorldConfigReader("core/minigame/levels/level%s.toml" % (level))
    writer = CSNadiaVMWriter(renpy.config.savedir + "/minigame/compiled/lvl%s.nvm" % (level))
    world = CSWorld(from_data=w_info.data)
    player = CSPlayer(in_world=world, vm=writer)
    return player, world

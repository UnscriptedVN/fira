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

from .player import CSPlayer
from .world import CSWorld
from ..core import CSWorldConfigReader
from ..core import CSNadiaVMWriter

def get_level_information(level, fn_path="", **kwargs):
    # type: (int, str, dict) -> tuple[CSPlayer, CSWorld]
    """Create a world and player based on a game level.

    Arguments:
        level (int): The level number as indicated by the minigame.
        fn_path (str): The path to where the NadiaVM file will be written to. This excludes
            the file name itself.
        **kwargs (dict): Arbitrary keyword arguments.

    Kwargs:
        config_file (str): The path to the level configuration file, excluding the file name.
        exists (callable): The function to use, if not relying on the built-in `os` module
            to determine whether the configuration file path is loadable.
        load (callable): The function to use, if not relying on the the built-in `open`
            function to load the file object.

    Returns:
        info (tuple): A tuple containing the `minigame.api.player.CSPlayer` object and the
            `minigame.api.world.CSWorld` object
    """
    conf = kwargs["config_file"] + "/level%s.toml" % (toml) \
        if "config_file" in kwargs \
            else "core/minigame/levels/level%s.toml" % (level)
    w_info = CSWorldConfigReader(conf, **kwargs)
    writer = CSNadiaVMWriter(fn_path + "/compiled/lvl%s.nvm" % (level))
    world = CSWorld(from_data=w_info.data)
    player = CSPlayer(in_world=world, vm=writer)
    return player, world

# coding=utf-8
#
# template.py
# Fira Core - Template
#
# Created by Marquis Kurt on 04/06/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""The template module contains the utilities to create file templates for the Unscripted
    minigame code.

The template files are generated when the game starts and are replaced if none are found.
"""


def generate_template(filepath, for_level=0):
    # type: (str, int) -> None
    """Generate a template file using the Minigame APIs.

    Arguments:
        filepath (str): The path to where the template file will be written.
        for_level (int): The corresponding level for the minigame. Defaults to 0.
    """
    template = """#
# This script corresponds to the Advanced Mode script for Level %s in the minigame.
# It is recommended to keep the appropriate template code to start. Remember that the goal is to
# power on all computers in the office and reach the exit.
#
# To access the documentation for the minigame APIs, either go to Settings > Minigame and click
# "Open Documentation", go to Help > Documentation, or visit the following link in your browser:
# https://fira.marquiskurt.net/api/. Go to https://fira.marquiskurt.net/gameplay.html#limitations-1
# to view the limitations of using the official API as called here.
#
# If you want to use a third-party tool or framework instead of the official Fira API and want to
# sideload in a virtual machine file, make sure "Force Python compiler" in Settings > Minigame is
# disabled and that your tool compiles the NadiaVM file to your save directory like the following:
# /path/to/RenPy saves/dev.unscriptedvn/minigame/compiled/adv_lvl%s.nvm
#

# Import the level information APIs.
from uvn_fira.api import MinigameLevel

with MinigameLevel(
    0,
    vm_path=renpy.config.savedir + "/minigame/compiled/adv_lvl%s.nvm",
    provide_config=True,
    config_file="core/src/minigame/levels/level%s.toml",
    exists=renpy.loadable,
    load=renpy.exports.file) as (vm, lvl):
    # Write your VM commands here. The file will automatically close when exiting this block.

""" % (for_level, for_level, for_level, for_level)
    with open(filepath, 'w+') as file_obj:
        file_obj.write(template)

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
    """Generate a template file using the Minigame APIs.

    Arguments:
        filepath (str): The path to where the template file will be written.
        for_level (int): The corresponding level for the minigame. Defaults to 0.
    """
    template = """#
# This script corresponds to the Advanced Mode script for Level %s in the minigame.
# It is recommended to keep the appropriate template code to start. Remember that the goal is to
# collect all coins and reach the exit.
#
# To access the documentation for the minigame APIs, either go to Settings > Minigame
# and click "Open Documentation" or go to Help > Documentation.
#

# Import the level information APIs.
from minigame.api import get_level_information

# Get all of the information for this particular level.
game_player, game_world = get_level_information(%s)

# WRITE CODE HERE
    """ % (for_level, for_level)
    with open(filepath, 'w+') as file_obj:
        file_obj.write(template)

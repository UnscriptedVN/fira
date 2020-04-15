# coding=utf-8
#
# world.py
# Fira API - World
#
# Created by Marquis Kurt on 03/31/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""The world module contains all of the classes and functions necessary to visualize
    and gather information about the game world.

The module contains the base grid class responsible for making two-dimensional arrays
    organized like a grid easier to work with (`minigame.api.grid.CSWorldGrid`), as well as the
    world class that contains all of the world's information such as the player's position and
    coins (`CSWorld`).

## World Implementation
Worlds are organized as a grid-like, two-dimensional array (matrix) consisting of rows and columns.
    Each element in the grid contains a string that describes what the world element at that
    position in the grid is. There are five possible options:

- `"PLAYER"`, which refers to the player character
- `"WALL"`, which refers to a wall
- `"COIN"`, which refers to a collectable coin
- `"EXIT"`, which refers to an exit
- `"AIR"`, which refers to a space that doesn't have a particular item

In most scenarios, the world itself does not get modified directly since the layout of items in the
    world need to be preserved. The `CSPlayer` object in the `player` module of the API handles
    world manipulation when a world is passed into its constructor, and most scripts will make a
    copy of world information such as the number of coins and the player's starting position.

It may be impractical in some cases to access an element in the grid directly. The
    `minigame.api.grid.CSWorldGrid` class allows for the world grid to be used in a more practical
    manner by making common operations such as getting a list containing coordinates of a specific
    type of item and getting the first instance of an item easier.
"""
from ..core import CSNadiaVMWriter, CSWorldDataGenerator
from .grid import CSWorldGrid

class CSWorld(object):
    """The base class for a minigame world.

    The minigame world contains a matrix containing the elements used to generate that world,
    as well as any specific world properties like coins and exit locations.
    """
    _dimensions = (0, 0)
    _player_position = (0, 0)
    _grid = CSWorldGrid([])
    _vm_author = CSNadiaVMWriter("null.nvm")

    def __init__(self, from_data, **kwargs):
        # type: (CSWorld, CSWorldDataGenerator, dict) -> None
        """Construct a World object.

        Arguments:
            from_data (CSWorldDataGenerator): The world generator used to create the world data.
            **kwargs: Arbitrary keyword arguments.
        """

        self._grid = from_data.to_grid()
        self._dimensions = from_data.size()
        self._player_position = from_data.to_grid().first("PLAYER")

        if "nvm" in kwargs:
            self._vm_author = CSNadiaVMWriter(kwargs["nvm"])

    def player(self):
        # type: (CSWorld) -> tuple[int, int]
        """Get the player's current location in the world.

        Returns:
            position (tuple): The current coordinates of the player.
        """
        return self._player_position

    def size(self):
        # type: (CSWorld) -> tuple[int, int]
        """Get the size of the world.

        Returns:
            dimensions (tuple): A tuple containing the number of rows and columns.
        """
        return self._dimensions

    def walls(self):
        # type: (CSWorld) -> CSWorldGrid
        """Get the grid of walls in the world.

        Returns:
            walls (minigame.api.grid.CSWorldGrid): Grid containing only the walls.
        """
        return CSWorldGrid(self._grid.grid, lambda a: a == "WALL")

    def coins(self):
        # type: (CSWorld) -> CSWorldGrid
        """Get the grid of coins in the world.

        Returns:
            coins (minigame.api.grid.CSWorldGrid): Grid containing only the coins.
        """
        return CSWorldGrid(self._grid.grid, lambda a: a == "COIN")

    def exit(self):
        # type: (CSWorld) -> any
        """Get the location of the exit.

        Returns:
            exit (tuple): A tuple containing the coordinates of the exit.
        """
        return self._grid.first("EXIT")

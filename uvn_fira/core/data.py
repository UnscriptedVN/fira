# coding=utf-8
#
# data.py
# Fira Core - Data
#
# Created by Marquis Kurt on 04/02/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""This submodule contains the world data generator code for the configuration system."""

from .grid import CSGrid

class CSWorldDataGenerateError(Exception):
    """Could not generate the world data."""

class CSWorldDataGenerator(object):
    """The base class for the world data generator for world maps.

    The world data generator reads the given input string and returns a grid-like two-dimensional
        array for use with world manipulation or storage.
    """

    _str = ""
    _data = []
    _dimensions = 0, 0

    def __init__(self, data=""):
        # type: (CSWorldDataGenerator, str) -> None
        """Construct the world data generator.

        Arguments:
            data: The string containing the world's data to parse. Defaults to an empty string.
        """
        self._str = data

        total_rows = total_columns = 0
        current_column = 0
        current_row = []
        world_matrix = []
        did_set_player = False
        did_set_exit = False
        player_position = 0, 0

        world_map_terrain = {
            "%": "WALL",
            "P": "PLAYER",
            "E": "EXIT",
            ".": "COIN"
        }

        for line in data:
            if line == "\n":
                world_matrix.append(current_row[:])
                current_column = 0
                total_rows += 1
                current_row = []
            else:
                current_tile = world_map_terrain.get(line, "AIR")
                current_row.append(current_tile)

                if current_tile == "EXIT":
                    if did_set_exit:
                        raise CSWorldDataGenerateError("Cannot instantiate more than one exit.")

                if current_tile == "PLAYER":
                    if did_set_player:
                        raise CSWorldDataGenerateError("Cannot instantiate more than one player \
                                                    at coordinates %s and %s."
                                                       % (player_position,
                                                          (total_rows, current_column)))

                    self._player_position = len(world_matrix), current_column - 1

                if total_rows == 0:
                    total_columns += 1
                current_column += 1

        self._data = world_matrix
        self._dimensions = total_rows, total_columns

    def __str__(self):
        return ("Dimensions: %s\nMap\n=====\n" + self._str) % (self._dimensions)

    def size(self):
        # type: (CSWorldDataGenerator) -> tuple[int, int]
        """Get the size of the given world data grid.

        Returns:
            A tuple containing the number of rows and columns in the grid.
        """
        return self._dimensions

    def to_grid(self):
        # type: (CSWorldDataGenerator) -> CSGrid
        """Get the world data as a world grid.

        Returns:
            A world grid containing the world data.
        """
        return CSGrid(self._data, grid_filter=None)

    def coins(self):
        # type: (CSWorldDataGenerator) -> CSGrid
        """Get the world coin data.

        Returns:
            grid (CSGrid): The world grid containing the coins.
        """
        return CSGrid(self._data, grid_filter=lambda x: x == "COIN")

    def walls(self):
        # type: (CSWorldDataGenerator) -> CSGrid
        """Get the world wall data.

        Returns:
            grid (CSGrid): The world grid containing the walls.
        """
        return CSGrid(self._data, grid_filter=lambda x: x == "WALL")

# coding=utf-8
#
# grid.py
# Fira Core - Grid
#
# Created by Marquis Kurt on 04/04/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""This submodule contains the grid data type used in the minigame world."""
from typing import Optional, Callable

class CSGrid(object):
    """A class representation of a grid.

    The grid is a two-dimensional array object that contains elements at given positions. This
        class contains methods that allow easy access to the contents of the grid without needing
        to access the grid directly.

    Attributes:
        grid (list): The two-dimensional array containing items at given positions,
            organized by row and column.

    """
    grid = []

    def __init__(self, grid, grid_filter=None):
        # type: (CSGrid, list, Optional[Callable[[any], any]]) -> None
        """Construct a grid.

        If a filter is supplied with the grid, the grid will filter for the items specified in the
            filter expression, marking those that don't match the filter as None.

        Arguments:
            grid (list): The two-dimensional array representing the grid.
            grid_filter (callable): A function that determines what items in the grid to keep.
                Defaults to None, indicating that no filter is applied.
        """
        temp_grid = []
        if callable(grid_filter):
            for row in grid:
                temp_grid.append([x if grid_filter(x) else None for x in row])
        else:
            temp_grid = grid[:]
        self.grid = temp_grid

    def __str__(self):
        data = ""
        for row in self.grid:
            data += str(row).replace("[", "").replace("]", "").replace(",", "\t") + "\n"
        return data

    def __eq__(self, value):
        return isinstance(value, CSGrid) and self.grid == value.grid

    def __ne__(self, value):
        return not self.__eq__(value)

    def shape(self):
        # type: (CSGrid) -> tuple[int, int]
        """Get the shape of the grid.

        Returns:
            shape (tuple): A tuple containig the total rows and columns of this grid.
        """
        rows = len(self.grid)
        columns = len(self.grid[0])
        return rows, columns

    def as_list(self):
        # type: (CSGrid) -> list[any]
        """Convert the grid to a list of coordinates containing a non-void item.

        .. NOTE::
           If a filter was applied to the grid at construction, it will only select items
           that are not `None`.

        Returns:
            coordinates (list): A list of tuples containing the coordinates to valid items in the
                grid.
        """
        coordinates = []
        for row in range(len(self.grid) - 1):
            for column in range(len(self.grid[0]) - 1):
                if self.grid[row][column] is not None:
                    coordinates.append((row, column))
        return coordinates

    def first(self, of=""):     #pylint:disable=invalid-name
        # type: (CSGrid, str) -> tuple[int, int]
        """Get the first instance of an item in the grid.

        Arguments:
            of (str): The item to look for the first instance of in this grid.

        Returns:
            coords (tuple): A tuple containing the row and column coordinates of the first item. If
                the item was not found, the tuple `-1, -1` is returned.
        """
        coords = (-1, -1)

        for row in range(len(self.grid) - 1):
            for column in range(len(self.grid[0]) - 1):
                if self.grid[row][column] == of:
                    coords = row, column
                    break
        return coords

    def last(self, of=""):      #pylint:disable=invalid-name
        # type: (CSGrid, str) -> tuple[int, int]
        """Get the last instance of an item in the grid.

        Arguments:
            of (str): The item to look for the last instance of in this grid.

        Returns:
            coords (tuple): A tuple containing the row and column coordinates of the last item. If
                the item was not found, the tuple `-1, -1` is returned.
        """
        inverse = [row[::-1] for row in self.grid][::-1]
        coords = -1, -1

        for row in range(len(inverse) - 1):
            for column in range(len(self.grid[0]) - 1):
                if inverse[row][column] == of:
                    coords = row, column
                    break

        return coords

    def element_at(self, row, column):
        # type: (CSGrid, int, int) -> Any
        """Get the element at a specified position.

        Arguments:
            row (int): The row that the element is located in
            column (int): The column that the element is located in

        Returns:
            element (str): The element at the specified position in the grid.
        """
        return self.grid[row][column]

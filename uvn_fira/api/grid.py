# coding=utf-8
#
# grid.py
# Fira API - Grid
#
# Created by Marquis Kurt on 04/04/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""The grid submodule contains a public-facing version of the internal grid used in the Unscripted
    minigame core.

The world grid is a two-dimensional array (list of lists) that contain strings that determine what
    element is present at the specific row and column. The main class responsible for working with
    the grid, `CSWorldGrid`, is a clean and lightweight implementation of this grid with multiple
    utilities to manage it. The grid implementation is not dependent on the `numpy` library and is
    geared towards accessing elements and other information, rather than mathematical operations.
"""
from typing import Callable, Optional

from ..core import CSGrid

# To expose the documentation for the grid without exposing the core, a subclassed version is
# created here. pdoc will automatically use the documentation based on class inheritance rules.

class CSWorldGrid(CSGrid):      #pylint:disable=missing-class-docstring

    def __init__(self, grid, filter=None):  #pylint:disable=redefined-builtin
        # type: (CSWorldGrid, list, Optional[Callable[[any], any]]) -> None
        CSGrid.__init__(self, grid, filter)

    def __str__(self):
        return CSGrid.__str__(self)

    def __eq__(self, value):
        return CSGrid.__eq__(self, value)

    def __ne__(self, value):
        return CSGrid.__ne__(self, value)

    def shape(self):
        # type: (CSWorldGrid) -> tuple[int, int]
        return CSGrid.shape(self)

    def as_list(self):
        # type: (CSWorldGrid) -> list[any]
        return CSGrid.as_list(self)

    def first(self, of=""):
        # type: (CSWorldGrid, str) -> any
        return CSGrid.first(self, of)

    def last(self, of=""):
        # type: (CSWorldGrid, str) -> any
        return CSGrid.last(self, of)

    def element_at(self, row, column):
        # type: (CSWorldGrid, int, int) -> any
        return CSGrid.element_at(self, row, column)

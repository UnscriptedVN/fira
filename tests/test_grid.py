# coding:utf-8
#
# test_grid.py
# Unscripted Fira
#
# Created by Marquis Kurt on 05/12/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from uvn_fira import core as cr

DUMMY_DATA = """%%%%%
%P.E%
%%%%%
"""


def test_data_load():
    """Test that the data for the dummy level properly loads."""
    data = cr.CSWorldDataGenerator(DUMMY_DATA)
    assert isinstance(data, cr.CSWorldDataGenerator)


def test_data_size():
    """Test that the data can successfully grab the shape of the world."""
    data = cr.CSWorldDataGenerator(DUMMY_DATA)
    assert data.size() == (3, 5)


def test_data_grid():
    """Test that the data can successfully return a grid."""
    data = cr.CSWorldDataGenerator(DUMMY_DATA)
    assert isinstance(data.to_grid(), cr.CSGrid)


def test_data_grid_walls():
    """Test that the data successfully captures all of the walls."""
    data = cr.CSWorldDataGenerator(DUMMY_DATA).walls().as_list()
    assert len(data) == 12


def test_data_grid_devices():
    """Test that the data successfully captures all of the devices."""
    data = cr.CSWorldDataGenerator(DUMMY_DATA).devices().as_list()
    assert len(data) == 1


def test_data_grid_locate_player():
    """Test that the data can successfully get the player's location."""
    grid = cr.CSWorldDataGenerator(DUMMY_DATA).to_grid()
    assert grid.first('PLAYER') == (1, 1) or grid.element_at(1, 1) == "PLAYER"


def test_data_grid_locate_error():
    """Test that the data will return bad values if it cannot locate something in the grid."""
    grid = cr.CSWorldDataGenerator(DUMMY_DATA).to_grid()
    assert grid.first("HORSE") == (-1, -1)

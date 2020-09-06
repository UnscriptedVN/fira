# coding=utf-8
#
# player.py
# Fira API - Player
#
# Created by Marquis Kurt on 03/31/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""The player module contains the functions and classes necessary to manipulate players in
    a minigame world.

The module contains a class that lets players control the behavior of their minigame counterpart
    by moving in a given direction, powering on a device, etc. (`CSPlayer`). To prevent accidental
    manipulation of the original world data, the player class uses its own position property to
    update its location.
"""
from typing import Tuple, Optional, List
from .world import CSWorld
from ..core import CSNadiaVMWriter


class CSPlayer(object):
    """The base class for a player in the minigame world.

    The player object contains methods for manipulating the current player's
        position and inventory system.
    """
    _position = (0, 0)  # type: Tuple[int, int]
    _inventory = []  # type: List[Tuple[int, int]]
    _world = None  # type: Optional[CSWorld]
    _world_coins = []  # type: List[Optional[Tuple[int, int]]]
    _world_devices = 0
    _current_device_count = 0
    _vm = None  # type: Optional[CSNadiaVMWriter]

    def __init__(self, in_world, **kwargs):
        # type: (CSWorld, dict) -> None
        """Construct the Player object.

        Arguments:
            in_world (uvn_fira.api.world.CSWorld): The world the player is located in.
            **kwargs (dict): Arbitrary keyword arguments.

        Kwargs:
            at_position (tuple): The position the player should be placed in. Defaults to the player
                position in the world (`uvn_fira.api.world.CSWorld.player`).
            with_inv (list): A list containing items that the player will have to start. Defaults to
                an empty list.
            vm (CSNadiaVMWriter): The virtual machine writer, if available.
        """
        if not isinstance(in_world, CSWorld):
            raise TypeError("Expected a minigame world type but received %s instead."
                            % (type(in_world)))
        self._world = in_world
        self._world_coins = self._world.devices().as_list()[:]

        self._world_devices = len(self._world.devices().as_list()[:])

        self._position = kwargs['at_position'] if "at_position" in kwargs else self._world.player(
        )
        self._inventory = kwargs['with_inv'] if "with_inv" in kwargs else []
        self._current_device_count = len(
            kwargs["with_inv"]) if "with_inv" in kwargs else 0

        if "vm" in kwargs:
            self._vm = kwargs["vm"]
            self._vm.alloc("world_coins", len(self._world_coins))
            self._vm.alloc("inventory", len(self._world_coins))

            for coin in self._world_coins:
                self._vm.set(coin)
                self._vm.push("world_coins", self._world_coins.index(coin))

    def location(self):
        # type: () -> Tuple[int, int]
        """Get the player's current position.

        Returns:
            position (tuple): The current coordinates of the player.
        """
        return self._position

    def origin(self):
        # type: () -> Tuple[int, int]
        """Get the original starting position of the player.

        Returns:
            origin (tuple): The coordinates of the player's original position.
        """
        return self._world.player()

    def capacity(self):
        # type: () -> int
        """Get the the count of how many devices the player has turned on.

        Returns:
            count (int): The number of devices that powered on.
        """
        return self._current_device_count

    def blocked(self):
        # type: () -> bool
        """Determine whether a player is blocked at a given position.

        Returns:
            blocked (bool): True if any walls are near the player (1-block radius).
        """
        px, py = self._position  # pylint:disable=invalid-name

        positions = [(px-1, py), (px+1, py), (px, py-1), (px, py+1)]

        for position in positions:
            if position in self._world.walls().as_list():
                return True
        return False

    def move(self, direction):
        # type: (str) -> 'CSPlayer'
        """Move the player in a direction, if the direction results in the player
            being able to move into a non-walled area.

        Arguments:
            direction (str): The direction the player should move in. Acceptable directions
                are `"north"`, `"south"`, `"east"`, and `"west"`.

        Returns:
            player (CSPlayer): The Player that committed the move action. This is useful in cases
                where chaining methods is preferred.
        """
        transforms = {
            "north": (-1, 0),
            "south": (1, 0),
            "west": (0, -1),
            "east": (0, 1)
        }

        trans_x, trans_y = transforms.get(direction, "east")
        curr_x, curr_y = self._position
        new_x, new_y = curr_x + trans_x, curr_y + trans_y

        if (new_x, new_y) not in self._world.walls().as_list():
            self._position = new_x, new_y

        if self._vm:
            self._vm.move(direction)

        return self

    def _manage_collected_state(self):
        # type: () -> 'CSPlayer'
        """Manage the device collection state and determine whether to increase the powered on
        device count.

        If the device is already on or there isn't a device there, nothing occurs.

        Returns:
            player (CSPlayer): The Player object that committed the collect action. This is useful
                in cases where chaining methods is preferred.
        """
        item_index = self._world_coins.index(self._position)
        self._inventory.append(self._position)

        if self._position in self._world_coins and self._position not in self._inventory:
            self._current_device_count += 1

        if self._vm:
            self._vm.pop("world_coins", item_index)
            self._vm.push("inventory", item_index)
            self._vm.collect()

        self._world_coins[item_index] = None
        return self

    def toggle(self):
        # type: () -> 'CSPlayer'
        """Turn a nearby computer on or off.

        .. versionadded:: 2.0.0-beta1

        If there isn't a device to turn on, nothing occurs.

        Returns:
            player (CSPlayer): The Player object that committed the collect action. This is useful
                in cases where chaining methods is preferred.
        """
        return self._manage_collected_state()

    def finish(self):
        # type: () -> None
        """Finish all instructions and compile the VM code."""
        if self._vm and isinstance(self._vm, CSNadiaVMWriter):
            self._vm.exit()
            self._vm.write()

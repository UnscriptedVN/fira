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
    by moving in a given direction, collecting an item, etc. (`CSPlayer`). To prevent accidental
    manipulation of the original world data, the player class uses its own position property to
    update its location.
"""
from .world import CSWorld
from ..core import CSNadiaVMWriter

class CSPlayer(object):
    """The base class for a player in the minigame world.

    The player object contains methods for manipulating the current player's
        position and inventory system.
    """
    _position = (0, 0)
    _inventory = []
    _world = None
    _world_coins = []
    _vm = None

    def __init__(self, in_world, **kwargs):
        # type: (CSPlayer, CSWorld, dict) -> None
        """Construct the Player object.

        Arguments:
            in_world (minigame.api.world.CSWorld): The world the player is located in.
            **kwargs (dict): Arbitrary keyword arguments.

        Kwargs:
            at_position (tuple): The position the player should be placed in. Defaults to the player
                position in the world (`minigame.api.world.CSWorld.player`).
            with_inv (list): A list containing items that the player will have to start. Defaults to
                an empty list.
            vm: The virtual machine writer, if available.
        """
        if not isinstance(in_world, CSWorld):
            raise TypeError("Expected a minigame world type but received %s instead."
                            % (type(in_world)))
        self._world = in_world
        self._world_coins = self._world.coins().as_list()[:]

        self._position = kwargs['at_position'] if "at_position" in kwargs else self._world.player()
        self._inventory = kwargs['with_inv'] if "with_inv" in kwargs else []

        if "vm" in kwargs:
            self._vm = kwargs["vm"]
            self._vm.alloc("world_coins", len(self._world_coins))
            self._vm.alloc("inventory", len(self._world_coins))

            for coin in self._world_coins:
                self._vm.set(coin)
                self._vm.push("world_coins", self._world_coins.index(coin))

    def location(self):
        # type: (CSPlayer) -> tuple[int, int]
        """Get the player's current position.

        Returns:
            position (tuple): The current coordinates of the player.
        """
        return self._position

    def origin(self):
        # type: (CSPlayer) -> tuple[int, int]
        """Get the original starting position of the player.

        Returns:
            origin (tuple): The coordinates of the player's original position.
        """
        return self._world.player()

    def capacity(self):
        # type: (CSPlayer) -> int
        """Get the the count of how many items the player has.

        Returns:
            count (int): The number of items in the inventory.
        """
        return len(self._inventory)

    def blocked(self):
        # type: (CSPlayer) -> bool
        """Determine whether a player is blocked at a given position.

        Returns:
            blocked (bool): True if any walls are near the player (1-block radius).
        """
        px, py = self._position #pylint:disable=invalid-name

        positions = [(px-1, py), (px+1, py), (px, py-1), (px, py+1)]

        for position in positions:
            if position in self._world.walls().as_list():
                return True
        return False

    def move(self, direction):
        # type: (CSPlayer, str) -> CSPlayer
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

    def collect(self):
        # type: (CSPlayer) -> CSPlayer
        """Add an item into the player's inventory at the player's current position.

        If the item does not exist in the world, or the player already has the item in question,
            nothing occurs.

        Returns:
            player (CSPlayer): The Player object that committed the collect action. This is useful
                in cases where chaining methods is preferred.
        """
        item_index = self._world_coins.index(self._position)
        self._inventory.append(self._position)

        if self._vm:
            self._vm.pop("world_coins", item_index)
            self._vm.push("inventory", item_index)
            self._vm.collect()

        self._world_coins[item_index] = None
        return self

    def exit(self):
        # type: (CSPlayer) -> None
        """Exit the level, if possible.

        If a VM is specified, the VM writer will also close the writer by writing to the VM file.
        """
        if self._vm:
            self._vm.exit()
            self._vm.write()

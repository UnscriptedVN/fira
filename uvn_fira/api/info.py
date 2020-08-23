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
from os import path
import warnings
from .player import CSPlayer
from .world import CSWorld
from .vm import CSMinigameWriter
from ..core import CSWorldConfigReader


def get_level_information(level, fn_path="", **kwargs):
    # type: (int, str, dict) -> tuple[CSPlayer, CSWorld]
    """Create a world and player based on a game level.

    .. WARNING::
        This function may no longer be supported in future releases of the Fira API and may cause
            unexpected results. It is recommended to use `MinigameLevel` instead of this function
            when possible.

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
        info (tuple): A tuple containing the `uvn_fira.api.player.CSPlayer` object and the
            `uvn_fira.api.world.CSWorld` object
    """
    warnings.warn(
        "get_level_information may not be supported in future releases of the Fira API."
        + " Using MinigameLevel is recommended instead.",
        FutureWarning)
    conf = path.join("core", "src", "minigame",
                     "levels", "level%s.toml" % (level))
    if "config" in kwargs:
        conf = kwargs["config"]
    w_info = CSWorldConfigReader(conf, **kwargs)
    writer = CSMinigameWriter(
        path.join(fn_path, "compiled", ("adv_lvl%s.nvm" % (level))))
    world = CSWorld(from_data=w_info.data)
    player = CSPlayer(in_world=world, vm=writer)
    return player, world


class MinigameLevel():
    """A class representation of a minigame level.

    .. versionadded:: 2.0.0-beta1

    This class is designed to be used with the `with` argument as a means to directly write virtual
        machine code without any abstraction involved.

    When used in a context with the `with` statement, the minigame level class may also return the
        configuration data for the level. This can be used to programmatically determine what needs
        to be written as VM code.

    Example:
    ```python
    with MinigameLevel(1) as vm, data:
        devices = data.devices().as_list()
        vm.alloc("world_coins", devices)
        vm.alloc("inventory", devices)
        for device in devices:
            vm.set(device)
            vm.push("world_coins", devices.index(device))
    ```
    """
    _level_number = 0
    _writer = CSMinigameWriter("local.nvm")
    _do_config = False
    _config_path = ""

    def __init__(self, level, vm_path, provide_config=False, **kwargs):
        # type: (MinigameLevel, int, str, bool, dict) -> None
        """Initialize a minigame level reader.

        Args:
            level (int): The level number to read.
            vm_path (str): The path to the compiled NadiaVM file to write.
            provide_config (bool): Whether to include the configuration file while accessing the
                writer. Defaults to False.
            **kwargs (dict): Arbitrary keyword arguments.

        Kwargs:
            config_file (str): The path to the level configuration file, excluding the file name.
            exists (callable): The function to use, if not relying on the built-in `os` module
                to determine whether the configuration file path is loadable.
            load (callable): The function to use, if not relying on the the built-in `open`
                function to load the file object.
        """
        self._level_number = level
        self._writer = CSMinigameWriter(vm_path)
        self._do_config = provide_config
        self._config_path = path.join(
            "core", "src", "minigame", "levels", "level%s.toml" % (self._level_number))

        if "config_file" in kwargs:
            self._config_path = kwargs["config_file"]

        self._config_reader = CSWorldConfigReader(self._config_path, **kwargs)

    def __enter__(self):
        # type: (MinigameLevel) -> Tuple[CSNadiaVMWriter, CSWorldConfigReader | None]
        """Enter the file context for the minigame level reader."""
        return self.startfile()

    def __exit__(self, type, value, traceback):
        """Write the VM file and exit the VM context."""
        self.close()

    def startfile(self):
        # type: (MinigameLevel) -> Tuple[CSNadiaVMWriter, CSWorldConfigReader | None]
        """Start the writing process.

        Returns:
            data (tuple): A tuple that contains the virtual machine writer 
                (`uvn_fira.api.vm.CSMinigameWriter`) and the game data (`CSWorldData`).
        """
        return self._writer, (self._config_reader.data if self._do_config else None)

    def close(self):
        """Write the contents of the virtual machine code to the requested file."""
        self._writer.write()

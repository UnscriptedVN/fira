# coding=utf-8
#
# config.py
# Fira Core - Config
#
# Created by Marquis Kurt on 04/01/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""This submodule contains the configuration system for reading worlds."""

from enum import Enum
from typing import List, Callable
import os
import warnings
import toml
from .data import CSWorldDataGenerator


class CSWorldConfigGenerateError(Exception):
    """Could not generate the world from the requested file or configuration."""


class CSWorldConfigCheckType(Enum):
    """An enumeration that describes the different kinds of checks in a given map."""
    power_on_all_devices = "player-powers-all-devices"
    arrives_at_exit = "player-at-exit"


class CSWorldConfigBugType(Enum):
    """An enumeration that describes the different intentional bugs a given map will use."""
    missing_bindings = "missing-poweron-bind"
    skip_collisions = "collision-checks-fail"
    random_exit = "exit-changes-randomly"


class CSWorldConfigReader(object):
    """The world configuration reader.

    The world configuration reader parses a TOML file and creates an object that stores information
        about the world that can be used to generate a map.

    Attributes:
        title: The title of the map.
        checks: A list containing the requirements for completing the puzzle.
        data: A `CSWorldDataGenerator` containing the world fata from the generated map that
            can be used to generate a world.
    """

    _world_str = """"""

    title = ""
    checks = []  # type: List[CSWorldConfigCheckType]
    bugs = []   # type: List[CSWorldConfigBugType]
    _allowed = []   # type: List[str]
    data = CSWorldDataGenerator("")

    @property
    def allowed(self):
        # type: () -> List[str]
        """A list containing the allowed blocks for a given world.

        Unnecessary if using Advanced Mode.
        """
        warnings.warn(DeprecationWarning(
            "Checking what code blocks are allowed will be removed in a future release."))
        return self._allowed

    def __init__(self, filepath="", **kwargs):
        # type: (str, dict) -> None
        """Construct the configuration reader.

        .. WARNING::
        World configurations will no longer include a key for what "code blocks" will be allowed.

        Arguments:
            filepath: The path to the configuration file to generate the world from. Defaults to
                an empty string.
            **kwargs: Arbitrary keyword arguments.

        Kwargs:
            title (str): The title of the map.
            checks (list): A list containing the checks for this particular level.
            bugs (list): A list containing the bugs for this particular level.
            allowed (list): A list containing the allowed blocks in basic mode.
            world (str): A string representation of the world layout.
            exists (callable): The function to use, if not relying on the built-in `os` module
                to determine whether the configuration file path is loadable.
            load (callable): The function to use, if not relying on the the built-in `open`
                function to load the file object.
        """
        config = {}

        if not filepath and not kwargs:
            raise CSWorldConfigGenerateError(
                "Cannot generate an empty configuration.")

        if filepath:

            exists_fn = os.path.isfile

            def default_load_fn(file):
                return open(file, 'r')

            load_fn = default_load_fn

            if "exists" in kwargs and callable(kwargs["exists"]):
                exists_fn = kwargs["exists"]  # type: Callable[[str]]

            if not exists_fn(filepath):
                raise IOError(
                    "Config file is inaccessible or doesn't exist: %s" % (filepath))

            if "load" in kwargs and callable(kwargs["load"]):
                load_fn = kwargs["load"]  # type: Callable[[str]]

            with load_fn(filepath) as file_object:
                config = toml.load(file_object)

            if "level" not in config:
                raise CSWorldConfigGenerateError(
                    "Missing key 'level' in config.")

            current_level = config["level"]

            if "map" not in current_level and "config" not in current_level:
                raise CSWorldConfigGenerateError(
                    "Missing configuration details.")

            lvl_config = current_level["config"]
            lvl_map = current_level["map"]

            self.title = lvl_config["name"]

            if "allowed_blocks" in lvl_config:
                warnings.warn(DeprecationWarning(
                    "Checking what code blocks are allowed will be removed in a future release."))
                self._allowed = lvl_config["allowed_blocks"]

            self._world_str = lvl_map["layout"]
            self.checks = [CSWorldConfigCheckType(c)
                           for c in lvl_config["check"]]

            if "bug" in lvl_config:
                self.bugs = [CSWorldConfigBugType(
                    c) for c in lvl_config["bug"]]

        if "title" in kwargs:
            self.title = kwargs["title"]

        if "checks" in kwargs:
            self.checks = kwargs["checks"]

        if "bugs" in kwargs:
            self.bugs = kwargs["bugs"]

        if "allowed" in kwargs:
            warnings.warn(DeprecationWarning(
                "Checking what code blocks are allowed will be removed in a future release."))
            self._allowed = kwargs["allowed"]

        if "world" in kwargs:
            self._world_str = kwargs["world"]

        self.data = CSWorldDataGenerator(str(self._world_str))

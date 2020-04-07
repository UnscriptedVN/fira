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

import toml
import renpy                                #pylint:disable=import-error
from .data import CSWorldDataGenerator

class CSWorldConfigGenerateError(Exception):
    """Could not generate the world from the requested file or configuration."""

class CSWorldConfigReader(object):
    """The world configuration reader.

    The world configuration reader parses a TOML file and creates an object that stores information
        about the world that can be used to generate a map.

    Attributes:
        title: The title of the map.
        checks: A list of strings containing the requirements for completing the puzzle.
        allowed: A list containing the allowed blocks for a given world. Unnecessary if using
            Advanced Mode.
        data: A `CSWorldDataGenerator` containing the world fata from the generated map that
            can be used to generate a world.
    """

    _world_str = """"""

    title = ""
    checks = []
    allowed = []
    data = CSWorldDataGenerator("")

    def __init__(self, filepath="", **kwargs):
        """Construct the configuration reader.

        Arguments:
            filepath: The path to the configuration file to generate the world from. Defaults to
                an empty string.
            **kwargs: List of keyword arguments to define the configuration (or override file
                configuration properties).
        """
        config = {}

        if not filepath and not kwargs:
            raise CSWorldConfigGenerateError("Cannot generate an empty configuration.")

        if filepath:
            if not renpy.loader.loadable(filepath):
                raise IOError("Cannot locate file %s" % (filepath))

            with renpy.exports.file(filepath) as file_object:
                config = toml.load(file_object)

            if "level" not in config:
                raise CSWorldConfigGenerateError("Missing key 'level' in config.")

            current_level = config["level"]

            if "map" not in current_level and "config" not in current_level:
                raise CSWorldConfigGenerateError("Missing configuration details.")

            lvl_config = current_level["config"]
            lvl_map = current_level["map"]

            self.title = lvl_config["name"]
            self.checks = lvl_config["check"]
            self.allowed = lvl_config["allowed_blocks"]
            self._world_str = lvl_map["layout"]

        if "title" in kwargs:
            self.title = kwargs["title"]

        if "checks" in kwargs:
            self.checks = kwargs["checks"]

        if "allowed" in kwargs:
            self.allowed = kwargs["allowed"]

        if "world" in kwargs:
            self._world_str = kwargs["world"]

        self.data = CSWorldDataGenerator(self._world_str)

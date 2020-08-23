# coding=utf-8
#
# __init__.py
# Fira
#
# Created by Marquis Kurt on 03/31/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

"""The `uvn_fira` package contains the API and core modules for the Fira backend.

Fira is the backend for the minigame in Unscripted. Fira includes a user-facing API to solve puzzles
    using Python code, and it provides the utilities and classes necessary to parse and execute
    virtual machine code for the Nadia virtual machine.

## What this package includes
The `api` submodule contains the API utilities players can use to generate code for the virtual
    machine to execute and solve puzzles. Documentation is provided in copies of Unscripted.

The `core` submodule contains the backend utilities such as the virtual machine language processor,
    virtual machine readers and writers, and world configuration utilities.
"""
from uvn_fira.api import *
from uvn_fira.core import *

__version__ = "2.0.0-beta1"

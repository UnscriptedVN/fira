# coding=utf-8
#
# vm.py
# Fira API - VM Authoring Tools
#
# Created by Marquis Kurt on 08/02/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""The `vm` submodule contains a public-facing version of the virtual machine author from the Core.

The VM writer is often used when using the `uvn_fira.api.info.MinigameLevel` class to quickly write
    virtual machine code in a low-level environment. The writer is an implementation for NadiaVM
    and is supported in the basic and advanced modes of the game.

## About NadiaVM

NadiaVM is a simple, stack-based virtual machine with a couple of commands. The VM is designed to focus specifically on the minigame’s internal game logic and is not necessarily suitable for general use. NadiaVM files are registered with the file extension .nvm and are typically plain text files with the corresponding instructions.

### Virtual Machine Commands
In the NadiaVM, there are several commands that players can use:

- `alloc (str) (int)`: Create a new array with a name and a specific size.
- `collect`: Collect a coin in the world. Acts like a pause in VM.
- `push (str) (int)`: Push the top of the stack to the given array at the index.
- `pop (str) (int)`: Pop the item located at the array's index and move it to the
    top of the stack.
- `set constant (any)`: Set the top of the stack to a constant value.
- `move player (str)`: Move the player in a given direction.
- `bind (str) (command)`: Makes an alias of the command to the assigned string.
- `cast (str) (any)`: Cast the value to the given name. If a value is already cast to the name, the
    new value will be used instead of the old one.
- `exit player`: Try to end the execution script and finish the level.
- `add`: Add the two topmost values on the stack.
- `sub`: Subtract the two topmost values on the stack.
- `mult`: Multiply the two topmost values on the stack.
- `div`: Divide the two topmost values on the stack.
- `neg`: Negate the topmost value on the stack. Effectively the same as pushing `-1` on the stack
    and calling `mult`.

The VM writer presented here provides abstracted versions of these commands that will be written to
    the requested path.
"""
from typing import Any
from ..core import CSNadiaVMWriter

# To expose the documentation for the grid without exposing the core, a subclassed version is
# created here. pdoc will automatically use the documentation based on class inheritance rules.


class CSMinigameWriter(CSNadiaVMWriter):
    """A list-based implementation of the NadiaVM file writer.

    .. versionadded:: 2.0.0-beta1

    This class is similar to CSNadaVMWriter and contains the same methods; however,
        CSNadiaVMWriterBuilder uses a list to store its code rather the string that CSNadiaVMWriter
        uses. This is useful in instances where the builder needs to remove pieces of code or work
        with the current set of instructions as a list.

    Attributes:
        instructions (list): The list of VM commands to write to the VM file.
    """

    def __init__(self, path):
        # type: (CSNadiaVMWriter, str) -> None
        CSNadiaVMWriter.__init__(self, path)

    def alloc(self, array_name, size=1):
        # type: (CSNadiaVMWriter, str, int) -> None
        CSNadiaVMWriter.alloc(self, array_name, size)

    def push(self, array, index):
        # type: (CSNadiaVMWriter, str, int) -> None
        CSNadiaVMWriter.push(self, array, index)

    def pop(self, array, index):
        # type: (CSNadiaVMWriter, str, int) -> None
        CSNadiaVMWriter.pop(self, array, index)

    def set(self, value):
        # type: (CSNadiaVMWriter, Any) -> None
        CSNadiaVMWriter.set(self, value)

    def move(self, direction):
        # type: (CSNadiaVMWriter, str) -> None
        CSNadiaVMWriter.move(self, direction)

    def bind(self, name, command):
        # type: (CSNadiaVMWriter, str, str) -> None
        CSNadiaVMWriter.bind(self, name, command)

    def cast(self, name, value):
        # type: (CSNadiaVMWriter, str, Any) -> None
        CSNadiaVMWriter.cast(self, name, value)

    def collect(self):
        # type: (CSNadiaVMWriter) -> None
        CSNadiaVMWriter.collect(self)

    def exit(self):
        # type: (CSNadiaVMWriter) -> None
        CSNadiaVMWriter.exit(self)

    def add(self):
        # type: (CSNadiaVMWriter) -> None
        CSNadiaVMWriter.add(self)

    def sub(self):
        # type: (CSNadiaVMWriter) -> None
        CSNadiaVMWriter.sub(self)

    def mult(self):
        # type: (CSNadiaVMWriter) -> None
        CSNadiaVMWriter.mult(self)

    def div(self):
        # type: (CSNadiaVMWriter) -> None
        CSNadiaVMWriter.div(self)

    def neg(self):
        # type: (CSNadiaVMWriter) -> None
        CSNadiaVMWriter.neg(self)

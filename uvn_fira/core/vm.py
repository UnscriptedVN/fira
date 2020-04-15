# coding=utf-8
#
# vm.py
# Fira Core - VM
#
# Created by Marquis Kurt on 04/03/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""This submodule contains the low-level virtual machine reader for the minigame
code.

## Implementation

The Unscripted API and the minigame GUI eventually write files readable by the
Nadia Virtual Machine (NVM). The Nadia Virtual Machine is a stack-based virtual
machine designed to perform operations specific to the Unscripted minigame.

### Commands
In the NadiaVM, there are several commands:

- `alloc (str) (int)`: Create a new array with a name and a specific size.
- `collect`: Collect a coin in the world. Acts like a pause in VM.
- `push (str) (int)`: Push the top of the stack to the given array at the index.
- `pop (str) (int)`: Pop the item located at the array's index and move it to the
    top of the stack.
- `set constant (any)`: Set the top of the stack to a constant value.
- `move player (str)`: Move the player in a given direction.
- `exit player`: Try to end the execution script and finish the level.
"""
from typing import Optional


class CSNadiaVMCommandNotFoundError(Exception):
    """VM command not found."""

class CSNadiaVM(object):
    """An implementation of the NadiaVM stack."""

    _instructions = []
    _stack = []

    def __init__(self, path, pl):
        # type: (CSNadiaVM, str, tuple[int, int]) -> None
        """Construct the VM reader.

        Arguments:
            path (str): The path to the compiled NadiaVM file (`.nvm`) to read from.
            pl (tuple): The coordinates of the player.
        """
        with open(path, 'r') as vm_file:
            self._instructions = list(filter(lambda a: a, vm_file.read().split("\n")))
        self._player_pos = pl

    def has_more_instructions(self):
        # type: (CSNadiaVM) -> bool
        """Determine if the VM has more instructions to execute.

        Returns:
            more (bool): Boolean that will be True if there are more instructions, False otherwise.
        """
        return len(self._instructions) > 0

    def preview_next_instruction(self):
        # type: (CSNadiaVM) -> Optional[str]
        """Get the next command in the instruction list without executing it in the VM.

        Returns:
            command (str): The command to be executed, excluding parameters, or None if there
                are no more instructions to execute in the VM.
        """
        if self.has_more_instructions():
            return self._instructions[0].split(" ")[0]
        else:
            return None

    def next(self):
        # type: (CSNadiaVM) -> None
        """Execute the next instruction in the VM code.

        Raises:
            error (CSNadiaVMCommandNotFoundError): Command not found.
        """
        current = self._instructions.pop(0).split(" ")

        if current[0] == "alloc":
            self._alloc(current[1], int(current[2]))
        elif current[0] == "push":
            self._push(current[1], int(current[2]))
        elif current[0] == "pop":
            self._pop(current[1], int(current[2]))
        elif current[0] == "set":
            self._set(current[2])
        elif current[0] == "move":
            self._move(current[2])
        elif current[0] == "collect":
            pass
        elif current[0] != "exit":
            raise CSNadiaVMCommandNotFoundError("Invalid command: '%s'" % (current[0]))

    def _alloc(self, name, size):
        """Allocate a space of memory for a given array.

        Arguments:
            name (str): The name of the array to allocate space for.
            size (int): The size of the array. Defaults to 1.
        """
        self.__dict__[name] = [None for x in range(size)]

    def _set(self, value):
        """Set the top of the stack to a constant value.

        Arguments:
            value (any): The value to create a constant for.
        """
        self._stack.append(value)

    def _push(self, name, index):
        """Push the top-most item on the current stack to the given array.

        Arguments:
            name (str): The name of the array to push to.
            index (int): The index of the array to push to.
        """
        self.__dict__[name][index] = self._stack.pop()

    def _pop(self, name, index):
        """Pop the item from the array at a given index and set it at the top
        of the execution stack.

        Arguments:
            array (str): The array to pop an item from.
            index (int): The index of the item in the array to pop.
        """
        self._stack.append(self.__dict__[name][index])
        self.__dict__[name][index] = None

    def _move(self, direction):
        """Move the player in a given direction.

        Arguments:
            direction (str): The direction the player will move in.
        """
        transforms = {
            "north": (-1, 0),
            "south": (1, 0),
            "west": (0, -1),
            "east": (0, 1)
        }

        trans_x, trans_y = transforms.get(direction, "east")
        curr_x, curr_y = self._player_pos
        self._player_pos = curr_x + trans_x, curr_y + trans_y

    def get(self, name):
        # type: (CSNadiaVM, str) -> Optional[list]
        """Get the specified item in the virtual machine.

        Arguments:
            name (str): The name of the item to get.

        Returns:
            array (list): The specified item, or None if it doesn't exist.
        """
        return self.__dict__[name] if name in self.__dict__ \
            and type(self.__dict__[name]) is list else None #pylint:disable=unidiomatic-typecheck

    def pos(self):
        # type: (CSNadiaVM) -> tuple[int, int]
        """Get the current player position from the VM execution stack.

        Returns:
            player (tuple): A tuple containing the coordinates of the player.
        """
        return self._player_pos

class CSNadiaVMWriterBuilder(object):
    """An list-based implementation of the NadiaVM file writer.

    This class is similar to CSNadaVMWriter and contains the same methods; however,
        CSNadiaVMWriterBuilder uses a list to store its code rather the string that CSNadiaVMWriter
        uses. This is useful in instances where the builder needs to remove pieces of code or work
        with the current set of instructions as a list.

    Attributes:
        instructions (list): The list of VM commands to write to the VM file.
    """

    instructions = []

    def __init__(self, path):
        # type: (CSNadiaVMWriterBuilder, str) -> None
        """Construct the VM writer builder.

        Arguments:
            path (str): The path to the compiled NadiaVM file (`.nvm`) to write to.
        """
        self.path = path

    def __str__(self):
        string = "Filepath: %s\n" % (self.path)
        for instruction in self.instructions:
            string += "%s\n" % (instruction)
        return string

    def alloc(self, array_name, size=1):
        # type: (CSNadiaVMWriterBuilder, str, int) -> None
        """Allocate a space of memory for a given array.

        Arguments:
            array_name (str): The name of the array to allocate space for.
            size (int): The size of the array. Defaults to 1.
        """
        self.instructions.append("alloc %s %s\n" % (array_name, size))

    def push(self, array, index):
        # type: (CSNadiaVMWriterBuilder, str, int) -> None
        """Push the top-most item on the current stack to the given array.

        Arguments:
            array (str): The name of the array to push to.
            index (int): The index of the array to push to.
        """
        self.instructions.append("push %s %s\n" % (array, index))

    def pop(self, array, index):
        # type: (CSNadiaVMWriterBuilder, str, int) -> None
        """Pop the item from the array at a given index and set it at the top
        of the execution stack.

        Arguments:
            array (str): The array to pop an item from.
            index (int): The index of the item in the array to pop.
        """
        self.instructions.append("pop %s %s\n" % (array, index))

    def set(self, value):
        # type: (CSNadiaVMWriterBuilder, any) -> None
        """Set the top of the stack to a constant value.

        Arguments:
            value (any): The value to create a constant for.
        """
        self.instructions.append("set constant " + str(value) + "\n")

    def move(self, direction):
        # type: (CSNadiaVMWriterBuilder, str) -> None
        """Move the player in a given direction.

        Arguments:
            direction (str): The direction the player will move in.
        """
        self.instructions.append("move player " + direction + "\n")

    def collect(self):
        # type: (CSNadiaVMWriterBuilder) -> None
        """Collect. In the VM, this acts like a pause."""
        self.instructions.append("collect\n")

    def exit(self):
        # type: (CSNadiaVMWriterBuilder) -> None
        """Try to exit the world and end execution of the script."""
        self.instructions.append("exit player\n")

    def write(self):
        # type: (CSNadiaVMWriterBuilder) -> None
        """Write the VM code to the requested file."""
        with open(self.path, 'w+') as vm_file_stream:
            vm_file_stream.write("".join(self.instructions))

    def clear(self):
        # type: (CSNadiaVMWriterBuilder) -> None
        """Clear all of the current instructions in the VM stack."""
        del self.instructions[:]

    def undo(self, ignore_collect=True):
        # type: (CSNadiaVMWriterBuilder, bool) -> None
        """Remove the top of the instruction stack.

        Arguments:
            ignore_collect (bool): Whether to ignore the pop and push statements preceding the
                collect statement. Defaults to True.
        """
        if len(self.instructions) > 0:
            instruction = self.instructions.pop()

            if instruction == "collect" and not ignore_collect:
                self.instructions.pop()     # Pops the push statement.
                self.instructions.pop()     # Pops the pop statement.

class CSNadiaVMWriter(object):
    """An implementation of the NadiaVM file writer."""

    code = """"""

    def __init__(self, path):
        # type: (CSNadiaVMWriter, str) -> None
        """Construct the VM writer.

        Arguments:
            path (str): The path to the compiled NadiaVM file (`.nvm`) to write to.
        """
        self.path = path

    def __str__(self):
        return "Filepath: " + self.path + "\n" + self.code

    def alloc(self, array_name, size=1):
        # type: (CSNadiaVMWriter, str, int) -> None
        """Allocate a space of memory for a given array.

        Arguments:
            array_name (str): The name of the array to allocate space for.
            size (int): The size of the array. Defaults to 1.
        """
        self.code += "alloc %s %s\n" % (array_name, size)

    def push(self, array, index):
        # type: (CSNadiaVMWriter, str, int) -> None
        """Push the top-most item on the current stack to the given array.

        Arguments:
            array (str): The name of the array to push to.
            index (int): The index of the array to push to.
        """
        self.code += "push %s %s\n" % (array, index)

    def pop(self, array, index):
        # type: (CSNadiaVMWriter, str, int) -> None
        """Pop the item from the array at a given index and set it at the top
        of the execution stack.

        Arguments:
            array (str): The array to pop an item from.
            index (int): The index of the item in the array to pop.
        """
        self.code += "pop %s %s\n" % (array, index)

    def set(self, value):
        # type: (CSNadiaVMWriter, any) -> None
        """Set the top of the stack to a constant value.

        Arguments:
            value (any): The value to create a constant for.
        """
        self.code += "set constant " + str(value) + "\n"

    def move(self, direction):
        # type: (CSNadiaVMWriter, str) -> None
        """Move the player in a given direction.

        Arguments:
            direction (str): The direction the player will move in.
        """
        self.code += "move player " + direction + "\n"

    def collect(self):
        # type: (CSNadiaVMWriter) -> None
        """Collect. In the VM, this can act like a pause."""
        self.code += "collect\n"

    def exit(self):
        # type: (CSNadiaVMWriter) -> None
        """Try to exit the world and end execution of the script."""
        self.code += "exit player\n"

    def write(self):
        # type: (CSNadiaVMWriter) -> None
        """Write the VM code to the requested file."""
        with open(self.path, 'w+') as vm_file_stream:
            vm_file_stream.write(self.code)

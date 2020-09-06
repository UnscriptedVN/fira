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
"""This submodule contains the utilities and classes for the low-level virtual machine for the
    minigame code, NadiaVM.

## Implementation

The Unscripted API and the minigame GUI eventually write files readable by the Nadia Virtual
    Machine (NVM). The Nadia Virtual Machine is a stack-based virtual machine designed to
    perform operations specific to the Unscripted minigame.

### Commands
In the NadiaVM, there are several commands:

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
"""
from typing import Optional, List, Any, Tuple, Callable, Dict
from . import lang as language


class CSNadiaVMCommandNotFoundError(Exception):
    """VM command not found."""


class CSNadiaVM(object):
    """An implementation of the Nadia virtual machine.

    Attributes:
        is_interactive (bool): Whether this VM instance is interactive.
    """

    is_interactive = False
    _instructions = []  # type: List[str]
    _parsed_instructions = []  # type: List[language.CSNadiaLanguageInstruction]
    _stack = []  # type: List[Any]
    _casts = {}  # type: Dict[str, Any]
    _binds = {}  # type: Dict[str, language.CSNadiaLanguageCommand]
    _player_pos = (0, 0)  # type: Tuple[int, int]

    def __init__(self, **kwargs):
        # type: (dict) -> None
        """Initialize the virtual machine.

        If a filepath is provided, the virtual machine will populate its instruction queue with
            the instructions written in the command file and attempt to parse the data into valid
            commands for the machine to execute.

        Args:
            **kwargs (dict): Arbitrary keyword arguments.

        Kwargs:
            path (str): A path to a NadiaVM file (`.nvm`) to read from.
            player_origin (tuple): The coordinates of the player. Defaults to (0, 0).
            interactive (bool): Whether this VM instance is interactive. Defaults to False.
        """
        self._stack = []
        self._casts = {}
        self._binds = {}

        if "path" in kwargs:
            with open(str(kwargs["path"]), 'r') as vm_file:
                source = vm_file.read()
                self._instructions = [a for a in source.split("\n") if a]
                self._parsed_instructions = language.CSNadiaLanguageParser(
                    source).parse()
        else:
            self._instructions = []
            self._parsed_instructions = []

        self._player_pos = kwargs["player_origin"] if "player_origin" in kwargs else (
            0, 0)
        self.is_interactive = kwargs["interactive"] if "interactive" in kwargs else False

    def has_more_instructions(self):
        # type: () -> bool
        """Determine if the VM has more instructions to execute.

        Returns:
            more (bool): Boolean that will be True if there are more instructions, False otherwise.
        """
        return len(self._parsed_instructions) > 0

    def preview_next_instruction(self):
        # type: () -> Optional[str]
        """Get the next command in the instruction list without executing it in the VM.

        Returns:
            command (str): The command to be executed, excluding parameters, or None if there
                are no more instructions to execute in the VM.
        """
        if not self.has_more_instructions():
            return None
        return self._parsed_instructions[0].command.value

    def get_vm_stack(self):
        # type: () -> List[Any]
        """Get the current virtual machine stack.

        Returns:
            stack (list): A list containing the current representation of the stack.
        """
        return self._stack

    def get_namespace(self, name):
        # type: (str) -> Optional[List[Any]]
        """Get the specified item in the virtual machine.

        Arguments:
            name (str): The name of the item to get.

        Returns:
            array (list): The specified item, or None if it doesn't exist.
        """
        if name not in self.__dict__:
            return None
        elif not isinstance(self.__dict__[name], list) or not type(self.__dict__[name]) is list:
            return None
        listed = self.__dict__[name]  # type: List[Any]
        return listed

    def get_position(self):
        # type: () -> Tuple[int, int]
        """Get the current player position from the VM execution stack.

        Returns:
            player (tuple): A tuple containing the coordinates of the player.
        """
        return self._player_pos

    def get_binding(self, name):
        # type: (str) -> Optional[language.CSNadiaLanguageCommand]
        """Get the associated command bound to a given name.

        Arguments:
            name (str): The name to look up the binding for.

        Returns:
            command (str): The associated command, or None if no bindings exist.
        """
        return self._binds.get(name, None)

    def clear(self):
        # type: () -> None
        """Clear all existing instructions, both parsed and unparsed."""
        self._instructions = []
        self._parsed_instructions = []

    def next(self):
        # type: () -> None
        """Execute the next instruction in the VM code.

        Raises:
            error (CSNadiaVMCommandNotFoundError): Command not found.
        """
        self._parse_all()

        current = self._parsed_instructions[0]
        command = ""
        dummy_func = lambda *_, **__: None

        instruct = {
            "alloc": self._alloc,
            "push": self._push,
            "pop": self._pop,
            "set": self._set,
            "move": self._move,
            "bind": self._bind,
            "cast": self._cast,
            "add": self._add,
            "sub": self._sub,
            "mult": self._mult,
            "div": self._div,
            "neg": self._neg,
            "exit": dummy_func,
            "collect": dummy_func,
        }  # type: dict[str, Callable]

        for cast in self._casts:
            if cast not in current.parameters:
                continue
            if current.command == language.CSNadiaLanguageCommand.CAST:
                continue
            if current.command == language.CSNadiaLanguageCommand.SET\
                    and current.parameters.index(cast) == 0:
                continue
            while cast in current.parameters:
                current.parameters[current.parameters.index(
                    cast)] = self._casts[cast]

        command = instruct.get(current.command.value, dummy_func)
        if current.command in [
                language.CSNadiaLanguageCommand.ALLOC,
                language.CSNadiaLanguageCommand.PUSH,
                language.CSNadiaLanguageCommand.POP,
                language.CSNadiaLanguageCommand.BIND,
                language.CSNadiaLanguageCommand.CAST,
                language.CSNadiaLanguageCommand.SET,
        ]:
            command(current.parameters[0], current.parameters[1])
        elif current.command in [
                language.CSNadiaLanguageCommand.MOVE,
        ]:
            command(current.parameters[len(current.parameters) - 1])
        else:
            command()

    def input(self, command):
        # type: (str) -> Optional[Any]
        """Run the specified command in the virtual machine.

        If the virtual machine is set to interactive, then the command will be inserted in the
            front of the queue and be executed immediately. Otherwise, the function will return
            immediately.

        Args:
            command (str): The command to add to the virutal machine's instruction queue
                and execute.

        Returns:
            top (any): The top of the current stack, or None if the command failed.
        """
        if not self.is_interactive:
            return None
        self._instructions.insert(0, command + "\n")
        self.next()  # pylint:disable=not-callable
        self._instructions.pop(0)
        if not self._stack:
            return None
        return self._stack[len(self._stack) - 1]

    def _parse_all(self):
        """Parse all of the available commands."""
        if self._instructions:
            source = "\n".join(self._instructions)
            parser = language.CSNadiaLanguageParser(
                source, bindings=self._binds.copy())
            self._parsed_instructions = parser.parse()

    def _alloc(self, name, size):
        """Allocate a space of memory for a given array.

        Arguments:
            name (str): The name of the array to allocate space for.
            size (int): The size of the array. Defaults to 1.
        """
        self.__dict__[name] = [None for _ in range(size)]

    def _set(self, target=language.CSNadiaLanguageKeyword.CONSTANT, value=0):
        """Set the top of the stack to a constant value.

        Arguments:
            target (CSNadiaLanguageKeyword | str): The target to set the value for.
            value (any): The value to create a constant for.
        """
        if isinstance(target, language.CSNadiaLanguageKeyword)\
                and target == language.CSNadiaLanguageKeyword.CONSTANT:
            self._stack.append(value)
        elif isinstance(target, str) and target in self._casts:
            self._casts[target] = value
        else:
            pass

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

        trans_x, trans_y = transforms.get(direction, transforms["east"])
        curr_x, curr_y = self._player_pos
        self._player_pos = curr_x + trans_x, curr_y + trans_y

    def _bind(self, name, command):
        """Bind the following name to a command.

        Arguments:
            name (str): The name to bind a command to.
            command (language.CSNadiaLanguageCommand): The command to bind the name to.
        """
        if name not in self._binds:
            self._binds[name] = command

    def _cast(self, name, value):
        """Cast the value to a name.

        Arguments:
            name (str): The name to cast the value to.
            value (str): The value to cast the name to.
        """
        if name not in language.CSNadiaLanguageParser.reserved():
            self._casts[name] = value

    def _bind(self, name, command):
        """Bind the following name to a command.

        Arguments:
            name (str): The name to bind a command to.
            command (str): The command to bind the name to.
        """
        if name not in self._binds:
            self._binds[name] = language.CSNadiaLanguageCommand(command)

    def _add(self):
        """Add the two topmost values on the stack."""
        x = self._stack.pop()
        y = self._stack.pop()
        self._stack.append(int(x) + int(y))

    def _sub(self):
        """Subtract the two topmost values on the stack."""
        x = self._stack.pop()
        y = self._stack.pop()
        self._stack.append(int(x) - int(y))

    def _mult(self):
        """Multiply the two topmost values on the stack."""
        x = self._stack.pop()
        y = self._stack.pop()
        self._stack.append(int(x) * int(y))

    def _div(self):
        """Divide the two topmost values on the stack."""
        x = self._stack.pop()
        y = self._stack.pop()
        self._stack.append(int(x) / int(y))

    def _neg(self):
        """Negate the topmost value on the stack.

        Effectively, this is the equivalent of pushing -1 onto the stack and calling mult.
        """
        self._stack.append(-1)
        self._mult()


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
        # type: (str) -> None
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

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.write()

    def alloc(self, array_name, size=1):
        # type: (str, int) -> None
        """Allocate a space of memory for a given array.

        Arguments:
            array_name (str): The name of the array to allocate space for.
            size (int): The size of the array. Defaults to 1.
        """
        self.instructions.append("alloc %s %s\n" % (array_name, size))

    def push(self, array, index):
        # type: (str, int) -> None
        """Push the top-most item on the current stack to the given array.

        Arguments:
            array (str): The name of the array to push to.
            index (int): The index of the array to push to.
        """
        self.instructions.append("push %s %s\n" % (array, index))

    def pop(self, array, index):
        # type: (str, int) -> None
        """Pop the item from the array at a given index and set it at the top
        of the execution stack.

        Arguments:
            array (str): The array to pop an item from.
            index (int): The index of the item in the array to pop.
        """
        self.instructions.append("pop %s %s\n" % (array, index))

    def set(self, value):
        # type: (Any) -> None
        """Set the top of the stack to a constant value.

        Arguments:
            value (any): The value to create a constant for.
        """
        self.instructions.append("set constant " + str(value) + "\n")

    def move(self, direction):
        # type: (str) -> None
        """Move the player in a given direction.

        Arguments:
            direction (str): The direction the player will move in.
        """
        self.instructions.append("move player " + direction + "\n")

    def bind(self, name, command):
        # type: (str, str) -> None
        """Bind the following name to a command.

        Arguments:
            name (str): The name to bind a command to.
            command (str): The command to bind the name to.
        """
        self.instructions.append("bind %s %s\n" % (name, command))

    def cast(self, name, value):
        # type: (str, Any) -> None
        """Cast the value to a name.

        Arguments:
            name (str): The name to cast the value to.
            value (str): The value to cast the name to.
        """
        self.instructions.append("bind %s %s\n" % (name, value))

    def collect(self):
        # type: () -> None
        """Collect. In the VM, this acts like a pause."""
        self.instructions.append("collect\n")

    def exit(self):
        # type: () -> None
        """Try to exit the world and end execution of the script."""
        self.instructions.append("exit player\n")

    def add(self):
        """Add the two topmost values on the stack."""
        self.instructions.append("add\n")

    def sub(self):
        """Subtract the two topmost values on the stack."""
        self.instructions.append("sub\n")

    def mult(self):
        """Multiply the two topmost values on the stack."""
        self.instructions.append("mult\n")

    def div(self):
        """Divide the two topmost values on the stack."""
        self.instructions.append("div\n")

    def neg(self):
        """Negate the topmost value on the stack.

        Effectively, this is the equivalent of pushing -1 onto the stack and calling mult.
        """
        self.instructions.append("neg\n")

    def write(self):
        # type: () -> None
        """Write the VM code to the requested file."""
        with open(self.path, 'w+') as vm_file_stream:
            vm_file_stream.write("".join(self.instructions))

    def clear(self):
        # type: () -> None
        """Clear all of the current instructions in the VM stack."""
        del self.instructions[:]

    def undo(self, ignore_collect=True):
        # type: (bool) -> None
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
        # type: (str) -> None
        """Construct the VM writer.

        Arguments:
            path (str): The path to the compiled NadiaVM file (`.nvm`) to write to.
        """
        self.path = path

    def __str__(self):
        return "Filepath: " + self.path + "\n" + self.code

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.write()

    def alloc(self, array_name, size=1):
        # type: (str, int) -> None
        """Allocate a space of memory for a given array.

        Arguments:
            array_name (str): The name of the array to allocate space for.
            size (int): The size of the array. Defaults to 1.
        """
        self.code += "alloc %s %s\n" % (array_name, size)

    def push(self, array, index):
        # type: (str, int) -> None
        """Push the top-most item on the current stack to the given array.

        Arguments:
            array (str): The name of the array to push to.
            index (int): The index of the array to push to.
        """
        self.code += "push %s %s\n" % (array, index)

    def pop(self, array, index):
        # type: (str, int) -> None
        """Pop the item from the array at a given index and set it at the top
        of the execution stack.

        Arguments:
            array (str): The array to pop an item from.
            index (int): The index of the item in the array to pop.
        """
        self.code += "pop %s %s\n" % (array, index)

    def set(self, value):
        # type: (Any) -> None
        """Set the top of the stack to a constant value.

        Arguments:
            value (any): The value to create a constant for.
        """
        self.code += "set constant " + str(value) + "\n"

    def move(self, direction):
        # type: (str) -> None
        """Move the player in a given direction.

        Arguments:
            direction (str): The direction the player will move in.
        """
        self.code += "move player " + direction + "\n"

    def bind(self, name, command):
        # type: (str, str) -> None
        """Bind the following name to a command.

        Arguments:
            name (str): The name to bind a command to.
            command (str): The command to bind the name to.
        """
        self.code += "bind %s %s\n" % (name, command)

    def cast(self, name, value):
        # type: (str, Any) -> None
        """Cast the value to a name.

        Arguments:
            name (str): The name to cast the value to.
            value (str): The value to cast the name to.
        """
        self.code += "bind %s %s\n" % (name, value)

    def collect(self):
        # type: () -> None
        """Collect. In the VM, this can act like a pause."""
        self.code += "collect\n"

    def exit(self):
        # type: () -> None
        """Try to exit the world and end execution of the script."""
        self.code += "exit player\n"

    def add(self):
        """Add the two topmost values on the stack."""
        self.code += "add\n"

    def sub(self):
        """Subtract the two topmost values on the stack."""
        self.code += "sub\n"

    def mult(self):
        """Multiply the two topmost values on the stack."""
        self.code += "mult\n"

    def div(self):
        """Divide the two topmost values on the stack."""
        self.code += "div\n"

    def neg(self):
        """Negate the topmost value on the stack.

        Effectively, this is the equivalent of pushing -1 onto the stack and calling mult.
        """
        self.code += "neg\n"

    def write(self):
        # type: () -> None
        """Write the VM code to the requested file."""
        with open(self.path, 'w+') as vm_file_stream:
            vm_file_stream.write(self.code)

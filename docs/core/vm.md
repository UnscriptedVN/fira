---
layout: default
title: Virtual Machine
parent: Core Utilities
---

# Virtual Machine
{: .no_toc}

## Table of Contents
{: .no_toc .text-delta}

1. TOC
{: toc}

This submodule contains the low-level virtual machine reader for the minigame
code.

## Implementation

The Unscripted API and the minigame GUI eventually write files readable by the [Nadia Virtual Machine](../implementation.html#nadiavm) (NVM). The Nadia Virtual Machine is a stack-based virtual machine designed to perform operations specific to the Unscripted minigame.

---

## CSNadiaVMCommandNotFoundError(Exception)

VM command not found.

## CSNadiaVM

An implementation of the NadiaVM stack.

### \_\_init\_\_
Construct the VM reader.

#### Arguments
{: .no_toc}

- **path** (str): The path to the compiled NadiaVM file (`.nvm`) to read from.
- **pl** (tuple): The coordinates of the player.

### has_more_instructions()

Determine if the VM has more instructions to execute.

#### Returns
{: .no_toc}

- **more** (bool): Boolean that will be True if there are more instructions, False otherwise.

### preview_next_instruction()
Get the next command in the instruction list without executing it in the VM.

#### Returns
{: .no_toc}

- **command** (str): The command to be executed, excluding parameters, or None if there
    are no more instructions to execute in the VM.

### next()
Execute the next instruction in the VM code.

#### Raises
{: .no_toc}

- **error** ([CSNadiaVMCommandNotFoundError](#csnadiavmcommandnotfounderrorexception)): Command not found.

### get(name)
Get the specified item in the virtual machine.

#### Arguments
{: .no_toc}

- **name** (str): The name of the item to get.

#### Returns
{: .no_toc}

- **array** (list): The specified item, or None if it doesn't exist.

### pos
Get the current player position from the VM execution stack.

#### Returns
{: .no_toc}

- **player** (tuple): A tuple containing the coordinates of the player.

## CSNadiaVMWriterBuilder
An list-based implementation of the NadiaVM file writer.

This class is similar to [CSNadaVMWriter](#csnadiavmwriter) and contains the same methods; however, CSNadiaVMWriterBuilder uses a list to store its code rather the string that CSNadiaVMWriter
uses. This is useful in instances where the builder needs to remove pieces of code or work
with the current set of instructions as a list.

### Attributes

- **instructions** (list): The list of VM commands to write to the VM file.

### \_\_init\_\_
Construct the VM writer builder.

#### Arguments
{: .no_toc}

- **path** (str): The path to the compiled NadiaVM file (`.nvm`) to write to.

### alloc(array_name, size=1)

Allocate a space of memory for a given array.

#### Arguments
{: .no_toc}

- **array_name** (str): The name of the array to allocate space for.
- **size** (int): The size of the array. Defaults to 1.

### push(array, index)
Push the top-most item on the current stack to the given array.

#### Arguments
{: .no_toc}

- **array** (str): The name of the array to push to.
- **index** (int): The index of the array to push to.

### pop(array, index)
Pop the item from the array at a given index and set it at the top
of the execution stack.

#### Arguments
{: .no_toc}

- **array** (str): The array to pop an item from.
- **index** (int): The index of the item in the array to pop.

### set(value)

Set the top of the stack to a constant value.

#### Arguments
{: .no_toc}

- **value** (any): The value to create a constant for.

### move(direction)
Move the player in a given direction.

#### Arguments
{: .no_toc}

- **direction** (str): The direction the player will move in.

### collect()
Collect. In the VM, this acts like a pause.

### exit()
Try to exit the world and end execution of the script.

### write()
Write the VM code to the requested file.

### clear()
Clear all of the current instructions in the VM stack.

### undo(ignore_collect=True)
Remove the top of the instruction stack.

#### Arguments
{: .no_toc}

- **ignore_collect** (bool): Whether to ignore the pop and push statements preceding the
    collect statement. Defaults to True.

## CSNadiaVMWriter

An implementation of the NadiaVM file writer.

### \_\_init\_\_
Construct the VM writer.

#### Arguments
{: .no_toc}

- **path** (str): The path to the compiled NadiaVM file (`.nvm`) to write to.

### alloc(array_name, size=1)

Allocate a space of memory for a given array.

#### Arguments
{: .no_toc}

- **array_name** (str): The name of the array to allocate space for.
- **size** (int): The size of the array. Defaults to 1.

### push(array, index)
Push the top-most item on the current stack to the given array.

#### Arguments
{: .no_toc}

- **array** (str): The name of the array to push to.
- **index** (int): The index of the array to push to.

### pop(array, index)
Pop the item from the array at a given index and set it at the top
of the execution stack.

#### Arguments
{: .no_toc}

- **array** (str): The array to pop an item from.
- **index** (int): The index of the item in the array to pop.

### set(value)

Set the top of the stack to a constant value.

#### Arguments
{: .no_toc}

- **value** (any): The value to create a constant for.

### move(direction)
Move the player in a given direction.

#### Arguments
{: .no_toc}

- **direction** (str): The direction the player will move in.

### collect()
Collect. In the VM, this acts like a pause.

### exit()
Try to exit the world and end execution of the script.

### write()
Write the VM code to the requested file.
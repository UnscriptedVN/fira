---
layout: default
title: Implementation
nav_order: 3
---

# Implementation
{: .no_toc}

## Table of Contents
{: .no_toc .text-delta}

1. TOC
{: toc}

## How the minigame works

In the minigame, players are tasked to create a set of commands that will be executed by a virtual machine in the preview scene in hopes of collecting all of the coins and reaching the exit. Although the method of getting the commands varies, the minigame will attempt to read from a virtual machine file and execute its commands as necessary.

![Abstraction diagram](/assets/img/abstraction.png)

### Obtaining code for basic and advanced modes

In the case of the two game modes in Unscripted, both modes make use of Fira's core module to generate virtual machine code. In either mode, memory management and pushing/popping from memory is automatically managed and written for the player.

#### Basic Mode

For the basic mode, a virtual machine writer ([`CSNadiaVMWriterBuilder`](./core/vm.html#csnadiavmwriterbuilder)) is used to keep track of the commands given by the player. When a player clicks a command button, the writer will add the command to the writer's command list; likewise, when a player clicks "Undo" or "Clear", the list is modified. After the player clicks "Run", the writer generates a VM file in the save directory of the game that will be read by the preview scene.

#### Advanced Mode

For the advanced mode via the Fira API module, the APIs link to a hidden VM writer ([`CSNadiaVMWriter`](./core/vm.html#csnadiavmwriter)) that gets invoked when the player calls functions in the API. The [`exit`](./api/player.html#exit) method of the [`CSPlayer`](./api/player.html#csplayer) class is responsible for writing the VM file, hence why Python scripts must invoke this function. When the player is finished writing the script and clicks "Run", the Python compiler compiles and executes the script inside of Ren'Py's Python environment, generating the VM file in the process in the save directory of the game that will be read by the preview scene.

### Obtaining code from third-party tools

Third-party tools will most likely create an abstraction layer in a similar fashion to the Fira API module. These tools will eventually create the VM file that the preview scene will read. Implementation of the VM varies depending on the tool, so it is recommended that you read the documentation of the respective tool or library on how it writes VM files.

Players may also choose to write their own VM files directly, though this is not generally recommended.

### Preview scene execution

Once the VM file is written, the data is sent to a virtual machine emulator ([`CSNadiaVM`](./core/vm.html#csnadiavm)), which is later sent to the preview scene. Once the preview scene renders the world and components, the preview scene will call on the VM emulator to execute the commands in order. For commands that require animation (i.e., `move` and `collect`), execution pauses as the preview scene presents the corresponding animation.

## NadiaVM

Fira contains the virtual machine used in processing and managing the preview scene, NadiaVM. NadiaVM is a simple, stack-based virtual machine with a couple of commands. The VM is designed to focus specifically on the minigame's internal game logic and is not necessarily suitable for general use. NadiaVM files are registered with the file extension `.nvm` and are typically plain text files with the corresponding instructions.


### Commands

NadiaVM comes with several commands used to perform tasks in the minigame:

- `alloc (str) (int)`: Create a new array with a name and a specific size.
- `collect`: Collect a coin in the world. Acts like a pause in VM.
- `push (str) (int)`: Push the top of the stack to the given array at the index.
- `pop (str) (int)`: Pop the item located at the array's index and move it to the
    top of the stack.
- `set constant (any)`: Set the top of the stack to a constant value.
- `move player (str)`: Move the player in a given direction.
- `exit player`: Try to end the execution script and finish the level.
- <span class="label label-purple">New</span> `add`: Add the two topmost values on the stack.
- <span class="label label-purple">New</span> `sub`: Subtract the two topmost values on the stack.
- <span class="label label-purple">New</span> `mult`: Multiply the two topmost values on the stack.
- <span class="label label-purple">New</span> `div`: Divide the two topmost values on the stack.
- <span class="label label-purple">New</span> `neg`: Negate the topmost value on the stack. Effectively the same as pushing `-1` on the stack and calling `mult`.

### Limitations

NadiaVM is a simple stack-based virtual machine designed to process commands quickly, meaning that there are limitations to how it works:

- NadiaVM files can't reference each other.
- NadiaVM doesn't support control flow or functions.
- NadiaVM doesn't work with pointers or deal with memory addresses; rather, it works with creating its own lists and modifying them accordingly.
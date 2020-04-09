---
layout: default
title: World
parent: API
---

# World
{: .no_toc}

## Table of Contents
{: .no_toc .text-delta}

1. TOC
{: toc}

The world module contains all of the classes and functions necessary to visualize
    and gather information about the game world.

The module contains the base grid class responsible for making two-dimensional arrays
    organized like a grid easier to work with ([`CSWorldGrid`](./grid.html#csworldgrid)), as well as the
    world class that contains all of the world's information such as the player's position and
    coins ([`CSWorld`](./grid.html#csworld)).

## World Implementation
Worlds are organized as a grid-like, two-dimensional array (matrix) consisting of rows and columns.
    Each element in the grid contains a string that describes what the world element at that
    position in the grid is. There are five possible options:

- `"PLAYER"`, which refers to the player character
- `"WALL"`, which refers to a wall
- `"COIN"`, which refers to a collectable coin
- `"EXIT"`, which refers to an exit
- `"AIR"`, which refers to a space that doesn't have a particular item

In most scenarios, the world itself does not get modified directly since the layout of items in the
    world need to be preserved. The [`CSPlayer`](./player.html#csplayer) object in the [`player`](./player.html) module of the API handles
    world manipulation when a world is passed into its constructor, and most scripts will make a
    copy of world information such as the number of coins and the player's starting position.

It may be impractical in some cases to access an element in the grid directly. The
    [`CSWorldGrid`](./grid.html#csworldgrid) class allows for the world grid to be used in a more practical
    manner by making common operations such as getting a list containing coordinates of a specific
    type of item and getting the first instance of an item easier.

---

## CSWorld

The base class for a minigame world.

The minigame world contains a matrix containing the elements used to generate that world, as well as any specific world properties like coins and exit locations.

### \_\_init\_\_
Construct a World object.

#### Arguments
{: .no_toc}

- **from_data** (CSWorldDataGenerator): The world generator used to create the world data.
- **\*\*kwargs**: Arbitrary keyword arguments.

### player()

Get the player's current location in the world.

#### Returns
{: .no_toc}

- **position** (tuple): The current coordinates of the player.

### size()

Get the size of the world.

#### Returns
{: .no_toc}
- **dimensions** (tuple): A tuple containing the number of rows and columns.

### walls()

Get the grid of walls in the world.

#### Returns
{: .no_toc}
- **walls** ([CSWorldGrid](./grid.html#csworldgrid)): Grid containing only the walls.

### coins()
Get the grid of coins in the world.

#### Returns
{: .no_toc}

- **coins** ([CSWorldGrid](./grid.html#csworldgrid)): Grid containing only the coins.

### exit()

Get the location of the exit.

#### Returns
{: .no_toc}

- **exit** (tuple): A tuple containing the coordinates of the exit.
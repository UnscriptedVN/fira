---
layout: default
title: Player
parent: API
---

# Player
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta}

1. TOC
{: toc}

The player module contains the functions and classes necessary to manipulate players in
    a minigame world.

The module contains a class that lets players control the behavior of their minigame counterpart
    by moving in a given direction, collecting an item, etc. ([`CSPlayer`](#csplayer)). To prevent accidental
    manipulation of the original world data, the player class uses its own position property to
    update its location.

## CSPlayer

The base class for a player in the minigame world.

The player object contains methods for manipulating the current player's position and inventory system.

### \_\_init\_\_

Construct the Player object.

#### Arguments
{: .no_toc}

- **in_world** ([CSWorld](./world.html#csworld)): The world the player is located in.
- **\*\*kwargs** (dict): Arbitrary keyword arguments.

#### Kwargs
{: .no_toc}

- **at_position** (tuple): The position the player should be placed in. Defaults to the player
    position in the world ([`CSWorld.player`](./world.html#player)).
- **with_inv** (list): A list containing items that the player will have to start. Defaults to
    an empty list.
- **vm**: The virtual machine writer, if available.

---
## Methods
{: .no_toc}

### location()

Get the player's current position.

#### Returns
{: .no_toc}

- **position** (tuple): The current coordinates of the player.

### origin()

Get the original starting position of the player.

#### Returns
{: .no_toc}

- **origin** (tuple): The coordinates of the player's original position.

### capacity()

Get the the count of how many items the player has.

#### Returns
{: .no_toc}

- **count** (int): The number of items in the inventory.

### blocked()
Determine whether a player is blocked at a given position.

#### Returns
{: .no_toc}

- **blocked** (bool): True if any walls are near the player (1-block radius).

### move(direction)

Move the player in a direction, if the direction results in the player
being able to move into a non-walled area.

#### Arguments
{: .no_toc}

- **direction** (str): The direction the player should move in. Acceptable directions
    are `"north"`, `"south"`, `"east"`, and `"west"`.

#### Returns
{: .no_toc}

- **player** ([CSPlayer](#csplayer)): The Player that committed the move action. This is useful in cases
    where chaining methods is preferred.

### collect()

Add an item into the player's inventory at the player's current position.

If the item does not exist in the world, or the player already has the item in question,
    nothing occurs.

#### Returns
{: .no_toc}

- **player** ([CSPlayer](#csplayer)): The Player object that committed the collect action. This is useful
    in cases where chaining methods is preferred.

### exit()
Exit the level, if possible.

If a VM is specified, the VM writer will also close the writer by writing to the VM file.
---
layout: default
title: Info
parent: API
---

# Info
{: .no_toc}

## Table of Contents
{: .no_toc .text-delta}

1. TOC
{: toc}

The info submodule contains the utilities to get the world and player information for a given
    level.

## Methods

### get_level_information(level)

Create a world and player based on a game level.

#### Arguments
{: .no_toc}

- **level** (int): The level number as indicated by the minigame.
- **fn_path** (str): The path to where the NadiaVM file will be written to. This excludes
the file name itself.
- **\*\*kwargs** (dict): Arbitrary keyword arguments.

#### Kwargs
{: .no_toc}

New
{: .label}

- **config_file** (str): The path to the level configuration file, excluding the file name.
- **exists** (callable): The function to use, if not relying on the built-in `os` module
    to determine whether the configuration file path is loadable.
- **load** (callable): The function to use, if not relying on the the built-in `open`
    function to load the file object.

#### Returns
{: .no_toc}

- **info** (tuple): A tuple containing the [`CSPlayer`](./player.html#csplayer) object and the
[`CSWorld`](./world.html#csworld) object
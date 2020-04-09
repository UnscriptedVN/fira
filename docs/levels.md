---
layout: default
title: Levels
nav_order: 4
---

# Level Structure
{: .no_toc}

## Table of Contents
{: .no_toc .text-delta}

1. TOC
{: toc}

The minigame's level files are a series of markup files using TOML that describe the information about that level, as well as the overall layout of the level's world. Level files have a root key `level` with two subkeys, `map` and `config`.

### Configuration Fields

There are three primary fields in the `config` entry of the TOML file:

- `name`: The name of the level
- `check`: A list of strings containing the requirements for completing the level
- `allowed-blocks`: A list of strings containing the allowed blocks that appear in the basic mode editor

#### Checks
- `player-at-exit`: Whether or not the player has reached the exit
- `player-collects-all`: Whether or not the player has collected all of the coins

#### Allowed blocks
- `move`: Directional movement blocks
- `collect`: Collect coin clock
- `exit`: Exit level block

## Map Construction

The `map` subkey contains a single value `layout` that contains a multiline string that describes the world using ASCII characters. An example is provided below:

```
%%%%%%%
%P . E%
%%%%%%%
```

### Map Symbols
There are five acceptable characters to use when creating the layout string:

- `%`: A wall
- `P`: The player's starting position
- `.`: A coin to be collected
- `E`: The exit block to stand on
- <code>&nbsp;</code>: An air block or null space

### Limitations

There are a few limitations regarding the world map string:

- There cannot be more than one player or exit in a map.
- Each line must have the same number of characters to keep a consistent size.
- Each level should have its own surrounding wall border.

## Example level configuration

```toml
[level.config]
name = "Example"
allowed-blocks = ["move", "exit"]
check = ["player-at-exit"]

[level.map]
layout = """
%%%%% %%%%%
%  P% %E  %
% %%% %%% %
% %%% %%% %
%         %
%%%%%%%%%%%
"""
```
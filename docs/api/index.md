---
layout: default
title: API
nav_order: 4
has_children: true
has_toc: false
---

# Fira API

The `api` module contains all of the player-facing functions and classes used in the
    Advanced Mode of the Unscripted minigame.

The Unscriped Minigame Application Programming Interface (API) allows players to directly
    manipulate the player's movements and actions while traversing in the minigame world using
    Python. The minigame's logic will handle translating any commands to display at the end of the
    script compilation.

> **Warning**: Although most (if not all) of the submodules in the parent package are publicly accessible,
> it is heavily encouraged that players make use of the standard utilities provided with
> the API module.

   The documentation for some components in the core submodule are provided for reference namely,
    [`CSWorldGrid`](./grid.html#csworldgrid).

## Submodules

The `api` module comes with a few submodules that contain function and utilities for multiple
    aspects of the minigame:

- [`player`](./player.html) hosts all of the code related to manipulating the player in the minigame.
- [`world`](./world.html) hosts all of the code related to viewing and gathering information about the world
    in the minigame.
- [`grid`](./grid.html) hosts a publicly available version of the internal grid system used for world generation.
- [`info`](./info.html) hosts all of the code related to generating the tools necessary to start scripting.
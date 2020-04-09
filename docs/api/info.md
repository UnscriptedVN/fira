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

#### Returns
{: .no_toc}

- **info** (tuple): A tuple containing the [`CSPlayer`](./player.html#csplayer) object and the
    [`CSWorld`](./world.html#csworld) object
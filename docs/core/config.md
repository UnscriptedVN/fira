---
layout: default
title: Configuration
parent: Core Utilities
---

# Configuration
{: .no_toc}

## Table of Contents
{: .no_toc .text-delta}

1. TOC
{: toc}

This submodule contains the configuration system for reading worlds.

## CSWorldConfigGenerateError(Exception)
Could not generate the world from the requested file or configuration.

## CSWorldConfigReader
he world configuration reader.

The world configuration reader parses a TOML file and creates an object that stores information
    about the world that can be used to generate a map.

### Attributes
- **title**: The title of the map.
- **checks**: A list of strings containing the requirements for completing the puzzle.
- **allowed**: A list containing the allowed blocks for a given world. Unnecessary if using
    Advanced Mode.
- **data**: A [`CSWorldDataGenerator`](./data.html#csworlddatagenerator) containing the world data from the generated map that
    can be used to generate a world.

### \_\_init\_\_(filepath="")
Construct the configuration reader.

#### Arguments
{: .no_toc}

- **filepath (str)**: The path to the configuration file to generate the world from. Defaults to
    an empty string.
- **\*\*kwargs**: Arbitrary keyword arguments.

#### Kwargs
{: .no_toc}

- **title** (str): The title of the map.
- **checks** (list): A list containing the checks for this particular level.
- **allowed** (list): A list containing the allowed blocks in basic mode.
- **world** (str): A string representation of the world layout.
- **exists** (callable): The function to use, if not relying on the built-in `os` module
to determine whether the configuration file path is loadable.
- **load** (callable): The function to use, if not relying on the the built-in `open`
function to load the file object.
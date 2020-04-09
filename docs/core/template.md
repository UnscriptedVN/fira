---
layout: default
title: Templates
parent: Core Utilities
---

# Templates
{: .no_toc}

## Table of Contents
{: .no_toc .text-delta}

1. TOC
{: toc}

The template module contains the utilities to create file templates for the Unscripted
    minigame code.

The template files are generated when the game starts and are replaced if none are found.

## Methods

### generate_template(filepath, for_level=0)

Generate a template file using the Minigame APIs.

#### Arguments
{: .no_toc}

- **filepath** (str): The path to where the template file will be written.
- **for_level** (int): The corresponding level for the minigame. Defaults to 0.
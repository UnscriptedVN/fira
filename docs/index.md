---
layout: default
title: Home
nav_order: 1
---

# The minigame backend for Unscripted

<div class="code-example">


###### Preview the new Fira

The new Unscripted Documentation Center provides the latest documentation for the upcoming versions of Fira and will be the new location for all Fira documentation.

<span class="fs-3">

[Visit now](https://docs.unscriptedvn.dev/fira/){: .btn .btn-purple}

</span>


</div>

**Fira** is the main backend and API code for the minigame in [Unscripted](https://unscripted.marquiskurt.net), a visual novel about software development. Fira provides many facets of the minigame, including a public API that players can use to code solutions to the minigame puzzles, a configuration and data generator from level files, and a virtual machine that runs low-level code that the minigame processes.

[Install on PyPI](https://pypi.org/project/uvn-fira){: .btn .btn-purple}
[View on GitHub](https://github.com/UnscriptedVN/fira){: .btn }

---

## Getting started

Fira comes pre-packaged in Unscripted but can be installed outside of the game to work better with IDEs and other Python tools such as Poetry.

### Dependencies

Fira is both a Python 2 and Python 3 package and relies on the TOML Python package. These dependencies will be installed with the package, either from source or from PyPI.

### Quick Start: Install on PyPI

Fira is available on PyPI and can be installed as such:

```
pip install uvn-fira
```

### Install from source

To install Fira from the source code, first clone the repository from GitHub via `git clone`. You'll also need to install [Poetry](https://python-poetry.org). In the root of the source, run the following commands:

```
poetry install
poetry build
```

The resulting wheel files will be available in the `dist` directory.

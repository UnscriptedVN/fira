---
layout: default
title: Grid
parent: API
---

# Grid
{: .no_toc}

## Table of Contents
{: .no_toc .text-delta}

1. TOC
{: toc}

The grid submodule contains a public-facing version of the internal grid used in the Unscripted
    minigame core.

The world grid is a two-dimensional array (list of lists) that contain strings that determine what
    element is present at the specific row and column. The main class responsible for working with
    the grid, [`CSWorldGrid`](#csworldgrid), is a clean and lightweight implementation of this grid with multiple
    utilities to manage it. The grid implementation is not dependent on the `numpy` library and is
    geared towards accessing elements and other information, rather than mathematical operations.

## CSWorldGrid

A class representation of a grid.

The grid is a two-dimensional array object that contains elements at given positions. This
    class contains methods that allow easy access to the contents of the grid without needing
    to access the grid directly.

### Attributes
{: .no_toc}

- **grid** (list): The two-dimensional array containing items at given positions,
        organized by row and column.

### \_\_init\_\_

Construct a grid.

If a filter is supplied with the grid, the grid will filter for the items specified in the
    filter expression, marking those that don't match the filter as None.

#### Arguments
{: .no_toc}

- **grid** (list): The two-dimensional array representing the grid.
- **grid_filter** (callable): A function that determines what items in the grid to keep.
    Defaults to None, indicating that no filter is applied.

---

## Methods
{: .no_toc}

### shape()

Get the shape of the grid.

#### Returns
{: .no_tocs}

- **shape** (tuple): A tuple containing the total rows and columns of this grid.

### as_list()

Convert the grid to a list of coordinates containing a non-void item.

> Note: If a filter was applied to the grid at construction, it will only select items that are not `None`.

#### Returns
{: .no_toc}

- **coordinates** (list): A list of tuples containing the coordinates to valid items in the grid.

### first(of="")

Get the first instance of an item in the grid.

#### Arguments
{: .no_toc}

- **of** (str): The item to look for the first instance of in this grid.

#### Returns
{: .no_toc}

- **coords** (tuple): A tuple containing the row and column coordinates of the first item. If
    the item was not found, the tuple `-1, -1` is returned.

### last(of="")

Get the last instance of an item in the grid.

#### Arguments
{: .no_toc}

- **of** (str): The item to look for the last instance of in this grid.

#### Returns
{: .no_toc}

- **coords** (tuple): A tuple containing the row and column coordinates of the last item. If
    the item was not found, the tuple `-1, -1` is returned.

### element_at(row, column)

Get the element at a specified position.

#### Arguments
{: .no_toc}

- **row** (int): The row that the element is located in
- **column** (int): The column that the element is located in

#### Returns
{: .no_toc}

- **element** (str): The element at the specified position in the grid.
# coding:utf-8
#
# test_package.py
# Unscripted Fira
#
# Created by Marquis Kurt on 05/12/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""This module contains the tests for the Fira package."""
from uvn_fira import __version__ as __fver, api

def test_version_matches():
    """Test that the version matches correctly."""
    assert __fver == "2.0.0"

def test_module_import():
    """Test that the API module was imported."""
    assert api

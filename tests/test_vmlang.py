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
"""This module contains the tests for the language parser."""

from ast import parse
import pytest
from uvn_fira.core.lang import CSNadiaLangParseError, CSNadiaLanguageCommand, CSNadiaLanguageKeyword, CSNadiaLanguageToken
from uvn_fira.core.vm import language as lang

EXAMPLE_STRINGS = {
    "one_token": "collect\n",
    "line_with_parameters": "set constant 5\n",
    "binding": "bind var set\n",
    "read_binding": "var constant 10\n",
    "bad": "notacommand\n",
}


def test_can_tokenize():
    """Test that the parser can successfully tokenize."""
    tokenizer = lang.CSNadiaLanguageParser(EXAMPLE_STRINGS["one_token"])
    tokens = tokenizer.tokenize()
    assert len(tokens) > 0 and tokens[0] == lang.CSNadiaLanguageToken(
        lang.CSNadiaLanguageTokenType.KEYWORD, "collect")


def test_can_parse():
    """Test that the parse can successfully create an AST."""
    parser = lang.CSNadiaLanguageParser(EXAMPLE_STRINGS["one_token"])
    ast = parser.parse()

    expected = lang.CSNadiaLanguageInstruction(CSNadiaLanguageCommand.COLLECT)

    assert len(ast) > 0 and ast[0] == expected


def test_can_parse_with_parameters():
    """Test that the parser can successfully parse out a command with parameters."""
    parser = lang.CSNadiaLanguageParser(
        EXAMPLE_STRINGS["line_with_parameters"])
    ast = parser.parse()

    expected = lang.CSNadiaLanguageInstruction(
        CSNadiaLanguageCommand.SET, [CSNadiaLanguageKeyword.CONSTANT, 5])

    assert len(ast) > 0 and ast[0] == expected


def test_can_create_bindings():
    """Test that the parser can create bindings and read from them."""
    parser = lang.CSNadiaLanguageParser(
        EXAMPLE_STRINGS["read_binding"], bindings={"var": "set"})
    ast = parser.parse()

    expected = lang.CSNadiaLanguageInstruction(
        CSNadiaLanguageCommand.SET, [CSNadiaLanguageKeyword.CONSTANT, 10])

    assert len(ast) > 0 and ast[0] == expected


def test_can_fail_parsing():
    """Test that the parser can fail parsing a bad string."""
    parser = lang.CSNadiaLanguageParser(EXAMPLE_STRINGS["bad"])
    with pytest.raises(CSNadiaLangParseError) as e_info:
        ast = parser.parse()

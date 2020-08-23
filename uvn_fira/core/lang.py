# coding=utf-8
#
# lang.py
# Fira Core
#
# Created by Marquis Kurt on 04/02/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""The `language` sumbodule contains all of the utilities for the NadiaVM language parser.

This module is typically accessed and an extension to `core.vm`.

# Lexical Elements

Currently, a few token types exist in NadiaVM and available as an enumeration,
    `CSNadiaLanguageTokenType`:
- Comments, preceded by a semicolon (;)
- Strings, Unicode characters wrapped in quotes (")
- Numbers, sets of digits
- Keywords, a pre-defined list of key words (see `CSNadiaLanguageKeyword`)
- Any, a type that can represent anything
- None, the equivalent of `None` or `null`

# Keywords
The following are registerd as keywords in NadiaVM. Most of them are commands:

- set
- alloc
- push
- pop
- move
- bind
- cast
- exit
- add
- sub
- mult
- div
- neg
- constant
- origin
- player

# General Language Grammar

Currently, the language parser recognizes the following grammar expression:

```
expr := command (keyword|number|string|any|none)*
```

As NadiaVM closely resembles langauges like Assembly, operations such as addition must be a series of commands:

```nvm
set constant 10
set constant 18
add
```
"""

from typing import List, Tuple, Any, Optional, Dict
from string import digits, ascii_letters
from enum import Enum


class CSNadiaLangTokenizeError(Exception):
    """An error occurred when attempting to tokenize the input."""


class CSNadiaLangParseError(Exception):
    """An error occurred when attempting to parse the input."""


class CSNadiaLanguageTokenType(Enum):
    """An enumerated representation of the types of tokens the NadiaVM language tokenizer
        produces.

    These are the following token types:
    - (COMMENT) Comments, preceded by a semicolon (;)
    - (STRING) Strings, Unicode characters wrapped in quotes (")
    - (NUMBER) Numbers, sets of digits
    - (KEYWORD) Keywords, a pre-defined list of key words
    - (ANY) Any, a type that can represent anything
    - (NONE) None, the equivalent of `None` or `null`
    """
    KEYWORD = "keyword"
    COMMENT = "comment"
    STRING = "string"
    NUMBER = "number"
    IDENTIFIER = "identifier"
    ANY = "any"
    NONE = "none"


class CSNadiaLanguageKeyword(Enum):
    """An enumerated representation of the NadiaVM language keywords."""
    SET = "set"
    BIND = "bind"
    CAST = "cast"
    COLLECT = "collect"
    EXIT = "exit"
    POP = "pop"
    PUSH = "push"
    ALLOC = "alloc"
    ADD = "add"
    SUB = "sub"
    MULT = "mult"
    DIV = "div"
    NEG = "neg"
    CONSTANT = "constant"
    ORIGIN = "origin"
    PLAYER = "player"
    MOVE = "move"


class CSNadiaLanguageCommand(Enum):
    """An enumerated representation of the NadiaVM Language commands.

    This is a subset of language keywords that filter out any non-command keywords.
    """
    SET = "set"
    BIND = "bind"
    CAST = "cast"
    COLLECT = "collect"
    EXIT = "exit"
    POP = "pop"
    PUSH = "push"
    ALLOC = "alloc"
    ADD = "add"
    SUB = "sub"
    MULT = "mult"
    DIV = "div"
    NEG = "neg"
    MOVE = "move"


class _CSNadiaLangTokenizerState(Enum):
    """An enumerated representation of the tokenizer's state."""
    START = "start"
    IN_PROGRESS = "progress"
    FINISH = "finish"
    ERROR = "error"


class CSNadiaLanguageInstruction(object):
    """A data class representation of a NadiaVM language command.

    Class Attributes:
        command (CSNadiaLanguageCommand): The command that this instruction represents.
        parameters (List[Any]): The list of parameters that this command takes.
    """
    command = CSNadiaLanguageCommand.EXIT       # type: CSNadiaLanguageCommand
    parameters = []                             # type: List[Any]

    def __init__(self, command, params=[]):
        # type: (CSNadiaLanguageInstruction, CSNadiaLanguageCommand, List[Any]) -> None
        self.command = command      # type: CSNadiaLanguageCommand
        self.parameters = params    # type: List[Any]

    def __repr__(self):
        return "%s(command=%s, parameters=%s)" % (
            self.__class__.__name__, self.command, self.parameters
        )

    def __eq__(self, o):
        return isinstance(o, CSNadiaLanguageInstruction) \
            and self.command == o.command \
            and self.parameters == o.parameters

    def __ne__(self, o):
        return not self.__eq__(o)


class CSNadiaLanguageToken(object):
    """A data structure that represents a language token."""
    type = CSNadiaLanguageTokenType.COMMENT  # type: CSNadiaLanguageTokenType
    contents = "; Example"  # type: str

    def __init__(self, type, content):  # pylint:disable=redefined-builtin
        # type: (CSNadiaLanguageToken, CSNadiaLanguageTokenType, str) -> None
        self.type = type  # type: CSNadiaLanguageTokenType
        self.contents = content  # type: str

    def __eq__(self, o):
        return isinstance(o, CSNadiaLanguageToken) and self.__dict__ == o.__dict__

    def __ne__(self, o):
        return not self.__eq__(o)

    def __repr__(self):
        return "%s(type=%s, contents=%s)" % (
            self.__class__.__name__, self.type, self.contents
        )

    @property
    def castable(self):
        # type: (CSNadiaLanguageToken) -> Any
        """Get a typecasted version of the contents of the token.

        Returns:
            value (Any): The typecasted version of the contents of this token.
        """
        casts = {
            CSNadiaLanguageTokenType.NUMBER: int,
            CSNadiaLanguageTokenType.KEYWORD: CSNadiaLanguageKeyword,
            CSNadiaLanguageTokenType.NONE: (lambda _: None),
        }
        castable_func = casts.get(self.type, str)   # type: Any
        return castable_func(self.contents)


class CSNadiaLanguageParser(object):
    """The language parser for NadiaVM.

    The NadiaVM language parser is a recursive descent parser that reads a stream of characters,
        usually from a provided string and/or a given file, and converts them into a list of
        readable command objects (`CSNadiaLanguageInstruction`).
    """
    _stream = []        # type: List[str]
    _tokens = []        # type: List[CSNadiaLanguageToken]
    _instructions = []  # type: List[CSNadiaLanguageInstruction]
    _parsable = {}      # type: dict[str, Optional[CSNadiaLanguageToken]]
    _binds = {}         # type: dict[str, CSNadiaLanguageCommand]

    @property
    def _can_tokenize(self):
        """Whether the parser can generate more tokens."""
        return len(self._stream) > 0

    @property
    def _can_parse(self):
        """Whether the parser can parse more tokens."""
        return len(self._tokens) > 0

    @staticmethod
    def reserved():
        # type: () -> List[str]
        """Get the list of reserved keywords."""
        return [v.value for v in CSNadiaLanguageKeyword.__members__.values()]

    def _unread_character(self, char):
        """Unread the character and insert it back to the stream."""
        self._stream = [char] + self._stream

    def _next_character(self):
        """Get the next character in the token stream."""
        return self._stream.pop(0)

    def _advance(self):
        # type: (CSNadiaLanguageParser) -> Optional[Dict[str, Optional[CSNadiaLanguageToken]]]
        """Advance the tokens to the next state."""
        prev = self._parsable["previous"]
        curr = self._tokens.pop(0) if self._can_parse else None
        self._parsable = {"previous": prev, "current": curr}
        return self._parsable.copy()

    def _is_keyword(self, key=""):
        """Whether the string is a keyword."""
        return key in [v.value for v in CSNadiaLanguageKeyword.__members__.values()]

    def _is_command(self, keyword):
        """Whether the keyword is a command, either bound or reserved."""
        nonkeys = [CSNadiaLanguageKeyword.CONSTANT,
                   CSNadiaLanguageKeyword.ORIGIN,
                   CSNadiaLanguageKeyword.PLAYER]
        if keyword in self._binds:
            return True
        if not self._is_keyword(keyword):
            return False
        if CSNadiaLanguageKeyword(keyword) in nonkeys:
            return False
        return True

    def __init__(self, lang_input="", **kwargs):
        self._tokens = []
        self._instructions = []
        self._stream = list(lang_input)
        self._parsable = {}  # type: dict[str, Optional[CSNadiaLanguageToken]]
        self._binds = {}
        self._parsable["current"] = None
        self._parsable["previous"] = None

        if "file" in kwargs:
            with open(kwargs["file"], "r") as file_obj:
                self._stream = list(file_obj.read())

        if "bindings" in kwargs:
            for binding in kwargs["bindings"]:
                self._binds[binding] = CSNadiaLanguageCommand(
                    kwargs["bindings"][binding])

    def _next_token(self):
        # type: (CSNadiaLanguageParser) -> Optional[CSNadiaLanguageToken]
        """Generate the next token in the list."""
        state = _CSNadiaLangTokenizerState.START    # type: _CSNadiaLangTokenizerState
        token_type = CSNadiaLanguageTokenType.NONE  # type: CSNadiaLanguageTokenType
        current_token = ""  # type: str
        current_char = ""   # type: str

        if not self._can_tokenize:
            return

        while state not in [_CSNadiaLangTokenizerState.FINISH, _CSNadiaLangTokenizerState.ERROR]:
            if not self._can_tokenize:
                return
            current_char = self._next_character()

            if state == _CSNadiaLangTokenizerState.START:
                if current_char == ";":
                    token_type = CSNadiaLanguageTokenType.COMMENT
                elif current_char == "\"":
                    token_type = CSNadiaLanguageTokenType.STRING
                elif current_char in digits:
                    token_type = CSNadiaLanguageTokenType.NUMBER
                elif current_char in ascii_letters:
                    token_type = CSNadiaLanguageTokenType.IDENTIFIER
                else:
                    token_type = CSNadiaLanguageTokenType.ANY
                current_token += current_char
                state = _CSNadiaLangTokenizerState.IN_PROGRESS
            elif state == _CSNadiaLangTokenizerState.IN_PROGRESS:
                if token_type == CSNadiaLanguageTokenType.COMMENT and current_char == "\n":
                    state = _CSNadiaLangTokenizerState.FINISH
                elif token_type == CSNadiaLanguageTokenType.NUMBER and current_char not in digits:
                    state = _CSNadiaLangTokenizerState.FINISH
                elif token_type == CSNadiaLanguageTokenType.STRING and current_char == "\"":
                    state = _CSNadiaLangTokenizerState.FINISH
                    current_token += current_char
                elif token_type == CSNadiaLanguageTokenType.IDENTIFIER\
                        and current_char not in ascii_letters + "_-":
                    state = _CSNadiaLangTokenizerState.FINISH
                elif token_type == CSNadiaLanguageTokenType.ANY and current_char == "\n":
                    state = _CSNadiaLangTokenizerState.FINISH
                else:
                    current_token += current_char

        if state == _CSNadiaLangTokenizerState.ERROR:
            raise CSNadiaLangTokenizeError(current_token)

        if self._is_keyword(current_token):
            token_type = CSNadiaLanguageTokenType.KEYWORD

        token = CSNadiaLanguageToken(token_type, current_token)
        self._tokens.append(token)
        return token

    def tokenize(self):
        """Tokenize the entire input."""
        while self._can_tokenize:
            self._next_token()
        return self._tokens

    def _parse_command(self):
        # type: (CSNadiaLanguageParser) -> CSNadiaLanguageInstruction
        """Parse a single command and any of its parameters as castable types."""
        command = CSNadiaLanguageCommand.EXIT
        parameters = []
        did_get_binding = False

        if not self._parsable["current"]:
            raise CSNadiaLangParseError("Tokenization may not have occurred.")

        curr = self._parsable["current"]
        if not curr.type == CSNadiaLanguageTokenType.KEYWORD and curr.contents not in self._binds:
            raise CSNadiaLangParseError(
                "Expected a keyword here: %s" % curr.contents)
        if not self._is_command(curr.contents) and curr.contents not in self._binds:
            raise CSNadiaLangParseError(
                "Expected a command: %s" % (curr.contents))
        command = CSNadiaLanguageCommand(
            curr.contents) if curr.contents not in self._binds else self._binds[curr.contents]
        self._advance()

        curr = self._parsable["current"]
        while curr and (not did_get_binding or not self._is_command(curr.contents)):
            if command == CSNadiaLanguageCommand.BIND and self._is_command(curr.contents):
                did_get_binding = True
                parameters.append(CSNadiaLanguageCommand(curr.contents))
            else:
                parameters.append(curr.castable)
            self._advance()
            curr = self._parsable["current"]

        instruct = CSNadiaLanguageInstruction(command, parameters)
        self._instructions.append(instruct)
        return instruct

    def parse(self):
        # type: (CSNadiaLanguageParser) -> List[CSNadiaLanguageInstruction]
        """Parse the list of tokens into a given list of instructions.

        If tokenization has not taken place, this function will try to tokenize the input first.
        """
        if not self._can_parse:
            if not self._can_tokenize:
                return []
            self.tokenize()

        while self._can_parse:
            self._advance()
            curr = self._parsable["current"]
            if curr:
                if curr.type == CSNadiaLanguageTokenType.COMMENT:
                    continue
                elif self._is_command(curr.contents) or curr.contents in self._binds:
                    self._parse_command()
                else:
                    raise CSNadiaLangParseError(
                        "Invalid expression: %s" % (curr.contents))
        return self._instructions

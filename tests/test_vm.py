# coding:utf-8
#
# test_vm.py
# Unscripted Fira
#
# Created by Marquis Kurt on 05/12/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""This test module tests the capabilities of the virtual machine I/O modules"""
import os
from uvn_fira.core import vm


def test_vm_write():
    """Test that the VM writer will write a NadiaVM file."""
    wrt = vm.CSNadiaVMWriter("test.nvm")
    wrt.set(5)
    wrt.set(10)
    wrt.add()
    wrt.write()
    assert os.path.isfile("test.nvm")


def test_vm_write_not_blank():
    """Test that the VM writer will write a NadiaVM file."""
    wrt = vm.CSNadiaVMWriter("test.nvm")
    wrt.set(5)
    wrt.set(10)
    wrt.add()
    wrt.write()

    file = """set constant 5
set constant 10
add
"""
    with open("test.nvm", 'r') as file_obj:
        assert file_obj.read() == file


def test_vm_read_file():
    """Test that the VM reader can read a file."""
    wrt = vm.CSNadiaVMWriter("test.nvm")
    wrt.set(5)
    wrt.set(10)
    wrt.add()
    wrt.write()

    read = vm.CSNadiaVM(path="test.nvm", player_origin=(-1, -1))
    assert isinstance(read, vm.CSNadiaVM)


def test_vm_execute():
    """Test that the VM reader executes a set of instructions."""
    test_vm = vm.CSNadiaVM(interactive=True)

    for ins in ["set constant 10", "set constant 5", "add"]:
        test_vm.input(ins)

    assert 15 in test_vm.get_vm_stack()


def test_vm_player_move():
    """Test that the VM reader sets the player's position correctly."""
    wrt = vm.CSNadiaVMWriter("test.nvm")
    wrt.move("east")
    wrt.write()

    read = vm.CSNadiaVM(path="test.nvm", player_origin=(0, 0))
    read.next()
    assert read.get_position() == (0, 1)

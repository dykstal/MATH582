#! /usr/bin/python3.6
'''
Initialize the Software Testing Container in PyTest.
'''

# PyTest Module
import pytest

def _initialize():
    return True

def test_initialize():
    assert _initialize()

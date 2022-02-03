# coding: utf-8

# https://docs.pytest.org/en/latest/
import pytest

from yabadaba.tools import ModuleManager

def test_ModuleManager():

    manager = ModuleManager('Test')
    assert manager.parentname == 'Test'

    


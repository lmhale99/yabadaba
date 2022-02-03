# coding: utf-8

# https://docs.pytest.org/en/latest/
import pytest

from yabadaba.tools import aslist

def test_aslist():

    # Test single values become lists
    assert aslist('a') == ['a']

    # Test long strings remain together
    assert aslist('abba') == ['abba']

    # Test collections become lists
    assert aslist(('a','b','c')) == ['a', 'b', 'c']
    assert aslist({'a','b','c'}) == ['a', 'b', 'c']
    assert aslist(['a','b','c']) == ['a', 'b', 'c']

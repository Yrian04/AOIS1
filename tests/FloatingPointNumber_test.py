import pytest
from src.FloatingPointNumber import FloatingPointNumber


def test_init():
    f = FloatingPointNumber(-0.12)
    assert f._bits == [True, False, True, True, True, True, False, True,
                       True, True, True, True, False, True, False, True,
                       True, True, False, False, False, False, True, False,
                       True, False, False, False, True, True, True, True]


def test_add():
    f1 = FloatingPointNumber(-0.12)
    f2 = FloatingPointNumber(0.1)
    assert f1 + f2 == FloatingPointNumber(-0.020000003278255462646484375)

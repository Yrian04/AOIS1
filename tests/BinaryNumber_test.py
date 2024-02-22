import pytest
from src.BinaryNumber import BinaryNumber
from src.BinaryNumber import FixedPointNumber
from copy import copy


def test_int():
    n = BinaryNumber(4)
    assert int(n) == 4


def test_addition():
    n1 = BinaryNumber(10)
    n2 = BinaryNumber(5)
    result = n1 + n2
    assert int(result) == 15


def test_subtraction():
    n1 = BinaryNumber(10)
    n2 = BinaryNumber(5)
    result = n1 - n2
    assert int(result) == 5


def test_multiplication():
    n1 = BinaryNumber(10)
    n2 = BinaryNumber(5)
    result = n1 * n2
    assert int(result) == 50


def test_floor_division():
    n1 = BinaryNumber(10)
    n2 = BinaryNumber(3)
    result = n1 // n2
    assert int(result) == 3


def test_floor_division_by_zero():
    n1 = BinaryNumber(10)
    n2 = BinaryNumber(0)
    with pytest.raises(ZeroDivisionError):
        result = n1 // n2


def test_true_division_of_fixed_pointed_numbers():
    f1 = FixedPointNumber(0.25)
    f2 = FixedPointNumber(0.5)
    result = f1 / f2
    assert float(result) == 0.5


def test_true_division_of_fixed_pointed_numbers_by_zero():
    f1 = FixedPointNumber(0.25)
    f2 = FixedPointNumber(0)
    with pytest.raises(ZeroDivisionError):
        result = f1 / f2


def test_true_division_of_binary_numbers():
    f1 = FixedPointNumber(2)
    f2 = FixedPointNumber(4)
    result = f1 / f2
    assert float(result) == 0.5


def test_true_division_of_binary_numbers_by_zero():
    f1 = FixedPointNumber(4)
    f2 = FixedPointNumber(0)
    with pytest.raises(ZeroDivisionError):
        result = f1 / f2


def test_ones_complement_representation():
    n = BinaryNumber(-7, length=4)
    assert n.ones_complement_representation()._bits == [True, False, False, False]


def test_sign_magnitude_representation():
    n = BinaryNumber(-7, length=4)
    assert n.sign_magnitude_representation()._bits == [True, True, True, True]


def test_inc():
    n = BinaryNumber(1)
    n.inc()
    assert n == BinaryNumber(2)


def test_dec():
    n = BinaryNumber(1)
    n.dec()
    assert n == BinaryNumber(0)


def test_to_fixed_point():
    b = BinaryNumber(pow(2, 32))
    assert b.to_fixed_point() == FixedPointNumber(1)


def test_copy():
    b = BinaryNumber(1)
    assert copy(b) == BinaryNumber(1)


def test_lshift():
    b = BinaryNumber(-1)
    assert b << 1 == BinaryNumber(-1 << 1)


def test_rshift():
    b = BinaryNumber(-1)
    assert b >> 1 == BinaryNumber(-1 >> 1)


if __name__ == "__main__":
    pytest.main()

from copy import copy
from src.BinaryNumber import BinaryNumber
from src.BinaryNumber import FixedPointNumber


class FloatingPointNumber:
    length = 32
    exponent = 8
    shift = 127

    def __init__(self, number: float = 0.):
        self._bits = [False] * self.length

        if number == 0:
            return

        sign = number < 0
        number = abs(number)

        exponent = self.shift
        while number > 2:
            number /= 2
            exponent += 1
        while number < 1:
            number *= 2
            exponent -= 1

        for i in range(self.exponent + 1, self.length):
            self[i] = (number := number * 2) >= 1
            if self[i]:
                number %= 1

        self[-1] = False
        self[0] = sign

        for i in range(self.exponent, 0, -1):
            self[i] = exponent % 2 == 1
            exponent //= 2

    def __getitem__(self, item: int):
        return self._bits[item]

    def __setitem__(self, key: int, value: bool):
        self._bits[key] = value

    def __str__(self):
        result = ""
        for i in self._bits:
            result += str(int(i))
        return result[0] + "s" + result[1:self.exponent+1] + "e" + result[self.exponent+1:]

    def get_exponent(self) -> BinaryNumber:
        result = BinaryNumber(length=self.exponent)
        for i in range(1, self.exponent + 1):
            result[i - 1] = self[i]
        return result

    def get_mantissa(self) -> BinaryNumber:
        result = FixedPointNumber(length=(self.length - self.exponent - 1) * 2 + 1,
                                  point=self.length - self.exponent - 1)
        for i in range(1 + self.exponent, self.length):
            result[i - self.exponent + 1] = self[i]
        result[1] = True
        result >>= self.length - self.exponent - 2
        result[0] = self[0]
        if result[0]:
            result[1:] = map(lambda b: not b, result[1:])
            result.inc()
        return result

    def __copy__(self):
        result = FloatingPointNumber()
        result._bits = self._bits[:]
        return result

    def __add__(self, other):
        first_exponent = self.get_exponent()
        first_mantissa = self.get_mantissa()
        second_exponent = other.get_exponent()
        second_mantissa = other.get_mantissa()

        while first_exponent < second_exponent:
            first_exponent.inc()
            first_mantissa >>= 1
        while first_exponent > second_exponent:
            second_exponent.inc()
            second_mantissa >>= 1

        result = FloatingPointNumber()
        exponent = first_exponent
        mantissa = (first_mantissa + second_mantissa).sign_magnitude_representation()
        result[0] = mantissa[0]
        count = 1
        mantissa <<= 1
        while not mantissa[0]:
            mantissa <<= 1
            count += 1
        if count < result.length - result.exponent - 1:
            exponent.inc()
        elif count > result.length - result.exponent - 1:
            exponent.dec()
        for i in range(1 + result.exponent, result.length):
            result[i] = mantissa[i - result.exponent]
        for i in range(1, result.exponent + 1):
            result[i] = exponent[i - 1]

        return result

    def __neg__(self):
        result = copy(self)
        result[0] = not result[0]
        return result

    def __sub__(self, other):
        return self + -other

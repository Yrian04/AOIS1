from copy import copy


class BinaryNumber:

    def __init__(self, value: int = 0, *, length=64):
        self.length = length
        self._bits = [False] * self.length
        self._bits[0] = value < 0
        value = abs(value)
        i = self.length - 1
        while value > 1:
            self._bits[i] = value % 2 == 1
            value //= 2
            i -= 1
        self._bits[i] = value == 1
        if self._bits[0]:
            self._bits[1:] = map(lambda b: not b, self._bits[1:])
            self.inc()

    def inc(self):
        for i in range(self.length - 1, -1, -1):
            self[i] = not self[i]
            if self[i]:
                break

    def dec(self):
        for i in range(self.length - 1, -1, -1):
            self[i] = not self[i]
            if not self[i]:
                break

    def __str__(self):
        result = ""
        for bit in self._bits:
            result += int(bit).__str__()
        return result

    def ones_complement_representation(self):
        if not self[0]:
            return copy(self)
        result = copy(self)
        result.dec()
        return result

    def sign_magnitude_representation(self):
        if not self[0]:
            return copy(self)
        result = self.ones_complement_representation()
        result._bits[1:] = map(lambda b: not b, result._bits[1:])
        return result

    def __getitem__(self, item: int):
        return self._bits[item]

    def __setitem__(self, key: int, value: bool):
        self._bits[key] = value

    def __add__(self, other):
        result = BinaryNumber(length=self.length)
        flag = False
        for i in range(result.length - 1, -1, -1):
            result[i] = flag != (self[i] != other[i])
            flag = ((self[i] and other[i]) or
                    (self[i] and flag) or
                    (other[i] and flag))
        return result

    def __neg__(self):
        result = BinaryNumber(length=self.length)
        result._bits[:] = map(lambda b: not b, self._bits)
        result.inc()
        return result

    def __sub__(self, other):
        return self + (-other)

    def _rsh(self, *, bit=False):
        for i in range(self.length - 1, 0, -1):
            self[i] = self[i - 1]
        self[0] = bit

    def _lsh(self, *, bit=False):
        for i in range(self.length - 1):
            self[i] = self[i + 1]
        self[-1] = bit

    def __mul__(self, other):
        if not isinstance(other, BinaryNumber):
            raise Exception
        second = copy(other)
        result = BinaryNumber(length=self.length)
        for i in range(1, result.length + 1):
            if self[-i]:
                result += second
            second._lsh()
        return result

    def __abs__(self):
        if self[0]:
            return -self
        result = BinaryNumber(length=self.length)
        result._bits = self._bits.copy()
        return result

    def __lt__(self, other):
        return (diff := self - other)[0] and any(diff)

    def __ge__(self, other):
        return not self < other

    def __gt__(self, other):
        return not (diff := self - other)[0] and any(diff)

    def __le__(self, other):
        return not self > other

    def __eq__(self, other):
        return not any(self - other)

    def __ne__(self, other):
        return not self == other

    def to_fixed_point(self, *, point=31):
        result = FixedPointNumber(length=self.length, point=point)
        result._bits = self._bits[:]
        return result

    def __copy__(self):
        result = BinaryNumber(length=self.length)
        result._bits = self._bits[:]
        result.length = self.length
        return result

    def __floordiv__(self, other):
        if not any(other._bits):
            raise ZeroDivisionError()
        if self[0]:
            return -(abs(self) // other)
        if other[0]:
            return -(self // abs(other))

        result = BinaryNumber(length=self.length)
        dividend = copy(self)
        divisor = copy(other)

        bits_number_of_result = 1
        while not divisor[1]:
            divisor._lsh()
            bits_number_of_result += 1

        while bits_number_of_result != 0:
            result._lsh(bit=not (diff := dividend - divisor)[0])
            if not diff[0]:
                dividend = diff
            divisor._rsh()
            bits_number_of_result -= 1

        return result

    def __lshift__(self, other: int):
        result = copy(self)
        for i in range(other):
            result._lsh()
        return result

    def __rshift__(self, other: int):
        result = copy(self)
        for i in range(other):
            result._rsh(bit=result[0])
        return result

    def __truediv__(self, other):
        return FixedPointNumber(binary=self) / FixedPointNumber(binary=other)

    def __int__(self) -> int:
        number = self.sign_magnitude_representation()
        result = 0
        for i in range(number.length - 1):
            if number[-i - 1]:
                result += pow(2, i)
        if number[0]:
            result *= -1
        return result




class FixedPointNumber(BinaryNumber):

    def __init__(self, value: float = 0., *,
                 binary=None,
                 point=31,
                 length=64):
        super().__init__(length=length)
        self.point = point

        if isinstance(binary, BinaryNumber):
            self._bits = binary._bits.copy()
            self.length = binary.length
            self.point = point
            for i in range(self.length - self.point - 1):
                self._lsh()
            return

        self[0] = value < 0
        value = abs(value)

        integer_part = int(value // 1)
        fractional_part = value % 1

        i = 0
        while integer_part >= 1:
            self[self.point - i] = integer_part % 2 == 1
            integer_part //= 2
            i += 1

        i = 1
        while fractional_part != 0 and i != self.length - self.point - 1:
            fractional_part *= 2
            self[self.point + i] = fractional_part >= 1
            fractional_part %= 1
            i += 1

        if self[0]:
            self._bits[1:] = map(lambda b: not b, self._bits[1:])
            self.inc()

    def __str__(self):
        result = ""
        for b in self._bits:
            result += int(b).__str__()
        return result[:self.point + 1] + "." + result[self.point + 1:]

    def __add__(self, other):
        return super().__add__(other).to_fixed_point(point=self.point)

    def __sub__(self, other):
        return super().__sub__(other).to_fixed_point(point=self.point)

    def __neg__(self):
        return super().__neg__().to_fixed_point(point=self.point)

    def __mul__(self, other):
        return super().__mul__(other).to_fixed_point(point=self.point)

    def __abs__(self):
        return super().__abs__().to_fixed_point(point=self.point)

    def __lshift__(self, other: int):
        return super().__lshift__(other)

    def __rshift__(self, other: int):
        return super().__rshift__(other)

    def length_of_frac_path(self):
        return self.length - self.point - 1

    def integer_part(self):
        result = BinaryNumber()
        result._bits = self._bits[:]
        return result >> self.length_of_frac_path()

    def __copy__(self):
        result = FixedPointNumber(length=self.length, point=self.point)
        result._bits = self._bits[:]
        return result

    def __truediv__(self, other):
        if not any(other._bits):
            raise ZeroDivisionError()
        if self[0]:
            return -(abs(self) / other)
        if other[0]:
            return -(self / abs(other))

        result = BinaryNumber()
        dividend = copy(self)
        divisor = copy(other)

        bits_number_of_result = 1 + self.length_of_frac_path()
        while not divisor[1]:
            divisor._lsh()
            bits_number_of_result += 1

        while bits_number_of_result != 0:
            if int(divisor) == 0:
                break
            result._lsh(bit=not (diff := dividend - divisor)[0])
            if not diff[0]:
                dividend = diff
            divisor._rsh()
            bits_number_of_result -= 1

        while bits_number_of_result != 0:
            result._lsh()
            bits_number_of_result -= 1

        return result.to_fixed_point(point=self.point)

    def __float__(self):
        result = 0
        number = self.sign_magnitude_representation()
        for i in range(self.length - 1):
            if self[-i - 1]:
                result += pow(2, i - self.length_of_frac_path())
        if number[0]:
            result *= -1
        return result

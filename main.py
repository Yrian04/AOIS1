from src.FloatingPointNumber import FloatingPointNumber
from src.BinaryNumber import BinaryNumber
from src.BinaryNumber import FixedPointNumber


def output(name, value):
    print(f"\n{name}:\nПрямой код: \t\t{value.sign_magnitude_representation()}")
    print(f"Обратный код: \t\t{value.ones_complement_representation()}")
    print(f"Дополнительный код:\t{value}")


a = int(input("Введите первое число: "))
b = int(input("Введите второе число: "))

first = BinaryNumber(a)
second = BinaryNumber(b)

output(a, first)
output(b, second)
output(f"{int(first)} + {int(second)} = {int(first + second)}", first + second)
output(f"{int(first)} - {int(second)} = {int(first - second)}", first - second)
output(f"{int(first)} * {int(second)} = {int(first * second)}", first * second)
output(f"{int(first)} / {int(second)} = "
       f"{float(FixedPointNumber(binary=first, point=58) / FixedPointNumber(binary=second, point=58))}",
       FixedPointNumber(binary=first, point=58) / FixedPointNumber(binary=second, point=58))

float1 = FloatingPointNumber(a)
print(f"\n{float(a)}:")
print(float1)

float2 = FloatingPointNumber(b)
print(f"\n{float(b)}:")
print(float2)

result = float1 + float2
print(f"\n{float(float1)} + {float(float2)} = {float(result)}:\n{result}")

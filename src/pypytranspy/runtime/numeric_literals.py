from typing import Callable
import math


def underscore_literal_format(value, conversion: Callable, format_spec: str) -> str:
    def format_int(value_str: str) -> str:
        new_value = ""
        value_str_len = len(value_str)

        for i in range(value_str_len):
            if i > 0 and i % 3 == 0:
                new_value = "_" + new_value

            new_value = value_str[value_str_len - i - 1] + new_value

        return new_value

    def format_hex(value: int, upper: bool = False) -> str:
        value_str = hex(value)
        new_value = ""
        value_str_len = len(value_str)

        for i in range(value_str_len - 2):  # Skip 0x prefix
            if i > 0 and i % 4 == 0:
                new_value = "_" + new_value

            print(value_str_len, i)
            new_value = value_str[value_str_len - i - 1] + new_value

        if upper:
            new_value = new_value.upper()

        return "0x" + new_value

    if isinstance(value, int):
        # Format ints
        if format_spec.lower().endswith("x"):
            new_value = format_hex(value, upper=format_spec[-1] == "X")
            format_spec = format_spec[:-1]
        else:
            new_value = format_int(conversion(value))
    elif isinstance(value, float):
        # Format floats
        fraction, integer = math.modf(value)

        if integer != 0:
            integer_str = format_int(conversion(math.trunc(integer)))
            fraction_str = conversion(abs(fraction))[1:]

            new_value = integer_str + fraction_str
        else:
            new_value = conversion(fraction)
    else:
        # Other formats
        new_value = conversion(value)

    if format_spec:
        format_string = "{:" + format_spec + "}"

        return format_string.format(new_value)
    else:
        return new_value

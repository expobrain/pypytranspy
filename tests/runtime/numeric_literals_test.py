import pytest

from runtime import underscore_literal_format


@pytest.mark.parametrize(
    "value, conversion, format_spec, expected",
    (
        # Hexadecimal
        (0xFFFFFF, str, "X", "0xFF_FFFF"),
        (0xFFFFFF, str, "x", "0xff_ffff"),
        # Decimal
        (1000000, str, "", "1_000_000"),
        (-1000000, str, "", "-1_000_000"),
        (1000.5, str, "", "1_000.5"),
        (-1000.5, str, "", "-1_000.5"),
        (0.5, str, "", "0.5"),
        (-0.5, str, "", "-0.5"),
        # Conversions
        ("a", str, "", "a"),
        ("a", ascii, "", "'a'"),
        ("a", repr, "", "'a'"),
    ),
)
def test_underscore_literal_format(value, conversion, format_spec, expected):
    result = underscore_literal_format(value, conversion, format_spec)

    assert result == expected

import pytest

from pypytranspy.transformations.string_format import StringFormat
from pypytranspy.transformations.underscore_numeric_literals_transformer import (
    parse_string_format_iter,
)

# -----------------------------------
# parse_string_format_iter
# -----------------------------------


@pytest.mark.parametrize(
    "format_string, expected",
    (
        #  Single
        ("{}", [(0, 1, StringFormat())]),
        ("{name}", [(0, 5, StringFormat("name"))]),
        ("{name!r}", [(0, 7, StringFormat("name", "r"))]),
        ("{name:x}", [(0, 7, StringFormat("name", None, "x"))]),
        ("{name!r:x}", [(0, 9, StringFormat("name", "r", "x"))]),
        #  Multiple
        ("{}{}", [(2, 3, StringFormat()), (0, 1, StringFormat())]),
        ("{first}{name}", [(7, 12, StringFormat("name")), (0, 6, StringFormat("first"))]),
    ),
)
def test_parse_string_format_iter(format_string, expected):
    results = list(parse_string_format_iter(format_string))

    assert results == expected


@pytest.mark.parametrize("string", (["\{\}"], ["\{"], ["\{name}"]))
def test_parse_escaped_string_format_iter(string):
    results = list(parse_string_format_iter(string))

    assert len(results) == 0

import pytest

from transformations.string_format import StringFormat


@pytest.mark.parametrize(
    "left, right, equal",
    [(StringFormat(), StringFormat(), True), (StringFormat("name"), StringFormat(), False)],
)
def test_string_format_equality(left, right, equal):
    if equal:
        assert left == right
    else:
        assert left != right


@pytest.mark.parametrize(
    "format_string, expected",
    (
        (StringFormat(), "{}"),
        (StringFormat("name"), "{name}"),
        (StringFormat("name", "r"), "{name!r}"),
        (StringFormat("name", None, "x"), "{name:x}"),
        (StringFormat("name", "r", "x"), "{name!r:x}"),
    ),
)
def test_string_format_to_string(format_string, expected):
    assert str(format_string) == expected


@pytest.mark.parametrize(
    "format_string, expected",
    (
        (StringFormat(), StringFormat()),
        (StringFormat("name"), StringFormat("name")),
        (StringFormat("name", "r"), StringFormat("name", "r")),
        (StringFormat("name", None, "_x"), StringFormat("name", None, "x")),
        (StringFormat("name", "r", "_x"), StringFormat("name", "r", "x")),
        (StringFormat(format_spec="_x"), StringFormat(format_spec="x")),
    ),
)
def test_string_format_transform(format_string, expected):
    assert format_string.transform() == expected

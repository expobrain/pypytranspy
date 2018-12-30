import ast

import pytest
import astor

from transformations import UnderscoreNumericLiteralsTransformer


@pytest.mark.parametrize(
    "source, expected",
    (
        # Literals
        ("1_000_000", "1000000"),
        ("0x_FF_FF", "0xffff"),
        # Literals formatting
        ('"formatted {:x}".format(n)', '"formatted {:x}".format(n)'),
        (
            '"formatted {:_x}".format(n)',
            '"formatted {}".format(pypytranspy.runtime.underscore_literal_format(n, str, "x"))',
        ),
        (
            '"formatted {!r:_x}".format(n)',
            '"formatted {}".format(pypytranspy.runtime.underscore_literal_format(n, repr, "x"))',
        ),
        (
            '"formatted {!a:_x}".format(n)',
            '"formatted {}".format(pypytranspy.runtime.underscore_literal_format(n, ascii, "x"))',
        ),
        # Non-format string calls
        ('"".upper()', '"".upper()'),
    ),
)
def test_underscore_numeric_literals(source, expected):
    source_ast = ast.parse(source)

    print(astor.dump_tree(source_ast))
    print(astor.dump_tree(ast.parse(expected)))

    UnderscoreNumericLiteralsTransformer(source_ast)
    print(astor.dump_tree(source_ast))

    result = astor.to_source(source_ast)
    expected_gen = astor.to_source(ast.parse(expected))

    assert result == expected_gen

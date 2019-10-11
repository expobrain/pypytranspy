import ast

import astor
import pytest

from pypytranspy.transformations import FStringToFormatTransformer


@pytest.mark.parametrize(
    "source ,expected",
    [
        ('"The answer {}!""".format(42)', '"The answer {}!".format(42)'),  # no=op
        ('f"The answer {value}!"', '"The answer {}!".format(value)'),
        ('f"The answer {42}!"', '"The answer {}!".format(42)'),
        ('f"formatted {n:x} value"', '"formatted {:x} value".format(n)'),
    ],
)
def test_fstring_to_format(source, expected):
    source_ast = ast.parse(source)

    print(astor.dump_tree(source_ast))
    print(astor.dump_tree(ast.parse(expected)))

    FStringToFormatTransformer(source_ast)
    print(astor.dump_tree(source_ast))

    result = astor.to_source(source_ast)
    expected_gen = astor.to_source(ast.parse(expected))

    assert result == expected_gen

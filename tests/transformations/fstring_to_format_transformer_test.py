import ast

import pytest
import astor

from transformations import FStringToFormatTransformer


@pytest.mark.parametrize(
    "source ,expected",
    [
        ('"The answer {}!""".format(42)', '"The answer {}!".format(42)'),  # no=op
        ('f"The answer {value}!"', '"The answer {}!".format(value)'),
        ('f"The answer {42}!"', '"The answer {}!".format(42)'),
    ],
)
def test_fstring_to_format(source, expected):
    source_ast = ast.parse(source)

    FStringToFormatTransformer(source_ast)

    result = astor.to_source(source_ast)
    expected_gen = astor.to_source(ast.parse(expected))

    assert result == expected_gen
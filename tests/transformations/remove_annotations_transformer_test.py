import ast

import astor
import pytest

from pypytranspy.transformations import RemoveAnnotationsTransformer


@pytest.mark.parametrize(
    "source, expected",
    [
        # Function defs
        ("def foo(a, b=5): pass", "def foo(a, b=5): pass"),  # no-op
        ("def foo(a: int, b: int = 5): pass", "def foo(a, b=5): pass"),
        ("def foo(*args: int, **kwargs: str): pass", "def foo(*args, **kwargs): pass"),
        ("def sum() -> int: pass", "def sum(): pass"),
        # Assignments
        ("a = 42", "a = 42"),  # no-op
        ("a, b = 1, 2", "a, b = 1, 2"),  # no-op
        ("a: int = 42", "a = 42"),
        # Import typing package
        ("import typing", ""),
        ("from typing import List", ""),
    ],
)
def test_remove_annotations(source, expected):
    source_ast = ast.parse(source)

    print(astor.dump_tree(source_ast))
    print(astor.dump_tree(ast.parse(expected)))

    RemoveAnnotationsTransformer(source_ast)

    result = astor.to_source(source_ast)
    expected_gen = astor.to_source(ast.parse(expected))

    assert result == expected_gen

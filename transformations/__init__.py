from typing import Iterable

import ast

from .fstring_to_format_transformer import FStringToFormatTransformer
from .remove_annotations_transformer import RemoveAnnotationsTransformer
from .underscore_numeric_literals_transformer import UnderscoreNumericLiteralsTransformer


def get_transformations() -> Iterable[ast.AST]:
    return (
        FStringToFormatTransformer,
        RemoveAnnotationsTransformer,
        UnderscoreNumericLiteralsTransformer,
    )

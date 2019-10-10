from typing import Iterable
import ast

from pypytranspy.transformations.fstring_to_format_transformer import FStringToFormatTransformer
from pypytranspy.transformations.remove_annotations_transformer import RemoveAnnotationsTransformer
from pypytranspy.transformations.underscore_numeric_literals_transformer import (
    UnderscoreNumericLiteralsTransformer,
)


def get_transformations() -> Iterable[ast.AST]:
    return (
        FStringToFormatTransformer,
        RemoveAnnotationsTransformer,
        UnderscoreNumericLiteralsTransformer,
    )

from pathlib import Path
from typing import Iterable, Optional, Set
import ast
import inspect

from pypytranspy.transformations.fstring_to_format_transformer import FStringToFormatTransformer
from pypytranspy.transformations.remove_annotations_transformer import RemoveAnnotationsTransformer
from pypytranspy.transformations.underscore_numeric_literals_transformer import (
    UnderscoreNumericLiteralsTransformer,
)

ALL_TRANSFORMATIONS = (
    FStringToFormatTransformer,
    RemoveAnnotationsTransformer,
    UnderscoreNumericLiteralsTransformer,
)


def get_transformations(transformations: Optional[Set[str]] = None) -> Iterable[ast.AST]:
    if transformations:
        return set(
            t for t in ALL_TRANSFORMATIONS if Path(inspect.getfile(t)).stem in transformations
        )
    else:
        return set(ALL_TRANSFORMATIONS)

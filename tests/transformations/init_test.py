from pathlib import Path
from typing import Optional, Set
import inspect

import pytest

from pypytranspy.transformations import ALL_TRANSFORMATIONS, get_transformations


@pytest.mark.parametrize(
    "transformations, expected",
    [
        [None, set(ALL_TRANSFORMATIONS)],
        [set([Path(inspect.getfile(ALL_TRANSFORMATIONS[0])).stem]), set([ALL_TRANSFORMATIONS[0]])],
    ],
)
def test_get_transformations(transformations: Optional[Set[str]], expected: Set[set]):
    result = get_transformations(transformations)

    assert result == expected

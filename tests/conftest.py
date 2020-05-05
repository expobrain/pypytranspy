from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from pypytranspy.cli import Context
from pypytranspy.transformations import ALL_TRANSFORMATIONS


@pytest.fixture
def context() -> Context:
    with TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        context = Context(tmp_path / "src", tmp_path / "out", ALL_TRANSFORMATIONS)

        context.src_path.mkdir(parents=True, exist_ok=True)
        context.out_path.mkdir(parents=True, exist_ok=True)

        yield context

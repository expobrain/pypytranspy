from pathlib import Path
from unittest.mock import patch

from pypytranspy.cli import Context, transpile_dir


def test_transpile_dir_excludes_out_path(context: Context):
    context.out_path = context.src_path / "out"

    context.out_path.mkdir(parents=True, exist_ok=True)

    with patch(f"{transpile_dir.__module__}.{transpile_dir.__name__}") as m_transpile:
        transpile_dir(context, Path("."))

        assert m_transpile.call_args is None

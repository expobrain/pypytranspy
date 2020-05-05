from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pypytranspy.cli import transpile_dir


def test_transpile_dir_excludes_out_path():
    with TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        src_path = tmp_path / "src"
        out_path = tmp_path / "src" / "out"

        out_path.mkdir(parents=True)

        with patch(f"{transpile_dir.__module__}.{transpile_dir.__name__}") as m_transpile:
            transpile_dir(src_path, out_path)

            assert m_transpile.call_args is None

from pathlib import Path
from typing import List, Optional
import logging

import astor
import click

from pypytranspy.transformations import get_transformations

logger = logging.getLogger("pypytranspy")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class TranspileException(Exception):
    pass


def transpile_dir(dir_src: Path, out_dir: Path):
    for item in dir_src.iterdir():
        # Skip if same as out dir
        if item == out_dir:
            continue

        # Transpile file
        if item.is_file() and item.suffix == ".py":
            logger.info("Transpiling %s ...", item)

            try:
                transpile_file(item, out_dir)
            except TranspileException as e:
                logger.error(f"Cannot transpile {item}: {e}")
                continue

        # Transpile dir
        elif item.is_dir():
            child_out_dir = out_dir / item.parts[-1]
            child_out_dir.mkdir(exist_ok=True)

            transpile_dir(item, child_out_dir)

        # Anything else
        else:
            logger.warning("Skipping %s ...", item)


def transpile_file(filename_src: Path, out_dir: Path):
    # Setup destination file
    filename_dest = out_dir / filename_src.name

    logger.info(f"Transpiling file {filename_src} into {filename_dest}")

    # Parse AST
    try:
        source_ast = astor.parse_file(filename_src)
    except Exception as e:
        raise TranspileException(e)

    # Apply transformations
    for transformation in get_transformations():
        transformation(source_ast)

    source = astor.to_source(source_ast)

    # Save file
    with open(filename_dest, "w") as f:
        f.write(source)


@click.command()
@click.option(
    "--transformation",
    "-t",
    "transformations",
    help="Transformation to be applied. It can be specified multiple times. Order does matter.",
)
@click.argument("src_dir", type=click.Path(exists=True, resolve_path=True))
@click.argument("out_dir", type=click.Path(exists=True, resolve_path=True, writable=True))
def main(src_dir: str, out_dir: str, transformations: Optional[List[str]] = None):
    src_path = Path(src_dir)
    out_path = Path(out_dir)

    if src_path.is_dir():
        # Check that out dir is not inside src dir
        if out_path in src_path.parents:
            logger.error(f"Output directory {out_path} is inside source directory {src_path}")
            exit(1)

        # Transpile directory content
        transpile_dir(src_path, out_path)
    elif src_path.is_file():
        transpile_file(src_path, out_path)
    else:
        logger.error(f"The path {src_path} is neither a directory nor a file")

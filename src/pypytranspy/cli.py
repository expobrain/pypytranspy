from pathlib import Path
from typing import List, Optional, Set
import dataclasses
import logging

import libcst as cst
from libcst.tool import dump
import click

logger = logging.getLogger("pypytranspy")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


@dataclasses.dataclass
class Context:
    src_path: Path
    out_path: Path
    transformations: Set[str]


class TranspileException(Exception):
    pass


def transpile_dir(context: Context, relative_path: Path):
    current_path = context.src_path / relative_path

    for item_path in current_path.iterdir():
        # Skip if same as out dir
        if item_path == context.out_path:
            continue

        # Transpile file
        if item_path.is_file() and item_path.suffix == ".py":
            # try:
            transpile_file(context, item_path)
            # except TranspileException as e:
            #     logger.error(f"Cannot transpile {item_path}: {e}")
            #     continue

        # Transpile dir
        elif item_path.is_dir():
            transpile_dir(context, item_path)

        # Anything else
        else:
            logger.warning("Skipping %s ...", item_path)


def transpile_file(content: Context, filename: Path):
    # Setup destination file
    # filename_src = content.src_path / relative_filename.name
    # filename_dest = content.out_path / relative_filename.name
    filename_src = filename_dest = filename

    logger.info(f"Transpiling file {filename_src} ...")

    # Parse AST
    original_src = filename_src.read_text()
    original_ast = cst.parse_module(original_src)

    # Apply transformations
    # for transformation in get_transformations():
    #     transformation(original_ast)

    source = original_ast.code

    # Create dirs if necessary
    filename_dest.parent.mkdir(parents=True, exist_ok=True)

    # Save file
    filename_dest.write_text(source)


@click.command()
@click.option(
    "--transformation",
    "-t",
    "transformations",
    help="Transformation to be applied. It can be specified multiple times. Order does matter.",
)
@click.argument("src_dir", type=click.Path(exists=True, resolve_path=True))
# @click.argument("out_dir", type=click.Path(exists=True, resolve_path=True, writable=True))
def main(src_dir: str, transformations: Optional[List[str]] = None):
    context = Context(Path(src_dir), Path(src_dir), set(transformations or []))

    if context.src_path.is_dir():
        # Check that out dir is not inside src dir
        if context.out_path in context.src_path.parents:
            logger.error(
                f"Output directory {context.out_path} is inside source directory {context.src_path}"
            )
            exit(1)

        # Transpile directory content
        transpile_dir(context, Path("."))
    elif context.src_path.is_file():
        transpile_file(context, context.src_path)
    else:
        logger.error(f"The path {context.src_path} is neither a directory nor a file")

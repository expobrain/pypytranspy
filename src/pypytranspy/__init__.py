from optparse import OptionParser
from pathlib import Path
import logging

import astor

from pypytranspy.transformations import get_transformations

logger = logging.getLogger("pypytranspy")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class TranspileException(Exception):
    pass


def transpile_dir(dir_src: Path, out_dir: Path):
    for item in dir_src.iterdir():
        if item.is_file() and item.suffix == ".py":
            try:
                transpile_file(item, out_dir)
            except TranspileException as e:
                logger.warning(f"Cannot transpile {item}: {e}")
                continue
        elif item.is_dir():
            child_out_dir: Path = out_dir / item.parts[-1]
            child_out_dir.mkdir(exist_ok=True)

            transpile_dir(item, child_out_dir)


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


def main():
    # Parse CLI arguments
    parser = OptionParser()
    parser.add_option(
        "-o", "--out", dest="out_dir", help="Output directory of the transpiled files"
    )

    (options, args) = parser.parse_args()

    # Check src path
    if len(args) != 1:
        logger.error("Need one file or directory as source")

    src = Path(args[0]).absolute()

    # Check out dir
    if options.out_dir is None:
        logger.error("Option `out_dir` is null")
        exit(1)

    out_dir = Path(options.out_dir).absolute()

    if not out_dir.exists():
        logger.error(f"Directory {out_dir} does not exists")
        exit(1)

    # Start transpilation
    if not src.exists():
        logger.error(f"Path {src} does not exist")
        exit(1)

    if src.is_dir():
        # Check that out dir is not inside src dir
        if out_dir in src.parents:
            logger.error(f"Output directory {out_dir} is inside source directory {src}")
            exit(1)

        # Transpile directory content
        transpile_dir(src, out_dir)
    elif src.is_file():
        transpile_file(src, out_dir)
    else:
        logger.error(f"The path {src} is neither a directory nor a file")


if __name__ == "__main__":
    main()

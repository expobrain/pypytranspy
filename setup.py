from pathlib import Path

import setuptools
from pkg_resources import parse_version

from setuptools import setup, find_packages

setup(
    name="pypytranspy",
    version="0.1.0",
    keywords="python javascript transpilation",
    author="Daniele Esposti",
    author_email="daniele.esposti@gmail.com",
    url="https://github.com/expobrain/pypytranspy",
    packages=find_packages(exclude=["tests", "tests.*"]),
    entry_points={"console_scripts": ["pypytranspy = pypytranspy:main"]},
    python_requires=">=3",
    license="MIT",
    install_requires=["astor>=0.8.0"],
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
)

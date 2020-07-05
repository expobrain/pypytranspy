from pathlib import Path

from setuptools import find_namespace_packages, setup

setup(
    name="pypytranspy",
    version="0.1.0",
    keywords="python javascript transpilation",
    author="Daniele Esposti",
    author_email="daniele.esposti@gmail.com",
    url="https://github.com/expobrain/pypytranspy",
    packages=find_namespace_packages(where="src"),
    entry_points={"console_scripts": ["pypytranspy = pypytranspy.cli:main"]},
    python_requires=">=3.6",
    license="MIT",
    package_dir={"": "src"},
    install_requires=["libcst~=0.3.7", "Click~=7.0", "dataclasses~=0.7;python_version<'3.7'"],
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
)

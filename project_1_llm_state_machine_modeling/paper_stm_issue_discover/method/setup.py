"""Compatibility setuptools metadata for method-release build frontends."""

from setuptools import find_packages, setup


setup(
    name="paper-stm-method",
    version="0.60.0",
    description="Typed evidence-discovery method for state-machine issue finding.",
    package_dir={"": "src"},
    packages=find_packages("src", include=("paper_stm_method*", "utils*")),
    package_data={"paper_stm_method": ["resources/*.json"]},
    entry_points={"console_scripts": ["paper-stm-method=paper_stm_method.cli:main"]},
)

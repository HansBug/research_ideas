"""Compatibility setuptools metadata for method-release build frontends."""

from setuptools import find_packages, setup


setup(
    name="paper-stm-method",
    version="0.60.0",
    description="Typed evidence-discovery method for state-machine issue finding.",
    python_requires=">=3.10",
    install_requires=(
        "pydantic>=2.10,<3",
        "PyYAML>=6.0",
        "httpx>=0.28,<1",
        "genai-prices==0.1.3",
        "langchain==1.3.4",
        "langchain-openai==1.2.2",
        "openai==2.41.0",
        "pyfcstm @ git+https://github.com/HansBug/pyfcstm.git@901f30e981c29eb8e304b33d61985652d2e85b2e",
    ),
    extras_require={"test": ("pytest>=8,<10",)},
    package_dir={"": "src"},
    packages=find_packages("src", include=("paper_stm_method*", "utils*")),
    package_data={"paper_stm_method": ["resources/*.json"]},
    entry_points={"console_scripts": ["paper-stm-method=paper_stm_method.cli:main"]},
)

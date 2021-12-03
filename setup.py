"""
if you run "pip install .", this will be used to install this repo
"""

from setuptools import find_packages, setup

setup(
    name="pycore",
    version='21.12.3',
    packages=find_packages(exclude=("tests", "docs")),
    description="Useful python functions and tools",
    url="https://github.com/sg-s/pycore/",
    author="Srinivas Gorur-Shandilya",
    author_email="code@srinivas.gs",
    install_requires=[
        "pandas>=1.3.2",
        "matplotlib>=3.4.3",
        "numpy>=1.20.3",
        "scipy>=1.7.1",
    ],
)

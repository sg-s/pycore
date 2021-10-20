"""
if you run "pip install .", this will be used to install this repo
"""

from setuptools import setup, find_packages

setup(
    name='pycore',
    version='21.10.20',
    packages=find_packages(exclude=('tests', 'docs')),
    description='Useful python functions and tools',
    url='URL',
    author='Srinivas Gorur-Shandilya',
    author_email='code@srinivas.gs',
    install_requires=[
        'pandas>=1.3.2',
        'matplotlib>=3.4.3',
        'numpy>=1.20.3',
        'scipy>=1.7.1',
    ],
)

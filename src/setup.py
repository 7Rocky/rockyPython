from codecs import open
from os import path
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rockyPython',
    version='1.0.0',
    description='Hello World app for running Python apps on Bluemix',
    long_description=long_description,
    url='https://github.com/7Rocky/rockypython',
    license='ISC'
)

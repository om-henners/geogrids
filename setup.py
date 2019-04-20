import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


def get_requirements():
    for line in open('requirements.txt'):
        yield line.strip()


setup(
    name="geogrids",
    version="1.0.1",
    url="https://github.com/om-henners/geogrids",
    license='WTFPL',

    author="Henry Walshaw",
    author_email="henry.walshaw@gmail.com",

    description="A Python implementation of the npm geogrids library - utilities for working with Global Discrete Geodetic Grids (GDGGs)",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),

    install_requires=get_requirements(),

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: GIS'
    ],
)

"""geogrids

A Python implementation of the npm geogrids library by Iván Sánchez Ortega -
utilities for working with Global Discrete Geodetic Grids (GDGGs)
"""
from . import gdgg
from . import encoders

__version__ = '1.0.1'
__author__ = 'Henry Walshaw'
__all__ = [gdgg, encoders, __version__, __author__]

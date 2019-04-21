geogrids
========

|Latest PyPI version|

A Python implementation of the npm
`geogrids <https://gitlab.com/IvanSanchez/geogrids>`__ library by `Iván
Sánchez Ortega <https://twitter.com/RealIvanSanchez>`__ - utilities for
working with Global Discrete Geodetic Grids (GDGGs).

This module contains both a Location object that can be used to generate
a hash or take a has and generate a location, along with an encoders
module that can transform the code into a (hopefully) useful text
string.

This is written with the default encoders from the original library, and
can be easily extended to use a text set of your choice.

Usage
-----

There are two components of the library:

Representing a location
~~~~~~~~~~~~~~~~~~~~~~~

Given some location with a latitude and longitude, for example:
-35.6498, 150.2935 you can easily create a hash as either a simple
string or a numeric value:

::

   >>> latitude = -35.6498
   >>> longitude = 150.2935
   >>> import geogrids
   >>> geogrids.gdgg.latitude_longitude_to_readable_hash(latitude=latitude, longitude=longitude)
   '702020210311'
   >>> geogrids.gdgg.latitude_longitude_to_numeric_hash(latitude=latitude, longitude=longitude)
   12108871

Of course you can go the other direction as well:

::

   >>> geogrids.gdgg.numeric_hash_to_latitude_longitude(12108871)
   (-35.65283203125, 150.2789682218808)
   >>> geogrids.gdgg.readable_hash_to_latitude_longitude('702020210311')
   (-35.65283203125, 150.2789682218808)

Notice that the hashes are location approximations depending on a level
of precision - the higher the precision the better the accuracy:

::

   >>> numeric_hash = geogrids.gdgg.latitude_longitude_to_numeric_hash(latitude=latitude, longitude=longitude, precision=55)
   >>> geogrids.gdgg.numeric_hash_to_latitude_longitude(numeric_hash, precision=55)
   (-35.64979965984821, 150.2934998246466)

Effectively these hashes define a location within a triangular region,
which you can retrieve from either the ``numeric_hash_to_area`` or the
``readable_hash_to_area`` functions, which return a collection of
``Location`` objects (usually the three vertices of a triangular region,
but close to the poles for simplification the default is to return a
box):

::

   >>> vertices = geogrids.gdgg.numeric_hash_to_area(numeric_hash)
   >>> vertices
   [<Location [702020210311]>, <Location [702020210311]>, <Location [702020210311]>]
   >>> vertices[0].latitude, vertices[0].longitude
   (-35.63964843750004, 150.24252223120465)

In general it's advisable to just stick to the hashes and the latitudes
and longitudes, but the ``Location`` object does implement a
`__geo_feature__ <https://gist.github.com/sgillies/2217756>`__
interface which means you can use it with other libraries that work with
this interface for more complicated geometric operations, for example
via the `Shapely <https://shapely.readthedocs.io/>`__ library:

::

   >>> from shapely import geometry
   >>> points = [geometry.shape(vertex) for vertex in vertices]
   >>> line = geometry.LineString(points)
   >>> line.length
   0.11570586750499379
   >>> polygon = geometry.Polygon(line)
   >>> polygon.area
   0.0015986572857657128

Encoding and decoding a hash
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The encoders allow you to transform a hash to an easily memorisable
string and back again. Out of the box this comes with a number of
encoders:

-  ``geogrids.encoders.fucks`` as featured in
   `http://www.what3fucks.com <http://www.what3fucks.com>`__
-  ``geogrids.encoders.goshdarnits`` as featured in
   `http://www.what3goshdarnits.com/ <http://www.what3goshdarnits.com/>`__
-  ``geogrids.encoders.pokes`` as featured in
   `http://www.what3pokemon.com/ <http://www.what3pokemon.com/>`__
-  ``geogrids.encoders.cheeses`` which doesn't yet feature anywhere
   (AFAIK)
-  ``geogrids.encoders.ducks`` as featured in
    `http://www.what3ducks.com <http://www.what3ducks.com>`__

Given a numeric hash of a location (see above) these are easy to use:

::

   >>> geogrids.encoders.cheeses.hash_to_string(numeric_hash, precision=25)
   'Dubliner Requeijão Provolone Telemea'
   >>> geogrids.encoders.cheeses.hash_to_string(numeric_hash, precision=55)
   'Dubliner Requeijão Provolone Telemea Danablu Coulommiers Chevrotin'

Or given the readable encoding it's simple to go back the other way:

::

   >>> numeric_hash, precision = geogrids.encoders.cheeses.string_to_hash('Dubliner Requeijão Provolone Telemea')
   >>> numeric_hash, precision
   (3870868551, 32)
   >>> geogrids.gdgg.numeric_hash_to_latitude_longitude(numeric_hash, precision)
   (-35.647064208984375, 150.2948563112389)

If you don't want to use one of the builtin encoders, you can generate
your own easily:

::

   >>> wordlist = list('😀😎🤬😱😈👍🖖⚽🐶🐍🐡🦜🍀🌞🌚🔥')

*Note* the wordlist should be length that is a power of two - the level
used for calculating precisions is rounded down to the closest power of
two - any words after that number will be skipped.

::

   >>> emoji_encoder = geogrids.encoders.Encoder(wordlist, separator='')
   >>> emoji_encoder.hash_to_string(numeric_hash, precision)
   '⚽😈😈🍀🐶🦜🖖🌚'

**Warning** One key consideration with the encoders: if you create an
encoding and share it with someone else the wordlist must be in exactly
the same order! Otherwise when decoding you'll get completely different
results!

::

   >>> numeric_hash, precision = emoji_encoder.string_to_hash('⚽😈😈🍀🐶🦜🖖🌚')
   >>> geogrids.gdgg.numeric_hash_to_latitude_longitude(numeric_hash, precision)
   (-35.647064208984375, 150.2948563112389)

Installation
------------

``pip install geogrids``

Requirements
~~~~~~~~~~~~

``geogrids`` doesn't have any third party library requirements

Compatibility
-------------

Python 3.5+

Licence
-------

This is licensed under the Do What The Fuck You Want Public License as
is the original JS implementation. So enjoy!

Authors
-------

``geogrids`` was written by Henry Walshaw in Python, translated from the
npm geogrids library by Iván Sánchez Ortega

``ducks`` encoder contributed by Adam Steer

.. |Latest PyPI version| image:: https://img.shields.io/pypi/v/geogrids.svg
   :target: https://pypi.python.org/pypi/geogrids

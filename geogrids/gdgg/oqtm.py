"""
Simplistic Octohedral Quaternary Triangle Mesh

Translated from the GeoGrids library on NPM written by Iván Sánchez Ortega
"""
import math


HASH_PRECISIONS = list(range(3, 60, 2))


class Location():
    """Representation of an XY location at levels

    A simple storage class for location objects. You can supply either a
    latitude and longitude or an x , y coordinate with an octant on
    creation to automatically generate the other values.

    Attributes
    ----------
    latitude : float
        Latitude coordinate of the location. Decimal degrees [-90, 90]
    longitude : float
        Longitudw coordinate of the location. Decimal degrees [-180, 180]
    octant : int
        [0, 8]
    levels : list of int
        ID in each level. [0, 3]
    x : float
        The remainder x-coordinate (longitude) in the deepest computed level
        (0, 1). Both x and y will be clamped to 0<x<1, 0<y<1, 0<(x+y)<1.
    y : float
        The remainder y-coordinate (latitude) in the deepest computed level
        (0, 1). Both x and y will be clamped to 0<x<1, 0<y<1, 0<(x+y)<1.
    """

    def __init__(self, latitude: float=None, longitude: float=None, octant: int=None, x: float=None, y: float=None):
        """

        Parameters
        ----------
        latitude : float
            Latitude coordinate of the location. Decimal degrees [-90, 90]
        longitude : float
            Longitudw coordinate of the location. Decimal degrees [-180, 180]
        octant : int
            [0, 8]
        x : float
            The remainder x-coordinate (longitude) in the deepest computed level
            (0, 1)
        y : float
            The remainder y-coordinate (latitude) in the deepest computed level
            (0, 1)
        """
        if (latitude is None or longitude is None) and any((octant is None, x is None, y is None)):
            raise ValueError('Either latitude and longitude or octant, x and y  are required')

        self.levels = []

        self._latitude = latitude
        self._longitude = longitude
        self._octant = octant
        self._x = x
        self._y = y

    @property
    def x(self):
        if self._x is None:
            self._compute_octant()
        return self._x

    @property
    def y(self):
        if self._y is None:
            self._compute_octant()
        return self._y

    @property
    def octant(self):
        if self._octant is None:
            self._compute_octant()
        return self._octant

    def _compute_octant(self):
        """
        Given latitude and longitude compute octant and first x, y
        """
                    
        if self._latitude > 0:
            if self._longitude < -90:
                self._octant = 0
            elif self._longitude < 0:
                self._octant = 1
            elif self._longitude < 90:
                self._octant = 2
            else:
                self._octant = 3
            
        else:
            if self._longitude < -90:
                self._octant = 4
            elif self._longitude < 0:
                self._octant = 5
            elif self._longitude < 90:
                self._octant = 6
            else:
                self._octant = 7

        # Compute remainder x,y mapping them to [0,1]
        self._x = ((self._longitude + 180) % 90) / 90
        self._y = abs(self._latitude) / 90
        self._x *= (1 - self.y)
        self.levels = []

    @property
    def latitude(self):
        if self._latitude is None:
            self._compute_lat_lng()
        return self._latitude

    @property
    def longitude(self):
        if self._longitude is None:
            self._compute_lat_lng()
        return self._longitude

    def _compute_lat_lng(self):
        """
        Given a location with `octant`, `x`, `y` compute its lat-lng.
        """
        x = self._x
        y = self._y

        for level in reversed(self.levels):
            if level == 1:
                x /= 2
                y = y/2 + 0.5
            elif level == 2:
                x /= 2
                y /= 2
            elif level == 3:
                x = x/2 + 0.5
                y /= 2
            elif level == 0:
                x = (1 - x) / 2
                y = (1 - y) / 2
            
            # console.log(level, x,y)
        
        x /= 1 - y
        x *= 90
        y *= 90
        
        if self._octant == 0:
            x -= 180
        elif self._octant == 1:
            x -= 90
        elif self._octant == 2:
            x += 0
        elif self._octant == 3:
            x += 90
        elif self._octant == 4:
            x -= 180
            y = -y
        elif self._octant == 5:
            x -= 90
            y = -y
        elif self._octant == 6:
            x += 0
            y = -y
        elif self._octant == 7:
            x += 90
            y = -y

        self._latitude = y
        self._longitude = x

    def compute_level(self):
        """
        Given `octant`, `x`, `y`, `max` and `levels`, compute the next level
        """
        if self.y > 0.5:  # use properties to guarantee first values populated
            self.levels.append(1)
            self._x *= 2
            self._y = (self._y - 0.5) * 2
        elif self.y < 0.5 - self.x:
            self.levels.append(2)
            self._x *= 2
            self._y *= 2
        elif self.x >= 0.5:
            self.levels.append(3)
            self._x = (self._x - 0.5) * 2
            self._y *= 2
        else:
            # And this is an inverse triangle
            self.levels.append(0)
    #         self._x = 2*x + 2*y - 1
            self._x = 1 - self._x * 2
            self._y = 1 - self._y * 2

    def location_to_readable_hash(self):
        """
        Given a location, return its human-readable hash

        Returns
        -------
        readable_hash : str
            human-readable hash
        """
        return str(self.octant) + ''.join([str(i) for i in self.levels])
    
    def location_to_numeric_hash(self):
        """
        Given a self, return its numeric hash

        Returns
        -------
        numeric_hash : int
            Numeric hash
        """
        acc = self.octant
        mult = 8
        
        for level in self.levels:
            acc += mult * level
            mult *= 4
        
        return acc

    @classmethod
    def readable_hash_to_location(cls, readable_hash):
        """
        Given a human-readable hash return a location

        Parameters
        ----------
        readable_hash : str
            Readable has of a location

        Returns
        -------
        Location
        """
        octant = int(readable_hash[0])
        levels = [int(i) for i in readable_hash[1:]]
        precision = 3 + 2 * len(levels)

        return cls.levels_to_location(octant, levels)

    @classmethod
    def levels_to_location(cls, octant, levels, x=None, y=None):
        """
        Given octant and levels, return a location with back-computed lat-lng.

        Parameters
        ----------
        octant : int
        levels : list of int
        x : float
        y : float

        Returns
        -------
        Location
        """
        if x is None:
            x = 0.3
        if y is None:
            y = 0.3
        
        location = cls(
            octant=octant,
            x=x,
            y=y
        )
        location.levels = levels
        
        return location

    @classmethod
    def numeric_hash_to_location(cls, numeric_hash, precision=None):
        """
        Given a numeric hash return a location

        Precision needs to be given to account for leading zeroes.

        Parameters
        ----------
        numeric_hash : int
        precision : int

        Returns
        -------
        Location
        """
        if precision is None:
            precision = 25
        octant = numeric_hash % 8
        numeric_hash = numeric_hash // 8
        i = 3
        levels = []

        while i < precision:
            levels.append(numeric_hash % 4)
            numeric_hash = numeric_hash // 4
            i += 2

        return cls.levels_to_location(octant, levels)

    @classmethod
    def lat_lng_to_precise_location(cls, latitude, longitude, precision):
        """
        Get location with computed octant and levels.

        Given latitude / longitude and a precision (in a number of bits), return
        a location with computed octant and levels

        Parameters
        ----------
        latitude : float
            Latitude
        longitude : float
            Longitude
        precision : int

        Returns
        -------
        Location
            location with the computed octant and levels
        """
        location = cls(latitude=latitude, longitude=longitude)

        for current_precision in range(3, precision, 2):
            location.compute_level()

        return location

    @classmethod
    def levels_to_triangle(cls, octant, levels, normalise_poles=False):
        """
        Get three locations with back-computed latitude / longitude.

        Given the octant and levels return three locations with back-computed
        latitude and longitude.

        Parameters
        ----------
        octant : int
        levels : list of int
        normalise_poles : bool
            The edge case - if a triangle has a pole, return a square instead of
            a triangle. Note this will change output from three locations to
            four locations

        Returns
        -------
        locations : list of Location
            A collection of locations - typically 3, but in the edge case of
            normalising the poles, this will have length 4.
        """
        ALMOST_ZERO = 1e-12
        ALMOST_ONE = 1 - 1e-12

        location1 = cls(octant=octant, x=ALMOST_ZERO, y=ALMOST_ZERO)
        location1.levels = levels
        # don't need to explicitly call compute latitude and longitude as it's
        # lazily processed as required

        location2 = cls(octant=octant, x=ALMOST_ZERO, y=ALMOST_ONE)
        location2.levels = levels

        location3 = cls(octant=octant, x=ALMOST_ONE, y=ALMOST_ZERO)
        location3.levels = levels

        if normalise_poles:

            if math.isclose(abs(location2.latitude), 90):
                location2a = cls(
                    octant=octant,
                    x=ALMOST_ZERO,
                    y=ALMOST_ONE,
                    latitude=location2.latitude,
                    longitude=location1.longitude
                )
                location2a.levels = levels

                location2b = cls(
                    octant=octant,
                    x=ALMOST_ZERO,
                    y=ALMOST_ONE,
                    latitude=location2.latitude,
                    longitude=location3.longitude
                )
                location2b.levels = levels

                return [location1, location2a, location2b, location3]

        return [location1, location2, location3]

    @property
    def __geo_interface__(self):
        """
        GeoInterface as per [1]_

        Returns
        -------
        dict
            A GeoJSON Point object

        .. [1] Gillies, Sean. "A Python Protocol for Geospatial Data" GitHub,
               2019, version 1.0, https://gist.github.com/sgillies/2217756
               Accessed 30 March 2019
        """
        return {
            'type': 'Point',
            'coordinates': (self.longitude, self.latitude)
        }

    def __repr__(self):

        return f'<Location [{self.location_to_readable_hash()}]>'


# utility functinos


def latitude_longitude_to_readable_hash(latitude, longitude, precision=25):
    """
    Utility function to get a readable hash from latitude and longitude

    Parameters
    ----------
    latitude : float
    longitude : float
    precision : int

    Returns
    -------
    readable_hash : str
        The readable hash of the supplied coordinates
    """
    location = Location.lat_lng_to_precise_location(
        latitude, longitude, precision)
    return location.location_to_readable_hash()


def latitude_longitude_to_numeric_hash(latitude, longitude, precision=25):
    """
    Utility function to get a numeric hash from latitude and longitude

    Parameters
    ----------
    latitude : float
    longitude : float
    precision : int

    Returns
    -------
    numeric_hash : int
        Numeric hash of the supplied coordinates
    """
    location = Location.lat_lng_to_precise_location(
        latitude, longitude, precision)
    return location.location_to_numeric_hash()


def numeric_hash_to_latitude_longitude(numeric_hash, precision=25):
    """
    Convert numeric hash to get location accurate to the level of precision

    Parameters
    ----------
    numeric_hash : int
    precision : int

    Returns
    -------
    latitude : float
    longitude : float
    """
    location = Location.numeric_hash_to_location(
        numeric_hash, precision
    )
    return location.latitude, location.longitude


def readable_hash_to_latitude_longitude(readable_hash):
    """
    Convert readable hash to location accurate to the level of precision

    Parameters
    ----------
    readable_hash : str

    Returns
    -------
    latitude : float
    longitude : float
    """
    location = Location.readable_hash_to_location(readable_hash)
    return location.latitude, location.longitude


def numeric_hash_to_area(numeric_hash, precision=25):
    """
    Convert numeric hash to triangular region

    Note at the poles this will cheat and calculate a square region instead

    Parameters
    ----------
    numeric_hash : int
    precision : int

    Returns
    -------
    areal_locations : list of Location
        The collection of Locations (usually 3, at the poles 4) that defines the
        areal region around the numeric hash
    """
    location = Location.numeric_hash_to_location(numeric_hash, precision)
    return Location.levels_to_triangle(
        location.octant,
        location.levels,
        normalise_poles=True
    )


def readable_hash_to_area(readable_hash):
    """
    Convert readable hash to triangular region

    Note at the poles this will cheat and calculate a square region instead

    Parameters
    ----------
    readable_hash : str

    Returns
    -------
    areal_locations : list of Location
        The collection of Locations (usually 3, at the poles 4) that defines the
        areal region around the numeric hash
    """
    location = Location.readable_hash_to_location(readable_hash)
    return Location.levels_to_triangle(
        location.octant,
        location.levels,
        normalise_poles=True
    )

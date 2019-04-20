from hypothesis import given
from hypothesis import strategies
import pytest

from geogrids.gdgg.oqtm import HASH_PRECISIONS
import geogrids


def test_create_location_fails():
    with pytest.raises(ValueError):
        location = geogrids.gdgg.Location()


@given(
    latitude=strategies.floats(min_value=-90, max_value=90, allow_nan=False, allow_infinity=False),
    longitude=strategies.floats(min_value=-180, max_value=180, allow_nan=False, allow_infinity=False)
)
def test_x_y_calculated_from_latitude_longitude(latitude, longitude):
    location = geogrids.gdgg.Location(latitude=latitude, longitude=longitude)

    assert location.x is not None and location.y is not None, "Location failed to generate X and Y"
    assert 0 <= location.x <= 1 and 0 <= location.y <= 1 and 0 <= location.x + location.y <= 1, 'X and Y values out of range'

@given(
    xy=strategies.floats(
        min_value=0,
        max_value=1,
        allow_nan=False,
        allow_infinity=False,
        exclude_min=True,
        exclude_max=True
    ),
    octant=strategies.integers(min_value=0, max_value=7)
)
def test_latitude_longitude_calculated_from_x_y(xy, octant):
    x = y = xy / 2
    location = geogrids.gdgg.Location(x=x, y=y, octant=octant)

    assert location.longitude is not None and location.latitude is not None, "Location failed to generate latitdue and longitude"
    assert -90 <= location.latitude <= 90 and -180 <= location.longitude <= 180, 'Latitude and longitude out of range'


@given(
    latitude=strategies.floats(min_value=-90, max_value=90, allow_nan=False, allow_infinity=False),
    longitude=strategies.floats(min_value=-180, max_value=180, allow_nan=False, allow_infinity=False)
)
def test_compute_level(latitude, longitude):
    location = geogrids.gdgg.Location(latitude=latitude, longitude=longitude)

    location.compute_level()

    assert len(location.levels) > 0, "At least one level in the location"


@given(
    latitude=strategies.floats(min_value=-90, max_value=90, allow_nan=False, allow_infinity=False),
    longitude=strategies.floats(min_value=-180, max_value=180, allow_nan=False, allow_infinity=False)
)
def test_location_to_readable_hash(latitude, longitude):
    location = geogrids.gdgg.Location(latitude=latitude, longitude=longitude)

    readable_hash = location.location_to_readable_hash()

    assert len(readable_hash) >= 1, 'At least the octant must be used to get a readable hash'


@given(
    latitude=strategies.floats(min_value=-90, max_value=90, allow_nan=False, allow_infinity=False),
    longitude=strategies.floats(min_value=-180, max_value=180, allow_nan=False, allow_infinity=False)
)
def test_location_to_numeric_hash(latitude, longitude):
    location = geogrids.gdgg.Location(latitude=latitude, longitude=longitude)

    numeric_hash = location.location_to_numeric_hash()

    assert numeric_hash >= 0, "Numeric hash must be positive"


@given(
    octant=strategies.integers(min_value=0, max_value=7),
    levels=strategies.lists(
        strategies.integers(min_value=0, max_value=3),
        min_size=0,
        max_size=10
    )
)
def test_readable_hash_to_location(octant, levels):

    readable_hash = str(octant) + ''.join(str(i) for i in levels)

    location = geogrids.gdgg.Location.readable_hash_to_location(readable_hash)

    assert location.latitude is not None and location.longitude is not None, "Location failed to generate latitdue and longitude"
    assert -90 <= location.latitude <= 90 and -180 <= location.longitude <= 180, 'Latitude and longitude out of range'


@given(
    octant=strategies.integers(min_value=0, max_value=7),
    levels=strategies.lists(
        strategies.integers(min_value=0, max_value=3),
        min_size=0,
        max_size=10
    ),
    xy=strategies.floats(
        min_value=0,
        max_value=1,
        allow_nan=False,
        allow_infinity=False,
        exclude_min=True,
        exclude_max=True
    ),
)
def test_levels_to_location_with_xy(octant, levels, xy):

    x = y = xy / 2
    location = geogrids.gdgg.Location.levels_to_location(octant, levels, x, y)

    assert location.latitude is not None and location.longitude is not None, "Location failed to generate latitdue and longitude"
    assert -90 <= location.latitude <= 90 and -180 <= location.longitude <= 180, 'Latitude and longitude out of range'


@given(
    numeric_hash=strategies.integers(min_value=0, max_value=1e6),
)
def test_numeric_hash_to_location(numeric_hash):

    location = geogrids.gdgg.Location.numeric_hash_to_location(numeric_hash=numeric_hash)
    assert location.latitude is not None and location.longitude is not None, "Location failed to generate latitdue and longitude"
    assert -90 <= location.latitude <= 90 and -180 <= location.longitude <= 180, 'Latitude and longitude out of range'


@given(
    numeric_hash=strategies.integers(min_value=0, max_value=1e6),
    precision=strategies.sampled_from(HASH_PRECISIONS)
)
def test_numeric_hash_to_location_with_precision(numeric_hash, precision):

    location = geogrids.gdgg.Location.numeric_hash_to_location(
        numeric_hash=numeric_hash,
        precision=precision
    )
    assert location.latitude is not None and location.longitude is not None, "Location failed to generate latitdue and longitude"
    assert -90 <= location.latitude <= 90 and -180 <= location.longitude <= 180, 'Latitude and longitude out of range'


@given(
    latitude=strategies.floats(min_value=-90, max_value=90, allow_nan=False,
                               allow_infinity=False),
    longitude=strategies.floats(min_value=-180, max_value=180, allow_nan=False,
                                allow_infinity=False),
    precision=strategies.sampled_from(HASH_PRECISIONS)
)
def test_lat_lng_to_precise_location(latitude, longitude, precision):

    location = geogrids.gdgg.Location.lat_lng_to_precise_location(
        latitude=latitude,
        longitude=longitude,
        precision=precision
    )

    assert location.x is not None and location.y is not None, "Location failed to generate X and Y"
    assert 0 <= location.x <= 1 and 0 <= location.y <= 1 and 0 <= location.x + location.y <= 1, 'X and Y values out of range'


@given(
    octant=strategies.integers(min_value=0, max_value=7),
    levels=strategies.lists(
        strategies.integers(min_value=0, max_value=3),
        min_size=1,
        max_size=10
    ),
    normalise_poles=strategies.booleans()
)
def test_levels_to_triangle(octant, levels, normalise_poles):

    location1, *location2, location3 = geogrids.gdgg.Location.levels_to_triangle(
        octant=octant,
        levels=levels,
        normalise_poles=normalise_poles
    )

    if normalise_poles:
        assert len(location2) in (1, 2), "One or two locations for location 2"
    else:
        assert len(location2) == 1, "If not normalised only one location 2"

    for location in [location1] + location2 + [location3]:
        assert location.latitude is not None and location.longitude is not None, "Location failed to generate latitdue and longitude"
        assert -90 <= location.latitude <= 90 and -180 <= location.longitude <= 180, 'Latitude and longitude out of range'


@given(
    latitude=strategies.floats(min_value=-90, max_value=90, allow_nan=False, allow_infinity=False),
    longitude=strategies.floats(min_value=-180, max_value=180, allow_nan=False, allow_infinity=False)
)
def test_geo_interface(latitude, longitude):
    location = geogrids.gdgg.Location(latitude=latitude, longitude=longitude)

    assert location.__geo_interface__['type'] == 'Point', 'Geo interface not correctly generated'


@given(
    latitude=strategies.floats(min_value=-90, max_value=90, allow_nan=False, allow_infinity=False),
    longitude=strategies.floats(min_value=-180, max_value=180, allow_nan=False, allow_infinity=False)
)
def test_repr(latitude, longitude):
    location = geogrids.gdgg.Location(latitude=latitude, longitude=longitude)

    assert repr(location).startswith('<Location'), "Representation isn't correctly generated"


@given(
    latitude=strategies.floats(min_value=-90, max_value=90, allow_nan=False,
                               allow_infinity=False),
    longitude=strategies.floats(min_value=-180, max_value=180, allow_nan=False,
                                allow_infinity=False),
)
def test_latitude_longitude_to_readable_hash(latitude, longitude):

    readable_hash = geogrids.gdgg.latitude_longitude_to_readable_hash(
        latitude, longitude
    )

    assert len(readable_hash) > 0, 'No readable hash generated'


@given(
    latitude=strategies.floats(min_value=-90, max_value=90, allow_nan=False,
                               allow_infinity=False),
    longitude=strategies.floats(min_value=-180, max_value=180, allow_nan=False,
                                allow_infinity=False),
    precision=strategies.sampled_from(HASH_PRECISIONS)
)
def test_latitude_longitude_to_readable_hash_with_precision(latitude, longitude, precision):
    readable_hash = geogrids.gdgg.latitude_longitude_to_readable_hash(
        latitude, longitude, precision
    )

    assert len(readable_hash) > 0, 'No readable hash generated'


@given(
    latitude=strategies.floats(min_value=-90, max_value=90, allow_nan=False,
                               allow_infinity=False),
    longitude=strategies.floats(min_value=-180, max_value=180, allow_nan=False,
                                allow_infinity=False)
)
def test_latitude_longitude_to_numeric_hash(latitude, longitude):

    numeric_hash = geogrids.gdgg.latitude_longitude_to_numeric_hash(
        latitude, longitude
    )
    assert numeric_hash >= 0, 'Numeric hash not correctly generated'


@given(
    latitude=strategies.floats(min_value=-90, max_value=90, allow_nan=False,
                               allow_infinity=False),
    longitude=strategies.floats(min_value=-180, max_value=180, allow_nan=False,
                                allow_infinity=False),
    precision=strategies.sampled_from(HASH_PRECISIONS)
)
def test_latitude_longitude_to_numeric_hash_with_precision(latitude, longitude, precision):
    numeric_hash = geogrids.gdgg.latitude_longitude_to_numeric_hash(
        latitude, longitude, precision
    )
    assert numeric_hash >= 0, 'Numeric hash not correctly generated'


@given(
    numeric_hash=strategies.integers(min_value=0, max_value=1e6),
)
def test_numeric_hash_to_latitude_longitude(numeric_hash):

    latitude, longitude = geogrids.gdgg.numeric_hash_to_latitude_longitude(
        numeric_hash
    )
    assert -90 <= latitude <= 90 and -180 <= longitude <= 180, 'Latitude and longitude out of range'


@given(
    numeric_hash=strategies.integers(min_value=0, max_value=1e6),
    precision=strategies.sampled_from(HASH_PRECISIONS)
)
def test_numeric_hash_to_latitude_longitude_with_precision(numeric_hash, precision):
    latitude, longitude = geogrids.gdgg.numeric_hash_to_latitude_longitude(
        numeric_hash, precision
    )
    assert -90 <= latitude <= 90 and -180 <= longitude <= 180, 'Latitude and longitude out of range'


@given(
    octant=strategies.integers(min_value=0, max_value=7),
    levels=strategies.lists(
        strategies.integers(min_value=0, max_value=3),
        min_size=1,
        max_size=10
    ),
)
def test_readable_hash_to_latitude_longitude(octant, levels):

    readable_hash = str(octant) + ''.join(str(i) for i in levels)

    latitude, longitude = geogrids.gdgg.readable_hash_to_latitude_longitude(readable_hash)

    assert -90 <= latitude <= 90 and -180 <= longitude <= 180, 'Latitude and longitude out of range'


@given(
    numeric_hash=strategies.integers(min_value=0, max_value=1e6),
)
def test_numeric_hash_to_area(numeric_hash):

    locations = geogrids.gdgg.numeric_hash_to_area(
        numeric_hash
    )

    assert len(locations) in (3, 4), 'Incorrect number of locations'
    for location in locations:
        assert location.latitude is not None and location.longitude is not None, "Location failed to generate latitdue and longitude"
        assert -90 <= location.latitude <= 90 and -180 <= location.longitude <= 180, 'Latitude and longitude out of range'


@given(
    numeric_hash=strategies.integers(min_value=0, max_value=1e6),
    precision=strategies.sampled_from(HASH_PRECISIONS)
)
def test_numeric_hash_to_area_with_precision(numeric_hash, precision):

    locations = geogrids.gdgg.numeric_hash_to_area(
        numeric_hash, precision
    )
    assert len(locations) in (3, 4), 'Incorrect number of locations'

    for location in locations:
        assert location.latitude is not None and location.longitude is not None, "Location failed to generate latitdue and longitude"
        assert -90 <= location.latitude <= 90 and -180 <= location.longitude <= 180, 'Latitude and longitude out of range'


@given(
    octant=strategies.integers(min_value=0, max_value=7),
    levels=strategies.lists(
        strategies.integers(min_value=0, max_value=3),
        min_size=1,
        max_size=10
    ),
)
def test_readable_hash_to_area(octant, levels):

    readable_hash = str(octant) + ''.join(str(i) for i in levels)

    locations = geogrids.gdgg.readable_hash_to_area(readable_hash)

    for location in locations:
        assert location.latitude is not None and location.longitude is not None, "Location failed to generate latitdue and longitude"
        assert -90 <= location.latitude <= 90 and -180 <= location.longitude <= 180, 'Latitude and longitude out of range'

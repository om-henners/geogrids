import os.path

from hypothesis import given
from hypothesis import strategies
import pytest

from geogrids.encoders import wordlists
import geogrids


@given(encoded=strategies.lists(
    strategies.sampled_from(wordlists.fucks),
    min_size=1,
    max_size=5
))
def test_fucks_encoder(encoded):
    text = ' '.join(encoded)

    encoded_hash, precision = geogrids.encoders.fucks.string_to_hash(
        text
    )

    assert precision > 0, 'Precision not above zero'


@given(encoded=strategies.lists(
    strategies.sampled_from(wordlists.pokes),
    min_size=1,
    max_size=5
))
def test_pokes_encoder(encoded):
    text = ' '.join(encoded)

    encoded_hash, precision = geogrids.encoders.pokes.string_to_hash(
        text
    )

    assert precision > 0, 'Precision not above zero'


@given(encoded=strategies.lists(
    strategies.sampled_from(wordlists.goshdarnits),
    min_size=1,
    max_size=5
))
def test_goshdarnits_encoder(encoded):
    text = ' '.join(encoded)

    encoded_hash, precision = geogrids.encoders.goshdarnits.string_to_hash(
        text
    )

    assert precision > 0, 'Precision not above zero'


@given(encoded=strategies.lists(
    strategies.sampled_from(wordlists.cheeses),
    min_size=1,
    max_size=5
))
def test_pokes_encoder(encoded):
    text = ' '.join(encoded)

    encoded_hash, precision = geogrids.encoders.cheeses.string_to_hash(
        text
    )

    assert precision > 0, 'Precision not above zero'


@pytest.fixture(scope='session')
def dog_breeds():
    path = os.path.join(
        os.path.dirname(__file__),
        'breeds.csv'
    )
    breeds = open(path).read().split('\n')

    return breeds


def test_build_custom_encoder(dog_breeds):

    breeds = geogrids.encoders.Encoder(wordlist=dog_breeds, separator='\t')

    numeric_hash, precision = breeds.string_to_hash(
        'Greyhound\tBulldog\tGalgo Español')

    assert precision > 0, 'Precision not above zero'

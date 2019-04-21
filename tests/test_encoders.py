import os.path
import string

from hypothesis import given
from hypothesis import strategies
import pytest

from geogrids.encoders import wordlists
from geogrids.encoders.encoder import DecodingError, DecodingWarning
import geogrids


@given(encoded=strategies.lists(
    strategies.sampled_from(wordlists.fucks[:32]),
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
    strategies.sampled_from(wordlists.pokes[:32]),
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
    strategies.sampled_from(wordlists.goshdarnits[:32]),
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
    strategies.sampled_from(wordlists.cheeses[:32]),
    min_size=1,
    max_size=5
))
def test_pokes_encoder(encoded):
    text = ' '.join(encoded)

    encoded_hash, precision = geogrids.encoders.cheeses.string_to_hash(
        text
    )

    assert precision > 0, 'Precision not above zero'


@given(encoded=strategies.lists(
    strategies.sampled_from(wordlists.ducks[:32]),
    min_size=1,
    max_size=5
))
def test_pokes_encoder(encoded):
    text = ' '.join(encoded)

    encoded_hash, precision = geogrids.encoders.ducks.string_to_hash(
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
    """
    Test the creation of a custom encoder with a custom separator

    Parameters
    ----------
    dog_breeds : list
        List of dog breeds taken from Wikipedia https://en.wikipedia.org/wiki/List_of_dog_breeds
    """

    breeds = geogrids.encoders.Encoder(wordlist=dog_breeds, separator='\t')

    numeric_hash, precision = breeds.string_to_hash(
        'Greyhound\tBulldog\tGalgo Español')

    assert precision > 0, 'Precision not above zero'


@given(
    separator=strategies.sampled_from(string.punctuation)
)
def test_build_custom_encoder_with_separator(dog_breeds, separator):
    breeds = geogrids.encoders.Encoder(wordlist=dog_breeds, separator=separator)

    encoded = separator.join(['Greyhound', 'Bulldog', 'Galgo Español'])

    numeric_hash, precision = breeds.string_to_hash(encoded)

    assert precision > 0, 'Precision not above zero'


def test_build_custom_encoder_no_separator():
    encoder = geogrids.encoders.Encoder(wordlist=list(string.punctuation), separator='')

    numeric_hash, precision = encoder.string_to_hash('!#&')

    assert precision > 0, 'Precision not above zero'


@given(
    numeric_hash=strategies.integers(min_value=0, max_value=1e20),
    precision=strategies.integers(min_value=1, max_value=65)
)
def test_hash_to_string(numeric_hash, precision):

    encoded = geogrids.encoders.cheeses.hash_to_string(numeric_hash, precision)

    assert encoded is not None, "No encoded string"


@given(
    first_word=strategies.sampled_from(wordlists.goshdarnits[:32]),
    second_word=strategies.sampled_from(wordlists.cheeses[:32])
)
def test_first_word_broken(first_word, second_word):

    encoded = ' '.join([first_word, second_word])

    with pytest.raises(DecodingError):
        numeric_hash, precision = geogrids.encoders.cheeses.string_to_hash(encoded)


@given(
    first_word=strategies.sampled_from(wordlists.cheeses[:32]),
    second_word=strategies.sampled_from(wordlists.goshdarnits[:32])
)
def test_second_word_broken(first_word, second_word):

    encoded = ' '.join([first_word, second_word])

    with pytest.warns(DecodingWarning):
        numeric_hash, precision = geogrids.encoders.cheeses.string_to_hash(encoded)

    assert precision > 0

from hypothesis import given
from hypothesis import strategies


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



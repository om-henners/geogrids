"""
Encoders to turn hashes into strings and vice versa

Convenience encoders already in place for the standard wordlists
"""

from .encoder import Encoder
from . import wordlists


fucks = Encoder(wordlist=wordlists.fucks)
cheeses = Encoder(wordlist=wordlists.cheeses)
goshdarnits = Encoder(wordlist=wordlists.goshdarnits)
pokes = Encoder(wordlist=wordlists.pokes)


__all__ = [Encoder, fucks, cheeses, goshdarnits, pokes]

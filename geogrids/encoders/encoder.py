"""
Generic hash encoder which can be combined with words lists to econde or decode
a geographic hash.
"""
import math
import warnings


from .wordlists import fucks


class DecodingWarning(Warning):
    """
    Custom warning for when the Encoder failed to decode completely
    """
    pass


class DecodingError(ValueError):
    """
    Custom error for when the Encoder failed to decode at all.

    Contains a reference to the offending word, and the wordlist
    """

    def __init__(self, word, wordlist):
        self.word = word
        self.wordlist = wordlist
        self.message = f"Could not match '{word}' in wordlist"
        super().__init__(self.message)


class Encoder:
    """
    Generic encoder class
    """

    def __init__(self, wordlist: list = fucks, separator=' '):
        """
        Encoder initialisation

        Parameters
        ----------
        wordlist : list of str
            words to use for the encoder. Note the order of the words (and the
            size of the collection) is important. Once you start encoding data
            with a parituclar wordlist you shouldn't change it (or version it
            when you do and store the date along with your encoding)

            In general the length of the list should be a power of two -
            remainder words after the highest power of two for the length of the
            list will be ignored. e.g. the wordlist ``['a', 'b', 'c']`` would
            ignore the ``'c'``.
        separator : str
            separator for the resulting encoded hashes, and used to split the
            incoming hashes
        """
        self.wordlist = wordlist
        self.separator = separator

        self.precision_per_word = int(math.log2(len(wordlist)))
        self.precisions = list(
            range(self.precision_per_word, 60, self.precision_per_word))


    def hash_to_string(self, numeric_hash : int, precision : int):
        """
        Convert a numeric hash to an encoded string with a given level of
        precision

        Parameters
        ----------
        numeric_hash : int
        precision : int

        Returns
        -------
        encoded : str
            The hash encoded to a string with the appropriate level of precision
        """
        digits = []

        while precision > 0:
            word_index = numeric_hash % len(self.wordlist)
            digits.append(self.wordlist[word_index])
            numeric_hash = int(numeric_hash / len(self.wordlist))
            precision -= self.precision_per_word

        return self.separator.join(digits)

    def string_to_hash(self, encoded : str):
        """
        Convert encoded string back to a numeric hash with accompanying precision

        Parameters
        ----------
        encoded : str

        Returns
        -------
        numeric_hash : int
        precision : int
        """
        numeric_hash = 0
        precision = 0
        multiplier = 1

        if self.separator:  # support for a zero length separator
            words = encoded.split(self.separator)
        else:
            words = list(encoded)

        for word in words:
            try:
                position = self.wordlist.index(word)
            except ValueError:
                if precision > 0:
                    warnings.warn(
                        f'Could not find {word} in wordlist',
                        DecodingWarning
                    )
                    return numeric_hash, precision
                else:
                    raise DecodingError(word, self.wordlist)

            numeric_hash += position * multiplier
            multiplier *= len(self.wordlist)
            precision += self.precision_per_word

        return numeric_hash, precision

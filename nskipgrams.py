"""nskipgrams: A lightweight Python package to work with ngrams and skipgrams

Author: Jackson L. Lee <jacksonlunlee@gmail.com>
License: MIT License
Source: https://github.com/jacksonllee/nskipgrams
"""

try:
    from importlib.metadata import version
except ModuleNotFoundError:
    # For Python < 3.8
    from importlib_metadata import version

from collections import defaultdict, OrderedDict
from itertools import combinations


__version__ = version("nskipgrams")


def _trie():
    return defaultdict(_trie)


def _flattened_ngrams_with_counts(trie, prefix):
    def _flatten_trie(trie_):
        try:
            # If `trie.values()` are not sum-able (hence TypeError), they
            # are tries themselves.
            sum(trie_.values())
        except TypeError:
            for token, inner_trie in trie_.items():
                for inner_tokens in _flatten_trie(inner_trie):
                    # Python < 3.8 doesn't allow `token, *inner_tokens` syntax
                    combined = (token,) + inner_tokens
                    yield combined
        else:
            yield from trie_.items()

    prefix = prefix or ()
    inner_trie = _get_inner_trie_from_prefix(trie, prefix)

    if inner_trie is None:
        return
    elif type(inner_trie) == int:
        # `inner_trie` is the count of the ngram (= the given prefix)
        yield prefix, inner_trie
    else:
        for tokens in _flatten_trie(inner_trie):
            ngram = tokens[:-1]
            count = tokens[-1]
            yield prefix + ngram, count


def _get_inner_trie_from_prefix(trie, ngram_prefix):
    for token in ngram_prefix:
        if type(trie) == int or token not in trie:
            # If we reach the end of the trie without exhausting the prefix,
            # then the prefix is simply not a prefix for the given trie.
            return None
        else:
            # Since `trie` is a defaultdict but not a vanilla dict,
            # we can't use a try-except block around `trie = trie[token]`
            # which would never raise KeyError and would undesirably
            # create an empty defaultdict by calling `trie[token]`
            # even for an unfound `token`.
            trie = trie[token]
    # `trie` at this point could be an int for the prefix's count,
    # or an actual trie that continues from the prefix.
    return trie


def skipgrams_from_seq(seq, n, skip):
    _validate_n(n, upper_bound=len(seq))
    _validate_skip(skip, upper_bound=len(seq))
    all_indices = OrderedDict()  # used an ordered set
    for k in range(len(seq) - n + 1):
        for indices in combinations(range(min(skip + n, len(seq))), n):
            all_indices[tuple(i + k for i in indices)] = 0  # value 0 is meaningless
    for indices in all_indices.keys():
        try:
            yield tuple(seq[i] for i in indices)
        except IndexError:
            pass


def ngrams_from_seq(seq, n):
    """Yield ngrams extracted from the given sequence.

    Parameters
    ----------
    seq : iterable
    n : int
        The size of the ngrams to extract.

    Yields
    ------
    tuple
        ngram of size `n`
    """
    yield from zip(*(seq[i:] for i in range(n)))


def _validate_n(n, upper_bound=None):
    if type(n) != int or n < 1:
        raise ValueError(f"n must be an integer >= 1: {n}")
    elif upper_bound is not None and n > upper_bound:
        raise ValueError(f"n is outside of [1, {upper_bound}]: {n}")
    return n


def _validate_skip(skip, upper_bound=None):
    if type(skip) != int or skip < 0:
        raise ValueError(f"skip must be an integer >= 0: {skip}")
    elif upper_bound is not None and skip > upper_bound:
        raise ValueError(f"skip is outside of [0, {upper_bound}]: {skip}")
    return skip


class Skipgrams:
    """A collection of skipgrams."""

    def __init__(self, n, skip=0):
        self.n = _validate_n(n)
        self.skip = _validate_skip(skip)
        self._tries = {(i + 1, k): _trie() for i in range(n) for k in range(skip + 1)}

    def add(self, skipgram, skip=0, count=1):
        """Add a skipgram.

        Parameters
        ----------
        skipgram : tuple
            Skipgram to add.
        skip : int
            Number of skips this skipgram has.
        count : int, optional
            Count for the skipgram, for the convenience of not having to call this
            method multiple times if this skipgram occurs multiple times in your data.
        """
        self._add(skipgram, skip, count, validated=False)

    def _add(self, skipgram, skip, count, validated):
        if not validated:
            if not 1 <= len(skipgram) <= self.n:
                raise ValueError(f"length of {skipgram} is outside of [1, {self.n}]")
            _validate_skip(skip, self.skip)
        trie = self._tries[(len(skipgram), skip)]
        for token in skipgram[:-1]:
            trie = trie[token]
        last_token = skipgram[-1]
        if last_token in trie:
            trie[last_token] += count
        else:
            trie[last_token] = count

    def add_from_seq(self, seq, count=1):
        """Add skipgrams from a sequence.

        Parameters
        ----------
        seq : iterable
            A sequence (e.g., a list or tuple of strings as a sentence with
            words, or a string as a word with characters) from which skipgrams
            are extracted.
        count : int, optional
            Count for the skipgram, for the convenience of not having to call this
            method multiple times if this skipgram occurs multiple times in your data.
        """
        for n in range(1, min(self.n, len(seq)) + 1):
            for skip in range(0, max(min(self.skip, len(seq) - n) + 1, 1)):
                for ngram in skipgrams_from_seq(seq, n, skip):
                    self._add(ngram, skip=skip, count=count, validated=True)

    def count(self, skipgram, skip=0):
        """Return the skipgram's count.

        If the skipgram is longer than the order of this skipgram collection,
        or if the skipgram isn't found in this collection, then 0  is returned.

        Parameters
        ----------
        skipgram : tuple
            Skipgram to get the count for.
        skip : int
            Number of skips this skipgram has.

        Returns
        -------
        int
        """
        _validate_skip(skip, self.skip)
        if len(skipgram) > self.n:
            return 0
        trie = self._tries[(len(skipgram), skip)]
        count_ = _get_inner_trie_from_prefix(trie, skipgram)
        if isinstance(count_, dict) or not count_:
            return 0
        else:
            return count_

    def __contains__(self, skipgram):
        """Determine if the skipgram is found in this collection.

        Note that this function returns ``True`` if and only if the skipgram exactly
        matches an existing one in the collection.

        Parameters
        ----------
        skipgram : tuple
            Skipgram to check membership for.

        Returns
        -------
        bool
        """
        for skip in range(self.skip + 1):
            c = self.count(skipgram, skip=skip)
            if c:
                return c
        else:
            return 0

    def skipgrams_with_counts(self, n, skip=0, prefix=None):
        """Yield pairs of skipgrams and counts.

        Parameters
        ----------
        n : int
        skip : int
            Number of skips to yield skipgrams for.
        prefix : iterable, optional
            If provided, all yielded skipgrams start with this prefix.

        Yields
        ------
        tuple, int
            A skipgram (tuple) and its count (int)
        """
        yield from self._skipgrams_with_counts(n, skip, prefix, validated=False)

    def _skipgrams_with_counts(self, n, skip, prefix, validated):
        if not validated:
            _validate_n(n, upper_bound=self.n)
            _validate_skip(skip, upper_bound=self.skip)
        trie = self._tries[(n, skip)]
        yield from _flattened_ngrams_with_counts(trie, prefix)

    def combine(self, *others):
        """Combine collections of skipgrams in-place.

        If any new skipgram collections' ``n`` and/or ``skip`` is larger than those
        of the current collection, then the current collection's ``n`` and/or ``skip``
        will be coerced to enlarge so that the new skipgrams can fit.

        Parameters
        ----------
        *others : iterable of ``Skipgrams`` instances

        Raises
        ------
        TypeError
            If any item in `others` is not a ``Skipgrams`` instance.
        """
        for other in others:
            if not isinstance(other, Skipgrams):
                raise TypeError(f"arg must be a Skipgrams instance: {type(other)}")
            if other.n > self.n:
                self.n = other.n
            if other.skip > self.skip:
                self.skip = other.skip
            for n in range(1, other.n + 1):
                for skip in range(0, other.skip + 1):
                    for ngram, count in other._skipgrams_with_counts(
                        n=n, skip=skip, prefix=None, validated=True
                    ):
                        self._add(ngram, skip, count, validated=True)


class Ngrams(Skipgrams):
    """A collection of ngrams.

    Ngrams are a special case of skipgrams, where skip = 0. This class has methods
    inherited from ``Skipgrams``.
    """

    def __init__(self, n):
        super().__init__(n, skip=0)

    def ngrams_with_counts(self, n, prefix=None):
        yield from super(Ngrams, self).skipgrams_with_counts(n, skip=0, prefix=prefix)

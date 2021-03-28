"""ngrams: A lightweight Python package to handle ngrams

Author: Jackson L. Lee <jacksonlunlee@gmail.com>
License: MIT License
Source: https://github.com/jacksonllee/ngrams
"""

from collections import defaultdict, OrderedDict
from itertools import combinations
import pkg_resources


__version__ = pkg_resources.get_distribution("ngrams").version


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


def skipgrams_from_seq(seq, skip, n):
    all_indices = OrderedDict()  # used an ordered set
    for k in range(len(seq) - n + 1):
        for indices in combinations(range(skip + n), n):
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


class _NSkipgrams:

    def __init__(self, n, skip=0):
        if type(n) != int or n < 1:
            raise ValueError(f"n must be an integer >= 1: {n}")
        if type(skip) != int or skip < 0:
            raise ValueError(f"skip must be an integer >= 0: {skip}")
        self.n = n
        self.skip = skip
        self._tries = {(i + 1, k): _trie() for i in range(n) for k in range(skip + 1)}

    def _add(self, ngram, skip=0, count=1):
        if not 1 <= len(ngram) <= self.n:
            raise ValueError(f"length of {ngram} is outside of [1, {self.n}]")
        if not 0 <= skip <= self.skip:
            raise ValueError(f"skip is outside of [0, {self.skip}]: {skip}")
        trie = self._tries[(len(ngram), skip)]
        for token in ngram[:-1]:
            trie = trie[token]
        last_token = ngram[-1]
        if last_token in trie:
            trie[last_token] += count
        else:
            trie[last_token] = count

    def _add_from_seq(self, seq, count=1):
        for n in range(1, min(self.n, len(seq)) + 1):
            for skip in range(0, min(self.skip + 1, len(seq) - 1)):
                for ngram in skipgrams_from_seq(seq, skip, n):
                    self._add(ngram, skip=skip, count=count)

    def _count(self, ngram, skip=0):
        if not 0 <= skip <= self.skip:
            raise ValueError(f"skip is outside of [0, {self.skip}]: {skip}")
        if len(ngram) > self.n:
            return 0
        trie = self._tries[(len(ngram), skip)]
        count_ = _get_inner_trie_from_prefix(trie, ngram)
        if isinstance(count_, dict) or not count_:
            return 0
        else:
            return count_

    def __contains__(self, ngram):
        for skip in range(self.skip + 1):
            c = self._count(ngram, skip=skip)
            if c:
                return c
        else:
            return 0

    def total_count(self, order=None, unique=False):
        ngrams_with_counts = self.ngrams_with_counts(order)
        if unique:
            return sum(1 for _ in ngrams_with_counts)
        else:
            return sum(count for _, count in ngrams_with_counts)

    def ngrams_with_counts(self, order=None, prefix=None):
        """Yield the pairs of ngrams and counts for the given order.

        Parameters
        ----------
        order : int or iterable of int, optional
            Either an integer for a single order (e.g., `2`),
            or an iterable of integers for multiple orders (e.g., `(1, 2)`).
            If not provided or if it is `None`, all orders of
            (1, 2, ..., `self.order`) handled by this collection of ngrams
            are used.
        prefix : iterable, optional
            If provided, all yielded ngrams start with this prefix.

        Yields
        ------
        tuple, int
            An ngram (tuple) and its count (int)
        """
        if type(order) == int:
            orders = [order]
        elif hasattr(order, "__iter__"):
            orders = list(order)
            if not all(type(x) == int for x in orders):
                raise ValueError(f"all orders must be integers: {orders}")
        elif order is None:
            orders = range(1, self.n + 1)
        else:
            raise ValueError(f"`order` must be an int or an iterable of int: {order}")
        for n in orders:
            trie = self._tries[n]
            yield from _flattened_ngrams_with_counts(trie, prefix)

    def combine(self, *others):
        """Combine collections of ngrams in-place.

        Parameters
        ----------
        *others : iterable of Ngrams

        Raises
        ------
        TypeError
            If any item in `others` is not an `Ngrams` instance.
        """
        for other in others:
            if type(other) != Ngrams:
                raise TypeError(f"arg must be an Ngrams instance: {type(other)}")
            order = range(1, min(other.n, self.n) + 1)
            for ngram, count in other.ngrams_with_counts(order=order):
                self._add(ngram, count)


class Ngrams:
    """A collection of ngrams.

    Once initialized, ngrams can be added. The ngrams are internally stored
    in tries for memory efficiency. This class makes it convenient to
    keep track and access counts of ngrams.

    Attributes
    ----------
    order : int
        This collection handles ngrams where n is from {1, 2, ..., order}.
    """

    def __init__(self, order):
        """Initialize the `Ngrams` object.

        Parameters
        ----------
        order : int
            This collection handles ngrams where n is from {1, 2, ..., order}.

        Raises
        ------
        ValueError
            If `order` is not an integer >= 1.
        """
        if order < 1 or type(order) != int:
            raise ValueError(f"order must be an integer >= 1: {order}")
        self.order = order
        self._tries = {(i + 1): _trie() for i in range(order)}

    def add(self, ngram, count=1):
        """Add an ngram.

        Parameters
        ----------
        ngram : iterable
            ngram to add
        count : int, optional
            Count for the ngram being added. This is for the convenience of
            not having to call this method multiple times if this ngram
            occurs multiple times.
        """
        if not 1 <= len(ngram) <= self.order:
            raise ValueError(f"length of {ngram} is outside of [1, {self.order}]")
        trie = self._tries[len(ngram)]
        for token in ngram[:-1]:
            trie = trie[token]
        last_token = ngram[-1]
        if last_token in trie:
            trie[last_token] += count
        else:
            trie[last_token] = count

    def add_from_seq(self, seq, count=1):
        """Add ngrams from a sequence.

        Parameters
        ----------
        seq : iterable
            A sequence (e.g., a list or tuple of strings as a sentence with
            words, or a string as a word with characters) from which ngrams
            are extracted
        count : int, optional
            Count for the sequence being added. This is for the convenience of
            not having to call this method multiple times if this sequence
            occurs multiple times.
        """
        for n in range(1, min(self.order, len(seq)) + 1):
            for ngram in ngrams_from_seq(seq, n):
                self.add(ngram, count=count)

    def count(self, ngram):
        """Return the ngram's count.

        If the ngram is longer than the order of this ngram collection,
        or if the ngram isn't found in this collection,
        then 0 (zero) is returned.

        Parameters
        ----------
        ngram : iterable

        Returns
        -------
        int
        """
        if len(ngram) > self.order:
            return 0
        trie = self._tries[len(ngram)]
        count_ = _get_inner_trie_from_prefix(trie, ngram)
        if isinstance(count_, dict) or not count_:
            return 0
        else:
            return count_

    def __contains__(self, ngram):
        """Determine if the ngram is found in this collection.

        Note that this function returns True if and only if the ngram _exactly_
        matches one of the existing ones in the collection.
        Other kinds of matching (e.g., prefix or suffix) all return False.

        Parameters
        ----------
        ngram : iterable

        Returns
        -------
        bool
        """
        return bool(self.count(ngram))

    def total_count(self, order=None, unique=False):
        """Return the total count of all ngrams for the given order.

        Parameters
        ----------
        order : int or iterable of int, optional
            Either an integer for a single order (e.g., `2`),
            or an iterable of integers for multiple orders (e.g., `(1, 2)`).
            If not provided or if it is `None`, all orders of
            (1, 2, ..., `self.order`) handled by this collection of ngrams
            are used.
        unique : bool
            If False (the default), the returned number is the sum of all
            occurrences of the relevant ngrams.
            If True, the returned number is the number of _unique_ ngrams
            of the given order.

        Returns
        -------
        int
        """
        ngrams_with_counts = self.ngrams_with_counts(order)
        if unique:
            return sum(1 for _ in ngrams_with_counts)
        else:
            return sum(count for _, count in ngrams_with_counts)

    def ngrams_with_counts(self, order=None, prefix=None):
        """Yield the pairs of ngrams and counts for the given order.

        Parameters
        ----------
        order : int or iterable of int, optional
            Either an integer for a single order (e.g., `2`),
            or an iterable of integers for multiple orders (e.g., `(1, 2)`).
            If not provided or if it is `None`, all orders of
            (1, 2, ..., `self.order`) handled by this collection of ngrams
            are used.
        prefix : iterable, optional
            If provided, all yielded ngrams start with this prefix.

        Yields
        ------
        tuple, int
            An ngram (tuple) and its count (int)
        """
        if type(order) == int:
            orders = [order]
        elif hasattr(order, "__iter__"):
            orders = list(order)
            if not all(type(x) == int for x in orders):
                raise ValueError(f"all orders must be integers: {orders}")
        elif order is None:
            orders = range(1, self.order + 1)
        else:
            raise ValueError(f"`order` must be an int or an iterable of int: {order}")
        for n in orders:
            trie = self._tries[n]
            yield from _flattened_ngrams_with_counts(trie, prefix)

    def combine(self, *others):
        """Combine collections of ngrams in-place.

        Parameters
        ----------
        *others : iterable of Ngrams

        Raises
        ------
        TypeError
            If any item in `others` is not an `Ngrams` instance.
        """
        for other in others:
            if type(other) != Ngrams:
                raise TypeError(f"arg must be an Ngrams instance: {type(other)}")
            order = range(1, min(other.order, self.order) + 1)
            for ngram, count in other.ngrams_with_counts(order=order):
                self.add(ngram, count)

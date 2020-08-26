"""Define the `Ngrams` class and related tools to handle ngrams."""

import collections
import pkg_resources


__version__ = pkg_resources.get_distribution("ngrams").version


def _trie():
    return collections.defaultdict(_trie)


def _flattened_ngrams_with_counts(trie):
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

    for tokens in _flatten_trie(trie):
        ngram = tokens[:-1]
        count = tokens[-1]
        yield ngram, count


def _get_inner_trie_from_prefix(trie, ngram_prefix):
    for token in ngram_prefix:
        try:
            trie = trie[token]
        except KeyError:
            return None
    return trie


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
            raise ValueError(
                f"length of {ngram} is outside of [1, {self.order}]"
            )
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

    def total_count(self, order, unique=False):
        """Return the total count of all ngrams for the given order.

        Parameters
        ----------
        order : int
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

    def ngrams_with_counts(self, order):
        """Yield the pairs of ngrams and counts for the given order.

        Parameters
        ----------
        order : int

        Yields
        ------
        tuple, int
            A tuple of the ngram (tuple) and its count (int)
        """
        trie = self._tries[order]
        yield from _flattened_ngrams_with_counts(trie)

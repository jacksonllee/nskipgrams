nskipgrams
==========

.. image:: https://badge.fury.io/py/nskipgrams.svg
   :target: https://pypi.python.org/pypi/nskipgrams
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/nskipgrams.svg
   :target: https://pypi.python.org/pypi/nskipgrams
   :alt: Supported Python versions

.. image:: https://circleci.com/gh/jacksonllee/nskiprams/tree/main.svg?style=svg
   :target: https://circleci.com/gh/jacksonllee/nskipgrams/tree/main
   :alt: CircleCI Build

``nskipgrams`` is a lightweight Python package to work with ngrams and skipgrams.
Fields of study using ngrams and skipgrams from sequential data, especially
computational linguistics and natural language processing, will find
this package helpful.

Highlights:

* Simple: Store, access, and count ngrams and skipgrams -- that's it!
* Memory-efficient: Tries are used for internal storage.
* Hassle-free: No dependencies. Written in pure Python. Today is a great day.

Download and Install
--------------------

To download and install the most recent version::

    $ pip install --upgrade nskipgrams

Usage
-----

The following are defined:

- Ngrams
    - The class ``Ngrams`` handles a collection of ngrams.
    - The function ``ngrams_from_seq`` yields ngrams for a given sequence.
- Skipgrams
    - The class ``Skipgrams`` handles a collection of skipgrams.
    - The function ``skipgrams_from_seq`` yields skipgrams for a given sequence.

Getting Ngrams from a Sequence
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you simply need ngrams from a sequence, ``ngrams_from_seq`` is what you're looking for:

.. code-block:: python

    >>> from nskipgrams import ngrams_from_seq
    >>> for ngram in ngrams_from_seq("abcdef", n=2):
    ...     print(ngram)
    ('a', 'b')
    ('b', 'c')
    ('c', 'd')
    ('d', 'e')
    ('e', 'f')

Initializing an Ngram Collection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    >>> from nskipgrams import Ngrams
    >>> char_ngrams = Ngrams(n=3)  # handles unigrams, bigrams, and trigrams

Adding Ngrams
^^^^^^^^^^^^^

.. code-block:: python

    >>> char_ngrams.add_from_seq("my cats")
    >>> char_ngrams.add_from_seq("your cat", count=2)

Here, a sequence is anything that can be iterated over,
and the corresponding ngrams are extracted from the individual elements
off of the sequence.
For example, if the sequence is a text string like ``"my cats"`` above,
then the ngrams are character-based (hence the chosen variable name ``char_ngrams``).

To add a single ngram:

.. code-block:: python

    >>> char_ngrams.add(("y", "o", "u"))

As a best practice, it is recommended that an ngram be represented as a ``tuple``
regardless of what the individual elements are,
e.g., ``("y", "o", "u")`` for character-based ngrams.
As output examples show below, the ``tuple`` data type is also what this package
uses to represent ngrams.

Accessing Ngrams
^^^^^^^^^^^^^^^^

.. code-block:: python

    >>> for ngram, count in char_ngrams.ngrams_with_counts(n=1):  # unigrams
    ...     print(ngram, count)
    ...
    ('m',), 1
    ('y',), 3
    (' ',), 3
    ('c',), 3
    ('a',), 3
    ('t',), 3
    ('s',), 1
    ('o',), 2
    ('u',), 2
    ('r',), 2
    >>>
    >>> for ngram, count in char_ngrams.ngrams_with_counts(n=2):  # bigrams
    ...     print(ngram, count)
    ...
    ('m', 'y'), 1
    ('y', ' '), 1
    ('y', 'o'), 2
    (' ', 'c'), 3
    ('c', 'a'), 3
    ('a', 't'), 3
    ('t', 's'), 1
    ('o', 'u'), 2
    ('u', 'r'), 2
    ('r', ' '), 2
    >>>
    >>> for ngram, count in char_ngrams.ngrams_with_counts(n=3):  # trigrams
    ...     print(ngram, count)
    ...
    ('m', 'y', ' '), 1
    ('y', ' ', 'c'), 1
    ('y', 'o', 'u'), 3
    (' ', 'c', 'a'), 3
    ('c', 'a', 't'), 3
    ('a', 't', 's'), 1
    ('o', 'u', 'r'), 2
    ('u', 'r', ' '), 2
    ('r', ' ', 'c'), 2

Accessing Ngrams with a Specific Prefix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    >>> for ngram, count in char_ngrams.ngrams_with_counts(n=3, prefix=("y",)):
    ...     print(ngram, count)
    ...
    ('y', ' ', 'c'), 1
    ('y', 'o', 'u'), 3

Accessing the Count of a Specific Ngram
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    >>> char_ngrams.count(("c", "a", "t"))
    3

Checking Membership
^^^^^^^^^^^^^^^^^^^

To check if an ngram has an exact match in the collection so far:

.. code-block:: python

    >>> ("c", "a", "t") in char_ngrams
    True

Combining Collections of Ngrams
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To combine collections of ngrams (e.g., when you process data sources in parallel
and have multiple ``Ngrams`` objects):

.. code-block:: python

    >>> char_ngrams1 = Ngrams(n=2)
    >>> char_ngrams1.add_from_seq("my cat")
    >>> set(char_ngrams1.ngrams_with_counts(n=2))
    {((' ', 'c'), 1),
     (('a', 't'), 1),
     (('c', 'a'), 1),
     (('m', 'y'), 1),
     (('y', ' '), 1)}
    >>>
    >>> char_ngrams2 = Ngrams(n=2)
    >>> char_ngrams2.add_from_seq("your cats")
    >>> set(char_ngrams2.ngrams_with_counts(n=2))
    {((' ', 'c'), 1),
     (('a', 't'), 1),
     (('c', 'a'), 1),
     (('o', 'u'), 1),
     (('r', ' '), 1),
     (('t', 's'), 1),
     (('u', 'r'), 1),
     (('y', 'o'), 1)}
    >>>
    >>> char_ngrams3 = Ngrams(n=2)
    >>> char_ngrams3.add_from_seq("her cats")
    >>> set(char_ngrams3.ngrams_with_counts(n=2))
    {((' ', 'c'), 1),
     (('a', 't'), 1),
     (('c', 'a'), 1),
     (('e', 'r'), 1),
     (('h', 'e'), 1),
     (('r', ' '), 1),
     (('t', 's'), 1)}
    >>>
    >>> char_ngrams1.combine(char_ngrams2, char_ngrams3)  # `combine` takes as many Ngrams objects as desired
    >>> set(char_ngrams1.ngrams_with_counts(n=2))
    {((' ', 'c'), 3),
     (('a', 't'), 3),
     (('c', 'a'), 3),
     (('e', 'r'), 1),
     (('h', 'e'), 1),
     (('m', 'y'), 1),
     (('o', 'u'), 1),
     (('r', ' '), 2),
     (('t', 's'), 2),
     (('u', 'r'), 1),
     (('y', ' '), 1),
     (('y', 'o'), 1)}

If you don't want to mutate any of the ``Ngrams`` instances
(the ``combine`` method works in-place and mutates ``these_ngrams``
when ``these_ngrams.combine`` is called),
then you can create an empty ngram collection and combine into it
all of your ngrams:

.. code-block:: python

    >>> collections = [char_ngrams1, char_ngrams2, char_ngrams3]
    >>> all_ngrams = Ngrams(n=2)  # A new, empty collection of ngrams
    >>> all_ngrams.combine(*collections)

Any "Sequences" and their Corresponding "Ngrams" Work
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While the examples above use text strings as sequences and character-based ngrams,
another common usage in computational linguistics and NLP is to have
segmented phrases/sentences as sequences and word-based ngrams:

.. code-block:: python

    >>> from nskipgrams import Ngrams
    >>> word_ngrams = Ngrams(n=2)
    >>> word_ngrams.add_from_seq(("in", "the", "beginning"))
    >>> word_ngrams.add_from_seq(("in", "the", "end"))
    >>> for ngram, count in word_ngrams.ngrams_with_counts(n=2):
    ...     print(ngram, count)
    ...
    ('in', 'the'), 2
    ('the', 'beginning'), 1
    ('the', 'end'), 1

Skipgrams
^^^^^^^^^

Ngrams are a special case of skipgrams, with skip = 0.
The class ``Skipgrams`` works the same as ``Ngrams``, with the following differences:

* ``Skipgrams`` has the method ``skipgrams_with_counts`` rather than ``ngrams_with_counts``.
  ``skipgrams_with_counts`` also has the keyword argument ``skip``
  (in addition to ``n`` and ``prefix``).
* For ``Skipgrams``, the methods ``add`` and ``count``, as well as collection instantiation
  (i.e., ``__init__``), also have a meaningful ``skip`` keyword argument.

The function ``skipgrams_from_seq`` works the same as ``ngrams_from_seq``, but has
the ``skip`` keyword argument (in addition to ``seq`` and ``n``).

License
-------

MIT License. Please see ``LICENSE.txt`` in the GitHub source code for details.

Changelog
---------

Please see ``CHANGELOG.md`` in the GitHub source code.

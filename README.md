# ngrams

[![CircleCI](https://circleci.com/gh/jacksonllee/ngrams/tree/main.svg?style=svg)](https://circleci.com/gh/jacksonllee/ngrams/tree/main)

`ngrams` is a lightweight Python package that makes it convenient to
keep track of ngrams.
Fields of study using ngrams from sequential data, especially
computational linguistics and natural language processing, will find
this package helpful.

## Usage

To initialize an empty collection of ngrams:

```python
>>> from ngrams import Ngrams
>>> char_ngrams = Ngrams(order=3)  # handles unigrams, bigrams, and trigrams
```

To add ngrams from a sequence:

```python
>>> char_ngrams.add_from_seq("my cats")
>>> char_ngrams.add_from_seq("your cat", count=2)
```

To iterate through the collected ngrams of a given order:

```python
# `list` below just materializes the generator for demo here, not necessary in actual usage
>>> list(char_ngrams.ngrams_with_counts(order=2))
[(('m', 'y'), 1),
 (('y', ' '), 1),
 (('y', 'o'), 2),
 ((' ', 'c'), 3),
 (('c', 'a'), 3),
 (('a', 't'), 3),
 (('t', 's'), 1),
 (('o', 'u'), 2),
 (('u', 'r'), 2),
 (('r', ' '), 2)]
```

To get the total count for a given order:

```python
>>> char_ngrams.total_count(order=2)
20
>>> char_ngrams.total_count(order=2, unique=True)  # counts the number of unique ngrams
10
```

To get the count of a particular ngram:

```python
>>> char_ngrams.count(("c", "a", "t"))
3
```

To check if an ngram has an exact match in the collection so far:

```python
>>> ("c", "a", "t") in char_ngrams
True
```

If instead of sequences you have ngrams to add directly:

```python
>>> char_ngrams.add(("f", "o", "o"))  # `add` here versus `add_from_seq` above
>>> ("f", "o", "o") in char_ngrams
True
```

The terms "ngrams" and "sequences" are generic
and can represent any compatible concepts.
While the examples above use text strings as sequences and character-based ngrams,
another common usage in computational linguistics and NLP is to have
segmented phrases/sentences as sequences and word-based ngrams:

```python
>>> from ngrams import Ngrams
>>> word_ngrams = Ngrams(order=2)
>>> word_ngrams.add_from_seq(("in", "the", "beginning"))
>>> word_ngrams.add_from_seq(("in", "the", "end"))
>>> list(word_ngrams.ngrams_with_counts(order=2))
[(('in', 'the'), 2),
 (('the', 'beginning'), 1),
 (('the', 'end'), 1)]
```

## Installation

Python 3.6 or above is required.

To install from the command line:

```bash
pip install -e git://github.com/jacksonllee/ngrams.git@v0.1.0#egg=ngrams
```

To include this package in `requirements.txt` ...

```
-e git://github.com/jacksonllee/ngrams.git@v0.1.0#egg=ngrams
```

... or in `setup.py`:

```python
setup(
    # ...
    install_requires=[
        # ...
        "ngrams @ git+https://github.com/jacksonllee/ngrams@v0.1.0#egg=ngrams",
        # ...
    ],
    # ...
)
```

If you would like to install by cloning (e.g., for development):

```bash
git clone https://github.com/jacksonllee/ngrams.git
cd ngrams
pip install -r dev-requirements.txt  # For running the linter and tests
pip install -e .
```

## License

MIT License. Please see [`LICENSE.txt`](LICENSE.txt).

## Changelog

Please see [`CHANGELOG.md`](CHANGELOG.md).

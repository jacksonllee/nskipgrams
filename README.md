# ngrams

[![DOI](https://zenodo.org/badge/290420602.svg)](https://zenodo.org/badge/latestdoi/290420602)
[![CircleCI](https://circleci.com/gh/jacksonllee/ngrams/tree/main.svg?style=svg)](https://circleci.com/gh/jacksonllee/ngrams/tree/main)

`ngrams` is a lightweight Python package that makes it convenient to
keep track of ngrams.
Fields of study using ngrams from sequential data, especially
computational linguistics and natural language processing, will find
this package helpful.

* Memory-efficient: Ngrams are internally stored in tries.
* Well-tested: Unit tests cover all supported functionality, run by continuous integration.
* Hassle-free: No dependencies. Written in pure Python. Today is a great day.

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

Here, a sequence is anything that can be iterated over,
and the corresponding ngrams are extracted from the individual elements
off of the sequence.
For example, if the sequence is a text string like `"my cats"` above,
then the ngrams are character-based (hence the chosen variable name `char_ngrams`).

To add a single ngram:

```python
>>> char_ngrams.add(("y", "o", "u"))
```

To iterate through the collected ngrams:

```python
>>> for ngram, count in char_ngrams.ngrams_with_counts():
...     print(ngram, count)
...
('m',) 1
('y',) 3
(' ',) 3
('c',) 3
('a',) 3
('t',) 3
('s',) 1
('o',) 2
('u',) 2
('r',) 2
('m', 'y') 1
('y', ' ') 1
('y', 'o') 2
(' ', 'c') 3
('c', 'a') 3
('a', 't') 3
('t', 's') 1
('o', 'u') 2
('u', 'r') 2
('r', ' ') 2
('m', 'y', ' ') 1
('y', ' ', 'c') 1
('y', 'o', 'u') 3
(' ', 'c', 'a') 3
('c', 'a', 't') 3
('a', 't', 's') 1
('o', 'u', 'r') 2
('u', 'r', ' ') 2
('r', ' ', 'c') 2
```

To iterate with a specific order...

```python
>>> for ngram, count in char_ngrams.ngrams_with_counts(order=2):
...     print(ngram, count)
...
('m', 'y') 1
('y', ' ') 1
('y', 'o') 2
(' ', 'c') 3
('c', 'a') 3
('a', 't') 3
('t', 's') 1
('o', 'u') 2
('u', 'r') 2
('r', ' ') 2
```

...or with a particular prefix:

```python
>>> for ngram, count in char_ngrams.ngrams_with_counts(prefix=("y",)):
...     print(ngram, count)
...
('y',) 3
('y', ' ') 1
('y', 'o') 2
('y', ' ', 'c') 1
('y', 'o', 'u') 3
```

...or with both order and prefix specified:

```python
>>> for ngram, count in char_ngrams.ngrams_with_counts(order=2, prefix=("y",)):
...     print(ngram, count)
...
('y', ' ') 1
('y', 'o') 2
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

While the examples above use text strings as sequences and character-based ngrams,
another common usage in computational linguistics and NLP is to have
segmented phrases/sentences as sequences and word-based ngrams:

```python
>>> from ngrams import Ngrams
>>> word_ngrams = Ngrams(order=2)
>>> word_ngrams.add_from_seq(("in", "the", "beginning"))
>>> word_ngrams.add_from_seq(("in", "the", "end"))
>>> for ngram, count in word_ngrams.ngrams_with_counts(order=2):
...     print(ngram, count)
...
('in', 'the') 2
('the', 'beginning') 1
('the', 'end') 1
```

## Installation

Python 3.6 or above is required.

To install from the command line:

```bash
pip install git+https://github.com/jacksonllee/ngrams@v0.1.0#egg=ngrams
```

To include this package in `requirements.txt` ...

```
git+https://github.com/jacksonllee/ngrams@v0.1.0#egg=ngrams
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

## Citation

Lee, Jackson L. 2020. ngrams: A lightweight Python package to keep track of ngrams. https://doi.org/10.5281/zenodo.4002095

```bibtex
@software{leengrams,
  author       = {Jackson L. Lee},
  title        = {ngrams: A lightweight Python package to keep track of ngrams},
  year         = 2020,
  doi          = {10.5281/zenodo.4002095},
  url          = {https://doi.org/10.5281/zenodo.4002095}
}
```

## License

MIT License. Please see [`LICENSE.txt`](LICENSE.txt).

## Changelog

Please see [`CHANGELOG.md`](CHANGELOG.md).

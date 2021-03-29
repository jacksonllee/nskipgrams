import itertools
import os
import re

import pytest

import ngrams


@pytest.fixture
def ngrams_for_testing():
    test_ngrams = ngrams.Ngrams(n=3)
    seqs = [
        "ab",
        "abc",
        "abcde",
        "abcde",
        "abcde",
        "abcdef",
        "abcdef",
    ]
    for seq in seqs:
        test_ngrams.add_from_seq(seq)
    return test_ngrams


@pytest.mark.parametrize(
    "seq, n, expected",
    [
        ("abcd", 2, [("a", "b"), ("b", "c"), ("c", "d")]),
        ("abcd", 3, [("a", "b", "c"), ("b", "c", "d")]),
    ],
)
def test_ngrams_from_seq(seq, n, expected):
    actual = list(ngrams.ngrams_from_seq(seq, n))
    assert actual == expected


@pytest.mark.parametrize(
    "seq, n, skip, expected",
    [
        # Example from https://en.wikipedia.org/wiki/N-gram#Skip-gram
        (
            "the rain in Spain falls mainly on the plain".split(),
            2,
            1,
            [
                ("the", "rain"),
                ("the", "in"),
                ("rain", "in"),
                ("rain", "Spain"),
                ("in", "Spain"),
                ("in", "falls"),
                ("Spain", "falls"),
                ("Spain", "mainly"),
                ("falls", "mainly"),
                ("falls", "on"),
                ("mainly", "on"),
                ("mainly", "the"),
                ("on", "the"),
                ("on", "plain"),
                ("the", "plain"),
            ],
        ),
    ],
)
def test_skipgrams_from_seq(seq, n, skip, expected):
    actual = list(ngrams.skipgrams_from_seq(seq, n, skip))
    assert actual == expected


@pytest.mark.parametrize("order", [-1, 0, 1.5])
def test_weird_order(order):
    with pytest.raises(ValueError):
        ngrams.Ngrams(n=order)


@pytest.mark.parametrize("ngram", ["", "abcd"])
def test_add_weird_ngram_length(ngram):
    with pytest.raises(ValueError):
        ngrams.Ngrams(n=3).add(ngram)


@pytest.mark.parametrize(
    "ngram, expected",
    [("ab", 7), ("def", 2), ("random", 0), ("foo", 0)],
)
def test_count(ngram, expected, ngrams_for_testing):
    actual = ngrams_for_testing.count(ngram)
    assert actual == expected


@pytest.mark.parametrize(
    "ngram, expected",
    [("ab", True), ("def", True), ("random", False), ("foo", False)],
)
def test___contains__(ngram, expected, ngrams_for_testing):
    actual = ngram in ngrams_for_testing
    assert actual == expected


@pytest.mark.parametrize(
    "order, expected",
    [
        (
            1,
            {
                (("a",), 7),
                (("b",), 7),
                (("c",), 6),
                (("d",), 5),
                (("e",), 5),
                (("f",), 2),
            },
        ),
        (
            2,
            {
                (("a", "b"), 7),
                (("b", "c"), 6),
                (("c", "d"), 5),
                (("d", "e"), 5),
                (("e", "f"), 2),
            },
        ),
        (
            3,
            {
                (("a", "b", "c"), 6),
                (("b", "c", "d"), 5),
                (("c", "d", "e"), 5),
                (("d", "e", "f"), 2),
            },
        ),
    ],
)
def test_ngrams_with_counts(order, expected, ngrams_for_testing):
    actual = set(ngrams_for_testing.ngrams_with_counts(order))
    assert actual == expected


@pytest.mark.parametrize(
    "order, prefix, expected",
    [
        (1, ("b",), {(("b",), 7)}),
        (1, ("s",), set()),
        (1, ("a", "b"), set()),
        (2, ("b",), {(("b", "c"), 6)}),
        (2, ("b", "c"), {(("b", "c"), 6)}),
        (2, ("b", "a"), set()),
        (2, ("a", "b", "c"), set()),
        (3, ("a",), {(("a", "b", "c"), 6)}),
        (3, ("a", "b"), {(("a", "b", "c"), 6)}),
        (3, ("a", "b", "c"), {(("a", "b", "c"), 6)}),
        (3, ("a", "c", "b"), set()),
        (3, ("a", "b", "c", "d"), set()),
    ],
)
def test_ngrams_with_counts_with_prefix(order, prefix, expected, ngrams_for_testing):
    actual = set(ngrams_for_testing.ngrams_with_counts(order, prefix=prefix))
    assert actual == expected


@pytest.mark.parametrize("order", ["foobar", 1.5])
def test_ngrams_with_counts_with_wrong_order_type(order, ngrams_for_testing):
    with pytest.raises(ValueError):
        set(ngrams_for_testing.ngrams_with_counts(order))


def test_version_number_match_with_changelog():
    """__version__ and CHANGELOG.md match for the latest version number."""
    repo_dir = os.path.dirname(os.path.realpath(__file__))
    changelog = open(os.path.join(repo_dir, "CHANGELOG.md")).read()
    # latest version number in changelog = the 1st occurrence of '[x.y.z]'
    version_in_changelog = (
        re.search(r"\[\d+\.\d+\.\d+\]", changelog).group().strip("[]")
    )
    assert ngrams.__version__ == version_in_changelog, (
        f"Make sure both __version__ ({ngrams.__version__}) and "
        f"CHANGELOG ({version_in_changelog}) "
        "are updated to match the latest version number"
    )


def test_combine():
    char_ngrams1 = ngrams.Ngrams(n=2)
    char_ngrams1.add_from_seq("my cat")
    all_ngrams_with_counts = itertools.chain(
        char_ngrams1.ngrams_with_counts(n=1), char_ngrams1.ngrams_with_counts(n=2)
    )
    assert set(all_ngrams_with_counts) == {
        (("c",), 1),
        (("t",), 1),
        ((" ",), 1),
        (("a",), 1),
        (("m",), 1),
        (("y",), 1),
        ((" ", "c"), 1),
        (("a", "t"), 1),
        (("c", "a"), 1),
        (("m", "y"), 1),
        (("y", " "), 1),
    }

    char_ngrams2 = ngrams.Ngrams(n=2)
    char_ngrams2.add_from_seq("your cats")
    all_ngrams_with_counts = itertools.chain(
        char_ngrams2.ngrams_with_counts(n=1), char_ngrams2.ngrams_with_counts(n=2)
    )
    assert set(all_ngrams_with_counts) == {
        (("c",), 1),
        (("y",), 1),
        (("s",), 1),
        (("a",), 1),
        (("t",), 1),
        ((" ",), 1),
        (("u",), 1),
        (("o",), 1),
        (("r",), 1),
        ((" ", "c"), 1),
        (("a", "t"), 1),
        (("c", "a"), 1),
        (("o", "u"), 1),
        (("r", " "), 1),
        (("t", "s"), 1),
        (("u", "r"), 1),
        (("y", "o"), 1),
    }

    char_ngrams3 = ngrams.Ngrams(n=2)
    char_ngrams3.add_from_seq("her cats")
    all_ngrams_with_counts = itertools.chain(
        char_ngrams3.ngrams_with_counts(n=1), char_ngrams3.ngrams_with_counts(n=2)
    )
    assert set(all_ngrams_with_counts) == {
        (("s",), 1),
        (("t",), 1),
        (("a",), 1),
        ((" ",), 1),
        (("h",), 1),
        (("r",), 1),
        (("e",), 1),
        (("c",), 1),
        ((" ", "c"), 1),
        (("a", "t"), 1),
        (("c", "a"), 1),
        (("e", "r"), 1),
        (("h", "e"), 1),
        (("r", " "), 1),
        (("t", "s"), 1),
    }

    char_ngrams1.combine(char_ngrams2, char_ngrams3)
    all_ngrams_with_counts = itertools.chain(
        char_ngrams1.ngrams_with_counts(n=1), char_ngrams1.ngrams_with_counts(n=2)
    )
    assert set(all_ngrams_with_counts) == {
        (("u",), 1),
        (("r",), 2),
        (("h",), 1),
        (("y",), 2),
        (("a",), 3),
        (("e",), 1),
        (("c",), 3),
        (("o",), 1),
        (("m",), 1),
        (("s",), 2),
        (("t",), 3),
        ((" ",), 3),
        ((" ", "c"), 3),
        (("a", "t"), 3),
        (("c", "a"), 3),
        (("e", "r"), 1),
        (("h", "e"), 1),
        (("m", "y"), 1),
        (("o", "u"), 1),
        (("r", " "), 2),
        (("t", "s"), 2),
        (("u", "r"), 1),
        (("y", " "), 1),
        (("y", "o"), 1),
    }


def test_combine_wrong_data_type(ngrams_for_testing):
    with pytest.raises(TypeError):
        ngrams_for_testing.combine("foobar")

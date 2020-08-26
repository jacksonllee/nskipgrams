import os
import re

import pytest

import ngrams


@pytest.fixture
def ngrams_for_testing():
    test_ngrams = ngrams.Ngrams(3)
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


@pytest.mark.parametrize("order", [-1, 0, 1.5])
def test_weird_order(order):
    with pytest.raises(ValueError):
        ngrams.Ngrams(order)


@pytest.mark.parametrize("ngram", ["", "abcd"])
def test_add_weird_ngram_length(ngram):
    with pytest.raises(ValueError):
        ngrams.Ngrams(3).add(ngram)


@pytest.mark.parametrize(
    "ngram, expected", [("ab", 7), ("def", 2), ("random", 0), ("foo", 0)],
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
    "order, unique, expected",
    [
        (1, True, 6),
        (1, False, 32),
        (2, True, 5),
        (2, False, 25),
        (3, True, 4),
        (3, False, 18),
    ],
)
def test_total_count(order, unique, expected, ngrams_for_testing):
    actual = ngrams_for_testing.total_count(order, unique)
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

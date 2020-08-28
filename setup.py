import os
from setuptools import setup


_THIS_DIR = os.path.dirname(__file__)
with open(os.path.join(_THIS_DIR, "README.md")) as f:
    _LONG_DESCRIPTION = f.read().strip()

_VERSION = "0.2.0"


def main():
    setup(
        name="ngrams",
        version=_VERSION,
        description="Make it easy to keep track of ngrams",
        long_description=_LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        url="https://github.com/jacksonllee/ngrams",
        author="Jackson L. Lee",
        author_email="jacksonlunlee@gmail.com",
        license="MIT License",
        py_modules=["ngrams"],
        python_requires=">=3.6",
        setup_requires="setuptools>=39",
        data_files=[(".", ["README.md", "LICENSE.txt", "CHANGELOG.md"])],
        zip_safe=False,
    )


if __name__ == "__main__":
    main()

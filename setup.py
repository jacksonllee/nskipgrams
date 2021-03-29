import os
from setuptools import setup


_THIS_DIR = os.path.dirname(__file__)
with open(os.path.join(_THIS_DIR, "README.rst")) as f:
    _LONG_DESCRIPTION = f.read().strip()

_VERSION = "0.3.0"


def main():
    setup(
        name="nskipgrams",
        version=_VERSION,
        description="A lightweight Python package to work with ngrams and skipgrams",
        long_description=_LONG_DESCRIPTION,
        long_description_content_type="text/x-rst",
        url="https://github.com/jacksonllee/nskipgrams",
        project_urls={
            "Bug Tracker": "https://github.com/jacksonllee/nskipgrams/issues",
            "Source Code": "https://github.com/jacksonllee/nskipgrams",
        },
        download_url="https://pypi.org/project/nskipgrams/#files",
        author="Jackson L. Lee",
        author_email="jacksonlunlee@gmail.com",
        license="MIT License",
        py_modules=["nskipgrams"],
        python_requires=">=3.6",
        setup_requires="setuptools>=39",
        data_files=[(".", ["README.rst", "LICENSE.txt", "CHANGELOG.md"])],
        keywords=[
            "computational linguistics",
            "natural language processing",
            "NLP",
            "linguistics",
            "language",
            "ngrams",
            "skipgrams",
        ],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Scientific/Engineering :: Human Machine Interfaces",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Text Processing",
            "Topic :: Text Processing :: Filters",
            "Topic :: Text Processing :: General",
            "Topic :: Text Processing :: Indexing",
            "Topic :: Text Processing :: Linguistic",
        ],
        zip_safe=False,
    )


if __name__ == "__main__":
    main()

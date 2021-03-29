# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [0.3.0] - 2021-03-28

### Added
- Added the new class `Skipgrams` (which `Ngrams` subclasses from now).

### Changed
- Changed package name from `ngrams` to `nskipgrams`.
- In various methods of `Ngrams`, the argument name `order` has been changed
  into `n`.

### Removed
- Removed the `total_count` method of `Ngrams`.
  Now that `Skipgrams` is added,
  `total_count` would be too confusing and/or not of much use in practice.

## [0.2.1] - 2020-09-06

### Fixed
* Avoided creating empty inner tries unnecessarily in the internal tries.

## [0.2.0] - 2020-08-28

### Added
* Implemented the prefix option and multiple orders in `Ngrams.ngrams_with_counts`.
* Implemented `Ngrams.combine` to combine collections of ngrams.

## [0.1.0] - 2020-08-26

Initial release

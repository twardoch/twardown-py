# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Git-tag-based semversioning with hatch-vcs
- Comprehensive test suite with 94% coverage
- Build and release scripts in `scripts/` directory
- GitHub Actions CI/CD pipeline for testing and releasing
- Multiplatform support (Linux, Windows, macOS)
- Python 3.8-3.12 support

### Changed
- Dynamic version detection from git tags
- Improved code quality with ruff and mypy
- Enhanced documentation and developer experience

## [0.1.0] - 2025-01-17

### Added
- Initial release with basic Markdown extension functionality
- Magic record preprocessor for file path tracking
- Task list processor for GitHub-style checkboxes
- Support for tables, fenced code, and metadata
- Configurable extension features
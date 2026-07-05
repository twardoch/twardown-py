# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Real GitHub Actions workflows: `ci.yml` (lint, type-check, test across Python
  3.10–3.13 on Linux/Windows/macOS) and `release.yml` (build, GitHub release,
  and PyPI trusted publishing on `v*` tags).
- Jekyll + Just the Docs documentation under `docs/` (home and usage pages),
  cross-linked to the twardown flavor spec (twardown-docs) and twardown-js.
- Render-fixture conformance tests pinning the flavor's expected HTML output.
- Project icon at `docs/assets/icon.png`.
- PyPI metadata: keywords and trove classifiers.

### Changed
- Raised the minimum Python to 3.10. The code already used PEP 585 builtin
  generics (`list[str]`), which never ran on the previously declared 3.8, so the
  floor now matches reality.
- Dropped the unused `importlib-metadata` backport dependency and its dead
  pre-3.8 import fallback; `importlib.metadata` is standard library on all
  supported versions.

### Removed
- `GITHUB_ACTIONS.md` — superseded by the actual workflow files.

## [0.1.0] - 2025-01-17

### Added
- Initial release with basic Markdown extension functionality
- Magic record preprocessor for file path tracking
- Task list processor for GitHub-style checkboxes
- Support for tables, fenced code, and metadata
- Configurable extension features
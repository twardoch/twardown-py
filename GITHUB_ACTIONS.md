# GitHub Actions Configuration

Due to permission constraints, the GitHub Actions workflow files need to be manually created in the repository. Below are the complete workflow configurations for CI/CD:

## Test Workflow

Create `.github/workflows/test.yml`:

```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v --cov=twardown_py --cov-report=xml --cov-report=term-missing
    
    - name: Run code quality checks
      run: |
        python -m ruff check src tests
        python -m mypy src
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v4
      if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.12'
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
        token: ${{ secrets.CODECOV_TOKEN }}
```

## Release Workflow

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - "v*"

permissions:
  contents: write
  id-token: write

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v --cov=twardown_py --cov-report=xml --cov-fail-under=90
    
    - name: Run code quality checks
      run: |
        python -m ruff check src tests
        python -m mypy src

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"
    
    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: |
        python -m build
    
    - name: Check package
      run: |
        python -m twine check dist/*
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v4
      with:
        name: dist
        path: dist/

  release:
    needs: build
    runs-on: ubuntu-latest
    environment: release
    
    steps:
    - name: Download artifacts
      uses: actions/download-artifact@v4
      with:
        name: dist
        path: dist/
    
    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref_name }}
        release_name: Release ${{ github.ref_name }}
        body: |
          Release ${{ github.ref_name }}
          
          See [CHANGELOG.md](https://github.com/twardoch/twardown-py/blob/main/CHANGELOG.md) for details.
        draft: false
        prerelease: ${{ contains(github.ref_name, '-') }}
    
    - name: Upload Release Assets
      uses: actions/upload-release-asset@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        upload_url: ${{ steps.create_release.outputs.upload_url }}
        asset_path: dist/
        asset_name: dist
        asset_content_type: application/zip
    
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        user: __token__
        password: ${{ secrets.PYPI_API_TOKEN }}
```

## Setup Instructions

1. Create the `.github/workflows/` directory in your repository
2. Add the above workflow files
3. Configure the following secrets in your GitHub repository:
   - `PYPI_API_TOKEN`: PyPI API token for publishing
   - `CODECOV_TOKEN`: (optional) Codecov token for coverage reporting

## Features

- **Automated Testing**: Runs tests on multiple Python versions and platforms
- **Release Automation**: Creates releases and publishes to PyPI on git tag push
- **Quality Checks**: Runs linting, formatting, and type checking
- **Artifact Generation**: Creates wheel and source distributions
- **Coverage Reporting**: Uploads coverage reports to Codecov
---
this_file: twardown-py/README.md
---

# twardown-py: An Opinionated Python Markdown Extension

**twardown-py** is a Python package that extends the functionality of the standard `Python-Markdown` library. It implements the "Twardown flavor," an opinionated set of enhancements and features designed to streamline Markdown processing for specific workflows, particularly those requiring file path tracking and GitHub Flavored Markdown (GFM) compatibility.

This extension is for Python developers who use the `Python-Markdown` library and are looking for an easy way to add a bundle of useful features, such as automatic file path embedding, task lists, and GFM-style tables, without configuring multiple individual extensions. It's particularly useful for projects where Markdown documents need to be aware of their source file location or require a consistent set of modern Markdown features.

## Features

`twardown-py` provides the following enhancements:

*   **Magic File Path Records**: Automatically inserts a `this_file: path/to/file.md` entry into the Markdown metadata. This is useful for documentation systems or static site generators that need to trace back to the source Markdown file.
*   **Enhanced Frontmatter Handling**: Works seamlessly with Markdown frontmatter (YAML blocks at the start of the file). The Magic Record is designed to be compatible with existing frontmatter.
*   **GFM-Style Tables**: Enables table parsing similar to GitHub Flavored Markdown.
*   **GFM-Style Task Lists**: Supports task lists with checkboxes (`- [ ]` and `- [x]`).
*   **Code Block Highlighting**: Provides syntax highlighting for fenced code blocks, leveraging the `CodeHilite` extension.
*   **Table of Contents Generation**: Can automatically generate a table of contents for your document, based on headings.
*   **Metadata Support**: Allows defining and extracting metadata from Markdown documents.

## Installation

You can install `twardown-py` using `pip` (or `uv pip`):

```bash
pip install twardown-py
```

If you are using `uv`:

```bash
uv pip install twardown-py
```

## Usage

`twardown-py` is used as an extension with the `Python-Markdown` library.

### Programmatic Usage

Here's a basic example of how to use `twardown-py`:

```python
import markdown
from twardown_py import TwardownExtension

# Example Markdown content
markdown_text = """\
// this_file: example.md (This line will be ignored if magic_records is enabled and configured)
# Example Document

This is a Twardown-enhanced document.

- [x] First task completed
- [ ] Second task pending
"""

# Create a Markdown instance with the TwardownExtension
# 'filename' is recommended for the magic record feature.
md = markdown.Markdown(extensions=[TwardownExtension(filename="example.md")])

# Convert Markdown to HTML
html_output = md.convert(markdown_text)

print(html_output)
```

This will produce HTML that includes the processed task list and, if `enable_magic_records` is true (default), the metadata will contain `this_file: example.md`.

### Configuration

You can configure `TwardownExtension` by passing keyword arguments when initializing it.

```python
from twardown_py import TwardownExtension

# Example: Disable tables and magic records, keep filename for other purposes
config = {
    "filename": "my_document.md",
    "enable_tables": False,
    "enable_magic_records": False,
    "enable_task_lists": True,
    # ... other options
}
my_extension = TwardownExtension(**config)

# md = markdown.Markdown(extensions=[my_extension])
# html = md.convert("Your markdown here")
```

Available configuration options:

| Option                     | Type    | Default | Description                                                                 |
| -------------------------- | ------- | ------- | --------------------------------------------------------------------------- |
| `filename`                 | `str`   | `""`    | Name of the file being processed. Used by `MagicRecordPreprocessor`.        |
| `enable_tables`            | `bool`  | `True`  | Enable GFM-style table support (`TableExtension`).                          |
| `enable_fenced_code`       | `bool`  | `True`  | Enable fenced code blocks (`FencedCodeExtension`).                          |
| `enable_code_highlighting` | `bool`  | `True`  | Enable code syntax highlighting (`CodeHiliteExtension`).                    |
| `enable_toc`               | `bool`  | `True`  | Enable table of contents generation (`TocExtension`).                       |
| `enable_meta`              | `bool`  | `True`  | Enable metadata handling (`MetaExtension`).                                   |
| `enable_task_lists`        | `bool`  | `True`  | Enable GFM-style task lists (custom `TaskListProcessor`).                   |
| `enable_magic_records`     | `bool`  | `True`  | Enable automatic `this_file:` record injection (custom `MagicRecordPreprocessor`). |

---

## Technical Details

### How It Works

`twardown-py` is an extension for the `Python-Markdown` library. It bundles several standard Markdown extensions and introduces custom processors.

*   **`TwardownExtension`**: This is the main entry point. Its `extendMarkdown` method registers all configured components (both standard extensions and custom processors) with the `Python-Markdown` instance. It manages the configuration options that enable or disable specific features.

*   **Custom Processors**:
    *   **`MagicRecordPreprocessor`**: This preprocessor runs early in the Markdown processing pipeline (priority 175). If `enable_magic_records` is true and a `filename` is provided, it checks the input document. If a `this_file:` key is not already present within a YAML frontmatter block, it prepends a new frontmatter block containing `this_file: <filename>`. This ensures the file path information is available in `md.Meta`.
    *   **`TaskListProcessor`**: This block processor identifies lines starting with `- [ ]` or `- [x]` (GFM task list syntax). It transforms these lines into HTML list items (`<li>`) containing checkboxes (`<input type="checkbox">`). By default, these checkboxes are rendered as `disabled`. Checked items (`- [x]`) will have the `checked` attribute.

*   **Standard Extensions Integration**: Based on the configuration, `TwardownExtension` initializes and registers the following standard `Python-Markdown` extensions:
    *   `markdown.extensions.meta.MetaExtension`: For metadata extraction.
    *   `markdown.extensions.tables.TableExtension`: For GFM-style tables.
    *   `markdown.extensions.fenced_code.FencedCodeExtension`: For code blocks.
    *   `markdown.extensions.codehilite.CodeHiliteExtension`: For syntax highlighting in code blocks. Requires `Pygments` to be installed.
    *   `markdown.extensions.toc.TocExtension`: For generating a Table of Contents.

### Project Structure

*   `src/twardown_py/__init__.py`: Contains the main source code for the extension, including all classes (`TwardownExtension`, `MagicRecordPreprocessor`, `TaskListProcessor`).
*   `tests/`: Contains unit tests for the extension. `tests/test_extension.py` provides examples of how features are expected to work.
*   `pyproject.toml`: Defines project metadata, dependencies, build system configuration (Hatch), and settings for development tools like Ruff and Mypy.
*   `README.md`: This file.

### Coding Conventions & Quality

*   **Type Hinting**: The codebase uses type hints extensively, checked with `mypy`.
*   **Linting & Formatting**: Code style is enforced by `Ruff`. Configuration can be found in `pyproject.toml`.
    *   To check: `python -m ruff check src tests`
    *   To format: `python -m ruff format src tests`
*   **Docstrings**: Functions and classes generally follow standard Python docstring conventions.

## Development & Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/twardoch/twardown-py.git
    cd twardown-py
    ```

2.  Create and activate a virtual environment (recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # or
    # .venv\Scripts\activate  # Windows
    ```

3.  Install dependencies, including development tools:
    ```bash
    pip install -e ".[dev]"
    # or using uv
    # uv pip install -e ".[dev]"
    ```

### Development Scripts

The project includes convenient scripts for common development tasks:

#### Testing
```bash
./scripts/test.sh          # Run comprehensive tests with coverage
```

#### Code Quality
```bash
./scripts/quality.sh       # Run linting, formatting, and type checking
```

#### Building
```bash
./scripts/build.sh         # Run full build process with validation
```

#### Releasing
```bash
./scripts/release.sh 1.0.0 # Create and push a new release tag
```

### Manual Commands

If you prefer to run commands manually:

#### Testing
```bash
python -m pytest tests/ -v --cov=twardown_py --cov-report=term-missing
```

#### Code Quality Checks
```bash
python -m ruff check src tests      # Linting
python -m ruff format src tests     # Formatting
python -m mypy src                  # Type checking
```

#### Building
```bash
python -m build                     # Build package
python -m twine check dist/*        # Validate package
```

### Release Process

This project uses git-tag-based semversioning with automated CI/CD:

1. **Local Development**: Make changes and test locally using the scripts above
2. **Create Release**: Use `./scripts/release.sh X.Y.Z` to create a new release
3. **Automated CI**: GitHub Actions will automatically:
   - Run tests on multiple Python versions and platforms
   - Build the package
   - Create a GitHub release
   - Publish to PyPI

> **Note**: See [GITHUB_ACTIONS.md](GITHUB_ACTIONS.md) for complete GitHub Actions workflow configurations.

### Version Management

The project uses dynamic versioning based on git tags:
- Development versions: `0.1.1.dev1+gc61c679.d20250717`
- Release versions: `1.0.0` (from git tag `v1.0.0`)
- Pre-release versions: `1.0.0a1` (from git tag `v1.0.0-alpha.1`)

## License

`twardown-py` is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## [DONTFIX] twardown-py
The line `[DONTFIX] twardown-py` from the original README.md has been preserved here as requested by the original file's comment. It might be a placeholder or a specific instruction for internal tooling.

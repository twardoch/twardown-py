---
this_file: twardown-py/README.md
---

# [DONTFIX] twardown-py

A Python Markdown extension that implements the twardown flavor - an opinionated "Twardoch Markdown" flavor with enhanced features.

## Features

- Magic record support for file path tracking
- Enhanced frontmatter handling
- GFM-style tables and task lists
- Code block highlighting
- Table of contents generation
- Metadata support

## Installation

```bash
uv pip install twardown-py
```

## Usage

```python
import markdown
from twardown_py import TwardownExtension

# Create Markdown instance with twardown extension
md = markdown.Markdown(extensions=[TwardownExtension()])

# Convert markdown to HTML
html = md.convert("""
// this_file: example.md
# Example Document

A simple example with a task list:

- [x] First task
- [ ] Second task
""")
```

## Development

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/twardoch/twardown-py.git
   cd twardown-py
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```

### Testing

Run tests with pytest:

```bash
python -m pytest
```

Run tests with coverage:

```bash
python -m pytest --cov=twardown_py
```

### Code Quality

Run type checking:

```bash
python -m mypy src
```

Run linting:

```bash
python -m ruff check src tests
```

Format code:

```bash
python -m ruff format src tests
```

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

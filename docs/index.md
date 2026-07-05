---
title: Home
layout: default
nav_order: 1
---

# twardown-py

A Python-Markdown extension that already made all the choices for you.

Plain Python-Markdown gives you a base parser and a pile of extensions to wire
up yourself. `twardown-py` bundles the ones a real document needs — GFM tables,
fenced code, syntax highlighting, a table of contents, frontmatter metadata,
GitHub-style task lists, and a `this_file` magic record — into a single
extension with one import.

```python
import markdown
from twardown_py import makeExtension

html = markdown.markdown(
    "- [x] Ship the docs\n- [ ] Cut the release",
    extensions=[makeExtension()],
)
```

## Install

```bash
pip install twardown-py
```

The importable module name is `twardown_py` (underscore); the PyPI/distribution
name is `twardown-py` (hyphen).

## What you get

| Feature | Backed by | Default |
|---------|-----------|---------|
| Tables | `markdown.extensions.tables` | on |
| Fenced code | `markdown.extensions.fenced_code` | on |
| Syntax highlighting | `markdown.extensions.codehilite` | on |
| Table of contents | `markdown.extensions.toc` | on |
| Frontmatter metadata | `markdown.extensions.meta` | on |
| Task lists | custom block processor | on |
| `this_file` magic record | custom preprocessor | on |

Every feature has an `enable_*` toggle. See [Usage](usage.md).

## The twardown flavor

`twardown-py` is the Python implementation of the **twardown** Markdown flavor.
The flavor itself is specified in
[twardown-docs](https://github.com/twardoch/twardown-docs), and a JavaScript
implementation lives in
[twardown-js](https://github.com/twardoch/twardown-js). The goal is one
opinionated flavor that renders the same whether a document passes through
Python or Node.

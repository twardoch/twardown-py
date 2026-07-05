---
title: Usage
layout: default
nav_order: 2
---

# Usage

## Basic conversion

```python
import markdown
from twardown_py import makeExtension

md = markdown.Markdown(extensions=[makeExtension()])
html = md.convert(source_text)
```

## Configuration

Pass any of the toggles as keyword arguments to `makeExtension`. All default to
`True` except `filename`, which defaults to an empty string.

| Option | Type | Purpose |
|--------|------|---------|
| `filename` | `str` | Value written into the `this_file` magic record |
| `enable_tables` | `bool` | GFM tables |
| `enable_fenced_code` | `bool` | Fenced code blocks |
| `enable_code_highlighting` | `bool` | CodeHilite syntax highlighting |
| `enable_toc` | `bool` | Table of contents |
| `enable_meta` | `bool` | YAML-style frontmatter metadata |
| `enable_task_lists` | `bool` | GitHub task lists |
| `enable_magic_records` | `bool` | `this_file` magic record injection |

```python
md = markdown.Markdown(
    extensions=[makeExtension(filename="doc.md", enable_toc=False)]
)
```

## Task lists

```markdown
- [x] Done
- [ ] Not done
```

renders to a `<ul class="task-list">` whose items carry `class="task-list-item"`
and a leading checkbox `<input>`; checked items get `checked="checked"`.

## The `this_file` magic record

When `enable_magic_records` is on and the document has no frontmatter, the
extension prepends a frontmatter block containing `this_file: <filename>`. If the
document already opens with frontmatter — or already carries a `this_file` key —
nothing is added. The record lands in `md.Meta`, not in the rendered HTML.

## Compatibility

`twardown-py` targets Python 3.10+ and `markdown>=3.5`.

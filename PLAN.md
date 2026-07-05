# Plan

`twardown-py` is the Python implementation of the **twardown** Markdown flavor.
The flavor is specified in [twardown-docs](https://github.com/twardoch/twardown-docs);
a JavaScript sibling lives in [twardown-js](https://github.com/twardoch/twardown-js).
This document tracks where the package is headed after the 1.x modernization.

## Status

The scaffolding is done: hatch-vcs git-tag versioning, ruff + mypy clean, a
pytest suite (parse/render fixtures plus feature toggles), real CI and release
workflows, and Jekyll docs. Minimum Python is 3.10.

## Near-term goals

### Cross-implementation conformance
The whole point of a named flavor is that Python and JavaScript agree. The next
substantive step is a shared fixture corpus — input Markdown plus expected
normalized HTML — that both `twardown-py` and `twardown-js` run. twardown-docs
should own the corpus; each implementation vendors or submodules it.

### Documentation on Pages
Wire `docs/` to GitHub Pages so the Just the Docs site publishes on merge to
`main`. Add a feature/compatibility matrix and a page dedicated to the
`this_file` magic record, since that behavior is unique to twardown.

## Longer-term ideas

### Richer task lists
The block processor handles only top-level `- [ ]` / `- [x]` items. Real
documents nest tasks and mix them with prose list items. Reworking task lists as
a treeprocessor over the core list parser's output — rather than a standalone
block — would handle nesting and stop competing with the list parser.

### Strict frontmatter mode
Today malformed frontmatter passes through untouched. An opt-in strict mode that
raises on obviously broken metadata would help documents-as-data pipelines fail
loudly at the boundary.

### Performance guardrails
Add a benchmark over a large representative document and track it so a future
extension addition can't quietly regress throughput.

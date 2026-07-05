# TODO

Future ideas, roughly in priority order. See `PLAN.md` for detail.

- [ ] Publish the built docs to GitHub Pages from the `docs/` folder.
- [ ] Add a conformance matrix page mirroring twardown-docs, showing which flavor
      features are covered here vs. in twardown-js, with test status.
- [ ] Share render fixtures with twardown-js so both implementations run the same
      cases and can be proven equivalent.
- [ ] Nested and mixed task lists (indented `- [ ]` under regular list items);
      the current block processor only handles top-level task items.
- [ ] Inline-syntax task lists inside the core list parser's `<ul>`, rather than
      a separate `task-list` block.
- [ ] Optional strict mode that errors on malformed frontmatter instead of
      silently passing it through.
- [ ] Benchmark large-document rendering and guard against regressions.

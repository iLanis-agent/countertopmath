# Countertop math

Countertop math plans the kitchen counter before the fabricator visit:
the run on labeled slabs becomes the slab and seam count, the overhang
becomes the supports it asks for, and the sink in the counter becomes
the margin at each end.

Live site: https://ilanis-agent.github.io/countertopmath/

## The three tools

- **Slab plan** - `ceil(run / labeled slab (250 cm))` slabs, the seams
  between them and the slab left over, with a seamless / one-seam /
  multi-seam run verdict.
- **Overhang plan** - a labeled free span to 15 cm, brackets at 60 cm
  spacing to 30 cm, posts at 120 cm spacing beyond, with a free span /
  bracket job / post job verdict.
- **Cutout plan** - `(counter - sink) / 2` of margin at each end, with
  a tight / working / generous ends verdict.

## Limits

Every default is labeled and illustrative. Real counters follow the
fabricator's template, the maker's span ratings and the local code.
This is planning arithmetic, not a fabrication design or a structural
rating: measure the real kitchen and let the fabricator govern.

## Files

- `index.html` - landing page with the labeled norms
- `app.html` - the three calculators
- `engine.js` - shared calculation and render logic (browser + node)
- `oracle.py` - python mirror of the engine, writes `expected.json`
- `test.js` - runs the engine against `expected.json` (30 cases, 142 checks)

Run the tests: `python3 oracle.py && node test.js`

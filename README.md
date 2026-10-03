# Naming Organic Compounds (CHEM&131)

A web guide to IUPAC nomenclature for Clark College CHEM&131 students preparing for
health-profession careers. Live at **https://mrkarlb.github.io/clarkcollegeGOBNomenclature/**.

Adapted from the IUPAC nomenclature handouts of **Dr. Jan Simek**, Cal Poly San Luis Obispo,
by Dr. Karl Bailey, Clark College. Names follow the IUPAC 2013 recommendations.
Licensed CC BY-NC 4.0 (see `LICENSE`).

## How it works

| File | What it holds |
|---|---|
| `content/*.md` | The text of each section, in Markdown, in page order |
| `structures.py` | Every structure: id, name, note, SMILES, and the numbering shown on worked examples; plus the practice problems |
| `render.py` | Draws each structure as an SVG that follows the page's light/dark theme |
| `build.py` | Checks every name against its structure, then assembles `_site/index.html` |
| `template.html` | Page layout, styles, search, and dark mode |
| `tools/review_sheet.py` | Builds `_site/structure_review.html`, a one-page sheet of every structure for chemistry review |

Every push to `main` runs `.github/workflows/pages.yml`, which builds and publishes the site.
**The build fails if any name does not match its structure**, as checked by OPSIN, so a wrong
structure can never go live.

## Editing

- **Change text:** edit the Markdown file in `content/`. Structures go in with shortcodes on their own line:
  - `[[fig id]]` one structure; `[[figs id1 id2 id3]]` a row
  - `[[practice id]]` a practice problem
  - `[[ladder]]`, `[[alkane-table]]`, `[[fischer glyD glyL glc]]` generated blocks
- **Add a structure:** add a line to `S` in `structures.py` with its name and SMILES. To show chain
  numbering, add its atom order to `LOCANTS`.
- **Add a practice problem:** add a line to `PRACTICE`. Its structure is generated from the name.

## Building locally (optional)

Requires Python 3.11+ and Java.

```
pip install -r requirements.txt
python build.py
python tools/review_sheet.py
```

Then open `_site/index.html`.

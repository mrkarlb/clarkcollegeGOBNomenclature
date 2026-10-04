# Naming Organic Compounds and Organic Reactions in the Body (CHEM&131)

A two-page web guide for Clark College CHEM&131 students preparing for health-profession careers:
IUPAC nomenclature (`index.html`) and the reaction types the body runs (`reactions.html`).
Live at **https://mrkarlb.github.io/clarkcollegeGOBNomenclature/**.

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
| `template.html` | Page layout, styles, search, and dark mode (shared by both pages) |
| `footer_naming.html`, `footer_reactions.html` | Each page's footer |
| `content-reactions/*.md` | The text of the Reactions page, in page order |
| `reactions.py` | Reactions page data: structures, the rule for each reaction type, every reaction shown, and practice problems |
| `rxncheck.py` | Applies each rule to its starting materials and checks products, atom and charge balance |
| `reactions_page.py` | Checks and renders the Reactions page |
| `sugars.py` | Draws sugar rings as Haworth projections and open-chain sugars as Fischer projections, from the structure itself |
| `tools/review_sheet.py` | Builds `_site/structure_review.html`, a one-page sheet of every structure for chemistry review |

Every push to `main` runs `.github/workflows/pages.yml`, which builds and publishes the site.
**The build fails if any name does not match its structure**, as checked by OPSIN, so a wrong
structure can never go live.

On the Reactions page, the build also fails if a reaction is wrong. Each reaction type is written
once as a rule in `reactions.py`; the build applies that rule to the starting materials and requires
the drawn products to be what it produces (including the major product, for additions and
dehydrations), requires atoms and charge to balance, checks two-way examples in both directions with
partner rules, and checks that "no reaction" examples really don't react.

## Editing

- **Change text:** edit the Markdown file in `content/`. Structures go in with shortcodes on their own line:
  - `[[fig id]]` one structure; `[[figs id1 id2 id3]]` a row
  - `[[practice id]]` a practice problem
  - `[[ladder]]`, `[[alkane-table]]`, `[[fischer glyD glyL glc]]` generated blocks
- **Add a structure:** add a line to `S` in `structures.py` with its name and SMILES. To show chain
  numbering, add its atom order to `LOCANTS`.
- **Add a practice problem:** add a line to `PRACTICE`. Its structure is generated from the name.
- **Reactions page:** reactions go in with `[[rxn id]]`, practice with `[[practice id]]`, structures with
  `[[fig id]]` or `[[figs id1 id2]]`. To add a reaction, add any new structures to `SP` in `reactions.py`,
  then a line to `RX` naming the rule it follows.

## Building locally (optional)

Requires Python 3.11+ and Java.

```
pip install -r requirements.txt
python build.py
python tools/review_sheet.py
```

Then open `_site/index.html`.

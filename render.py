"""Render structures to inline SVG that follows the page theme.

Bonds and carbon use currentColor; heteroatoms and annotations use CSS
custom properties (--mol-o, --mol-n, ...) defined for light and dark themes.
"""
import html
import re
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D

# Sentinel palette: RDKit draws these exact hex values, which are then
# swapped for CSS variables.
SENTINEL = {
    "#000000": "var(--mol-c)",
    "#FF0000": "var(--mol-o)",
    "#0000FF": "var(--mol-n)",
    "#CCCC00": "var(--mol-s)",
    "#00CC00": "var(--mol-x)",
    "#FF7F00": "var(--mol-p)",
    "#7F7F7F": "var(--mol-note)",
}
PALETTE = {
    -1: (0, 0, 0), 6: (0, 0, 0), 1: (0, 0, 0),
    8: (1, 0, 0), 7: (0, 0, 1), 16: (0.8, 0.8, 0),
    9: (0, 0.8, 0), 17: (0, 0.8, 0), 35: (0, 0.8, 0), 53: (0, 0.8, 0),
    15: (1, 0.5, 0), 11: (0, 0, 0), 3: (0, 0, 0),
}


# Style declarations that match the defaults set in the site CSS (.mol path / .mol text)
_DEFAULTS = {
    "fill:none", "fill-rule:evenodd", "fill-opacity:1", "stroke-width:2.0px",
    "stroke-linecap:butt", "stroke-linejoin:miter", "stroke-miterlimit:10",
    "stroke-opacity:1", "font-style:normal", "font-weight:normal",
    "font-family:sans-serif", "text-anchor:start", "stroke:none",
}


def _slim_style(m):
    keep = [p for p in m.group(1).split(";") if p and p not in _DEFAULTS]
    return f"style='{';'.join(keep)}'" if keep else ""


SCALE = 1.5  # display size relative to the drawing


def svg_for(sid, smiles, alt, locants=None, show_cip=False):
    generic = "*" in smiles
    mol = Chem.MolFromSmiles(smiles.replace("[X]", "[Cl]"))
    if mol is None:
        raise ValueError(f"bad SMILES for {sid}: {smiles}")
    for a in mol.GetAtoms():
        if "[X]" in smiles and a.GetSymbol() == "Cl":
            a.SetProp("atomLabel", "X")
        if a.GetAtomicNum() == 0:
            a.SetProp("atomLabel", "R")
    if locants:
        for n, idx in enumerate(locants, 1):
            mol.GetAtomWithIdx(idx).SetProp("atomNote", str(n))

    # Flexible canvas + fixed bond length: every structure is drawn at the same scale.
    d = rdMolDraw2D.MolDraw2DSVG(-1, -1, -1, -1, True)  # True: real <text>, not glyph paths
    o = d.drawOptions()
    o.clearBackground = False
    o.bondLineWidth = 2
    o.annotationFontScale = 0.75
    o.setAnnotationColour((0.5, 0.5, 0.5))
    o.setAtomPalette(PALETTE)
    o.addStereoAnnotation = show_cip
    o.padding = 0.08
    o.fixedBondLength = 38
    o.minFontSize = 15
    o.annotationFontScale = 0.6
    d.DrawMolecule(mol)
    d.FinishDrawing()
    svg = d.GetDrawingText()
    w, h = re.search(r"viewBox='0 0 ([\d.]+) ([\d.]+)'", svg).groups()
    w, h = round(float(w)), round(float(h))

    svg = svg.split("<!-- END OF HEADER -->", 1)[1]
    svg = re.sub(r"<rect[^>]*/>", "", svg, count=1)  # no background box
    svg = svg.replace("</svg>", "").strip()
    for hexv, var in SENTINEL.items():
        svg = svg.replace(hexv, var).replace(hexv.lower(), var)
    leftover = re.findall(r"#[0-9A-Fa-f]{6}", svg)
    if leftover:
        raise ValueError(f"{sid}: unmapped colors {set(leftover)}")
    svg = re.sub(r"\s+class='[^']*'", "", svg)  # drop RDKit classes, saves space
    svg = re.sub(r"style='([^']*)'", _slim_style, svg)
    svg = re.sub(r"\s*\n\s*", "", svg)
    tid = f"t-{sid}"
    return (
        f'<svg class="mol{" generic" if generic else ""}" viewBox="0 0 {w} {h}" width="{round(w * SCALE)}" height="{round(h * SCALE)}" '
        f'role="img" aria-labelledby="{tid}" xmlns="http://www.w3.org/2000/svg">'
        f'<title id="{tid}">{html.escape(alt)}</title>{svg}</svg>'
    )

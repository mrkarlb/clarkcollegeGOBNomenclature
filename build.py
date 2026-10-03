"""Build the CHEM&131 nomenclature site.

    python build.py            # verify every name, render, write _site/index.html

The build stops if any name does not match its structure (checked with OPSIN),
so a wrong structure can never be published.
"""
import datetime
import glob
import html
import os
import re
import sys
import warnings
from zoneinfo import ZoneInfo

import markdown
from py2opsin import py2opsin
from rdkit import Chem, RDLogger

from render import svg_for
from structures import LOCANTS, PRACTICE, S, SHOW_CIP

RDLogger.DisableLog("rdApp.*")
warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_site")

BY_ID = {s[0]: s for s in S}
PRACTICE_BY_ID = {p[0]: p for p in PRACTICE}
STEREO_IN_NAME = re.compile(r"\((?:\d*[RSEZrs],?)+\)|\bcis-|\btrans-|(?:^|-)[DL]-")


# ---------------------------------------------------------------- verification
def _canon(smi, stereo=True):
    m = Chem.MolFromSmiles(smi)
    if m is None:
        return None
    if not stereo:
        Chem.RemoveStereochemistry(m)
    return Chem.MolToSmiles(m)


def verify():
    """Check every named structure against OPSIN's reading of its name."""
    named = [s for s in S if s[5] != "generic"]
    opsin = py2opsin([s[2] for s in named])
    problems = []
    for s, o in zip(named, opsin):
        stereo = bool(STEREO_IN_NAME.search(s[2]))
        if not o or _canon(s[4], stereo) != _canon(o, stereo):
            problems.append(f"  {s[0]}: '{s[2]}' -> OPSIN {o or 'could not parse'}; ours {s[4]}")
    practice_smiles = dict(zip([p[0] for p in PRACTICE], py2opsin([p[2] for p in PRACTICE])))
    for pid, smi in practice_smiles.items():
        if not smi:
            problems.append(f"  practice {pid}: OPSIN could not parse '{PRACTICE_BY_ID[pid][2]}'")
    if problems:
        print("NAME CHECK FAILED:\n" + "\n".join(problems))
        sys.exit(1)
    print(f"Name check passed: {len(named)} structures, {len(PRACTICE)} practice problems.")
    return practice_smiles


# ---------------------------------------------------------------- name styling
def style_name(name):
    """Italicize locant letters and stereodescriptors the way IUPAC prints them."""
    n = html.escape(name)
    n = re.sub(r"(?<![A-Za-z])(N)(?=[,\-])", r"<i>\1</i>", n)
    n = re.sub(r"\b(tert|sec|cis|trans)-", r"<i>\1</i>-", n)
    n = re.sub(r"(?<=[\d(,])([RSEZ])(?=[,)])", r"<i>\1</i>", n)
    n = re.sub(r"(\d)H-", r"\1<i>H</i>-", n)
    return n


def alt_for(sid):
    s = BY_ID[sid]
    alt = f"Structure of {s[2]}"
    if s[3]:
        alt += f" ({s[3]})"
    if sid in LOCANTS:
        alt += f". Main chain or ring numbered 1 to {len(LOCANTS[sid])}."
    return alt


USED = set()


SHOWN = {}


def figure(sid, cls="fig"):
    USED.add(sid)
    SHOWN[sid] = SHOWN.get(sid, 0) + 1
    uid = sid if SHOWN[sid] == 1 else f"{sid}-{SHOWN[sid]}"  # keep SVG title ids unique if a figure repeats
    s = BY_ID[sid]
    svg = svg_for(uid, s[4], alt_for(sid), LOCANTS.get(sid), sid in SHOW_CIP)
    note = f'<span class="cm">{html.escape(s[3])}</span>' if s[3] else ""
    tag = {"health": '<span class="tag health">health</span>'}.get(s[5], "")
    return (f'<figure class="{cls}"><div class="pic">{svg}</div>'
            f'<figcaption><span class="nm">{style_name(s[2])}</span>{note}{tag}</figcaption></figure>')


# ---------------------------------------------------------------- generated blocks
LADDER = [
    ("A", "lad_acid", "Carboxylic acid", "-oic acid<br>-carboxylic acid (ring)", "carboxy-", "butanoic acid"),
    ("A", "lad_anhyd", "Anhydride", "-oic anhydride", "—", "acetic anhydride"),
    ("A", "lad_ester", "Ester", "alkyl -oate", "—", "ethyl acetate"),
    ("A", "lad_amide", "Amide", "-amide", "—", "butanamide"),
    ("A", "lad_ald", "Aldehyde", "-al<br>-carbaldehyde (ring)", "oxo-, formyl-", "ethanal"),
    ("A", "lad_ket", "Ketone", "-one", "oxo-", "propan-2-one"),
    ("A", "lad_alc", "Alcohol", "-ol", "hydroxy-", "ethanol"),
    ("A", "lad_thiol", "Thiol", "-thiol", "sulfanyl-", "ethanethiol"),
    ("A", "lad_amine", "Amine", "-amine", "amino-", "propan-1-amine"),
    ("B", "lad_ene", "Alkene", "-ene", "—", "but-1-ene"),
    ("B", "lad_yne", "Alkyne", "-yne", "—", "but-1-yne"),
    ("C", "lad_alkoxy", "Ether (alkoxy)", "never a suffix", "methoxy-, ethoxy-", "methoxyethane"),
    ("C", "lad_halo", "Halogen", "never a suffix", "fluoro-, chloro-, bromo-, iodo-", "chloroethane"),
    ("C", "lad_nitro", "Nitro", "never a suffix", "nitro-", "nitromethane"),
    ("C", "alk_me", "Alkyl branch", "never a suffix", "methyl-, ethyl-, …", "2-methylpropane"),
]
TIER_LABEL = {"A": "Tier A: can be the suffix (highest priority first)",
              "B": "Tier B: multiple bonds (an ending, not a suffix)",
              "C": "Tier C: always a prefix (equal priority; alphabetize)"}


def ladder():
    rows, tier = [], None
    for t, sid, cls, suf, pre, ex in LADDER:
        USED.add(sid)
        if t != tier:
            rows.append(f'<tr class="tier tier-{t}"><th colspan="5" scope="colgroup">{TIER_LABEL[t]}</th></tr>')
            tier = t
        svg = svg_for(f"ladder-{sid}", BY_ID[sid][4], f"General structure of {cls.lower()}; R is any carbon group")
        rows.append(f'<tr class="t{t}"><th scope="row">{cls}</th><td class="lad-pic">{svg}</td>'
                    f"<td>{suf}</td><td>{pre}</td><td>{ex}</td></tr>")
    return ('<div class="table-wrap"><table class="ladder"><caption>Priority ladder for naming. '
            "Higher rows in Tier A take the suffix; every other group becomes a prefix.</caption>"
            '<thead><tr><th scope="col">Group</th><th scope="col">Structure</th><th scope="col">Suffix</th>'
            '<th scope="col">Prefix</th><th scope="col">Example</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


ALKANES = [(1, "methane"), (2, "ethane"), (3, "propane"), (4, "butane"), (5, "pentane"), (6, "hexane"),
           (7, "heptane"), (8, "octane"), (9, "nonane"), (10, "decane"), (12, "dodecane"),
           (14, "tetradecane"), (16, "hexadecane"), (18, "octadecane"), (20, "icosane")]


def alkane_table():
    def formula(n):
        return f"C{_sub(n) if n > 1 else ''}H{_sub(2 * n + 2)}"
    rows = "".join(
        f'<tr><td>{n}</td><td>{name}{" <span class=cm>(older: eicosane)</span>" if n == 20 else ""}</td>'
        f"<td>{formula(n)}</td></tr>" for n, name in ALKANES)
    return ('<div class="table-wrap"><table class="alkanes"><caption>Straight-chain alkanes. '
            "The longer chains shown are the lengths found in fatty acids.</caption>"
            '<thead><tr><th scope="col">Carbons</th><th scope="col">Name</th><th scope="col">Formula</th>'
            f"</tr></thead><tbody>{rows}</tbody></table></div>")


def _sub(n):
    return "".join("₀₁₂₃₄₅₆₇₈₉"[int(d)] for d in str(n))


def practice(pid, smiles):
    _, _, name, kind, desc, why = PRACTICE_BY_ID[pid]
    if kind == "name":
        svg = svg_for(pid, smiles, f"Practice structure to name: {desc}")
        prompt = f'<p class="q"><strong>Name this compound.</strong></p><div class="pic">{svg}</div>'
        answer = f'<p class="ans">{style_name(name)}</p><p>{html.escape(why)}</p>'
    else:
        svg = svg_for(pid, smiles, f"Structure of {name}")
        prompt = f'<p class="q"><strong>Draw:</strong> {style_name(name)}</p>'
        answer = f'<div class="pic">{svg}</div><p>{html.escape(why)}</p>'
    return (f'<div class="practice">{prompt}<details class="answer"><summary>Show answer</summary>'
            f"{answer}</details></div>")


FISCHER = {
    "glyD": ("D-glyceraldehyde", "the (R) enantiomer; OH on the right", "CHO", [("H", "OH")], "CH₂OH"),
    "glyL": ("L-glyceraldehyde", "the (S) enantiomer; OH on the left", "CHO", [("HO", "H")], "CH₂OH"),
    "glc": ("D-glucose", "open-chain form; bottom OH on the right, so D", "CHO",
            [("H", "OH"), ("HO", "H"), ("H", "OH"), ("H", "OH")], "CH₂OH"),
}


def _label(text, x, y, anchor):
    color = "var(--mol-o)" if "O" in text and text not in ("CHO",) else "var(--mol-c)"
    if text == "CHO":
        return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="fill:var(--mol-c)">CH'
                f'<tspan style="fill:var(--mol-o)">O</tspan></text>')
    if text == "CH₂OH":
        return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="fill:var(--mol-c)">CH₂'
                f'<tspan style="fill:var(--mol-o)">OH</tspan></text>')
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="fill:{color}">{text}</text>'


def fischer(key):
    title, note, top, rows, bottom = FISCHER[key]
    step, cx, y0 = 46, 100, 34
    h = y0 + step * (len(rows) + 1) + 18
    parts = [_label(top, cx, y0 - 8, "middle")]
    for i, (left, right) in enumerate(rows):
        y = y0 + step * (i + 1)
        parts.append(f'<line x1="{cx}" y1="{y - step + 6}" x2="{cx}" y2="{y}" />')
        parts.append(f'<line x1="{cx - 40}" y1="{y}" x2="{cx + 40}" y2="{y}" />')
        parts.append(_label(left, cx - 46, y + 6, "end"))
        parts.append(_label(right, cx + 46, y + 6, "start"))
    yb = y0 + step * (len(rows) + 1)
    parts.append(f'<line x1="{cx}" y1="{yb - step}" x2="{cx}" y2="{yb - 10}" />')
    parts.append(_label(bottom, cx, yb + 8, "middle"))
    desc = (f"Fischer projection of {title}: {top} at top, {bottom} at bottom; "
            + "; ".join(f"carbon {i + 2}: {l} on left, {r} on right" for i, (l, r) in enumerate(rows)))
    svg = (f'<svg class="mol fischer" viewBox="0 0 200 {h}" width="200" height="{h}" role="img" '
           f'aria-labelledby="t-{key}" xmlns="http://www.w3.org/2000/svg"><title id="t-{key}">{desc}</title>'
           f'<g style="stroke:var(--mol-c);stroke-width:2">{"".join(p for p in parts if p.startswith("<line"))}</g>'
           f'<g style="font-size:17px">{"".join(p for p in parts if p.startswith("<text"))}</g></svg>')
    return (f'<figure class="fig"><div class="pic">{svg}</div><figcaption><span class="nm">{title}</span>'
            f'<span class="cm">{html.escape(note)}</span></figcaption></figure>')


# ---------------------------------------------------------------- markdown
def expand_shortcodes(md, practice_smiles):
    def repl(m):
        kind, *args = m.group(1).split()
        if kind == "fig":
            out = figure(args[0])
        elif kind == "figs":
            out = '<div class="figrow">' + "".join(figure(a) for a in args) + "</div>"
        elif kind == "fischer":
            out = '<div class="figrow">' + "".join(fischer(a) for a in args) + "</div>"
        elif kind == "ladder":
            out = ladder()
        elif kind == "alkane-table":
            out = alkane_table()
        elif kind == "practice":
            out = practice(args[0], practice_smiles[args[0]])
        else:
            raise ValueError(f"unknown shortcode [[{m.group(1)}]]")
        return f"\n\n{out}\n\n"
    return re.sub(r"^\[\[(.+?)\]\]\s*$", repl, md, flags=re.M)


def build_sections(practice_smiles):
    sections = []
    for path in sorted(glob.glob(os.path.join(ROOT, "content", "*.md"))):
        md = open(path, encoding="utf-8").read()
        title, sid = re.match(r"#\s+(.+?)\s+\{#([\w-]+)\}", md).groups()
        body = expand_shortcodes(md, practice_smiles)
        out = markdown.markdown(body, extensions=["tables", "attr_list", "md_in_html"])
        out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>\n", "</table></div>\n") \
            if "<table>" in out else out
        sections.append((sid, title, out))
    return sections


def main():
    practice_smiles = verify()
    sections = build_sections(practice_smiles)
    unused = sorted(set(BY_ID) - USED)
    if unused:
        print("Note: structures not shown on the page:", ", ".join(unused))
    now = datetime.datetime.now(ZoneInfo("America/Los_Angeles"))
    updated = now.strftime("%B %-d, %Y")
    toc = "".join(f'<a href="#{sid}" data-target="{sid}">{html.escape(t)}</a>' for sid, t, _ in sections)
    main_html = "".join(f'<section class="block" id="{sid}-sec">{h}</section>' for sid, _, h in sections)
    page = open(os.path.join(ROOT, "template.html"), encoding="utf-8").read()
    page = page.replace("{{TOC}}", toc).replace("{{MAIN}}", main_html).replace("{{UPDATED}}", updated)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    print(f"Wrote _site/index.html ({len(page) // 1024} KB, {len(sections)} sections).")


if __name__ == "__main__":
    main()

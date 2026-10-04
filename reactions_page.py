"""Build the Reactions page (reactions.html).

Called from build.py. Checks every reaction (rxncheck.py) and every name
(OPSIN), then renders content-reactions/*.md with reaction schemes.
"""
import glob
import math
import html
import os
import re
import sys

import markdown
from py2opsin import py2opsin
from rdkit import Chem, Geometry
from rdkit.Chem import rdDepictor, rdFMCS

from reactions import NO_REACTION, PARTNER, PRACTICE, RULES, RX, SP, TX
from render import style_name, svg_for
from rxncheck import Rule, check_reaction
from sugars import fischer_chain, fischer_svg, haworth_svg, is_fischer, is_haworth

ROOT = os.path.dirname(os.path.abspath(__file__))
SP_BY = {s[0]: s for s in SP}
TX_BY = {t[0]: t for t in TX}
RX_BY = {r[0]: r for r in RX}
NR_BY = {n[0]: n for n in NO_REACTION}
PR_BY = {p[0]: p for p in PRACTICE}
STEREO_IN_NAME = re.compile(r"\((?:\d*[RSEZrs],?)+\)|\bcis-|\btrans-|(?:^|-)[DL]-|[αβ]-|alpha|beta")
RULE_OBJ = {k: (Rule(k, v[1], v[2], v[3], v[4]) if v[2] else None) for k, v in RULES.items()}


def smiles_of(sid):
    return SP_BY[sid][3] if sid in SP_BY else TX_BY[sid][3]


def words_of(sid):
    return SP_BY[sid][1] if sid in SP_BY else TX_BY[sid][2]


# ---------------------------------------------------------------- checks
def _canon(smi, stereo):
    m = Chem.MolFromSmiles(smi)
    if not stereo:
        Chem.RemoveStereochemistry(m)
    return Chem.MolToSmiles(m)


def verify():
    problems = []
    opsin = py2opsin([s[1] for s in SP])
    for s, o in zip(SP, opsin):
        stereo = bool(STEREO_IN_NAME.search(s[1]))
        if not o or _canon(s[3], stereo) != _canon(o, stereo):
            problems.append(f"  {s[0]}: '{s[1]}' -> OPSIN {o or 'could not parse'}; ours {s[3]}")
    for rid, rule, steps, left, right, *_ in RX:
        L = [(c, smiles_of(s)) for c, s in left]
        R = [(c, smiles_of(s)) for c, s in right]
        if isinstance(rule, tuple):
            fwd, rev = rule
            for p in check_reaction(RULE_OBJ[fwd], steps, L, R):
                problems.append(f"  {rid} (forward, {fwd}): {p}")
            for p in check_reaction(RULE_OBJ[rev], steps, R, L):
                problems.append(f"  {rid} (reverse, {rev}): {p}")
            if RULES[rev][0] != PARTNER.get(RULES[fwd][0]):
                problems.append(f"  {rid}: {fwd} and {rev} are not partner reactions")
        else:
            for p in check_reaction(RULE_OBJ[rule], steps, L, R):
                problems.append(f"  {rid} ({rule}): {p}")
    for nid, rule, sps in NO_REACTION:
        if RULE_OBJ[rule].apply([smiles_of(s) for s in sps]):
            problems.append(f"  {nid}: '{rule}' applies to {sps}, but the page says no reaction")
    for pid, ref, mode, *_ in PRACTICE:
        if (mode == "noreaction") != (ref in NR_BY) or (ref not in RX_BY and ref not in NR_BY):
            problems.append(f"  practice {pid}: bad reference {ref} for mode {mode}")
    if problems:
        print("REACTION CHECK FAILED:\n" + "\n".join(problems))
        sys.exit(1)
    print(f"Reaction check passed: {len(SP)} structures named, {len(RX)} reactions "
          f"({sum(isinstance(r[1], tuple) for r in RX)} checked both ways), {len(NO_REACTION)} no-reaction cases.")


# ---------------------------------------------------------------- rendering
SHOWN = {}
USED, USED_RX, USED_PRACTICE = set(), set(), set()


def _uid(base):
    SHOWN[base] = SHOWN.get(base, 0) + 1
    return base if SHOWN[base] == 1 else f"{base}-{SHOWN[base]}"


RXN_SCALE = 1.35  # structures inside reaction schemes are drawn a little smaller


ALDEHYDE_C = Chem.MolFromSmarts("[CX3H1](=O)[#6]")


def one_carbon(m):
    return sum(a.GetSymbol() == "C" for a in m.GetAtoms()) == 1


def lewis_layout(m):
    """A one-carbon molecule as a full structural formula: every H on the carbon drawn,
    bonds at right angles (sp3) or spread around the carbon (sp2), as in an intro course."""
    c = next(a.GetIdx() for a in m.GetAtoms() if a.GetSymbol() == "C")
    m = Chem.AddHs(m, onlyOnAtoms=(c,))
    rdDepictor.Compute2DCoords(m)
    nb = list(m.GetAtomWithIdx(c).GetNeighbors())
    heavy = [n for n in nb if n.GetSymbol() != "H"]
    hs = [n for n in nb if n.GetSymbol() == "H"]
    dbl = [n for n in heavy if m.GetBondBetweenAtoms(c, n.GetIdx()).GetBondTypeAsDouble() == 2]
    sgl = [n for n in heavy if n not in dbl]
    if len(nb) == 4:
        order, angs = heavy + hs, [0, 90, 180, 270]
    elif len(nb) == 3 and len(heavy) == 2:
        order, angs = dbl + sgl + hs, [90, 0, 180]
    elif len(nb) == 3:
        order, angs = dbl + hs, [0, 120, 240]
    else:
        return m                                   # CO2: the default straight line is right
    conf = m.GetConformer()
    conf.SetAtomPosition(c, Geometry.Point3D(0, 0, 0))
    for n, a in zip(order, angs):
        r = math.radians(a)
        conf.SetAtomPosition(n.GetIdx(), Geometry.Point3D(1.5 * math.cos(r), 1.5 * math.sin(r), 0))
    return m


def prepared(smi):
    """Molecule for drawing, with 2D coordinates.
    - One-carbon molecules are drawn as full structural formulas (a bare line can't show methanol).
    - An aldehyde shows its C–H, the H that separates it from a ketone and is lost on oxidation;
      this also centers the C=O."""
    m = Chem.MolFromSmiles(smi)
    if one_carbon(m) and smi != "O=C=O":
        return lewis_layout(m)
    ald = [t[0] for t in m.GetSubstructMatches(ALDEHYDE_C)]
    # In a salt, an ion with a single carbon (methylammonium) shows that carbon's H atoms too.
    lone = []
    for frag in Chem.GetMolFrags(m):
        cs = [i for i in frag if m.GetAtomWithIdx(i).GetSymbol() == "C"]
        if len(frag) < m.GetNumAtoms() and len(cs) == 1:
            lone += cs
    if ald or lone:
        m = Chem.AddHs(m, onlyOnAtoms=tuple(ald + lone))
    rdDepictor.Compute2DCoords(m)
    triglyceride_layout(m)
    return m


TG = Chem.MolFromSmarts("[CH2:1](O[CX3](=O)[#6])[CH1:2](O[CX3](=O)[#6])[CH2:3](O[CX3](=O)[#6])")


def triglyceride_layout(m):
    """Textbook layout for a triglyceride: glycerol drawn vertically, three acyl
    chains running to the right in parallel rows, C=O pointing up."""
    match = m.GetSubstructMatch(TG)
    if not match:
        return False
    glyc = [match[0], match[5], match[10]]         # the three glycerol carbons
    conf = m.GetConformer()
    gap, dx, dy = 3.0, 1.3, 0.75
    placed = set()
    for row, cg in enumerate(glyc):
        y = -row * gap
        conf.SetAtomPosition(cg, (0.0, y, 0.0))
        placed.add(cg)
        o_e = next(n.GetIdx() for n in m.GetAtomWithIdx(cg).GetNeighbors() if n.GetSymbol() == "O")
        chain, prev, cur = [], cg, o_e
        while cur is not None:                      # walk O–C(=O)–C–C–... away from glycerol
            chain.append(cur)
            nxt = [n.GetIdx() for n in m.GetAtomWithIdx(cur).GetNeighbors()
                   if n.GetIdx() != prev and n.GetIdx() not in glyc and n.GetSymbol() in "CO"
                   and m.GetBondBetweenAtoms(cur, n.GetIdx()).GetBondTypeAsDouble() == 1]
            prev, cur = cur, (nxt[0] if nxt else None)
        for k, idx in enumerate(chain, 1):
            conf.SetAtomPosition(idx, (k * dx, y + (dy if k % 2 else 0.0), 0.0))
            placed.add(idx)
        carbonyl_c = chain[1]
        o_dbl = next(n.GetIdx() for n in m.GetAtomWithIdx(carbonyl_c).GetNeighbors()
                     if m.GetBondBetweenAtoms(carbonyl_c, n.GetIdx()).GetBondTypeAsDouble() == 2)
        cx, cy = 2 * dx, y
        conf.SetAtomPosition(o_dbl, (cx, cy - 1.5, 0.0))   # C=O points down, into the gap between rows
        placed.add(o_dbl)
    return len(placed) == m.GetNumAtoms()


def aligned(smi, ref):
    """Draw smi with the atoms it shares with ref in the same positions as in ref,
    so a product sits the same way round as its starting material."""
    m = prepared(smi)
    if ref is None or one_carbon(Chem.MolFromSmiles(smi)):
        return m
    res = rdFMCS.FindMCS([ref, m], timeout=2, atomCompare=rdFMCS.AtomCompare.CompareElements,
                         bondCompare=rdFMCS.BondCompare.CompareAny, ringMatchesRingOnly=True,
                         completeRingsOnly=True)
    if res.numAtoms < 3 or res.numAtoms < 0.7 * m.GetNumHeavyAtoms():
        return m   # too little in common (e.g. a dipeptide vs. one amino acid): draw it its own way
    patt = Chem.MolFromSmarts(res.smartsString)
    rm, mm = ref.GetSubstructMatch(patt), m.GetSubstructMatch(patt)
    if not rm or not mm:
        return m
    conf = ref.GetConformer()
    cmap = {j: Geometry.Point2D(conf.GetAtomPosition(i).x, conf.GetAtomPosition(i).y) for i, j in zip(rm, mm)}
    rdDepictor.Compute2DCoords(m, coordMap=cmap)
    return m


def species_fig(sid, mol=None, scale=None, top=None, bond_len=None):
    """mol: 2D layout lined up with the reaction; top: for an open-chain sugar, the atom drawn as C1."""
    USED.add(sid)
    _, name, note, smi = SP_BY[sid]
    alt = f"Structure of {name}" + (f" ({note})" if note else "")
    uid = _uid(f"r-{sid}")
    if is_haworth(smi):
        svg = haworth_svg(uid, smi, alt + ", drawn as a Haworth projection")
    elif is_fischer(smi):
        svg = fischer_svg(uid, smi, alt + ", drawn as a Fischer projection", top)[0]
    else:
        svg = svg_for(uid, smi, alt, mol=mol if mol is not None else prepared(smi), scale=scale, pad_thin=True,
                      bond_len=bond_len)
    cm = f'<span class="cm">{html.escape(note)}</span>' if note else ""
    return (f'<figure class="fig"><div class="pic">{svg}</div>'
            f'<figcaption><span class="nm">{style_name(name)}</span>{cm}</figcaption></figure>')


COMPACT_BOND = 30   # bond length for reactions with a very large molecule (triglycerides)


def condense_chains(m, min_len=8):
    """Draw each long fatty-acid chain in condensed form, (CH2)nCH3, as textbooks do:
    the C=O end that reacts stays drawn, the unchanging tail becomes a label.
    Display only; the full structure is what the build checks."""
    rw = Chem.RWMol(m)
    conf = rw.GetConformer()
    remove = []
    for co in [a.GetIdx() for a in rw.GetAtoms() if a.GetSymbol() == "C" and any(
            b.GetBondTypeAsDouble() == 2 and b.GetOtherAtom(a).GetSymbol() == "O" for b in a.GetBonds())]:
        for start in [n.GetIdx() for n in rw.GetAtomWithIdx(co).GetNeighbors() if n.GetSymbol() == "C"]:
            chain, prev, cur = [], co, start
            while True:
                at = rw.GetAtomWithIdx(cur)
                if at.GetSymbol() != "C" or at.GetIsAromatic() or at.IsInRing() or at.GetDegree() > 2:
                    chain = []
                    break
                chain.append(cur)
                nxt = [n.GetIdx() for n in at.GetNeighbors() if n.GetIdx() != prev]
                if not nxt:
                    break
                if any(rw.GetBondBetweenAtoms(cur, x).GetBondTypeAsDouble() != 1 for x in nxt):
                    chain = []
                    break
                prev, cur = cur, nxt[0]
            if len(chain) >= min_len:
                n_ch2 = len(chain) - 1
                first = rw.GetAtomWithIdx(chain[0])
                first.SetAtomicNum(0)
                first.SetNoImplicit(True)
                first.SetProp("atomLabel", f"(CH<sub>2</sub>)<sub>{n_ch2}</sub>CH<sub>3</sub>")
                remove += chain[1:]
    for idx in sorted(remove, reverse=True):
        rw.RemoveAtom(idx)
    out = rw.GetMol()
    # put each condensed tail to the right of its C=O, so the label reads left to right
    conf = out.GetConformer()
    for a in out.GetAtoms():
        if a.HasProp("atomLabel") and a.GetAtomicNum() == 0:
            c = a.GetNeighbors()[0].GetIdx()
            if conf.GetAtomPosition(a.GetIdx()).x < conf.GetAtomPosition(c).x:
                for i in range(out.GetNumAtoms()):
                    p_ = conf.GetAtomPosition(i)
                    conf.SetAtomPosition(i, Geometry.Point3D(-p_.x, p_.y, 0))
                break
    return out


def upright_glycerol():
    """Glycerol drawn as a column with its OH groups to the right, lined up with the
    backbone of the triglyceride it comes from (or goes into)."""
    m = Chem.MolFromSmiles("OCC(O)CO")
    rdDepictor.Compute2DCoords(m)
    conf = m.GetConformer()
    pos = {0: (1.3, 0.75), 1: (0, 0), 2: (0, -3.0), 3: (1.3, -2.25), 4: (0, -6.0), 5: (1.3, -5.25)}
    for i, (x, y) in pos.items():
        conf.SetAtomPosition(i, Geometry.Point3D(x, y, 0))
    return m


def has_long_chain(smi):
    m = Chem.MolFromSmiles(smi)
    return condense_chains(prepared(smi)).GetNumAtoms() < Chem.AddHs(m, onlyOnAtoms=()).GetNumAtoms()


def item(coef, sid, mol=None, top=None, compact=False, scale=None):
    c = f'<span class="coef">{coef}</span>' if coef > 1 else ""
    if sid in TX_BY:
        return f'{c}<span class="chip">{TX_BY[sid][1]}</span>'
    if compact and has_long_chain(SP_BY[sid][3]):
        mol = condense_chains(prepared(SP_BY[sid][3]))
    if compact and Chem.CanonSmiles(SP_BY[sid][3]) == Chem.CanonSmiles("OCC(O)CO"):
        mol = upright_glycerol()
    if compact and coef > 1:
        # Draw each molecule, stacked, like the chains of a triglyceride (the textbook layout),
        # instead of one molecule with a coefficient in front.
        USED.add(sid)
        _, name, note, smi = SP_BY[sid]
        m = mol if mol is not None else prepared(smi)
        svgs = "".join(svg_for(_uid(f"r-{sid}"), smi, f"Structure of {name}", mol=m, scale=1.0, pad_thin=True,
                               bond_len=COMPACT_BOND) for _ in range(coef))
        cm = f'<span class="cm">{html.escape(note)}</span>' if note else ""
        return (f'<figure class="fig stack"><div class="pic">{svgs}</div><figcaption>'
                f'<span class="nm">{coef} × {style_name(name)}</span>{cm}</figcaption></figure>')
    if compact:   # every structure in the reaction gets the same short bonds, so they stay to scale
        return c + species_fig(sid, mol=mol, scale=1.0, top=top, bond_len=COMPACT_BOND)
    return c + species_fig(sid, mol=mol, scale=scale or RXN_SCALE, top=top)


def is_compact(*sides):
    return any(s in SP_BY and Chem.MolFromSmiles(SP_BY[s][3]).GetNumHeavyAtoms() > 30
               for side in sides for _, s in side)


ARROWS = {
    "→": '<svg viewBox="0 0 100 22" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
         '<line x1="2" y1="11" x2="96" y2="11" stroke="currentColor" stroke-width="2" vector-effect="non-scaling-stroke"/>'
         '<path d="M86 4 L98 11 L86 18" fill="none" stroke="currentColor" stroke-width="2" vector-effect="non-scaling-stroke"/></svg>',
    "⇌": '<svg viewBox="0 0 100 22" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
         '<line x1="2" y1="7" x2="96" y2="7" stroke="currentColor" stroke-width="2" vector-effect="non-scaling-stroke"/>'
         '<path d="M86 1 L98 7" fill="none" stroke="currentColor" stroke-width="2" vector-effect="non-scaling-stroke"/>'
         '<line x1="4" y1="15" x2="98" y2="15" stroke="currentColor" stroke-width="2" vector-effect="non-scaling-stroke"/>'
         '<path d="M14 21 L2 15" fill="none" stroke="currentColor" stroke-width="2" vector-effect="non-scaling-stroke"/></svg>',
}
ARROWS["pair"] = ARROWS["⇌"]


def arrow(kind, above, below):
    width = min(max(len(above), len(below), 9) * 0.6 + 1.5, 26)   # em; long labels wrap past 26em
    return (f'<span class="arrow" style="width:{width:.1f}em"><span class="ab">{html.escape(above)}</span>{ARROWS[kind]}'
            f'<span class="be">{html.escape(below)}</span></span>')


def side_list(side, mols=None, compact=False, scale=None):
    out = []
    for i, (c, s) in enumerate(side):
        plus = '<span class="plus">+</span>' if i else ""
        out.append(f'<span class="term">{plus}{item(c, s, (mols or {}).get(s), (mols or {}).get(("top", s)), compact, scale)}</span>')
    return "".join(out)


def layout(left, right):
    """Coordinates for every drawn species in a reaction, lined up to the largest starting material."""
    drawn = [s for _, s in left + right if s in SP_BY]
    lefts = [s for _, s in left if s in SP_BY]
    if not lefts:
        return {}
    ref_id = max(lefts, key=lambda s: Chem.MolFromSmiles(SP_BY[s][3]).GetNumHeavyAtoms())
    ref = prepared(SP_BY[ref_id][3])
    mols = {ref_id: ref}
    for s in drawn:
        if s not in mols:
            mols[s] = aligned(SP_BY[s][3], ref)
    # Open-chain sugars: draw each product with the same carbon on top as the starting sugar.
    ref_smi = SP_BY[ref_id][3]
    if is_fischer(ref_smi):
        rm = Chem.MolFromSmiles(ref_smi)
        top_ref = fischer_chain(rm)[0]
        for s in drawn:
            if s != ref_id and is_fischer(SP_BY[s][3]):
                pm = Chem.MolFromSmiles(SP_BY[s][3])
                res = rdFMCS.FindMCS([rm, pm], timeout=2, atomCompare=rdFMCS.AtomCompare.CompareElements,
                                     bondCompare=rdFMCS.BondCompare.CompareAny)
                patt = Chem.MolFromSmarts(res.smartsString)
                for r_match in rm.GetSubstructMatches(patt, uniquify=False, useChirality=False):
                    if top_ref in r_match:
                        p_match = pm.GetSubstructMatch(patt)
                        mols[("top", s)] = p_match[r_match.index(top_ref)]
                        break
    return mols


def words(side):
    return " plus ".join((f"{c} " if c > 1 else "") + words_of(s) for c, s in side)


def tag_for(rule):
    if isinstance(rule, tuple):
        a, b = RULES[rule[0]], RULES[rule[1]]
        return f'<span class="rtype">{a[0]} ⇄ {b[0]}</span>'
    side, specific = RULES[rule][0], RULES[rule][1]
    label = side + (f" · {specific}" if specific and specific != side else "")
    return f'<span class="rtype">{html.escape(label)}</span>'


def type_words(rule):
    if isinstance(rule, tuple):
        return f"{RULES[rule[0]][0]} and its partner, {RULES[rule[1]][0]}"
    return RULES[rule][0] + (f" ({RULES[rule][1]})" if RULES[rule][1] else "")


def scheme(rid, show_tag=True, hide_products=False):
    USED_RX.add(rid)
    _, rule, _, left, right, above, below, kind = RX_BY[rid]
    mols = layout(left, right)
    compact = is_compact(left, right)
    atoms = sum(Chem.MolFromSmiles(SP_BY[s_][3]).GetNumHeavyAtoms() for _, s_ in left + right
                if s_ in SP_BY and not is_haworth(SP_BY[s_][3]) and not is_fischer(SP_BY[s_][3]))
    scale = 1.0 if atoms > 30 else None   # a reaction with many atoms in all is drawn a little smaller
    rhs = '<span class="unknown">?</span>' if hide_products else side_list(right, mols, compact, scale)
    sentence = f"{words(left)} gives {'what product?' if hide_products else words(right)}"
    if kind == "pair":
        sentence = f"Forward ({above}): {words(left)} gives {words(right)}. Reverse ({below}): {words(right)} gives {words(left)}."
    else:
        if kind == "⇌":
            sentence = sentence.replace(" gives ", " is in equilibrium with ")
        extras = "; ".join(x for x in (above, below) if x)
        sentence = "Reaction: " + sentence + (f" ({extras})." if extras else ".")
    if show_tag:
        sentence = f"{type_words(rule).capitalize()}. " + sentence
    head = f'<div class="rxn-head">{tag_for(rule)}</div>' if show_tag else ""
    return (f'<figure class="rxn">{head}<p class="sr-only">{html.escape(sentence)}</p>'
            f'<div class="rxn-row" aria-hidden="true">{side_list(left, mols, compact, scale)}{arrow(kind, above, below)}{rhs}</div></figure>')


def noreaction_scheme(nid, label):
    _, rule, sps = NR_BY[nid]
    left = [(1, s) for s in sps if s in SP_BY]
    sentence = f"{words(left)}, {label}, gives what?"
    return (f'<figure class="rxn"><p class="sr-only">{html.escape(sentence)}</p><div class="rxn-row" aria-hidden="true">'
            f'{side_list(left)}{arrow("→", label, "")}<span class="unknown">?</span></div></figure>')


def practice(pid):
    USED_PRACTICE.add(pid)
    _, ref, mode, prompt, why = PR_BY[pid]
    q = f'<p class="q"><strong>{html.escape(prompt)}</strong></p>'
    if mode == "products":
        body = scheme(ref, show_tag=False, hide_products=True)
        ans = scheme(ref) + f"<p>{html.escape(why)}</p>"
    elif mode == "type":
        body = scheme(ref, show_tag=False)
        ans = f'<p class="ans">{html.escape(type_words(RX_BY[ref][1]).capitalize())}</p><p>{html.escape(why)}</p>'
    else:
        body = noreaction_scheme(ref, RULES[NR_BY[ref][1]][0])
        ans = f'<p class="ans">No reaction</p><p>{html.escape(why)}</p>'
    return (f'<div class="practice">{q}{body}<details class="answer"><summary>Show answer</summary>'
            f"{ans}</details></div>")


def oxladder(ids):
    lis = "".join(f"<li>{species_fig(s, scale=RXN_SCALE)}</li>" for s in ids)
    return (f'<ol class="oxladder" aria-label="From least to most oxidized carbon: '
            f'{", ".join(SP_BY[s][1] for s in ids)}">{lis}</ol>')


def expand(md):
    def repl(m):
        kind, *args = m.group(1).split()
        if kind == "rxn":
            out = scheme(args[0])
        elif kind == "practice":
            out = practice(args[0])
        elif kind == "fig":
            out = species_fig(args[0])
        elif kind == "figs":
            out = '<div class="figrow">' + "".join(species_fig(a) for a in args) + "</div>"
        elif kind == "oxladder":
            out = oxladder(args)
        else:
            raise ValueError(f"unknown shortcode [[{m.group(1)}]]")
        return f"\n\n{out}\n\n"
    return re.sub(r"^\[\[(.+?)\]\]\s*$", repl, md, flags=re.M)


def sections():
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "content-reactions", "*.md"))):
        md = open(path, encoding="utf-8").read()
        title, sid = re.match(r"#\s+(.+?)\s+\{#([\w-]+)\}", md).groups()
        h = markdown.markdown(expand(md), extensions=["tables", "attr_list", "md_in_html"])
        h = h.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
        out.append((sid, title, h))
    return out


def report_unused():
    notes = []
    for label, allv, used in (("structures", SP_BY, USED), ("reactions", RX_BY, USED_RX),
                              ("practice problems", PR_BY, USED_PRACTICE)):
        missing = sorted(set(allv) - used)
        if missing:
            notes.append(f"{label} not shown: " + ", ".join(missing))
    if notes:
        print("Note (reactions page): " + "; ".join(notes))

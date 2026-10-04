"""Draw sugars the way students learn them: Haworth projections for rings,
Fischer projections for open chains.

Every position is computed from the structure itself, not typed in: the
molecule is built in 3D (RDKit), and each OH is placed up or down (Haworth)
or left or right (Fischer) from its actual geometry. So a drawing can't
disagree with the SMILES that the build checks against the name.
"""
import html

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem


# ---------------------------------------------------------------- detection
def _pyranose_rings(m):
    """Rings of five C + one O whose C1 (next to ring O) carries a second O: sugar rings."""
    out = []
    for ring in m.GetRingInfo().AtomRings():
        if len(ring) != 6:
            continue
        os_ = [i for i in ring if m.GetAtomWithIdx(i).GetSymbol() == "O"]
        if len(os_) != 1 or any(m.GetAtomWithIdx(i).GetIsAromatic() for i in ring):
            continue
        out.append(ring)
    return out


def is_haworth(smiles):
    m = Chem.MolFromSmiles(smiles)
    rings = _pyranose_rings(m)
    return bool(rings) and len(rings) == m.GetRingInfo().NumRings() and all(_ring_order(m, r) for r in rings)


def _sugar_chain(m):
    """Open-chain sugar: an acyclic chain of 5-6 carbons, with OH on every carbon but the ends' carbonyl."""
    if m.GetRingInfo().NumRings():
        return None
    cs = [a.GetIdx() for a in m.GetAtoms() if a.GetSymbol() == "C"]
    if not 5 <= len(cs) <= 6:
        return None
    ends = [i for i in cs if sum(n.GetSymbol() == "C" for n in m.GetAtomWithIdx(i).GetNeighbors()) == 1]
    if len(ends) != 2:
        return None
    chain, prev, cur = [ends[0]], None, ends[0]
    while True:
        nxt = [n.GetIdx() for n in m.GetAtomWithIdx(cur).GetNeighbors() if n.GetSymbol() == "C" and n.GetIdx() != prev]
        if not nxt:
            break
        prev, cur = cur, nxt[0]
        chain.append(cur)
    if len(chain) != len(cs):
        return None
    if not all(any(n.GetSymbol() == "O" for n in m.GetAtomWithIdx(i).GetNeighbors()) for i in chain):
        return None
    return chain


def is_fischer(smiles):
    return _sugar_chain(Chem.MolFromSmiles(smiles)) is not None


# ---------------------------------------------------------------- geometry
def _embed(m):
    mh = Chem.AddHs(m)
    if AllChem.EmbedMolecule(mh, randomSeed=7) != 0:
        raise ValueError("could not build 3D model for " + Chem.MolToSmiles(m))
    return mh, mh.GetConformer()


def _pos(conf, i):
    p = conf.GetAtomPosition(i)
    return np.array([p.x, p.y, p.z])


def _ring_order(m, ring):
    """Ring atoms in order O5, C1, C2, C3, C4, C5 (C1 = the ring carbon next to O5 that has a second O)."""
    o5 = next(i for i in ring if m.GetAtomWithIdx(i).GetSymbol() == "O")
    nbrs = [n.GetIdx() for n in m.GetAtomWithIdx(o5).GetNeighbors() if n.GetIdx() in ring]
    def extra_o(i):
        return sum(1 for n in m.GetAtomWithIdx(i).GetNeighbors() if n.GetSymbol() == "O" and n.GetIdx() != o5)
    c1s = [i for i in nbrs if extra_o(i) >= 1 and not any(
        n.GetSymbol() == "C" and n.GetIdx() not in ring for n in m.GetAtomWithIdx(i).GetNeighbors())]
    if len(c1s) != 1:
        return None
    order, prev, cur = [o5, c1s[0]], o5, c1s[0]
    while len(order) < 6:
        nxt = next(n.GetIdx() for n in m.GetAtomWithIdx(cur).GetNeighbors() if n.GetIdx() in ring and n.GetIdx() != prev)
        order.append(nxt)
        prev, cur = cur, nxt
    return order


def _up_down(mh, conf, order):
    """For each ring carbon, its non-ring heavy substituent and whether it points up in a Haworth drawing.

    A Haworth drawing shows the ring O at the back right and runs O5 → C1 → ... → C5
    clockwise seen from above, so 'up' is opposite the right-hand-rule normal of that order."""
    pts = [_pos(conf, i) for i in order]
    n = np.zeros(3)
    for k in range(6):
        a, b = pts[k], pts[(k + 1) % 6]
        n += np.cross(a, b)
    up = -n / np.linalg.norm(n)
    ring = set(order)
    subs = {}
    for k, idx in enumerate(order[1:], 1):          # C1..C5
        atom = mh.GetAtomWithIdx(idx)
        heavy = [x.GetIdx() for x in atom.GetNeighbors() if x.GetIdx() not in ring and x.GetSymbol() != "H"]
        hs = [x.GetIdx() for x in atom.GetNeighbors() if x.GetSymbol() == "H"]
        here = _pos(conf, idx)
        entries = []
        for h in heavy:
            entries.append((h, float(np.dot(_pos(conf, h) - here, up))))
        if hs:
            entries.append(("H", float(np.dot(_pos(conf, hs[0]) - here, up))))
        if len(entries) == 2:
            entries.sort(key=lambda e: -e[1])
            subs[k] = {"up": entries[0][0], "down": entries[1][0]}
        else:
            subs[k] = {"up": entries[0][0] if entries[0][1] > 0 else None,
                       "down": entries[0][0] if entries[0][1] <= 0 else None}
    return subs


# ---------------------------------------------------------------- drawing helpers
FONT = 16


def _t(x, y, text, anchor="middle"):
    """Text with O and N colored like the other structures. text uses plain chars; ₂ is kept."""
    parts = []
    for ch in text:
        color = "var(--mol-o)" if ch == "O" else "var(--mol-c)"
        parts.append(f'<tspan style="fill:{color}">{html.escape(ch)}</tspan>')
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}">{"".join(parts)}</text>'


def _line(x1, y1, x2, y2, w=2):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke-width="{w}"/>'


def _svg(uid, alt, w, h, lines, texts):
    return (f'<svg class="mol haworth" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-labelledby="t-{uid}" xmlns="http://www.w3.org/2000/svg"><title id="t-{uid}">{html.escape(alt)}</title>'
            f'<g style="stroke:var(--mol-c);stroke-linecap:round">{"".join(lines)}</g>'
            f'<g style="font-size:{FONT}px;font-family:\'Source Sans 3\',sans-serif">{"".join(texts)}</g></svg>')


# Haworth ring, one unit: positions of O5, C1..C5 (ring O at back right)
RING = {0: (122, 40), 1: (166, 78), 2: (132, 116), 3: (58, 116), 4: (24, 78), 5: (68, 40)}
FRONT = {(1, 2), (2, 3), (3, 4)}                    # thick front edge
STEM = 30


def _label(m, sub, ring_atoms):
    if sub == "H":
        return "H"
    a = m.GetAtomWithIdx(sub)
    if a.GetSymbol() == "O":
        return "OH" if a.GetTotalNumHs() == 1 else "O"
    if a.GetSymbol() == "C":                          # exocyclic CH2OH on C5
        return "CH₂OH"
    return a.GetSymbol()


def haworth_svg(uid, smiles, alt):
    m = Chem.MolFromSmiles(smiles)
    rings = [_ring_order(m, r) for r in _pyranose_rings(m)]
    mh, conf = _embed(m)
    units = [(order, _up_down(mh, conf, order)) for order in rings]

    # Order units left to right: the unit whose anomeric O bridges to another ring goes first.
    bridge = None
    if len(units) == 2:
        for a_i, (oa, sa) in enumerate(units):
            ob, sb = units[1 - a_i]
            for side in ("up", "down"):
                o = sa[1][side]
                if o not in (None, "H") and m.GetAtomWithIdx(o).GetSymbol() == "O":
                    for k in range(1, 6):
                        for side2 in ("up", "down"):
                            if sb[k][side2] == o:
                                bridge = (a_i, side, 1 - a_i, k, side2, o)
        if bridge is None:
            raise ValueError(f"{uid}: can't find the glycosidic bond")
        if bridge[0] == 1:
            units = [units[1], units[0]]
            bridge = (0, bridge[1], 1, bridge[3], bridge[4], bridge[5])
        if bridge[3] != 4:
            raise ValueError(f"{uid}: only 1→4 links are drawn")
    elif len(units) != 1:
        raise ValueError(f"{uid}: Haworth drawing handles one or two rings")

    dx = 240
    lines, texts = [], []
    ring_atoms = {i for o, _ in units for i in o}
    for u, (order, subs) in enumerate(units):
        ox = u * dx
        pts = {k: (RING[k][0] + ox, RING[k][1] + 34) for k in RING}
        seq = [0, 1, 2, 3, 4, 5, 0]
        for a, b in zip(seq, seq[1:]):
            (x1, y1), (x2, y2) = pts[a], pts[b]
            if a == 0 or b == 0:   # bonds to the ring O stop short of the label
                (x1, y1), (x2, y2) = ((x1, y1), (x2, y2))
                if a == 0:
                    x1, y1 = x1 + (x2 - x1) * 0.28, y1 + (y2 - y1) * 0.28
                else:
                    x2, y2 = x2 - (x2 - x1) * 0.28, y2 - (y2 - y1) * 0.28
            thick = (min(a, b), max(a, b)) in FRONT
            lines.append(_line(x1, y1, x2, y2, 5 if thick else 2))
        texts.append(_t(pts[0][0], pts[0][1] + 6, "O"))
        for k in range(1, 6):
            x, y = pts[k]
            for side, sign in (("up", -1), ("down", 1)):
                s = subs[k][side]
                if s is None or s == "H":
                    continue                          # simplified Haworth: ring H atoms are left off
                if bridge and ((u == 0 and k == 1 and side == bridge[1]) or (u == 1 and k == 4 and side == bridge[4])):
                    continue                          # drawn as the bridge below
                y2 = y + sign * STEM
                lines.append(_line(x, y, x, y2))
                lab = _label(m, s, ring_atoms)
                if lab == "H":
                    ty = y2 - 3 if sign < 0 else y2 + 13
                else:
                    ty = y2 - 4 if sign < 0 else y2 + 15
                anchor = "middle"
                if lab == "OH" and k in (3, 4, 5):
                    lab, anchor = "HO", "middle"
                texts.append(_t(x, ty, lab, anchor))
    if bridge:
        # C1 of the left ring → bridging O → C4 of the right ring
        x1, y1 = RING[1][0], RING[1][1] + 34
        x4, y4 = RING[4][0] + dx, RING[4][1] + 34
        s1 = -1 if bridge[1] == "up" else 1
        s4 = -1 if bridge[4] == "up" else 1
        ya, yb = y1 + s1 * STEM, y4 + s4 * STEM
        ox, oy = (x1 + x4) / 2, (ya + yb) / 2 + (8 if s1 == s4 == 1 else -8 if s1 == s4 == -1 else 0)
        lines += [_line(x1, y1, x1, ya), _line(x1, ya, ox - 7, oy), _line(ox + 7, oy, x4, yb), _line(x4, yb, x4, y4)]
        texts.append(_t(ox, oy + 6, "O"))
    w = 196 + (dx if bridge else 0)
    return _svg(uid, alt, w, 200, lines, texts)


# ---------------------------------------------------------------- Fischer
def _end_label(m, idx):
    a = m.GetAtomWithIdx(idx)
    os_ = [(n, m.GetBondBetweenAtoms(idx, n.GetIdx()).GetBondTypeAsDouble()) for n in a.GetNeighbors() if n.GetSymbol() == "O"]
    if len(os_) == 2:
        return "COOH" if any(o.GetFormalCharge() == 0 for o, _ in os_) else "COO⁻"
    if os_ and os_[0][1] == 2:
        return "CHO"
    return "CH₂OH"


def _oxidation(m, idx):
    return sum(m.GetBondBetweenAtoms(idx, n.GetIdx()).GetBondTypeAsDouble()
               for n in m.GetAtomWithIdx(idx).GetNeighbors() if n.GetSymbol() == "O")


def fischer_chain(m, top=None):
    chain = _sugar_chain(m)
    if top is not None:
        if chain[0] != top:
            chain = chain[::-1]
    elif _oxidation(m, chain[-1]) > _oxidation(m, chain[0]):
        chain = chain[::-1]
    return chain


def fischer_svg(uid, smiles, alt, top=None):
    """top: index of the atom to put at the top (C1); default the more oxidized end."""
    m = Chem.MolFromSmiles(smiles)
    chain = fischer_chain(m, top)
    mh, conf = _embed(m)
    step, cx, y0 = 40, 90, 30
    lines, texts = [], []
    n = len(chain)
    texts.append(_t(cx, y0 - 6, _end_label(m, chain[0])))
    rows = []
    for k in range(1, n - 1):
        idx = chain[k]
        c = _pos(conf, idx)
        up, down = _pos(conf, chain[k - 1]) - c, _pos(conf, chain[k + 1]) - c
        o = next(x.GetIdx() for x in mh.GetAtomWithIdx(idx).GetNeighbors() if x.GetSymbol() == "O")
        x_vec = _pos(conf, o) - c
        right = np.linalg.det(np.array([up, down, x_vec])) < 0   # same handedness as (up back, down back, X front-right)
        y = y0 + step * k
        lines.append(_line(cx - 34, y, cx + 34, y))
        texts.append(_t(cx - 38, y + 6, "H" if right else "HO", "end"))
        texts.append(_t(cx + 38, y + 6, "OH" if right else "H", "start"))
        rows.append(right)
    yb = y0 + step * (n - 1)
    lines.append(_line(cx, y0 + 8, cx, yb - 10))       # one continuous vertical bond, no gaps at the crossings
    texts.append(_t(cx, yb + 8, _end_label(m, chain[-1])))
    return _svg(uid, alt, 180, yb + 22, lines, texts), rows

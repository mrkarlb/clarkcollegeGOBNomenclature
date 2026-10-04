"""Reaction checker for the Reactions page.

Each reaction type is written once, as a rule (an RDKit reaction SMARTS).
For every reaction drawn on the page, the build:

  1. applies the rule to the starting materials and requires the drawn
     products to be exactly what the rule produces;
  2. requires atoms of every element, and total charge, to balance;
  3. requires every name to match its structure (checked with OPSIN, in build.py).

Products are compared by constitution (stereo removed), because a rule says
which atoms bond, not which face an enzyme picks; stereochemistry in names is
still checked against the drawn structure by OPSIN.
"""
import itertools
from collections import Counter

from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem

RDLogger.DisableLog("rdApp.*")


def mol(smi):
    m = Chem.MolFromSmiles(smi)
    if m is None:
        raise ValueError(f"bad SMILES: {smi}")
    return m


def key(m_or_smi):
    """Canonical SMILES with stereochemistry removed."""
    m = mol(m_or_smi) if isinstance(m_or_smi, str) else Chem.Mol(m_or_smi)
    Chem.RemoveStereochemistry(m)
    return Chem.MolToSmiles(m)


def formula_counts(smi):
    m = Chem.AddHs(mol(smi))
    c = Counter(a.GetSymbol() for a in m.GetAtoms())
    c["charge"] = sum(a.GetFormalCharge() for a in m.GetAtoms())
    return c


def balance(reactants, products):
    """reactants/products: [(coef, smiles)]. Returns '' if balanced, else a description."""
    def total(side):
        t = Counter()
        for coef, smi in side:
            for k, v in formula_counts(smi).items():
                t[k] += coef * v
        return t
    r, p = total(reactants), total(products)
    diffs = [f"{k}: {r[k]} → {p[k]}" for k in sorted(set(r) | set(p)) if r[k] != p[k]]
    return "; ".join(diffs)


# ------------------------------------------------------------------ selectors
# When a rule can act at more than one place, a selector names the product
# the page should show (the major product). Products it doesn't select are
# still legal outcomes of the rule; the selector just picks among them.

def _new_bond_carbons(prod, tag):
    return [a for a in prod.GetAtoms() if a.HasProp("_rxn_tag") and a.GetProp("_rxn_tag") == tag]


def markovnikov(outcomes):
    """Addition of H–X or H–OH: X goes to the alkene carbon that had more carbons attached."""
    def score(o):
        return o["x_carbon_degree"]
    best = max(score(o) for o in outcomes)
    return [o for o in outcomes if score(o) == best]


def zaitsev(outcomes):
    """Dehydration: the major alkene has the most carbons on the C=C."""
    def score(o):
        m = o["mols"][0]
        best = 0
        for b in m.GetBonds():
            if b.GetBondType() == Chem.BondType.DOUBLE and {b.GetBeginAtom().GetSymbol(), b.GetEndAtom().GetSymbol()} == {"C"}:
                n = sum(1 for at in (b.GetBeginAtom(), b.GetEndAtom()) for nb in at.GetNeighbors()
                        if nb.GetSymbol() == "C" and nb.GetIdx() not in (b.GetBeginAtomIdx(), b.GetEndAtomIdx()))
                best = max(best, n)
        return best
    best = max(score(o) for o in outcomes)
    return [o for o in outcomes if score(o) == best]


SELECTORS = {"markovnikov": markovnikov, "zaitsev": zaitsev}


# ------------------------------------------------------------------ apply
class Rule:
    def __init__(self, rid, title, smarts, selector=None, x_map=None):
        self.id, self.title, self.selector, self.x_map = rid, title, selector, x_map
        self.rxn = AllChem.ReactionFromSmarts(smarts)
        self.rxn.Initialize()
        self.n_in = self.rxn.GetNumReactantTemplates()

    def outcomes(self, smiles_list):
        return self.apply(smiles_list)

    def run(self, smiles_list):
        """All distinct outcomes of one application. Each outcome: dict(mols, keys)."""
        if len(smiles_list) != self.n_in:
            raise ValueError(f"rule {self.id} takes {self.n_in} reactants, got {len(smiles_list)}")
        ms = [mol(s) for s in smiles_list]
        seen, outs = set(), []
        for prods in self.rxn.RunReactants(ms):
            ok, fixed = True, []
            for p in prods:
                p = Chem.Mol(p)
                for a in p.GetAtoms():
                    a.SetNoImplicit(False)
                    a.SetNumExplicitHs(0)
                try:
                    Chem.SanitizeMol(p)
                except Exception:
                    ok = False
                    break
                fixed.append(p)
            if not ok:
                continue
            frags = []
            for p in fixed:
                frags += [Chem.MolFromSmiles(Chem.MolToSmiles(f)) for f in Chem.GetMolFrags(p, asMols=True)]
            if any(f is None for f in frags):
                continue
            k = tuple(sorted(key(f) for f in frags))
            if k in seen:
                continue
            seen.add(k)
            x_deg = 0
            if self.x_map is not None:
                # degree (in carbons) of the reactant atom that receives X, read from the first product
                for a in fixed[0].GetAtoms():
                    if a.HasProp("old_mapno") and a.GetIntProp("old_mapno") == self.x_map:
                        ridx = a.GetIntProp("react_atom_idx")
                        ra = ms[0].GetAtomWithIdx(ridx)
                        x_deg = sum(1 for nb in ra.GetNeighbors() if nb.GetSymbol() == "C")
            outs.append({"mols": frags, "keys": k, "x_carbon_degree": x_deg})
        return outs

    def apply(self, smiles_list, select=True):
        outs = self.run(smiles_list)
        if outs and select and self.selector:
            outs = SELECTORS[self.selector](outs)
        return outs


def check_reaction(rule, steps, reactants, products):
    """
    rule      : Rule
    steps     : how many times the rule is applied (3 for a triglyceride, else 1)
    reactants : [(coef, smiles)] as drawn
    products  : [(coef, smiles)] as drawn
    Returns a list of problems ('' list means it passed).
    """
    problems = []
    b = balance(reactants, products)
    if b:
        problems.append(f"atoms or charge do not balance ({b})")

    if rule is None:          # balance-only equation (combustion)
        return problems

    want = Counter()
    for coef, smi in products:
        for part in smi.split("."):    # a salt is compared ion by ion
            want[key(part)] += coef

    if steps == 1:
        ins = []
        for coef, smi in reactants:
            ins += [smi] * coef
        try:
            outs = rule.apply(ins)
        except ValueError as e:
            return problems + [str(e)]
        if not outs:
            return problems + [f"rule '{rule.id}' does not apply to these starting materials"]
        got = [Counter(o["keys"]) for o in outs]
        if want not in got:
            shown = " | ".join(" + ".join(sorted(g.elements())) for g in got)
            problems.append(f"drawn products don't match the rule. Rule gives: {shown}")
        return problems

    # Multi-step: apply the rule repeatedly, feeding the product back in.
    pool = Counter()
    for coef, smi in reactants:
        pool[key(smi)] += coef
    for _ in range(steps):
        done = False
        species = list(pool.elements())
        # try every ordered choice of distinct pool entries for the templates
        for combo in itertools.permutations(range(len(species)), rule.n_in):
            picked = [species[i] for i in combo]
            outs = rule.apply(picked, select=False)
            if outs:
                for s in picked:
                    pool[s] -= 1
                for k in outs[0]["keys"]:
                    pool[k] += 1
                pool = +pool
                done = True
                break
        if not done:
            return problems + [f"rule '{rule.id}' stopped applying after fewer than {steps} steps"]
    if +pool != +want:
        problems.append("after {} steps the rule gives {}, not the drawn products".format(
            steps, " + ".join(f"{v} {k}" for k, v in pool.items())))
    return problems

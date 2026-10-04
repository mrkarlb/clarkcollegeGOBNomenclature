# Reaction data for the CHEM&131 Reactions page (reactions.html).
#
# Everything here is checked at build time (see rxncheck.py and build.py):
#   - every name must match its structure (OPSIN);
#   - every reaction must be what its rule produces from the starting materials;
#   - every reaction must balance in atoms and charge.
# To add a reaction: add any new species to SP, then a line to RX using an
# existing rule. To add a reaction type: add a rule to RULES first.

# ---------------------------------------------------------------- species
# (id, name_2013, common_or_note, smiles)   drawn as structures
SP = [
("propene", "prop-1-ene", "propene (propylene)", "C=CC"),
("ipa", "propan-2-ol", "isopropyl alcohol", "CC(C)O"),
("propane", "propane", "", "CCC"),
("dibr", "1,2-dibromopropane", "", "CC(Br)CBr"),
("chlpr", "2-chloropropane", "", "CC(C)Cl"),
("bu2ol", "butan-2-ol", "", "CCC(C)O"),
("bu2ene", "(2E)-but-2-ene", "trans shown; the cis isomer also forms", "C/C=C/C"),
("prop1ol", "propan-1-ol", "", "CCCO"),
("fum", "(2E)-but-2-enedioate", "fumarate", "O=C([O-])/C=C/C(=O)[O-]"),
("mal", "(2S)-2-hydroxybutanedioate", "(S)-malate", "O=C([O-])C[C@H](O)C(=O)[O-]"),
("oaa", "2-oxobutanedioate", "oxaloacetate", "O=C([O-])CC(=O)C(=O)[O-]"),
("succ", "butanedioate", "succinate", "O=C([O-])CCC(=O)[O-]"),
("cit", "2-hydroxypropane-1,2,3-tricarboxylate", "citrate", "O=C([O-])CC(O)(CC(=O)[O-])C(=O)[O-]"),
("acon", "(1Z)-prop-1-ene-1,2,3-tricarboxylate", "cis-aconitate", "O=C([O-])/C=C(/CC(=O)[O-])C(=O)[O-]"),
("ole", "(9Z)-octadec-9-enoic acid", "oleic acid (olive oil); cis", "CCCCCCCC/C=C\\CCCCCCCC(=O)O"),
("ste", "octadecanoic acid", "stearic acid; saturated", "CCCCCCCCCCCCCCCCCC(=O)O"),
("ela", "(9E)-octadec-9-enoic acid", "elaidic acid, a trans fat", "CCCCCCCC/C=C/CCCCCCCC(=O)O"),
("etoh", "ethanol", "", "CCO"),
("ethanal", "ethanal", "acetaldehyde", "CC=O"),
("acoh", "acetic acid", "ethanoic acid", "CC(=O)O"),
("meoh", "methanol", "", "CO"),
("methanal", "methanal", "formaldehyde", "C=O"),
("formic", "formic acid", "methanoic acid", "O=CO"),
("acetone", "propan-2-one", "acetone", "CC(C)=O"),
("tbuoh", "2-methylpropan-2-ol", "tert-butyl alcohol; a 3° alcohol", "CC(C)(C)O"),
("lact", "(2S)-2-hydroxypropanoate", "(S)-lactate", "C[C@H](O)C(=O)[O-]"),
("lacth", "(2S)-2-hydroxypropanoic acid", "(S)-lactic acid", "C[C@H](O)C(=O)O"),
("pyr", "2-oxopropanoate", "pyruvate", "CC(=O)C(=O)[O-]"),
("buacid", "butanoic acid", "butyric acid", "CCCC(=O)O"),
("etbut", "ethyl butanoate", "smells like pineapple", "CCCC(=O)OCC"),
("meam", "methanamine", "methylamine", "CN"),
("nmeacet", "N-methylacetamide", "", "CNC(C)=O"),
("gly", "glycine", "", "NCC(=O)O"),
("ala", "L-alanine", "", "C[C@H](N)C(=O)O"),
("glyala", "glycyl-L-alanine", "a dipeptide; the new amide is the peptide bond", "C[C@H](NC(=O)CN)C(=O)O"),
("glycerol", "propane-1,2,3-triol", "glycerol", "OCC(O)CO"),
("tristearin", "propane-1,2,3-triyl trioctadecanoate", "tristearin, a triglyceride", "CCCCCCCCCCCCCCCCCC(=O)OCC(COC(=O)CCCCCCCCCCCCCCCCC)OC(=O)CCCCCCCCCCCCCCCCC"),
("stearate", "octadecanoate", "stearate, a soap", "CCCCCCCCCCCCCCCCCC(=O)[O-]"),
("asp", "2-(acetyloxy)benzoic acid", "aspirin", "CC(=O)Oc1ccccc1C(=O)O"),
("sal", "2-hydroxybenzoic acid", "salicylic acid", "O=C(O)c1ccccc1O"),
("aglc", "α-D-glucopyranose", "α-D-glucose (ring form)", "OC[C@H]1O[C@H](O)[C@H](O)[C@@H](O)[C@@H]1O"),
("bglc", "β-D-glucopyranose", "β-D-glucose (ring form)", "OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O"),
("bgal", "β-D-galactopyranose", "β-D-galactose (ring form)", "OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O"),
("maltose", "4-O-α-D-glucopyranosyl-α-D-glucopyranose", "maltose; an α(1→4) glycosidic bond", "OC[C@H]1O[C@H](O[C@H]2[C@H](O)[C@@H](O)[C@@H](O)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@@H]1O"),
("lactose", "β-D-galactopyranosyl-(1→4)-β-D-glucopyranose", "lactose (milk sugar); a β(1→4) glycosidic bond", "OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](O)[C@H](O)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@H]1O"),
("glc", "D-glucose", "open-chain form", "O=C[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO"),
("glcacid", "D-gluconic acid", "", "O=C(O)[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO"),
("sorb", "D-glucitol", "sorbitol, a sugar alcohol", "OC[C@@H](O)[C@@H](O)[C@H](O)[C@@H](O)CO"),
("etoxy", "1-ethoxyethan-1-ol", "a hemiacetal", "CCOC(C)O"),
("meamm_ac", "methanaminium acetate", "an ammonium carboxylate salt", "CC(=O)[O-].C[NH3+]"),
("dph", "2-(diphenylmethoxy)-N,N-dimethylethan-1-amine", "diphenhydramine, an antihistamine", "CN(C)CCOC(c1ccccc1)c1ccccc1"),
("dphcl", "2-(diphenylmethoxy)-N,N-dimethylethan-1-aminium chloride", "diphenhydramine hydrochloride, the form in the tablet", "C[NH+](C)CCOC(c1ccccc1)c1ccccc1.[Cl-]"),
("alazw", "(2S)-2-azaniumylpropanoate", "L-alanine as a zwitterion", "C[C@H]([NH3+])C(=O)[O-]"),
("methane", "methane", "", "C"),
("co2", "carbon dioxide", "", "O=C=O"),
# practice problems
("ibut", "2-methylprop-1-ene", "isobutylene", "C=C(C)C"),
("pen3ol", "pentan-3-ol", "", "CCC(O)CC"),
("mb2ol", "2-methylbutan-2-ol", "", "CCC(C)(C)O"),
("mb2ene", "2-methylbut-2-ene", "", "CC=C(C)C"),
("mb1ene", "2-methylbut-1-ene", "", "C=C(C)CC"),
("pen2ene", "pent-2-ene", "cis and trans both form", "CC=CCC"),
("cpent", "cyclopentene", "", "C1=CCCC1"),
("cpentane", "cyclopentane", "", "C1CCCC1"),
("but1ene", "but-1-ene", "", "C=CCC"),
("brbut", "2-bromobutane", "", "CCC(C)Br"),
("buoh", "butan-1-ol", "", "CCCCO"),
("butanal", "butanal", "", "CCCC=O"),
("butanone", "butan-2-one", "methyl ethyl ketone", "CCC(C)=O"),
("banana", "3-methylbutyl acetate", "isoamyl acetate; banana flavoring", "CC(=O)OCCC(C)C"),
("isoamyl", "3-methylbutan-1-ol", "isoamyl alcohol", "CC(C)CCO"),
("propacid", "propanoic acid", "", "CCC(=O)O"),
("nmeprop", "N-methylpropanamide", "", "CCC(=O)NC"),
("benzo", "ethyl 4-aminobenzoate", "benzocaine, a topical anesthetic", "CCOC(=O)c1ccc(N)cc1"),
("paba", "4-aminobenzoic acid", "PABA", "Nc1ccc(C(=O)O)cc1"),
("etam", "ethanamine", "ethylamine", "CCN"),
("etamcl", "ethanaminium chloride", "ethylamine hydrochloride", "CC[NH3+].[Cl-]"),
("propanoate", "propanoate", "", "CCC(=O)[O-]"),
("glyzw", "2-azaniumylacetate", "glycine as a zwitterion", "[NH3+]CC(=O)[O-]"),
("dgal", "D-galactose", "open-chain form", "O=C[C@H](O)[C@@H](O)[C@@H](O)[C@H](O)CO"),
("galol", "galactitol", "a sugar alcohol", "OC[C@@H](O)[C@H](O)[C@H](O)[C@@H](O)CO"),
("alagly", "L-alanylglycine", "", "C[C@H](N)C(=O)NCC(=O)O"),
]

# Small species written as formulas, not drawn: (id, formula_html, words_for_screen_readers, smiles)
TX = [
("h2o", "H₂O", "water", "O"),
("h2", "H₂", "hydrogen", "[H][H]"),
("2h", "2 H", "two hydrogen atoms", "[H][H]"),
("br2", "Br₂", "bromine", "BrBr"),
("hcl", "HCl", "hydrogen chloride", "Cl"),
("hbr", "HBr", "hydrogen bromide", "Br"),
("h3o", "H₃O⁺", "hydronium ion", "[OH3+]"),
("oh", "OH⁻", "hydroxide ion", "[OH-]"),
("o2", "O₂", "oxygen", "O=O"),
("co2t", "CO₂", "carbon dioxide", "O=C=O"),
("glcf", "C₆H₁₂O₆", "glucose", "OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O"),
]

# ---------------------------------------------------------------- rules
# id: (side of the pair, specific name, reaction SMARTS, selector, atom map that receives X)
# Enzymes run these reactions in pairs: oxidation/reduction, addition/elimination,
# condensation/hydrolysis. Acid-base and combustion stand outside the pairs.
# A selector picks the major product when a rule can act in more than one place.
RULES = {
 "hydration":     ("addition", "hydration", "[C:1]=[C:2].[OH2:3]>>[C:1](-[O:3])-[C:2]", "markovnikov", 1),
 "dehydration":   ("elimination", "dehydration", "[CX4;!H0:1]-[CX4:2]-[OH1:3]>>[C:1]=[C:2].[O:3]", "zaitsev", None),
 "hydrogenation": ("addition", "hydrogenation", "[C:1]=[C:2].[H][H]>>[C:1]-[C:2]", None, None),
 "halogenation":  ("addition", "halogenation", "[C:1]=[C:2].[Cl,Br:3]-[Cl,Br:4]>>[C:1](-[*:3])-[C:2]-[*:4]", None, None),
 "hx":            ("addition", "HX addition", "[C:1]=[C:2].[Cl,Br,I;H1:3]>>[C:1](-[*:3])-[C:2]", "markovnikov", 1),
 "hemiacetal":    ("addition", "hemiacetal formation", "[CX3;!$(C-[O,N]):1]=[O:2].[OH1:3]-[CX4:4]>>[C:1](-[O:2])-[O:3]-[C:4]", None, None),
 "hemiacetal_open": ("elimination", "hemiacetal breakdown", "[CX4:1](-[OH1:2])-[O:3]-[CX4:4]>>[C:1]=[O:2].[O:3]-[C:4]", None, None),
 "ring":          ("addition", "ring closing", "[CX3;!$(C-[O,N]):1](=[O:2])-[C:3]-[C:4]-[C:5]-[C:6]-[OH1:7]>>[C:1]1(-[O:2])-[C:3]-[C:4]-[C:5]-[C:6]-[O:7]1", None, None),
 "ring_open":     ("elimination", "ring opening", "[CX4:1]1(-[OH1:2])-[C:3]-[C:4]-[C:5]-[C:6]-[O:7]1>>[C:1](=[O:2])-[C:3]-[C:4]-[C:5]-[C:6]-[O:7]", None, None),
 "ox_alcohol":    ("oxidation", "alcohol to carbonyl", "[CX4;!H0:1]-[OH1:2]>>[C:1]=[O:2].[H][H]", None, None),
 "ox_aldehyde":   ("oxidation", "aldehyde to acid", "[CX3;!$(C(=O)[O,N]);!H0:1]=[O:2].[OH2:3]>>[C:1](=[O:2])-[O:3].[H][H]", None, None),
 "dehydrogenation": ("oxidation", "C–C to C=C", "[CX4;!H0:1]-[CX4;!H0:2]>>[C:1]=[C:2].[H][H]", None, None),
 "reduction":     ("reduction", "carbonyl to alcohol", "[CX3;!$(C-[O,N]):1]=[O:2].[H][H]>>[C:1]-[O:2]", None, None),
 "esterification": ("condensation", "ester", "[CX3:1](=[O:2])-[OH1:3].[OH1:4]-[CX4:5]>>[C:1](=[O:2])-[O:4]-[C:5].[O:3]", None, None),
 "amidation":     ("condensation", "amide", "[CX3:1](=[O:2])-[OH1:3].[NX3;!H0;!$(N-C=O):4]>>[C:1](=[O:2])-[N:4].[O:3]", None, None),
 "glycoside":     ("condensation", "glycosidic bond", "[C:1](-[O;R:2])-[OH1:3].[OH1:4]-[C:5]>>[C:1](-[O:2])-[O:4]-[C:5].[O:3]", None, None),
 "ester_hydrolysis": ("hydrolysis", "ester", "[CX3:1](=[O:2])-[O:3]-[#6;!$([#6]=O):4].[OH2:5]>>[C:1](=[O:2])-[O:5].[O:3]-[*:4]", None, None),
 "amide_hydrolysis": ("hydrolysis", "amide", "[CX3:1](=[O:2])-[N;!R:3].[OH2:4]>>[C:1](=[O:2])-[O:4].[N:3]", None, None),
 "glycoside_hydrolysis": ("hydrolysis", "glycosidic bond", "[C:1](-[O;R:2])-[O;!R:3]-[C:4].[OH2:5]>>[C:1](-[O:2])-[O:5].[O:3]-[C:4]", None, None),
 "saponification": ("hydrolysis", "saponification", "[CX3:1](=[O:2])-[O:3]-[#6;!$([#6]=O):4].[OH1-:5]>>[C:1](=[O:2])-[O-:5].[O:3]-[*:4]", None, None),
 "acid_water":    ("acid–base", "proton transfer", "[CX3:1](=[O:2])-[OH1:3].[OH2:4]>>[C:1](=[O:2])-[O-:3].[O+:4]", None, None),
 "acid_amine":    ("acid–base", "proton transfer", "[CX3:1](=[O:2])-[OH1:3].[NX3;!$(N-C=O);!$(N-a):4]>>[C:1](=[O:2])-[O-:3].[N+:4]", None, None),
 "amine_hcl":     ("acid–base", "proton transfer", "[NX3;!$(N-C=O):1].[Cl;H1:2]>>[N+:1].[Cl-:2]", None, None),
 "zwitterion":    ("acid–base", "proton transfer", "([CX3:1](=[O:2])-[OH1:3].[NX3;H2:4])>>([C:1](=[O:2])-[O-:3].[N+:4])", None, None),
 "combustion":    ("combustion", "", None, None, None),   # balance check only
}
PARTNER = {"oxidation": "reduction", "reduction": "oxidation", "addition": "elimination",
           "elimination": "addition", "condensation": "hydrolysis", "hydrolysis": "condensation"}

# ---------------------------------------------------------------- reactions
# (id, rule, steps, reactants, products, above_arrow, below_arrow, arrow)
#   reactants/products: [(coefficient, species_id)]
#   steps: times the rule is applied (3 for a triglyceride)
#   arrow: "→", "⇌" (equilibrium), or "pair" (a two-way reaction: rule is
#          (forward_rule, reverse_rule) and the build checks both directions;
#          above_arrow labels the forward reaction, below_arrow the reverse)
RX = [
# two-way examples: one for each pair, simple molecule first, then the body
("pr_redox", ("ox_alcohol", "reduction"), 1, [(1, "etoh")], [(1, "ethanal"), (1, "2h")], "oxidation: NAD⁺ → NADH + H⁺", "reduction: NADH + H⁺ → NAD⁺", "pair"),
("pr_ldh", ("ox_alcohol", "reduction"), 1, [(1, "lact")], [(1, "pyr"), (1, "2h")], "oxidation (liver, heart)", "reduction (working muscle)", "pair"),
("pr_addelim", ("hydration", "dehydration"), 1, [(1, "propene"), (1, "h2o")], [(1, "ipa")], "addition of water", "elimination of water", "pair"),
("pr_fum", ("hydration", "dehydration"), 1, [(1, "fum"), (1, "h2o")], [(1, "mal")], "fumarase: addition", "fumarase: elimination", "pair"),
("pr_hemi", ("hemiacetal", "hemiacetal_open"), 1, [(1, "ethanal"), (1, "etoh")], [(1, "etoxy")], "addition", "elimination", "pair"),
("pr_ring", ("ring", "ring_open"), 1, [(1, "glc")], [(1, "bglc")], "ring closes (addition)", "ring opens (elimination)", "pair"),
("pr_condhyd", ("esterification", "ester_hydrolysis"), 1, [(1, "buacid"), (1, "etoh")], [(1, "etbut"), (1, "h2o")], "condensation", "hydrolysis", "pair"),
("pr_pep", ("amidation", "amide_hydrolysis"), 1, [(1, "gly"), (1, "ala")], [(1, "glyala"), (1, "h2o")], "condensation (ribosome)", "hydrolysis (peptidase)", "pair"),

# hydration and dehydration
("r_aconitase", "dehydration", 1, [(1, "cit")], [(1, "acon"), (1, "h2o")], "aconitase", "citric acid cycle", "→"),
# other additions to alkenes
("r_hydrog", "hydrogenation", 1, [(1, "propene"), (1, "h2")], [(1, "propane")], "Ni or Pt catalyst", "", "→"),
("r_ole", "hydrogenation", 1, [(1, "ole"), (1, "h2")], [(1, "ste")], "Ni catalyst", "how margarine is made", "→"),
("r_br2", "halogenation", 1, [(1, "propene"), (1, "br2")], [(1, "dibr")], "", "", "→"),
("r_hcl", "hx", 1, [(1, "propene"), (1, "hcl")], [(1, "chlpr")], "", "", "→"),
# oxidation and reduction
("r_etoh1", "ox_alcohol", 1, [(1, "etoh")], [(1, "ethanal"), (1, "2h")], "alcohol dehydrogenase", "NAD⁺ → NADH + H⁺", "→"),
("r_etoh2", "ox_aldehyde", 1, [(1, "ethanal"), (1, "h2o")], [(1, "acoh"), (1, "2h")], "aldehyde dehydrogenase", "NAD⁺ → NADH + H⁺", "→"),
("r_ipa", "ox_alcohol", 1, [(1, "ipa")], [(1, "acetone"), (1, "2h")], "alcohol dehydrogenase", "NAD⁺ → NADH + H⁺", "→"),
("r_meoh1", "ox_alcohol", 1, [(1, "meoh")], [(1, "methanal"), (1, "2h")], "alcohol dehydrogenase", "NAD⁺ → NADH + H⁺", "→"),
("r_meoh2", "ox_aldehyde", 1, [(1, "methanal"), (1, "h2o")], [(1, "formic"), (1, "2h")], "aldehyde dehydrogenase", "NAD⁺ → NADH + H⁺", "→"),
("r_sdh", "dehydrogenation", 1, [(1, "succ")], [(1, "fum"), (1, "2h")], "succinate dehydrogenase", "FAD → FADH₂", "→"),
("r_fum2", "hydration", 1, [(1, "fum"), (1, "h2o")], [(1, "mal")], "fumarase", "", "→"),
("r_mdh", "ox_alcohol", 1, [(1, "mal")], [(1, "oaa"), (1, "2h")], "malate dehydrogenase", "NAD⁺ → NADH + H⁺", "→"),
# condensation
("r_amide", "amidation", 1, [(1, "acoh"), (1, "meam")], [(1, "nmeacet"), (1, "h2o")], "heat", "", "→"),
("r_tg", "esterification", 3, [(1, "glycerol"), (3, "ste")], [(1, "tristearin"), (3, "h2o")], "", "", "→"),
("r_malt", "glycoside", 1, [(1, "aglc"), (1, "aglc")], [(1, "maltose"), (1, "h2o")], "", "", "→"),
# hydrolysis
("r_asp", "ester_hydrolysis", 1, [(1, "asp"), (1, "h2o")], [(1, "sal"), (1, "acoh")], "moisture, over time", "", "→"),
("r_lipase", "ester_hydrolysis", 3, [(1, "tristearin"), (3, "h2o")], [(1, "glycerol"), (3, "ste")], "lipase", "fat digestion", "→"),
("r_pephyd", "amide_hydrolysis", 1, [(1, "glyala"), (1, "h2o")], [(1, "gly"), (1, "ala")], "peptidase", "protein digestion", "→"),
("r_sapon", "saponification", 3, [(1, "tristearin"), (3, "oh")], [(1, "glycerol"), (3, "stearate")], "NaOH, heat", "soap making", "→"),
("r_lactase", "glycoside_hydrolysis", 1, [(1, "lactose"), (1, "h2o")], [(1, "bgal"), (1, "bglc")], "lactase", "digestion", "→"),
# acid-base
("r_acidw", "acid_water", 1, [(1, "lacth"), (1, "h2o")], [(1, "lact"), (1, "h3o")], "", "", "⇌"),
("r_acidam", "acid_amine", 1, [(1, "acoh"), (1, "meam")], [(1, "meamm_ac")], "", "", "→"),
("r_dph", "amine_hcl", 1, [(1, "dph"), (1, "hcl")], [(1, "dphcl")], "", "", "→"),
("r_zw", "zwitterion", 1, [(1, "ala")], [(1, "alazw")], "near pH 7", "", "⇌"),
# sugars
("r_glcox", "ox_aldehyde", 1, [(1, "glc"), (1, "h2o")], [(1, "glcacid"), (1, "2h")], "glucose oxidase", "on a test strip, the 2 H go to O₂", "→"),
("r_benedict", "ox_aldehyde", 1, [(1, "glc"), (1, "h2o")], [(1, "glcacid"), (1, "2h")], "Benedict's reagent, heat", "blue Cu²⁺ → brick-red Cu₂O", "→"),
("r_sorb", "reduction", 1, [(1, "glc"), (1, "2h")], [(1, "sorb")], "aldose reductase", "NADPH + H⁺ → NADP⁺", "→"),
# combustion (balance only)
("r_comb", "combustion", 1, [(1, "glcf"), (6, "o2")], [(6, "co2t"), (6, "h2o")], "", "", "→"),

# ---- practice reactions (shown with part hidden; see PRACTICE)
("x_hydra", "hydration", 1, [(1, "ibut"), (1, "h2o")], [(1, "tbuoh")], "H₃O⁺ catalyst", "", "→"),
("x_dehyd", "dehydration", 1, [(1, "pen3ol")], [(1, "pen2ene"), (1, "h2o")], "H₃O⁺, heat", "", "→"),
("x_hydrog", "hydrogenation", 1, [(1, "cpent"), (1, "h2")], [(1, "cpentane")], "Ni catalyst", "", "→"),
("x_hbr", "hx", 1, [(1, "but1ene"), (1, "hbr")], [(1, "brbut")], "", "", "→"),
("x_ox1", "ox_alcohol", 1, [(1, "buoh")], [(1, "butanal"), (1, "2h")], "", "NAD⁺ → NADH + H⁺", "→"),
("x_ox2", "ox_alcohol", 1, [(1, "bu2ol")], [(1, "butanone"), (1, "2h")], "", "NAD⁺ → NADH + H⁺", "→"),
("x_red", "reduction", 1, [(1, "butanone"), (1, "2h")], [(1, "bu2ol")], "", "NADH + H⁺ → NAD⁺", "→"),
("x_banana", "ester_hydrolysis", 1, [(1, "banana"), (1, "h2o")], [(1, "acoh"), (1, "isoamyl")], "", "", "→"),
("x_amide", "amidation", 1, [(1, "propacid"), (1, "meam")], [(1, "nmeprop"), (1, "h2o")], "heat", "", "→"),
("x_benzo", "ester_hydrolysis", 1, [(1, "benzo"), (1, "h2o")], [(1, "paba"), (1, "etoh")], "esterase in blood", "", "→"),
("x_alagly", "amide_hydrolysis", 1, [(1, "alagly"), (1, "h2o")], [(1, "ala"), (1, "gly")], "peptidase", "", "→"),
("x_acid", "acid_water", 1, [(1, "propacid"), (1, "h2o")], [(1, "propanoate"), (1, "h3o")], "", "", "⇌"),
("x_amine", "amine_hcl", 1, [(1, "etam"), (1, "hcl")], [(1, "etamcl")], "", "", "→"),
("x_glyzw", "zwitterion", 1, [(1, "gly")], [(1, "glyzw")], "near pH 7", "", "⇌"),
("x_galol", "reduction", 1, [(1, "dgal"), (1, "2h")], [(1, "galol")], "aldose reductase", "NADPH + H⁺ → NADP⁺", "→"),
("x_malt", "glycoside_hydrolysis", 1, [(1, "maltose"), (1, "h2o")], [(1, "aglc"), (1, "aglc")], "maltase", "", "→"),
]

# Major and minor products, for showing Markovnikov's and Zaitsev's rules side by side.
# (id, rule, rule_name, reactants, major, minor, above_arrow, below_arrow, major_why, minor_why, minor_label)
# The build requires: the major products are what the rule picks (its selector); the minor
# products are another outcome the same rule allows, but not the one it picks; both balance.
MAJMIN = [
 ("m_hydra", "hydration", "Markovnikov's rule", [(1, "propene"), (1, "h2o")], [(1, "ipa")], [(1, "prop1ol")],
  "H₃O⁺ catalyst", "", "OH on the carbon with more carbons attached", "OH on the end carbon",
  "minor (little or none forms)"),
 ("m_dehyd", "dehydration", "Zaitsev's rule", [(1, "bu2ol")], [(1, "bu2ene"), (1, "h2o")], [(1, "but1ene"), (1, "h2o")],
  "H₃O⁺, heat", "", "more carbons on the C=C (H from the CH₂)", "fewer carbons on the C=C (H from the CH₃)",
  "minor"),
 ("m_mb2ol", "dehydration", "Zaitsev's rule", [(1, "mb2ol")], [(1, "mb2ene"), (1, "h2o")], [(1, "mb1ene"), (1, "h2o")],
  "H₃O⁺, heat", "", "three carbons on the C=C", "two carbons on the C=C", "minor"),
]

# Rules that must NOT apply: (id, rule, reactant species). The build fails if they do.
NO_REACTION = [
 ("n_tbuoh", "ox_alcohol", ["tbuoh"]),          # 3° alcohols don't oxidize
 ("n_ketone", "ox_aldehyde", ["acetone", "h2o"]),  # ketones don't oxidize further
 ("n_acid", "ox_aldehyde", ["acoh", "h2o"]),     # carboxylic acids are the end of the line
]

# ---------------------------------------------------------------- practice
# (id, reaction_or_noreaction_id, mode, prompt, why)
#   mode "products":  show reactants, hide products
#   "type":           show the whole reaction, ask which type it is
#   "noreaction":     show the starting material; the answer is "no reaction"
PRACTICE = [
 ("p_hydra", "x_hydra", "products", "Draw the major product.",
  "Water adds across the C=C, following Markovnikov's rule: the H goes to the CH₂ end (the carbon with more hydrogens), and the OH goes to the carbon with more carbons attached (here, two). The product is a 3° alcohol."),
 ("p_dehyd", "x_dehyd", "products", "Draw the organic product of dehydration.",
  "Removing the OH and an H from a neighboring carbon makes a C=C. Both neighbors are equivalent here, so Zaitsev's rule has no choice to make: there is only one alkene, pent-2-ene."),
 ("p_zaitsev", "m_mb2ol", "majmin", "Dehydrating this alcohol can give either alkene, A or B. Which is the major product, and which rule decides?",
  "B, 2-methylbut-2-ene. Zaitsev's rule: the H comes off the neighboring carbon with fewer hydrogens. The OH carbon's neighbors are two CH₃ groups and one CH₂; taking the H from the CH₂ puts three carbons on the C=C, while taking it from a CH₃ puts only two."),
 ("p_hydrog", "x_hydrog", "products", "Draw the product.",
  "H₂ adds one H to each carbon of the C=C, giving the saturated ring."),
 ("p_hbr", "x_hbr", "products", "Draw the major product.",
  "Markovnikov's rule: H goes to the CH₂ end of the C=C (more hydrogens), and Br goes to the carbon with more carbons attached, carbon 2."),
 ("p_ox1", "x_ox1", "products", "Draw the organic product when one pair of H is removed.",
  "A 1° alcohol loses 2 H (one from O, one from C) to become an aldehyde. In the body the aldehyde would usually go on to a carboxylic acid."),
 ("p_ox2", "x_ox2", "products", "Draw the organic product of oxidation.",
  "A 2° alcohol oxidizes to a ketone, and stops there: the carbonyl carbon has no H left to lose."),
 ("p_tbuoh", "n_tbuoh", "noreaction", "What does oxidation of this alcohol give?",
  "No reaction. In a 3° alcohol the carbon holding the OH has no H, so there is no C–H to give up."),
 ("p_red", "x_red", "type", "Which type of reaction is this, and what is its partner?",
  "Reduction: the C=O gains 2 H (from NADH) and becomes a C–OH, so a ketone becomes a 2° alcohol. Its partner is oxidation, which removes the same 2 H."),
 ("p_banana", "x_banana", "products", "This ester gives bananas their smell. Draw the carboxylic acid and alcohol it is made from (or breaks down into).",
  "Split the ester at the C–O single bond next to the C=O. The C=O side becomes the acid (acetic acid); the other side becomes the alcohol (3-methylbutan-1-ol)."),
 ("p_amide", "x_amide", "products", "Draw the products of this condensation.",
  "The acid's OH and one H from the amine's N leave as water, and the C=O carbon bonds to N, forming an amide."),
 ("p_benzo", "x_benzo", "products", "Benzocaine is an ester. Draw the products when an enzyme in the blood hydrolyzes it.",
  "Water splits the ester into its acid (4-aminobenzoic acid) and alcohol (ethanol). Ester-type anesthetics are broken down this way within minutes, which is part of why their effects wear off quickly."),
 ("p_alagly", "x_alagly", "type", "Which type of reaction is this, and what is its partner?",
  "Hydrolysis of a peptide (amide) bond: water is used up to split the C–N bond, freeing the two amino acids. This is protein digestion. Its partner is condensation, which forms the peptide bond on the ribosome."),
 ("p_acid", "x_acid", "products", "Draw the products when this acid gives up a proton to water.",
  "The COOH loses its H⁺ to water, forming the carboxylate (propanoate) and hydronium. The double arrow shows an equilibrium."),
 ("p_amine", "x_amine", "products", "Draw the product of this amine with hydrochloric acid.",
  "The lone pair on nitrogen picks up H⁺, making an ammonium ion; chloride is its partner. Amine drugs are sold as salts like this because the salts dissolve in water."),
 ("p_glyzw", "x_glyzw", "products", "Draw glycine as it exists in solution near pH 7.",
  "The COOH gives up H⁺ (to COO⁻) and the NH₂ picks one up (to NH₃⁺): a zwitterion, with no overall charge."),
 ("p_galol", "x_galol", "products", "Draw the product of reducing this sugar's aldehyde.",
  "The CHO gains 2 H and becomes CH₂OH, giving a sugar alcohol, galactitol. In galactosemia, galactitol builds up in the lens of the eye and can cause cataracts."),
 ("p_acon", "r_aconitase", "type", "Which type of reaction is this, and what is its partner?",
  "Elimination (dehydration): an OH and an H leave as water and a C=C forms. Its partner is addition (hydration), which the very next enzyme in the citric acid cycle carries out on the new C=C."),
 ("p_mdh", "r_mdh", "type", "Which type of reaction is this, and what is its partner?",
  "Oxidation: the 2° alcohol loses 2 H (picked up by NAD⁺) and becomes a ketone. Its partner is reduction."),
 ("p_lipase", "r_lipase", "type", "Which type of reaction is this, and what is its partner?",
  "Hydrolysis: three water molecules split the three ester bonds, releasing glycerol and three fatty acids. Its partner is condensation, which builds the triglyceride and releases the same three waters."),
 ("p_malt", "x_malt", "type", "Which type of reaction is this, and what is its partner?",
  "Hydrolysis of a glycosidic bond: water splits maltose into two glucose units. The enzyme maltase does this in the small intestine. Its partner is condensation, which joins the two glucose units and releases water."),
]

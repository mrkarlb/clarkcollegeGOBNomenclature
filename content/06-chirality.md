# Chirality, R and S, and Meso Compounds {#chirality}

Your hands are mirror images, but you can't stack one perfectly on top of the other. Molecules can have this "handedness" too. A molecule that can't be superimposed on its mirror image is **chiral**, and the two mirror-image forms are **enantiomers**. Enantiomers have identical names except for one letter, R or S, yet the body can treat them very differently.

## Finding a chiral center

A **chiral center** is usually a carbon bonded to **four different groups**. To check a carbon:

- Skip any carbon with a double or triple bond, and any CH₂ or CH₃: these can't have four different groups.
- For each remaining carbon, compare its four groups. Look all the way along each chain, not just at the first atom: an ethyl group and a methyl group are different.

Butan-2-ol has one chiral center (C2: H, OH, CH₃, and CH₂CH₃), so it exists as two enantiomers.

[[figs rs3 rs2]]

## Assigning R and S

### Step 1: rank the four groups

These are the **Cahn–Ingold–Prelog (CIP) priority rules**, the same ones used for E and Z.

1. **Higher atomic number wins.** Look at the atoms bonded directly to the chiral center: I > Br > Cl > S > F > O > N > C > H.
2. **If two atoms tie, move outward.** List the atoms attached to each tied atom, highest first, and compare the lists. The first difference decides. For example, –CH₂OH has (O, H, H), which beats –CH(CH₃)₂ with (C, C, H), because O beats C at the first comparison.
3. **Double bonds count twice.** Treat a C=O as if the carbon had two oxygens attached. So –CHO counts as (O, O, H) and beats –CH₂OH with (O, H, H).

### Step 2: point the lowest priority away and trace the circle

1. Turn the molecule (in your head or with a model) so the **lowest-priority group, usually H, points away from you**.
2. Trace a path from priority **1 → 2 → 3**.
3. **Clockwise** is **R** (Latin *rectus*, right). **Counterclockwise** is **S** (*sinister*, left).

<div class="note" markdown="1">
**Shortcut when the lowest priority points toward you.** If the H is on a wedge (toward you), don't rotate the molecule. Trace 1 → 2 → 3 as drawn, then **reverse your answer**: clockwise becomes S, counterclockwise becomes R.
</div>

[[fig rs1]]

<details class="walk" markdown="1">
<summary>Walk through it: bromochlorofluoroiodomethane</summary>

1. **Rank by atomic number:** I (53) > Br (35) > Cl (17) > F (9). No ties, so Rule 1 is enough.
2. **Lowest priority:** F. Orient the molecule so F points away from you.
3. **Trace I → Br → Cl:** this path runs clockwise, so this is **(R)-bromochlorofluoroiodomethane**.
</details>

[[figs rs4 rs5]]

<details class="walk" markdown="1">
<summary>Walk through it: glyceraldehyde uses Rule 3</summary>

The chiral center (C2) holds OH, CHO, CH₂OH, and H.

1. **Rule 1:** OH (O) is first, H is last. CHO and CH₂OH both attach through carbon: a tie.
2. **Rule 2 and Rule 3:** list what's on each carbon. The CHO carbon has a double bond to O, which counts as two O's: (O, O, H). The CH₂OH carbon has (O, H, H). At the second comparison, O beats H, so **CHO is priority 2** and **CH₂OH is priority 3**.
3. **Trace 1 → 2 → 3** with H pointing away: clockwise for this enantiomer, so it's **(2R)-2,3-dihydroxypropanal**: D-glyceraldehyde, the reference molecule for naming sugars.
</details>

<div class="health" markdown="1">
**Health connection: chiral drugs.** Enzymes and receptors in the body are chiral, so they often respond to only one enantiomer of a drug. Ibuprofen is sold as a mix of both enantiomers, but only **(S)-ibuprofen** relieves pain; the body slowly converts much of the R form into S. Some drugs are sold as the single active enantiomer: **levalbuterol** (an asthma inhaler) is the R form of albuterol, and **esomeprazole** (Nexium) is the S form of omeprazole. The most tragic example is **thalidomide**, given for morning sickness around 1960: one enantiomer eased nausea and the other was linked to severe birth defects, and the two interconvert in the body, so even the "safe" form wasn't safe.
</div>

[[fig rs6]]

## Meso compounds: chiral centers, but not chiral

A molecule with **two or more chiral centers** usually is chiral. But if it has an **internal mirror plane**, so one half is the mirror image of the other, the molecule is identical to its own mirror image. That makes it **not chiral**, even though it has chiral centers. These molecules are called **meso compounds**.

[[figs meso1 meso2 meso3]]

<details class="walk" markdown="1">
<summary>Walk through it: spotting a meso compound</summary>

1. **Count chiral centers:** butane-2,3-diol has two, C2 and C3. Each has H, OH, CH₃, and the rest of the molecule.
2. **Assign each one:** the first structure is (2R,3R); the second is (2R,3S).
3. **Look for a mirror plane:** in the (2R,3S) form, a plane through the middle of the C2–C3 bond reflects the top half onto the bottom half. It's meso: superimposable on its own mirror image.
4. **Pattern to remember:** in a symmetrical molecule like this, R,S combinations are often meso; R,R and S,S are a chiral pair of enantiomers.
</details>

<div class="note" markdown="1">
**Meso compounds you've already met.** *cis*-1,2-Dimethylcyclopentane from [Alkenes](#alkenes) is meso. So is **xylitol**: it has chiral centers at C2 and C4, and a mirror plane through its middle carbon (C3).
</div>

## Practice

[[practice p6a]]
[[practice p6b]]
[[practice p6c]]

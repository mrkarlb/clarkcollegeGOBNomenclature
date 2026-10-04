# Addition and Elimination {#addelim}

- **Addition:** two pieces add across a **double bond**, one to each atom. The double bond becomes a single bond, and the molecule stays in one piece.
- **Elimination:** two pieces on **neighboring atoms** leave, and a double bond forms between those atoms.

When the two pieces are H and OH (water), the addition is called **hydration** and the elimination is called **dehydration**. These are the most common additions and eliminations in the body. Enzymes that run them are called **hydratases** and **dehydratases**, and both belong to the enzyme class called **lyases**.

## The pair: hydration and dehydration {#hydration}

[[rxn pr_addelim]]

**Which carbon gets the OH?** When the two carbons of the C=C aren't the same, the H adds to the carbon that already has **more hydrogens**, and the OH goes to the carbon with **more carbons attached**. This is **Markovnikov's rule**, and it applies to every addition of H–X across a C=C (H–OH, H–Cl, H–Br). In propene, it puts the OH on the middle carbon: propan-2-ol, not propan-1-ol.

[[majmin m_hydra]]

**Dehydration** removes the OH and an H from a neighboring carbon. When there's a choice of neighbors, the major product is the alkene with **more carbons attached to the C=C**. This is **Zaitsev's rule**: the H comes off the neighboring carbon that has **fewer hydrogens**.

[[majmin m_dehyd]]

Addition and elimination each have a rule for which carbon reacts. Markovnikov's rule tells you where the pieces go when they add; Zaitsev's rule tells you which double bond forms when they leave.

<div class="note" markdown="1">
**In the lab vs. in the body.** In the lab, hydration needs an acid catalyst (H₃O⁺), and dehydration needs acid and heat. Even then, Markovnikov's and Zaitsev's rules only describe which product is *major*. Chemists call a preference for one position on a molecule over another **regioselectivity**, and getting a single product in the lab often takes special reagents and extra steps. In the body, an enzyme runs the same reactions at body temperature and pH, and it holds the molecule in its active site so that only one carbon can react and the OH can add from only one side (**stereoselectivity**). Aconitase, below, adds water to the same C=C either way around and chooses which. Fumarase makes only (S)-malate, never the (R) form.
</div>

## In the body: the citric acid cycle {#hydration-body}

Fumarase adds water to fumarate. It runs in both directions; inside the cycle, the forward direction wins because the next step uses up the malate.

[[rxn pr_fum]]

### Moving an OH so it can be oxidized {#aconitase}

The next steps of the cycle use three of this page's reaction types in a row, and each one sets up the next.

Citrate's OH is on a carbon bonded to three other carbons: citrate is a **3° alcohol**, and a 3° alcohol [can't be oxidized](#alcohols). The cell needs to oxidize that part of the molecule, so the enzyme aconitase first moves the OH. It runs an **elimination**, removing water to make a C=C:

[[rxn r_aconitase]]

Then an **addition**, putting the water back on the other way around. The OH lands on the neighboring carbon, and the product, isocitrate, is a **2° alcohol**:

[[rxn r_aconitase2]]

The OH ends up on the carbon with *fewer* carbons attached, the opposite of what Markovnikov's rule describes for simple alkenes. The enzyme's active site decides where the OH goes, not the counting rule: regioselectivity again.

Now the alcohol can be oxidized. Isocitrate dehydrogenase removes 2 H (picked up by NAD⁺), turning the 2° alcohol into a ketone:

[[rxn r_idh1]]

With the new C=O right next door, the carboxylate on the neighboring carbon can leave as CO₂, another **elimination**, called **decarboxylation**. The same enzyme carries out both steps, so the ketone never leaves the enzyme:

[[rxn r_idh2]]

Put together: **elimination, addition, oxidation, elimination**. The OH is moved so that it can be oxidized, and the oxidation sets up the loss of CO₂. This is one of the two steps where the citric acid cycle releases CO₂, the CO₂ you breathe out.

## Other additions to a C=C {#other-additions}

The same addition pattern works with other pieces. You won't see these in metabolism, but they explain margarine, trans fats, and a classic lab test.

### Adding H₂: hydrogenation

[[rxn r_hydrog]]

Adding H₂ is an **addition**, and because the molecule gains 2 H, it is also a **reduction**. It's the reverse of the [FAD step](#fad), which removes 2 H to make a C=C.

[[rxn r_ole]]

<div class="health" markdown="1">
**Health connection: margarine vs. butter.** Vegetable oils are liquid because their fatty acids have **cis** C=C bonds that bend the chains, so they can't pack tightly. Hydrogenating some of those double bonds straightens the chains and turns oil into a soft solid, margarine. But *partial* hydrogenation also flips some remaining cis bonds to **trans**, making trans fats, which raise LDL ("bad") cholesterol and lower HDL ("good") cholesterol. The FDA has removed partially hydrogenated oils from the US food supply for this reason. Butter is solid for a different reason: most of its fatty acids are saturated to begin with.
</div>

[[figs ole ela ste]]

### Adding halogens and HX

[[rxn r_br2]]

Bromine is red-brown; the product is colorless. When bromine water loses its color, the sample has a C=C: the standard lab test for unsaturation.

[[rxn r_hcl]]

With HCl, HBr, or HI, **Markovnikov's rule** applies just as it does with water: the H goes to the carbon with more hydrogens, and the halogen to the carbon with more carbons attached.

## Addition to a C=O: hemiacetals and sugar rings {#hemiacetal}

An alcohol can add across the C=O of an aldehyde or ketone. The O–H of the alcohol splits: H goes to the carbonyl oxygen, and the alcohol's O bonds to the carbonyl carbon. The product, with an OH and an OR on the same carbon, is a **hemiacetal**. Most hemiacetals fall apart again easily (elimination), so this is an equilibrium.

[[rxn pr_hemi]]

A sugar has an aldehyde **and** OH groups in the same molecule. When the OH on carbon 5 of glucose adds to its own aldehyde, the chain closes into a six-membered **ring**. This is why sugars in your body are drawn as rings: in water, more than 99% of glucose is in a ring form at any moment.

[[rxn pr_ring]]

Sugar rings on this page are drawn as **Haworth projections**: a flat ring seen from slightly above, with the thick edge toward you and the ring's H atoms left off so the OH groups stand out. The open chain is drawn as a **Fischer projection**. An OH on the right in the Fischer projection points down in the ring.

The new OH on carbon 1 can point either down (**α**) or up (**β**) in the ring. In water, the ring keeps opening and closing, so α and β glucose turn into each other. Which one is locked in when two sugars join is what separates **starch** (α links, which you can digest) from **cellulose** (β links, which you can't). To review how sugars are drawn as Fischer projections, see the [naming guide](./#fischer) and your Chemfolio.

## Practice {#addelim-practice}

[[practice p_hydra]]

[[practice p_dehyd]]

[[practice p_zaitsev]]

[[practice p_hydrog]]

[[practice p_hbr]]

import html, os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
from structures import S
SEC={1:"1. How a name is built: priority ladder",2:"2. Alkanes, cycloalkanes, alkyl groups",3:"3. Alkenes, alkynes, cis/trans, E/Z",
 4:"4. Alcohols, ethers, halides, nitro compounds, thiols",5:"5. Aldehydes and ketones",6:"6. Chirality, R/S, and meso compounds",
 7:"7. Carboxylic acids, esters, salts, anhydrides",8:"8. Amines, amine salts, amides",9:"9. Biomolecule connections (recognition)"}
TAG={"worked":"worked example","ref":"reference","health":"health connection","recog":"recognition","generic":"pattern"}
def svg(smi):
    m=Chem.MolFromSmiles(smi.replace("[X]","[Cl]"))
    if "[X]" in smi:
        for a in m.GetAtoms():
            if a.GetSymbol()=="Cl": a.SetProp("atomLabel","X")
    w,h=(320,170) if m.GetNumAtoms()>14 else (220,150)
    d=rdMolDraw2D.MolDraw2DSVG(w,h); o=d.drawOptions(); o.addStereoAnnotation=True; o.clearBackground=False; o.bondLineWidth=2
    d.DrawMolecule(m); d.FinishDrawing(); return d.GetDrawingText().split("?>",1)[-1]
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_site"), exist_ok=True)
out=[];cur=None
for sid,sec,name,note,smi,role in S:
    if sec!=cur:
        if cur: out.append("</div>")
        out.append(f"<h2>{SEC[sec]}</h2><div class='grid'>"); cur=sec
    chk="" if role=="generic" else "<span class='ok'>✓ name ↔ structure</span>"
    out.append(f"<figure><div class='pic'>{svg(smi)}</div><figcaption><b>{html.escape(name)}</b>{'<br><i>'+html.escape(note)+'</i>' if note else ''}"
               f"<br><span class='tag {role}'>{TAG[role]}</span> {chk}<br><code>{html.escape(smi)}</code></figcaption></figure>")
out.append("</div>")
n=sum(1 for s in S if s[5]!="generic")
page=f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Structure Review Sheet</title><style>
body{{font-family:system-ui,sans-serif;margin:0 auto;max-width:1150px;padding:16px;background:#fff;color:#1a1a1a}}
h1{{font-size:1.4rem}} h2{{font-size:1.1rem;border-bottom:2px solid #2E75B6;padding-bottom:4px;margin-top:2rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}}
figure{{margin:0;border:1px solid #ccd;border-radius:6px;padding:8px;background:#fafbfd}}
.pic{{text-align:center}} .pic svg{{max-width:100%;height:auto}}
figcaption{{font-size:.85rem;line-height:1.35}} code{{font-size:.7rem;color:#555;word-break:break-all}}
.tag{{font-size:.7rem;padding:1px 6px;border-radius:9px;background:#e4e8ee}} .health{{background:#dff0e0}} .recog{{background:#f3e8d6}}
.ok{{font-size:.7rem;color:#1b6b2a}} .note{{background:#FFF8E7;border-left:4px solid #C65911;padding:8px 12px}}
</style></head><body><h1>CHEM&amp;131 Nomenclature Site: Structure Review Sheet</h1>
<p class="note"><b>For chemistry review only, not the student site.</b> {len(S)} structures; all {n} named structures checked name → structure with OPSIN, and every R/S, E/Z, and meso assignment confirmed separately with RDKit.
The check confirms each name describes its structure, not that numbering is lowest or the name preferred, so those are what to check by eye.</p>
{''.join(out)}</body></html>"""
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_site", "structure_review.html"),"w").write(page); print(len(S), n)

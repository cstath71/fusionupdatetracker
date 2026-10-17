"""Draw 1200x627 Open Graph cards in the Fusion Updates brand style (from /workspace/brand) with headless Chrome.
Cards are cached in assets/og with a manifest of spec hashes; only new or changed cards are redrawn."""
import os, json, hashlib, html, subprocess, tempfile, shutil
E=html.escape
CHROME=shutil.which('google-chrome') or shutil.which('chromium') or shutil.which('chromium-browser')
FONT='/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf'
TPL="""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:I;src:url("file://{font}");font-weight:100 900}}
*{{box-sizing:border-box;margin:0;padding:0}}html,body{{overflow:hidden;width:1200px;height:627px}}
body{{font-family:I,sans-serif;color:#fff;background:linear-gradient(135deg,#14202b 0%,#1d2d3d 55%,#2a3d50 100%);position:relative}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:48px 48px}}
.bar{{position:absolute;left:0;top:0;bottom:0;width:10px;background:#c74634}}
.wrap{{position:absolute;inset:0;padding:56px 64px;display:flex;flex-direction:column}}
.top{{display:flex;justify-content:space-between;align-items:center;gap:24px}}
.brand{{font-weight:800;letter-spacing:-.02em;font-size:34px}}.brand span{{color:#ff8a70}}
.tag{{display:inline-block;background:#ff8a70;color:#14202b;font-weight:800;border-radius:999px;text-transform:uppercase;letter-spacing:.05em;font-size:16px;padding:7px 16px;white-space:nowrap}}
h1{{font-size:{fs}px;line-height:1.07;font-weight:800;letter-spacing:-.025em;margin-top:54px;max-width:1080px}}
.sub{{font-size:28px;font-weight:600;color:#d6dee6;margin-top:22px;max-width:1080px}}
.foot{{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;color:#9fb0c0;font-size:18px}}
.foot .url{{color:#fff;font-weight:700;font-size:24px}}
</style></head><body><div class="grid"></div><div class="bar"></div><div class="wrap">
<div class="top"><div class="brand">Fusion<span>Updates</span></div><div class="tag">{tag}</div></div>
<h1>{h1}</h1><div class="sub">{sub}</div>
<div class="foot"><div class="url">fusionupdates.com</div><div>Independent. Not affiliated with or endorsed by Oracle.</div></div>
</div></body></html>"""
def card_html(tag,h1,sub):
    n=len(h1); fs=66 if n<=40 else (58 if n<=60 else 50)
    return TPL.format(font=FONT,tag=E(tag),h1=E(h1),sub=E(sub),fs=fs)
def generate(specs,outdir):
    os.makedirs(outdir,exist_ok=True)
    mf=os.path.join(outdir,'manifest.json')
    man=json.load(open(mf)) if os.path.exists(mf) else {}
    todo={k:v for k,v in specs.items() if man.get(k)!=hashlib.sha1(json.dumps(v).encode()).hexdigest() or not os.path.exists(os.path.join(outdir,k+'.png'))}
    if todo and not CHROME: raise SystemExit('og.py: Chrome not found; cannot draw OG cards')
    with tempfile.TemporaryDirectory() as td:
        for k,(tag,h1,sub) in todo.items():
            f=os.path.join(td,k+'.html'); open(f,'w').write(card_html(tag,h1,sub))
            out=os.path.join(outdir,k+'.png')
            subprocess.run([CHROME,'--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=1',f'--screenshot={out}','--window-size=1200,627',f'file://{f}'],check=True,capture_output=True,timeout=60)
            man[k]=hashlib.sha1(json.dumps([tag,h1,sub]).encode()).hexdigest()
    for k in list(man):
        if k not in specs:
            man.pop(k); p=os.path.join(outdir,k+'.png')
            if os.path.exists(p): os.remove(p)
    json.dump(man,open(mf,'w'),indent=1,sort_keys=True)
    return len(todo)

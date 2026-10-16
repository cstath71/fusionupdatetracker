import os, html, json, shutil, collections
E=html.escape
SITE='FusionUpdateTracker'
CSS="""
:root{--ink:#14202b;--mut:#5b6875;--bg:#f6f7f9;--card:#fff;--acc:#c74634;--line:#e3e6ea}
*{box-sizing:border-box}body{margin:0;font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg)}
a{color:#1f5fa8}header{background:#14202b;color:#fff}header .w{display:flex;gap:24px;align-items:center;flex-wrap:wrap}
header a{color:#fff;text-decoration:none;opacity:.9}header a.brand{font-weight:700;font-size:20px;opacity:1}header a.brand span{color:#ff8a70}
.w{max-width:1150px;margin:0 auto;padding:16px 20px}nav{display:flex;gap:18px;flex-wrap:wrap}
.hero{padding:40px 0 10px}.hero h1{font-size:34px;margin:0 0 8px}.lead{color:var(--mut);font-size:18px;max-width:760px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin:20px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px}
.card h3{margin:0 0 6px}.muted{color:var(--mut)}.small{font-size:13px}
.draft{display:inline-block;background:#fff4d6;border:1px solid #f0d27a;color:#7a5a00;border-radius:6px;padding:2px 8px;font-size:12px;font-weight:600}
.filters{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0;position:sticky;top:0;background:var(--bg);padding:10px 0;z-index:2}
select,input{padding:8px 10px;border:1px solid var(--line);border-radius:8px;font:inherit;background:#fff}
.item{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:10px 0}
.item h4{margin:0 0 4px;font-size:16px}.meta{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0}
.pill{font-size:12px;border-radius:999px;padding:2px 10px;background:#eef1f4;color:#33414e}
.i-high{background:#fde2dd;color:#a32b17;font-weight:700}.i-medium{background:#fff0cf;color:#865d00;font-weight:700}.i-low{background:#e3f3e6;color:#1f6b33;font-weight:700}
.e-auto{background:#dfeafe;color:#1e4f9a}.e-exp{background:#fde2dd;color:#a32b17}
.box{background:#fff;border:1px solid var(--line);border-radius:10px;padding:20px;margin:18px 0}
form.nl{display:flex;gap:8px;flex-wrap:wrap}form.nl input[type=email]{flex:1;min-width:240px}
button{background:var(--acc);color:#fff;border:0;border-radius:8px;padding:9px 16px;font:inherit;font-weight:600;cursor:pointer}
footer{color:var(--mut);font-size:13px;border-top:1px solid var(--line);margin-top:40px}
table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top;font-size:14px}
ul.check li{margin:6px 0}
"""
def page(title, body, depth=0, desc=''):
    p='../'*depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | {SITE}</title><meta name="description" content="{E(desc or 'Plain-English tracker of Oracle Fusion Cloud quarterly updates: what changed, what turns on automatically, what to test.')}">
<link rel="stylesheet" href="{p}style.css"></head><body>
<header><div class="w"><a class="brand" href="{p}index.html">Fusion<span>Update</span>Tracker</a><nav>
<a href="{p}updates/26b/index.html">26B</a><a href="{p}updates/26c/index.html">26C</a><a href="{p}newsletter.html">Newsletter</a><a href="{p}sponsor.html">Sponsor</a><a href="{p}about.html">About</a></nav></div></header>
<main class="w">{body}</main>
<footer><div class="w">Independent site, not affiliated with or endorsed by Oracle. Oracle and Oracle Fusion are trademarks of Oracle and/or its affiliates.
Summaries are condensed from Oracle's public readiness documentation; always confirm details on the linked Oracle page. Impact ratings are editorial drafts.</div></footer></body></html>"""
def nl_form(p=''):
    return f"""<div class="box"><h3 style="margin-top:0">Get the quarterly briefing</h3><p class="muted">One email per update (plus short alerts before opt-in expirations): the changes that matter, by module, and what to test.</p>
<form class="nl" action="#" method="post" onsubmit="alert('Newsletter signup is not connected yet (placeholder).');return false;"><input type="email" name="email" placeholder="you@company.com" required>
<select name="area"><option>All modules</option><option>Financials</option><option>Procurement</option><option>Supply Chain &amp; Manufacturing</option><option>Logistics</option><option>Project Management</option><option>HCM</option></select><button type="submit">Subscribe</button></form>
<p class="small muted">Placeholder form: not connected to any email service yet.</p></div>"""
def enc(e): return 'e-exp' if 'expires' in e else ('e-auto' if e.startswith('Automatically') else '')
def update_page(u):
    items=u['items']; fams=sorted(set(i['family'] for i in items)); prods=sorted(set(i['product'] for i in items))
    cnt=collections.Counter(i['family'] for i in items)
    rows=[]
    for i in items:
        rows.append(f"""<div class="item" data-family="{E(i['family'])}" data-product="{E(i['product'])}" data-impact="{i['impact']}" data-en="{E(i['enablement'])}" data-text="{E((i['title']+' '+i['summary']+' '+i['module']).lower())}">
<h4><a href="{E(i['url'])}" target="_blank" rel="noopener">{E(i['title'])}</a></h4>
<div class="meta"><span class="pill i-{i['impact']}">Impact: {i['impact']} (draft)</span><span class="pill {enc(i['enablement'])}">{E(i['enablement'])}</span><span class="pill">{E(i['family'])}</span><span class="pill">{E(i['product'])} · {E(i['module'])}</span>{'<span class="pill">'+E(i['tags'])+'</span>' if i.get('tags') else ''}</div>
<div>{E(i['summary']) or '<span class="muted">Summary pending, see Oracle page.</span>'}</div>
<div class="small muted">Oracle's own impact label: {E(i['oracle_impact'])} · Action to enable: {E(i['action'])} · <a href="{E(i['url'])}" target="_blank" rel="noopener">Oracle source</a></div></div>""")
    opt=lambda xs:''.join(f'<option>{E(x)}</option>' for x in xs)
    body=f"""<div class="hero"><h1>Oracle Fusion Cloud {u['release']}: what changed</h1>
<p class="lead">{len(items)} of the most impactful changes (out of {u['total_features']} features in Oracle's {u['release']} readiness documents), across all module families. <a href="checklist.html">See the {u['release']} what-to-test checklist →</a></p>
<p><span class="draft">DRAFT impact ratings, pending editorial review</span></p>
<p class="small muted">{' · '.join(f'{E(f)}: {cnt[f]}' for f in fams)}</p></div>
<div class="filters"><select id="fam"><option value="">All module families</option>{opt(fams)}</select>
<select id="prod"><option value="">All products</option>{opt(prods)}</select>
<select id="imp"><option value="">Any impact</option><option>high</option><option>medium</option><option>low</option></select>
<select id="en"><option value="">Any enablement</option><option value="Automatically">Automatically on</option><option value="Opt-in">Opt-in</option><option value="expires">Opt-in expiring</option><option value="Off until">Off until set up</option></select>
<input id="q" placeholder="Search…"><span id="n" class="muted small" style="align-self:center"></span></div>
<div id="list">{''.join(rows)}</div>
<script>
const $=id=>document.getElementById(id);function f(){{let n=0;document.querySelectorAll('.item').forEach(e=>{{const ok=(!$('fam').value||e.dataset.family==$('fam').value)&&(!$('prod').value||e.dataset.product==$('prod').value)&&(!$('imp').value||e.dataset.impact==$('imp').value)&&(!$('en').value||e.dataset.en.includes($('en').value))&&(!$('q').value||e.dataset.text.includes($('q').value.toLowerCase()));e.style.display=ok?'':'none';if(ok)n++}});$('n').textContent=n+' shown'}}
['fam','prod','imp','en','q'].forEach(i=>$(i).addEventListener('input',f));f();</script>{nl_form()}"""
    return page(f"Oracle Fusion {u['release']} changes", body, 2, f"What changed in Oracle Fusion Cloud {u['release']}: plain-English summaries, impact, and enablement across Financials, Procurement, SCM, Projects and HCM.")
def checklist_page(u):
    items=u['items']
    auto_hi=[i for i in items if i['enablement'].startswith('Automatically') and i['impact'] in('high','medium')]
    byfam=collections.defaultdict(list)
    for i in auto_hi: byfam[i['family']].append(i)
    exp=''.join(f"<tr><td>{E(e['product'])}</td><td>{E(e['module'])}</td><td>{'<a href=\"'+E(e['url'])+'\" target=_blank>' if e['url'] else ''}{E(e['title'])}{'</a>' if e['url'] else ''}</td><td>{E(e['impact'])}</td><td>{E(e['action'])}</td><td>{E(e['introduced'])}</td></tr>" for e in u['expiring'])
    fams=''.join(f"<h3>{E(f)}</h3><ul class='check'>"+''.join(f"<li><label><input type=checkbox> <a href='{E(i['url'])}' target=_blank>{E(i['title'])}</a> <span class='small muted'>({E(i['product'])} · {E(i['module'])}, {i['impact']})</span></label></li>" for i in v)+"</ul>" for f,v in sorted(byfam.items()))
    imp=''.join(f"<li><a href='{E(x['url'])}' target=_blank>{E(x['product'])}</a> <span class='small muted'>{E(x['family'])}</span></li>" for x in sorted(u['important'],key=lambda x:(x['family'],x['product'])))
    body=f"""<div class="hero"><h1>{u['release']} what-to-test checklist</h1><p class="lead">A starting point for regression testing the {u['release']} quarterly update in your test environment. Tick items as you go (ticks are not saved).</p><p><span class="draft">DRAFT, pending editorial review</span></p></div>
<div class="box"><h2>1. Baseline regression (every update)</h2><p class="small muted">Based on Oracle's published guidance: <a href="https://docs.oracle.com/en/cloud/saas/transportation/26b/otmpt/what-should-i-test-after-a-quarterly-update.html" target=_blank>What Should I Test After a Quarterly Update?</a></p><ul class="check">
{''.join(f'<li><label><input type=checkbox> {x}</label></li>' for x in ["Validate your <b>current</b> configuration first; don't enable new features yet","Key end-to-end business flows for each role (e.g. procure-to-pay, order-to-cash, plan-to-produce, hire-to-retire)","Integrations: REST/SOAP APIs, FBDI/HDL imports, and third-party systems","Critical custom reports and analytics (BI Publisher, OTBI)","Custom workflows, approvals, extensions, and personalizations","Security: roles and privileges for new or changed pages","Features delivered automatically on (section 2) and opt-ins expiring this update (section 3)","Performance of key flows with production-like volumes"])}</ul></div>
<div class="box"><h2>2. Changes that switch on automatically (medium/high draft impact)</h2>{fams or '<p class=muted>None in this selection.</p>'}</div>
<div class="box"><h2>3. Opt-ins that expire in {u['release']} (become mandatory)</h2><p class="small muted">From Oracle's <a href="https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html" target=_blank>Current Opt-In Expirations</a> list (all pillars, including non-ERP).</p>
<table><tr><th>Product</th><th>Module</th><th>Feature</th><th>Impact</th><th>Action</th><th>Introduced</th></tr>{exp or '<tr><td colspan=6>None listed.</td></tr>'}</table></div>
<div class="box"><h2>4. Read Oracle's "IMPORTANT Actions and Considerations" per product</h2><ul>{imp}</ul></div>{nl_form()}"""
    return page(f"{u['release']} what-to-test checklist", body, 2)
def render(updates, dist):
    if os.path.exists(dist): shutil.rmtree(dist)
    os.makedirs(dist); open(os.path.join(dist,'style.css'),'w').write(CSS)
    for k,u in updates.items():
        d=os.path.join(dist,'updates',k.lower()); os.makedirs(d)
        open(os.path.join(d,'index.html'),'w').write(update_page(u)); open(os.path.join(d,'checklist.html'),'w').write(checklist_page(u))
    cards=''.join(f"""<div class="card"><h3>Update {k}</h3><p class="muted">{len(u['items'])} key changes tracked · {u['total_features']} features in Oracle docs · {len(u['expiring'])} opt-ins expiring</p>
<p><a href="updates/{k.lower()}/index.html">Browse changes →</a><br><a href="updates/{k.lower()}/checklist.html">What to test →</a></p></div>""" for k,u in sorted(updates.items(),reverse=True))
    fams=sorted(set(i['family'] for u in updates.values() for i in u['items']))
    home=f"""<div class="hero"><h1>Every Oracle Fusion quarterly update, in plain English.</h1>
<p class="lead">What changed in Financials, Procurement, Supply Chain, Logistics, Project Management and HCM, what switches on automatically, which opt-ins are about to become mandatory, and what to test before it hits production.</p></div>
<div class="cards">{cards}</div><div class="box"><h3 style="margin-top:0">Covered module families</h3><p>{' · '.join(E(f) for f in fams)}</p></div>{nl_form()}"""
    open(os.path.join(dist,'index.html'),'w').write(page('Oracle Fusion Cloud quarterly update tracker',home))
    open(os.path.join(dist,'newsletter.html'),'w').write(page('Newsletter','<div class="hero"><h1>The quarterly briefing</h1><p class="lead">Before each Oracle Fusion update reaches your test environment: the changes that matter, by module, the opt-ins about to expire, and a ready-to-use test checklist. Free.</p></div>'+nl_form()))
    open(os.path.join(dist,'sponsor.html'),'w').write(page('Sponsor',"""<div class="hero"><h1>Sponsor FusionUpdateTracker</h1><p class="lead">Reach the people who plan, test and run Oracle Fusion Cloud updates: application owners, functional leads, testers and consultants across Financials, Procurement, SCM, Projects and HCM.</p></div>
<div class="cards"><div class="card"><h3>Newsletter sponsor</h3><p class="muted">One sponsor slot per quarterly briefing, sent before each update's test window.</p></div>
<div class="card"><h3>Update page sponsor</h3><p class="muted">"Presented by" placement on an update's change list and test checklist.</p></div>
<div class="card"><h3>Module sponsor</h3><p class="muted">Placement on one module family (e.g. Supply Chain or HCM) across updates.</p></div></div>
<div class="box"><p>Good fits: test automation, data loading and migration tools, Oracle partners and add-on vendors. Sponsors never influence summaries or ratings, and sponsored placements are always labeled.</p><p><b>Rates and audience numbers:</b> available on request. <span class="muted small">(Contact address to be added.)</span></p></div>"""))
    open(os.path.join(dist,'about.html'),'w').write(page('About',"""<div class="hero"><h1>About</h1><p class="lead">FusionUpdateTracker turns Oracle's quarterly readiness documentation into a filterable, plain-English list of changes across Oracle Fusion Cloud, with draft impact ratings and a what-to-test checklist for every update.</p></div>
<div class="box"><p>It is run by an Oracle supply chain and ERP consultant based in Switzerland (PrimeLogic Advisory). Every entry links back to its Oracle source page. Summaries are condensed from Oracle's text, and impact ratings are editorial judgment, so always check the Oracle page and your own configuration.</p>
<p>This is an independent site, not affiliated with or endorsed by Oracle.</p><p class="small muted">Method: features come from the "Feature Summary" tables in Oracle's What's New documents. Enablement comes from Oracle's "Action to Enable" column plus the Current Opt-In Expirations list. Impact draft: Oracle's "Larger scale" maps to high; opt-ins expiring this update or next are high; "Small scale" or automatically enabled Redwood changes are medium; everything else is low.</p></div>"""))

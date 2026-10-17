import os, html, json, shutil, collections
E=html.escape
SITE='Fusion Updates'
BASE='https://fusionupdates.com'
import os as _os
CONTACT=_os.environ.get('FUT_CONTACT') or 'hello@fusionupdates.com'  # public contact / reply-to address
def contact_html(): return f'<a href="mailto:{CONTACT}">{CONTACT}</a>' if CONTACT else '<b>[contact address to be added]</b>'
# Sponsorship pages and links stay off until there are subscribers (Gus's rule). Set True (or env FUT_SHOW_SPONSORS=1) to turn back on.
SHOW_SPONSORS=_os.environ.get('FUT_SHOW_SPONSORS')=='1'
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
.current{background:linear-gradient(135deg,#14202b,#2a3d50);color:#fff;border-radius:14px;padding:28px;margin:22px 0}.current h2{font-size:30px;margin:8px 0}.current .lead{color:#d6dee6}
.current .tag{background:#ff8a70;color:#14202b;font-weight:700;border-radius:999px;padding:3px 12px;font-size:13px;text-transform:uppercase;letter-spacing:.04em}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:18px 0}.stats div{background:rgba(255,255,255,.08);border-radius:10px;padding:14px}.stats b{display:block;font-size:30px;color:#ff8a70}.stats span{color:#d6dee6;font-size:14px}
.btn{display:inline-block;background:var(--acc);color:#fff;text-decoration:none;font-weight:600;padding:10px 16px;border-radius:8px;margin:4px 6px 4px 0}.btn.alt{background:#fff;color:#14202b}
"""
NAV=''
P_CUR='/'
def page(title, body, depth=0, desc='', path='', head=''):
    p='../'*depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | {SITE}</title><meta name="description" content="{E(desc or 'Plain-English tracker of Oracle Fusion Cloud quarterly updates: what changed, what turns on automatically, what to test.')}">
<link rel="canonical" href="{BASE}/{path}"><meta property="og:url" content="{BASE}/{path}"><meta property="og:title" content="{E(title)} | {SITE}"><meta property="og:type" content="website"><meta property="og:site_name" content="{SITE}"><meta property="og:description" content="{E(desc or 'Plain-English tracker of Oracle Fusion Cloud quarterly updates.')}"><link rel="stylesheet" href="{p}style.css">{head}</head><body>
<header><div class="w"><a class="brand" href="{p}index.html">Fusion<span>Updates</span></a><nav>
{NAV.replace("@",p)}<a href="{p}newsletter.html">Newsletter</a>{f'<a href="{p}sponsor.html">Sponsor</a>' if SHOW_SPONSORS else ''}<a href="{p}about.html">About</a></nav></div></header>
<main class="w">{body}</main>
<footer><div class="w">Independent site, not affiliated with or endorsed by Oracle. Oracle and Oracle Fusion are trademarks of Oracle and/or its affiliates.
Summaries are condensed from Oracle's public readiness documentation; always confirm details on the linked Oracle page. Impact ratings are editorial drafts. · <a href="{p}privacy.html">Privacy</a> · <a href="{p}about.html">About</a> · Contact: <a href="mailto:{CONTACT}">{CONTACT}</a></div></footer></body></html>"""
def nl_form(p=''):
    p=P_CUR
    return f"""<div class="box"><h3 style="margin-top:0">Get the quarterly briefing</h3><p class="muted">One email per update (plus short alerts before opt-in expirations): the changes that matter, by module, and what to test.</p>
<form class="nl" action="https://uufmlmwgvoqhhtqgrclu.supabase.co/functions/v1/fut-subscribe" method="post" onsubmit="return futSub(this)"><input type="email" name="email" placeholder="you@company.com" required maxlength="254">
<input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
<select name="area"><option>All modules</option><option>Financials</option><option>Procurement</option><option>Supply Chain &amp; Manufacturing</option><option>Logistics</option><option>Project Management</option><option>HCM</option></select><button type="submit">Subscribe</button></form>
<p class="small muted nl-msg" aria-live="polite">Free. One email per update. Unsubscribe any time. <a href="{p}privacy.html">Privacy</a></p>
<script>if(!window.futSub){{window.futSub=function(f){{const m=f.parentNode.querySelector('.nl-msg'),b=f.querySelector('button');b.disabled=true;m.textContent='Subscribing…';
fetch(f.action,{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(Object.fromEntries(new FormData(f)))}}).then(r=>r.json().then(j=>[r.status,j])).then(([s,j])=>{{
m.textContent=j.ok?"Thanks! You're on the list.":(j.error==='invalid_email'?'Please enter a valid email address.':(s===429?'Too many attempts. Please try again later.':'Something went wrong. Please try again.'));if(j.ok)f.reset();}}).catch(()=>{{m.textContent='Network error. Please try again.'}}).finally(()=>{{b.disabled=false}});return false;}}}}</script></div>"""
def enc(e): return 'e-exp' if 'expires' in e else ('e-auto' if e.startswith('Automatically') else '')
def update_page(u):
    items=u['items']; fams=sorted(set(i['family'] for i in items)); prods=sorted(set(i['product'] for i in items))
    cnt=collections.Counter(i['family'] for i in items)
    rows=[item_html(i) for i in items]
    for i in []:
        rows.append(f"""<div class="item" data-family="{E(i['family'])}" data-product="{E(i['product'])}" data-impact="{i['impact']}" data-en="{E(i['enablement'])}" data-text="{E((i['title']+' '+i['summary']+' '+i['module']).lower())}">
<h4><a href="{E(i['url'])}" target="_blank" rel="noopener">{E(i['title'])}</a></h4>
<div class="meta"><span class="pill i-{i['impact']}">Impact: {i['impact']} (draft)</span><span class="pill {enc(i['enablement'])}">{E(i['enablement'])}</span><span class="pill">{E(i['family'])}</span><span class="pill">{E(i['product'])} · {E(i['module'])}</span>{'<span class="pill">'+E(i['tags'])+'</span>' if i.get('tags') else ''}</div>
<div>{E(i['summary']) or '<span class="muted">Summary pending, see Oracle page.</span>'}</div>
<div class="small muted">Oracle's own impact label: {E(i['oracle_impact'])} · Action to enable: {E(i['action'])} · <a href="{E(i['url'])}" target="_blank" rel="noopener">Oracle source</a></div></div>""")
    opt=lambda xs:''.join(f'<option>{E(x)}</option>' for x in xs)
    body=f"""<div class="hero"><h1>Oracle Fusion Cloud {u['release']}: what changed</h1>
<p class="lead">{len(items)} changes we track: the most relevant ones, up to 25 per module family (out of {u['total_features']} features, by our count, in the {u['release']} What's New documents for Financials, Procurement, SCM, Logistics, Projects and HCM). <a href="checklist.html">See the {u['release']} what-to-test checklist →</a></p>
<p><span class="draft">DRAFT impact ratings, pending editorial review</span></p>
<p class="small muted">By module family: {' · '.join(f'<a href="../../{u["release"].lower()}/{FSLUG[f]}/">{E(FNAME[f])}</a> ({cnt[f]})' for f in fams)} · <a href="../../{u['release'].lower()}/former-opt-ins-now-standard/">Former opt-ins now standard in {u['release']} ({len(u['expiring'])})</a></p></div>
<div class="filters"><select id="fam"><option value="">All module families</option>{opt(fams)}</select>
<select id="prod"><option value="">All products</option>{opt(prods)}</select>
<select id="imp"><option value="">Any impact</option><option>high</option><option>medium</option><option>low</option></select>
<select id="en"><option value="">Any enablement</option><option value="Automatically">Automatically on</option><option value="Opt-in">Opt-in</option><option value="expires">Opt-in expiring</option><option value="Off until">Off until set up</option></select>
<input id="q" placeholder="Search…"><span id="n" class="muted small" style="align-self:center"></span></div>
<div id="list">{''.join(rows)}</div>
<script>
const $=id=>document.getElementById(id);function f(){{let n=0;document.querySelectorAll('.item').forEach(e=>{{const ok=(!$('fam').value||e.dataset.family==$('fam').value)&&(!$('prod').value||e.dataset.product==$('prod').value)&&(!$('imp').value||e.dataset.impact==$('imp').value)&&(!$('en').value||e.dataset.en.includes($('en').value))&&(!$('q').value||e.dataset.text.includes($('q').value.toLowerCase()));e.style.display=ok?'':'none';if(ok)n++}});$('n').textContent=n+' shown'}}
['fam','prod','imp','en','q'].forEach(i=>$(i).addEventListener('input',f));f();</script>{nl_form()}"""
    return page(f"Oracle Fusion {u['release']} changes", body, 2, f"What changed in Oracle Fusion Cloud {u['release']}: plain-English summaries, impact, and enablement across Financials, Procurement, SCM, Projects and HCM.", f"updates/{u['release'].lower()}/")
def checklist_page(u):
    items=u['items']
    auto_hi=[i for i in items if i['enablement'].startswith('Automatically') and i['impact'] in('high','medium')]
    byfam=collections.defaultdict(list)
    for i in auto_hi: byfam[i['family']].append(i)
    exp=''.join(f"<tr><td>{E(e['product'])}</td><td>{E(e['module'])}</td><td>{'<a href=\"'+E(e['url'])+'\" target=_blank>' if e['url'] else ''}{E(e['title'])}{'</a>' if e['url'] else ''}</td><td>{E(e.get('now_enabled',''))}</td><td>{E(e['impact'])}</td><td>{E(e['action'])}</td><td>{E(e['introduced'])}</td></tr>" for e in u['expiring'])
    fams=''.join(f"<h3>{E(f)}</h3><ul class='check'>"+''.join(f"<li><label><input type=checkbox> <a href='{E(i['url'])}' target=_blank>{E(i['title'])}</a> <span class='small muted'>({E(i['product'])} · {E(i['module'])}, {i['impact']})</span></label></li>" for i in v)+"</ul>" for f,v in sorted(byfam.items()))
    imp=''.join(f"<li><a href='{E(x['url'])}' target=_blank>{E(x['product'])}</a> <span class='small muted'>{E(x['family'])}</span></li>" for x in sorted(u['important'],key=lambda x:(x['family'],x['product'])))
    body=f"""<div class="hero"><h1>{u['release']} what-to-test checklist</h1><p class="lead">A starting point for checking the {u['release']} quarterly update: in your test environment before it reaches production, or in production if you're already on it. Tick items as you go (ticks are not saved).</p><p><span class="draft">DRAFT, pending editorial review</span></p></div>
<div class="box" id="baseline"><h2>1. Baseline regression (every update)</h2><p class="small muted">Based on Oracle's published guidance: <a href="https://docs.oracle.com/en/cloud/saas/transportation/26b/otmpt/what-should-i-test-after-a-quarterly-update.html" target=_blank>What Should I Test After a Quarterly Update?</a></p><ul class="check">
{''.join(f'<li><label><input type=checkbox> {x}</label></li>' for x in ["Validate your <b>current</b> configuration first; don't enable new features yet","Key end-to-end business flows for each role (e.g. procure-to-pay, order-to-cash, plan-to-produce, hire-to-retire)","Integrations: REST/SOAP APIs, FBDI/HDL imports, and third-party systems","Critical custom reports and analytics (BI Publisher, OTBI)","Custom workflows, approvals, extensions, and personalizations","Security: roles and privileges for new or changed pages","Features delivered automatically on (section 2) and former opt-ins that are now standard (section 3)","Performance of key flows with production-like volumes"])}</ul></div>
<div class="box" id="auto"><h2>2. Changes that switch on automatically (medium/high draft impact)</h2>{fams or '<p class=muted>None in this selection.</p>'}</div>
<div class="box" id="expiring"><h2>3. Former opt-ins that are standard from {u['release']}</h2><p class="small muted">From Oracle's <a href="https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html" target=_blank>Current Opt-In Expirations</a> list (all pillars, including non-ERP).</p>
<table><tr><th>Product</th><th>Module</th><th>Feature</th><th>Now enabled</th><th>Impact</th><th>Action</th><th>Introduced</th></tr>{exp or '<tr><td colspan=7>None listed.</td></tr>'}</table></div>
<div class="box"><h2>4. Read Oracle's "IMPORTANT Actions and Considerations" per product</h2><ul>{imp}</ul></div>{nl_form()}"""
    return page(f"{u['release']} what-to-test checklist", body, 2, desc=f"Oracle Fusion {u['release']} what-to-test checklist: baseline regression, changes delivered switched on, former opt-ins now standard, and Oracle's IMPORTANT actions per product.", path=f"updates/{u['release'].lower()}/checklist.html")
def render(updates, dist, upcoming=None, generated=''):
    global NAV
    NAV=''.join(f'<a href="@updates/{k.lower()}/index.html">{k}{" (current)" if n==0 else ""}</a>' for n,k in enumerate(sorted(updates,reverse=True)))
    if os.path.exists(dist): shutil.rmtree(dist)
    os.makedirs(dist); open(os.path.join(dist,'style.css'),'w').write(CSS)
    for k,u in updates.items():
        d=os.path.join(dist,'updates',k.lower()); os.makedirs(d)
        open(os.path.join(d,'index.html'),'w').write(update_page(u)); open(os.path.join(d,'checklist.html'),'w').write(checklist_page(u))
    order=sorted(updates, reverse=True)  # newest first, e.g. 26D > 26C > 26B; 27A > 26D
    cur=updates[order[0]]; ck=order[0].lower()
    hi=sum(1 for i in cur['items'] if i['impact']=='high'); auto=sum(1 for i in cur['items'] if i['enablement'].startswith('Automatically'))
    hero=f"""<section class="current"><span class="tag">Current update</span><h2>Oracle Fusion Cloud {cur['release']}</h2>
<p class="lead">The current quarterly update. Start here: what changed, what switches on automatically, and which former opt-ins are now standard.</p>
<div class="stats"><div><b>{len(cur['items'])}</b><span>changes we track</span></div><div><b>{len(cur['expiring'])}</b><span>former opt-ins now standard (Oracle's opt-in expiration list, all pillars)</span></div><div><b>{hi}</b><span>tracked changes rated high impact (draft)</span></div><div><b>{auto}</b><span>tracked changes delivered switched on</span></div></div>
<p class="small">We track up to 25 changes per module family, out of {cur['total_features']} features (our count) in the {cur['release']} What's New documents for these modules. The opt-in figure is Oracle's own Current Opt-In Expirations list.</p>
<p><a class="btn" href="updates/{ck}/index.html">Browse {cur['release']} changes →</a> <a class="btn alt" href="updates/{ck}/checklist.html">{cur['release']} what-to-test checklist →</a> <a class="btn alt" href="{ck}/former-opt-ins-now-standard/">{cur['release']} former opt-ins now standard →</a></p></section>"""
    prev=''.join(f"""<div class="card"><h3>Update {k}</h3><p class="muted">{len(updates[k]['items'])} changes we track · {updates[k]['total_features']} features in the What's New documents (our count) · {len(updates[k]['expiring'])} opt-ins expiring</p>
<p><a href="updates/{k.lower()}/index.html">Browse changes →</a><br><a href="updates/{k.lower()}/checklist.html">What to test →</a></p></div>""" for k in order[1:])
    prevsec=f'<h2>Previous updates</h2><div class="cards">{prev}</div>' if prev else ''
    fams=sorted(set(i['family'] for u in updates.values() for i in u['items']))
    famlinks=''.join(f"<p><b>{E(FNAME[f])}:</b> "+' · '.join(f'<a href="{k.lower()}/{FSLUG[f]}/">{k}</a>' for k in order)+"</p>" for f in fams)
    upsec=f'<div class="box"><h3 style="margin-top:0">Coming next: {upcoming["release"]}</h3><p>Oracle has published its {upcoming["release"]} What\'s New documents. <a href="{upcoming["release"].lower()}/">Oracle Fusion {upcoming["release"]}: what to expect →</a></p></div>' if upcoming else ''
    home=f"""<div class="hero"><h1>Every Oracle Fusion quarterly update, in plain English.</h1>
<p class="lead">What changed in Financials, Procurement, Supply Chain, Logistics, Project Management and HCM, what switches on automatically, which opt-ins are becoming standard features, and what to test before it hits production.</p></div>
{hero}{upsec}{prevsec}<div class="box"><h3 style="margin-top:0">Covered module families</h3>{famlinks}</div>{nl_form()}"""
    open(os.path.join(dist,'index.html'),'w').write(page('Oracle Fusion Cloud quarterly update tracker',home,desc='Every Oracle Fusion Cloud quarterly update in plain English: what changed by module, what switches on automatically, former opt-ins now standard, and what to test.',path='',head=jsonld({"@context":"https://schema.org","@graph":[{"@type":"WebSite","@id":BASE+"/#website","url":BASE+"/","name":SITE,"description":"Plain-English tracker of Oracle Fusion Cloud quarterly updates.","publisher":{"@id":BASE+"/#org"}},{"@type":"Organization","@id":BASE+"/#org","name":SITE,"url":BASE+"/","logo":BASE+"/logo.png","email":CONTACT}]})))
    # SEO pages
    extra=[]
    for k,u in updates.items():
        rk=k.lower()
        for f in sorted(set(i['family'] for i in u['items'])):
            d=os.path.join(dist,rk,FSLUG[f]); os.makedirs(d,exist_ok=True)
            open(os.path.join(d,'index.html'),'w').write(family_page(u,f,updates)); extra.append(f'{rk}/{FSLUG[f]}/')
        d=os.path.join(dist,rk,'former-opt-ins-now-standard'); os.makedirs(d,exist_ok=True)
        open(os.path.join(d,'index.html'),'w').write(standard_page(u)); extra.append(f'{rk}/former-opt-ins-now-standard/')
    if upcoming:
        d=os.path.join(dist,upcoming['release'].lower()); os.makedirs(d,exist_ok=True)
        open(os.path.join(d,'index.html'),'w').write(upcoming_page(upcoming,updates)); extra.append(f"{upcoming['release'].lower()}/")
    lp=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'static')
    if os.path.isdir(lp):
        for fn in os.listdir(lp): shutil.copy(os.path.join(lp,fn),os.path.join(dist,fn))
    open(os.path.join(dist,'privacy.html'),'w').write(page('Privacy',desc='How Fusion Updates handles newsletter subscriber data: what we store, where, and how to unsubscribe or ask for deletion.',path='privacy.html',body='''<div class="hero"><h1>Privacy</h1><p class="lead">Short version: we only store what's needed to send you the newsletter.</p></div>
<div class="box"><h3 style="margin-top:0">What we store when you subscribe</h3><ul><li>Your email address</li><li>The module area you picked (e.g. Supply Chain or HCM)</li><li>When you signed up</li><li>A one-way hash of your IP address, kept only to limit spam signups (we never store the IP address itself)</li></ul>
<h3>How we use it</h3><p>Only to send the Fusion Updates newsletter (about one email per Oracle quarterly update, plus occasional short alerts about opt-in expirations). We don't sell or share your data, and we don't add you to other lists.</p>
<h3>Where it's kept</h3><p>Subscriber data is stored with Supabase (EU region, Frankfurt), and newsletters are sent with Resend (EU region). Both act as processors for us.</p>
<h3>Unsubscribe and deletion</h3><p>Every email has a one-click unsubscribe link. To have your data deleted, or for any question, write to '''+contact_html()+'''.</p>
<h3>Analytics</h3><p>This site uses no tracking cookies, and newsletter open and click tracking is turned off.</p>
<p class="small muted">Fusion Updates is an independent publication. Questions about your data: hello@fusionupdates.com. Last updated: October 2026.</p></div>'''))
    open(os.path.join(dist,'CNAME'),'w').write('fusionupdates.com\n')
    open(os.path.join(dist,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
    urls=['','newsletter.html']+(['sponsor.html'] if SHOW_SPONSORS else [])+['about.html','privacy.html']+[f'updates/{k.lower()}/' for k in updates]+[f'updates/{k.lower()}/checklist.html' for k in updates]+extra
    lm=f'<lastmod>{generated}</lastmod>' if generated else ''
    open(os.path.join(dist,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE}/{u}</loc>{lm}</url>\n' for u in urls)+'</urlset>\n')
    open(os.path.join(dist,'newsletter.html'),'w').write(page('Newsletter',desc='Free quarterly briefing on Oracle Fusion Cloud updates: the changes that matter by module, opt-in expirations and a test checklist.',path='newsletter.html',body='<div class="hero"><h1>The quarterly briefing</h1><p class="lead">Before each Oracle Fusion update reaches your test environment: the changes that matter, by module, the opt-ins about to expire, and a ready-to-use test checklist. Free.</p></div>'+nl_form()))
    if SHOW_SPONSORS: open(os.path.join(dist,'sponsor.html'),'w').write(page('Sponsor',desc='Sponsor Fusion Updates to reach people who plan, test and run Oracle Fusion Cloud quarterly updates.',path='sponsor.html',body="""<div class="hero"><h1>Sponsor Fusion Updates</h1><p class="lead">Reach the people who plan, test and run Oracle Fusion Cloud updates: application owners, functional leads, testers and consultants across Financials, Procurement, SCM, Projects and HCM.</p></div>
<div class="cards"><div class="card"><h3>Newsletter sponsor</h3><p class="muted">One sponsor slot per quarterly briefing, sent before each update's test window.</p></div>
<div class="card"><h3>Update page sponsor</h3><p class="muted">"Presented by" placement on an update's change list and test checklist.</p></div>
<div class="card"><h3>Module sponsor</h3><p class="muted">Placement on one module family (e.g. Supply Chain or HCM) across updates.</p></div></div>
<div class="box"><p>Good fits: test automation, data loading and migration tools, Oracle partners and add-on vendors. Sponsors never influence summaries or ratings, and sponsored placements are always labeled.</p><p><b>Rates and audience numbers:</b> available on request. """+(f"Write to {contact_html()}." if CONTACT else '<span class="muted small">(Contact address to be added.)</span>')+"""</p></div>"""))
    open(os.path.join(dist,'about.html'),'w').write(page('About',desc='About Fusion Updates: an independent, plain-English tracker of Oracle Fusion Cloud quarterly updates, and how it is built.',path='about.html',body="""<div class="hero"><h1>About</h1><p class="lead">Fusion Updates (fusionupdates.com) turns Oracle's quarterly readiness documentation into a filterable, plain-English list of changes across Oracle Fusion Cloud, with draft impact ratings and a what-to-test checklist for every update.</p></div>
<div class="box"><p>It is run by an experienced Oracle consultant. Every entry links back to its Oracle source page. Summaries are condensed from Oracle's text, and impact ratings are editorial judgment, so always check the Oracle page and your own configuration.</p>
<p>This is an independent site, not affiliated with or endorsed by Oracle.</p><p class="small muted">Method: features come from the "Feature Summary" tables in Oracle's What's New documents. Enablement comes from Oracle's "Action to Enable" column plus the Current Opt-In Expirations list. Impact draft: Oracle's "Larger scale" maps to high; opt-ins expiring this update or next are high; "Small scale" or automatically enabled Redwood changes are medium; everything else is low.</p></div>"""))

# ---------------- SEO pages ----------------
FSLUG={'Financials':'financials','Procurement':'procurement','Supply Chain & Manufacturing':'supply-chain-manufacturing','Logistics (OTM/GTM/WMS)':'logistics','Project Management':'project-management','HCM':'hcm'}
FNAME={'Financials':'Financials','Procurement':'Procurement','Supply Chain & Manufacturing':'Supply Chain & Manufacturing','Logistics (OTM/GTM/WMS)':'Logistics (OTM, GTM, WMS)','Project Management':'Project Management','HCM':'HCM'}
def jsonld(o): return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False).replace('</','<\\/')+'</script>'
def crumbs(lst): return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":n+1,"name":nm,"item":BASE+'/'+u} for n,(nm,u) in enumerate(lst)]}
def crumbs_html(lst,p): return '<p class="small muted">'+' › '.join(f'<a href="{p}{u}">{E(nm)}</a>' if n<len(lst)-1 else E(nm) for n,(nm,u) in enumerate(lst))+'</p>'
def item_html(i):
    return f"""<div class="item" data-family="{E(i['family'])}" data-product="{E(i['product'])}" data-impact="{i['impact']}" data-en="{E(i['enablement'])}" data-text="{E((i['title']+' '+i['summary']+' '+i['module']).lower())}">
<h4><a href="{E(i['url'])}" target="_blank" rel="noopener">{E(i['title'])}</a></h4>
<div class="meta"><span class="pill i-{i['impact']}">Impact: {i['impact']} (draft)</span><span class="pill {enc(i['enablement'])}">{E(i['enablement'])}</span><span class="pill">{E(i['family'])}</span><span class="pill">{E(i['product'])} · {E(i['module'])}</span>{'<span class="pill">'+E(i['tags'])+'</span>' if i.get('tags') else ''}</div>
<div>{E(i['summary']) or '<span class="muted">Summary pending, see Oracle page.</span>'}</div>
<div class="small muted">Oracle's own impact label: {E(i['oracle_impact'])} · Action to enable: {E(i['action'])} · <a href="{E(i['url'])}" target="_blank" rel="noopener">Oracle source</a></div></div>"""
def exp_family(e):
    pl,pr=e['pillar'],e['product']
    if pl.startswith('Enterprise Resource'): return 'Project Management' if pr.startswith('Project') else 'Financials'
    if pl.startswith('Supply Chain'): return 'Procurement' if pr.startswith('Procurement') or 'Sourcing' in pr or 'Supplier' in pr else 'Supply Chain & Manufacturing'
    if pl.startswith('Human Capital') or pl=='HCM': return 'HCM'
    if 'Logistics' in pl: return 'Logistics (OTM/GTM/WMS)'
    return None
ACT={'None':'Nothing to do: on for everyone','Setup':'Set up if you want to use it'}
def exp_table(es):
    if not es: return '<p class="muted">None in Oracle\'s list.</p>'
    return '<table><tr><th>Feature (Oracle source)</th><th>Product · Module</th><th>Now enabled</th><th>What this means</th><th>Oracle\'s impact</th><th>First delivered</th></tr>'+''.join(
        f"<tr><td>{'<a href=\"'+E(e['url'])+'\" target=_blank rel=noopener>' if e['url'] else ''}{E(e['title'])}{'</a>' if e['url'] else ''}</td><td>{E(e['product'])} · {E(e['module'])}</td><td>{E(e['now_enabled'])}</td><td>{E(ACT.get(e['action'],e['action']))}</td><td>{E(e['impact'])}</td><td>{E(e['introduced'])}</td></tr>" for e in es)+'</table>'
def family_page(u,f,updates):
    rel=u['release']; rk=rel.lower(); fn=FNAME[f]
    its=sorted([i for i in u['items'] if i['family']==f],key=lambda i:({'high':0,'medium':1,'low':2}[i['impact']],i['product'],i['title']))
    auto=[i for i in its if i['enablement'].startswith('Automatically')]; rest=[i for i in its if not i['enablement'].startswith('Automatically')]
    tot=u.get('family_totals',{}).get(f); books=[b for b in u.get('books',[]) if b['family']==f]
    exps=[e for e in u['expiring'] if exp_family(e)==f]
    title=f"Oracle Fusion {fn} {rel}: what changed"
    desc=f"What changed in Oracle Fusion {fn} {rel}, in plain English: {len(its)} changes we track, {len(auto)} delivered switched on, and {len(exps)} former opt-in{'s' if len(exps)!=1 else ''} now standard. Every item links to Oracle's docs."
    path=f"{rk}/{fn and FSLUG[f]}/"
    cl=[('Home',''),(f'{rel}',f'updates/{rk}/'),(fn,path)]
    others=' · '.join(f'<a href="../{FSLUG[g]}/">{E(FNAME[g])}</a>' for g in sorted(set(i['family'] for i in u['items'])) if g!=f)
    otherrel=' · '.join(f'<a href="../../{k.lower()}/{FSLUG[f]}/">{fn} {k}</a>' for k in sorted(updates,reverse=True) if k!=rel and any(i['family']==f for i in updates[k]['items']))
    booklinks=' · '.join(f'<a href="{E(b["url"])}" target=_blank rel=noopener>{E(b["product"])} {rel} What\'s New</a>' for b in books)
    body=f"""{crumbs_html(cl,'../../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">We track {len(its)} {E(fn)} changes in {rel}{f', out of {tot} features (our count) in Oracle&#39;s {rel} What&#39;s New documents for this area' if tot else ''}. {len(auto)} of them are delivered switched on; {len(rest)} need setup or an opt-in before anyone can use them.</p>
<p class="small muted">Oracle sources: {booklinks}</p><p><span class="draft">DRAFT impact ratings, pending editorial review</span></p></div>
<div class="box"><h2 style="margin-top:0">Former opt-ins now standard in {rel}</h2><p class="small muted">From Oracle's <a href="https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html" target=_blank rel=noopener>Current Opt-In Expirations</a> list: features whose opt-in period ended with {rel}. If you already opted in and finished setup, nothing changes. <a href="../former-opt-ins-now-standard/">All former opt-ins now standard in {rel} →</a></p>{exp_table(exps)}</div>
<h2>Delivered switched on ({len(auto)})</h2>{''.join(item_html(i) for i in auto) or '<p class="muted">None among the changes we track.</p>'}
<h2>Needs setup or opt-in ({len(rest)})</h2>{''.join(item_html(i) for i in rest) or '<p class="muted">None among the changes we track.</p>'}
<div class="box"><p><b>More {rel}:</b> <a href="../../updates/{rk}/">All {len(u['items'])} tracked {rel} changes</a> · <a href="../../updates/{rk}/checklist.html">{rel} what-to-test checklist</a> · <a href="../former-opt-ins-now-standard/">{rel} former opt-ins now standard</a></p><p><b>Other module families in {rel}:</b> {others}</p>{f'<p><b>Other releases:</b> {otherrel}</p>' if otherrel else ''}</div>{nl_form()}"""
    ld=jsonld({"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":BASE+'/'+path,"url":BASE+'/'+path,"name":title,"description":desc,"inLanguage":"en","isPartOf":{"@type":"WebSite","@id":BASE+"/#website","name":SITE,"url":BASE+"/"},"about":{"@type":"SoftwareApplication","name":f"Oracle Fusion Cloud {fn}","softwareVersion":rel,"applicationCategory":"BusinessApplication"},"dateModified":None},
        crumbs(cl),{"@type":"ItemList","name":f"{fn} {rel} changes we track","numberOfItems":len(its),"itemListElement":[{"@type":"ListItem","position":n+1,"name":i['title'],"url":i['url']} for n,i in enumerate(its)]}]})
    ld=ld.replace(',"dateModified":null','')
    return page(title,body,2,desc,path,ld)
def standard_page(u):
    rel=u['release']; rk=rel.lower(); es=u['expiring']
    on=sum(1 for e in es if e['now_enabled']=='Yes'); st=len(es)-on
    grp=collections.OrderedDict()
    for f in FSLUG:
        x=[e for e in es if exp_family(e)==f]
        if x: grp[FNAME[f]]=x
    oth=[e for e in es if exp_family(e) is None]
    if oth: grp['Other Oracle pillars (outside the modules we track)']=oth
    core=len(es)-len(oth)
    title=f"Oracle Fusion {rel}: former opt-ins now standard"
    desc=f"The {len(es)} Oracle Fusion features whose opt-in period ended with {rel}, from Oracle's opt-in expiration list: {on} switched on automatically, {st} need setup if you want them. Plain English, with Oracle links."
    path=f"{rk}/former-opt-ins-now-standard/"; cl=[('Home',''),(rel,f'updates/{rk}/'),('Former opt-ins now standard',path)]
    body=f"""{crumbs_html(cl,'../../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">Oracle's <a href="https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html" target=_blank rel=noopener>Current Opt-In Expirations</a> list names {len(es)} features whose opt-in period ended with {rel}. They are now standard: {on} are switched on automatically, and {st} need setup if you want to use them.{f' {core} of them are in the module families we track.' if oth else ''}</p>
<p class="small muted">Oracle's note: if you already opted in and finished the setup, nothing changes for you. "Now enabled" and "Oracle's impact" are Oracle's own columns.</p></div>
{''.join(f'<div class="box"><h2 style="margin-top:0">{E(g)} ({len(x)})</h2>{exp_table(x)}</div>' for g,x in grp.items())}
<div class="box"><p><b>More {rel}:</b> <a href="../../updates/{rk}/">All tracked {rel} changes</a> · <a href="../../updates/{rk}/checklist.html">{rel} what-to-test checklist</a> · {' · '.join(f'<a href="../{FSLUG[f]}/">{E(FNAME[f])} {rel}</a>' for f in sorted(set(i['family'] for i in u['items'])))}</p></div>{nl_form()}"""
    ld=jsonld({"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":BASE+'/'+path,"url":BASE+'/'+path,"name":title,"description":desc,"inLanguage":"en","isPartOf":{"@type":"WebSite","@id":BASE+"/#website","name":SITE,"url":BASE+"/"}},crumbs(cl),
        {"@type":"ItemList","name":title,"numberOfItems":len(es),"itemListElement":[{"@type":"ListItem","position":n+1,"name":e['title'],"url":e['url']} for n,e in enumerate(es) if e['url']]}]})
    return page(title,body,2,desc,path,ld)
def upcoming_page(up,updates):
    rel=up['release']; rk=rel.lower(); es=up['expiring']
    on=sum(1 for e in es if e['now_enabled']=='Yes')
    byf=collections.defaultdict(list)
    for b in up['books']: byf[FNAME.get(b['family'],b['family'])].append(b)
    ann=[i for k in updates for i in updates[k]['items'] if rel in i['title']]
    title=f"Oracle Fusion {rel}: what to expect"
    desc=f"Oracle Fusion Cloud {rel} is next. Links to Oracle's published {rel} What's New documents, features Oracle has already announced for {rel}, and the {len(es)} opt-ins Oracle lists as ending with {rel}."
    path=f"{rk}/"; cl=[('Home',''),(f'{rel}: what to expect',path)]
    body=f"""{crumbs_html(cl,'../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">{rel} is the next Oracle Fusion Cloud quarterly update. Oracle has published its {rel} What's New documents. We haven't added {rel} to the tracker yet; plain-English summaries follow. Until then, here is what Oracle has already published.</p><p><span class="draft">Placeholder, to be expanded</span></p></div>
<div class="box"><h2 style="margin-top:0">When it arrives</h2><p>Oracle updates environments in cohorts. Per Oracle, Cohort A gets quarterly updates in February, May, August and November, Cohort B in March, June, September and December, and Cohort C in April, July, October and January. Test environments update on the first Friday of the update month and production two weeks later, on the third Friday. Your cohort is shown in the Oracle Cloud Console. <span class="small muted">Source: <a href="https://blogs.oracle.com/fusioninsider/quarterly-updates-made-easy" target=_blank rel=noopener>Oracle Fusion Insider, "Quarterly updates made easy"</a></span></p></div>
<div class="box"><h2 style="margin-top:0">Oracle's {rel} What's New documents</h2>{''.join(f'<p><b>{E(g)}:</b> '+' · '.join(f'<a href="{E(b["url"])}" target=_blank rel=noopener>{E(b["product"])}</a>' for b in bs)+'</p>' for g,bs in byf.items())}</div>
{f'<div class="box"><h2 style="margin-top:0">Already announced for {rel} in earlier What&#39;s New documents</h2><ul>'+''.join(f'<li><a href="{E(i["url"])}" target=_blank rel=noopener>{E(i["title"])}</a> <span class="small muted">({E(i["product"])}, from the {i["_rel"]} What&#39;s New)</span></li>' for i in ann)+'</ul></div>' if ann else ''}
<div class="box"><h2 style="margin-top:0">Opt-ins Oracle lists as ending with {rel} ({len(es)})</h2><p class="small muted">From Oracle's <a href="https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html" target=_blank rel=noopener>Current Opt-In Expirations</a> list. With {rel} they become standard features. Oracle's "Now enabled" column shows Yes for {on} of them; the rest need setup if you want to use them. Oracle can update this list.</p>{exp_table(es)}</div>{nl_form()}"""
    ld=jsonld({"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":BASE+'/'+path,"url":BASE+'/'+path,"name":title,"description":desc,"inLanguage":"en","isPartOf":{"@type":"WebSite","@id":BASE+"/#website","name":SITE,"url":BASE+"/"}},crumbs(cl)]})
    return page(title,body,1,desc,path,ld)

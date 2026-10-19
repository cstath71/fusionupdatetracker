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
.note{color:var(--mut);font-size:13px}
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
.nlc{background:#fff;border:1px solid var(--line);border-left:4px solid var(--acc);border-radius:10px;padding:14px 16px;margin:6px 0 18px;max-width:860px}.nlc h3{margin:0 0 2px;font-size:17px}.nlc p{margin:4px 0}
.nlc form.nl input[type=email]{min-width:220px}
.sticky-sub{display:none}
code{word-break:break-all}.item{overflow-wrap:anywhere}
@media(max-width:700px){table{display:block;overflow-x:auto;max-width:100%}.hero h1{font-size:27px}.sticky-sub{display:block;position:fixed;left:12px;right:12px;bottom:12px;z-index:9;background:var(--acc);color:#fff;text-align:center;font-weight:700;text-decoration:none;padding:12px;border-radius:10px;box-shadow:0 4px 14px rgba(0,0,0,.25);transition:opacity .2s}.sticky-sub.hide{opacity:0;pointer-events:none}body{padding-bottom:64px}form.nl input[type=email],form.nl select,form.nl button{width:100%;min-width:0}}
.btn{display:inline-block;background:var(--acc);color:#fff;text-decoration:none;font-weight:600;padding:10px 16px;border-radius:8px;margin:4px 6px 4px 0}.btn.alt{background:#fff;color:#14202b}
"""
NAV=''
P_CUR='/'
NEXT_REL='26D'   # set in render() from the upcoming release
UPCOMING=None
UPD_KEYS=[]
HUB_FROM='26D'   # releases from 26D on get a hub page at /<release>/
CURRENT=None    # current update (set in render() from build.py)
LEAD={'rel':'26D','pdf':'downloads/fusion-26d-readiness-checklist.pdf','ics':'downloads/fusion-quarterly-update-calendar.ics'}
OG_SPECS={}      # slug -> (tag, headline, sub); images are drawn by scripts/og.py
def og_slug(path):
    s=path.strip('/').replace('.html','').replace('/','-') or 'home'
    return s+'-archive' if path=='newsletter/' else s
def cta_for(path):
    """Page-specific CTA for the top-of-page signup box: (heading, area preset)."""
    n=NEXT_REL; parts=path.strip('/').split('/')
    fam={v:k for k,v in FSLUG.items()}
    AREA={'Financials':'Financials','Procurement':'Procurement','Supply Chain & Manufacturing':'Supply Chain & Manufacturing','Logistics (OTM/GTM/WMS)':'Logistics','Project Management':'Project Management','HCM':'HCM'}
    if path.startswith('hcm-redwood') or 'redwood-' in path: return ('Get the next HCM Redwood switches in your inbox','HCM')
    if len(parts)==2 and parts[1] in fam:
        f=fam[parts[1]]
        if f=='HCM': return (f'Get the {n} HCM changes and the next Redwood switches before your test pod updates','HCM')
        return (f'Get the {n} {FNAME[f]} briefing before your test pod updates',AREA[f])
    if path.startswith('newsletter/'): return (f'Get the next issue ({n}) in your inbox','All modules')
    if path.startswith('downloads/'): return ('Get the next checklist by email','All modules')
    return (f'Get the {n} briefing before your test pod updates','All modules')
def _after_hero(body,ins):
    i=body.find('<div class="hero">')
    if i<0: return ins+body
    depth=0; j=i
    import re as _re
    for m in _re.finditer(r'<div\b|</div>',body[i:]):
        depth+=1 if m.group(0)!='</div>' else -1
        if depth==0: j=i+m.end(); break
    return body[:j]+ins+body[j:]
def page(title, body, depth=0, desc='', path='', head='', og=None, top_form=True):
    p='../'*depth
    d=desc or 'Plain-English tracker of Oracle Fusion Cloud quarterly updates: what changed, what turns on automatically, what to test.'
    slug=og_slug(path); tag,sub=(og or (None,None))
    OG_SPECS[slug]=(tag or 'Oracle Fusion Cloud quarterly updates', title, sub or 'What changed, what switches on, what to test')
    img=f'{BASE}/og/{slug}.png'; ft=f'{title} | {SITE}'
    ogm=(f'<meta property="og:image" content="{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="627"><meta property="og:image:type" content="image/png"><meta property="og:image:alt" content="{E(title)}">'
         f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(ft)}"><meta name="twitter:description" content="{E(d)}"><meta name="twitter:image" content="{img}"><meta name="twitter:image:alt" content="{E(title)}">')
    if top_form: body=_after_hero(body,nl_compact(*cta_for(path)))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | {SITE}</title><meta name="description" content="{E(d)}">
<link rel="canonical" href="{BASE}/{path}"><meta property="og:url" content="{BASE}/{path}"><meta property="og:title" content="{E(ft)}"><meta property="og:type" content="website"><meta property="og:site_name" content="{SITE}"><meta property="og:description" content="{E(d)}">{ogm}<link rel="stylesheet" href="{p}style.css">{head}</head><body>
<header><div class="w"><a class="brand" href="{p}index.html">Fusion<span>Updates</span></a><nav>
{NAV.replace("@",p)}<a href="{p}newsletter.html">Newsletter</a><a href="{p}downloads/">Free downloads</a>{f'<a href="{p}sponsor.html">Sponsor</a>' if SHOW_SPONSORS else ''}<a href="{p}about.html">About</a></nav></div></header>
<main class="w">{body}</main>
<a class="sticky-sub hide" href="#subscribe">Subscribe: free {LEAD['rel']} checklist</a>
<script>(function(){{var s=document.querySelector('.sticky-sub');if(!s)return;if(!('IntersectionObserver' in window)){{s.classList.remove('hide');return;}}var v=new Set();var o=new IntersectionObserver(function(es){{es.forEach(function(e){{e.isIntersecting?v.add(e.target):v.delete(e.target)}});s.classList.toggle('hide',v.size>0)}});document.querySelectorAll('form.nl').forEach(function(f){{o.observe(f)}});}})();</script>
<footer><div class="w">Independent site, not affiliated with or endorsed by Oracle. Oracle and Oracle Fusion are trademarks of Oracle and/or its affiliates.
Summaries are condensed from Oracle's public readiness documentation. Impact ratings are our editorial view of how much a change affects day-to-day users and testing. Always confirm details on the linked Oracle page. · <a href="{p}privacy.html">Privacy</a> · <a href="{p}about.html">About</a> · Contact: <a href="mailto:{CONTACT}">{CONTACT}</a></div></footer></body></html>"""
FORM_ACTION='https://uufmlmwgvoqhhtqgrclu.supabase.co/functions/v1/fut-subscribe'
HONEYPOT='<input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">'
FINE='Free. 4 emails a year plus short opt-in alerts. Unsubscribe anytime.'
def nl_script():
    p=P_CUR
    ok=f"Thanks! You&#39;re on the list. <a href=\\'{p}{LEAD['pdf']}\\'>Download your free {LEAD['rel']} checklist (PDF)</a>"
    return ("<script>if(!window.futSub){window.futSub=function(f){const m=f.parentNode.querySelector('.nl-msg'),b=f.querySelector('button');b.disabled=true;m.textContent='Subscribing…';"
    "fetch(f.action,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(f)))}).then(r=>r.json().then(j=>[r.status,j])).then(([s,j])=>{"
    "if(j.ok){m.innerHTML='"+ok+"';f.reset();}else{m.textContent=(j.error==='invalid_email'?'Please enter a valid email address.':(s===429?'Too many attempts. Please try again later.':'Something went wrong. Please try again.'));}}).catch(()=>{m.textContent='Network error. Please try again.'}).finally(()=>{b.disabled=false});return false;}}</script>")
def nl_compact(heading,area='All modules'):
    p=P_CUR
    return f"""<div class="nlc" id="subscribe"><h3>{E(heading)}</h3><p class="small muted">Free {LEAD['rel']} checklist PDF when you subscribe. One plain-English email per Oracle quarterly update, linked to Oracle's docs.</p>
<form class="nl" action="{FORM_ACTION}" method="post" onsubmit="return futSub(this)"><input type="email" name="email" placeholder="you@company.com" required maxlength="254" aria-label="Email address">{HONEYPOT}<input type="hidden" name="area" value="{E(area)}"><button type="submit">Send me the briefing</button></form>
<p class="small muted nl-msg" aria-live="polite">{FINE} <a href="{p}privacy.html">Privacy</a></p>{nl_script()}</div>"""
def nl_form(p='',latest=False,top=False):
    p=P_CUR
    li=ISSUES[0] if (latest and ISSUES) else None
    lk=f' <a href="{p}newsletter/{li["slug"]}/">Read issue #{li["number"]} →</a>' if li else ''
    return f"""<div class="box" id="{'subscribe' if top else 'subscribe-bottom'}"><h3 style="margin-top:0">Get the quarterly briefing</h3><p class="muted">One email per update (plus short alerts before opt-in expirations): the changes that matter, by module, and what to test. Free {LEAD['rel']} readiness checklist PDF when you subscribe.{lk}</p>
<form class="nl" action="{FORM_ACTION}" method="post" onsubmit="return futSub(this)"><input type="email" name="email" placeholder="you@company.com" required maxlength="254" aria-label="Email address">
{HONEYPOT}
<select name="area" aria-label="Module area"><option>All modules</option><option>Financials</option><option>Procurement</option><option>Supply Chain &amp; Manufacturing</option><option>Logistics</option><option>Project Management</option><option>HCM</option></select><button type="submit">Send me the briefing</button></form>
<p class="small muted nl-msg" aria-live="polite">{FINE} <a href="{p}privacy.html">Privacy</a></p>
{nl_script()}</div>"""
BASELINE=["Validate your <b>current</b> configuration first; don't enable new features yet","Key end-to-end business flows for each role (e.g. procure-to-pay, order-to-cash, plan-to-produce, hire-to-retire)","Integrations: REST/SOAP APIs, FBDI/HDL imports, and third-party systems","Critical custom reports and analytics (BI Publisher, OTBI)","Custom workflows, approvals, extensions, and personalizations","Security: roles and privileges for new or changed pages","Features delivered automatically on (section 2) and former opt-ins that are now standard (section 3)","Performance of key flows with production-like volumes"]
def enc(e): return 'e-exp' if 'expires' in e else ('e-auto' if e.startswith('Automatically') else '')
def update_page(u):
    items=u['items']; fams=sorted(set(i['family'] for i in items)); prods=sorted(set(i['product'] for i in items))
    cnt=collections.Counter(i['family'] for i in items)
    rows=[item_html(i) for i in items]
    opt=lambda xs:''.join(f'<option>{E(x)}</option>' for x in xs)
    body=f"""<div class="hero"><h1>Oracle Fusion Cloud {u['release']}: what changed</h1>
<p class="lead">{len(items)} changes we track: the most relevant ones, up to 25 per module family (out of {u['total_features']} features, by our count, in the {u['release']} What's New documents for Financials, Procurement, SCM, Logistics, Projects and HCM). <a href="checklist.html">See the {u['release']} what-to-test checklist →</a></p>
<p class="note">Impact ratings are our editorial view of how much a change affects day-to-day users and testing. Always confirm details on the linked Oracle page.</p>
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
    return page(f"Oracle Fusion {u['release']} changes", body, 2, f"What changed in Oracle Fusion Cloud {u['release']}: plain-English summaries, impact, and enablement across Financials, Procurement, SCM, Projects and HCM.", f"updates/{u['release'].lower()}/",og=(f"Oracle Fusion Cloud {u['release']}",f"{len(items)} changes we track · {len(u['expiring'])} former opt-ins now standard"))
def checklist_page(u):
    items=u['items']
    auto_hi=[i for i in items if i['enablement'].startswith('Automatically') and i['impact'] in('high','medium')]
    byfam=collections.defaultdict(list)
    for i in auto_hi: byfam[i['family']].append(i)
    exp=''.join(f"<tr><td>{E(e['product'])}</td><td>{E(e['module'])}</td><td>{'<a href=\"'+E(e['url'])+'\" target=_blank>' if e['url'] else ''}{E(e['title'])}{'</a>' if e['url'] else ''}</td><td>{E(e.get('now_enabled',''))}</td><td>{E(e['impact'])}</td><td>{E(e['action'])}</td><td>{E(e['introduced'])}</td></tr>" for e in u['expiring'])
    fams=''.join(f"<h3>{E(f)}</h3><ul class='check'>"+''.join(f"<li><label><input type=checkbox> <a href='{E(i['url'])}' target=_blank>{E(i['title'])}</a> <span class='small muted'>({E(i['product'])} · {E(i['module'])}, {i['impact']})</span></label></li>" for i in v)+"</ul>" for f,v in sorted(byfam.items()))
    imp=''.join(f"<li><a href='{E(x['url'])}' target=_blank>{E(x['product'])}</a> <span class='small muted'>{E(x['family'])}</span></li>" for x in sorted(u['important'],key=lambda x:(x['family'],x['product'])))
    body=f"""<div class="hero"><h1>{u['release']} what-to-test checklist</h1><p class="lead">A starting point for checking the {u['release']} quarterly update: in your test environment before it reaches production, or in production if you're already on it. Tick items as you go (ticks are not saved).</p><p class="note">Impact ratings are our editorial view of how much a change affects day-to-day users and testing. Always confirm details on the linked Oracle page.</p></div>
<div class="box" id="baseline"><h2>1. Baseline regression (every update)</h2><p class="small muted">Based on Oracle's published guidance: <a href="https://docs.oracle.com/en/cloud/saas/transportation/26b/otmpt/what-should-i-test-after-a-quarterly-update.html" target=_blank>What Should I Test After a Quarterly Update?</a></p><ul class="check">
{''.join(f'<li><label><input type=checkbox> {x}</label></li>' for x in BASELINE)}</ul></div>
<div class="box" id="auto"><h2>2. Changes that switch on automatically (rated medium or high impact)</h2>{fams or '<p class=muted>None in this selection.</p>'}</div>
<div class="box" id="expiring"><h2>3. Former opt-ins that are standard from {u['release']}</h2><p class="small muted">From Oracle's <a href="https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html" target=_blank>Current Opt-In Expirations</a> list. It covers all Fusion modules: {E(exp_scope(u['expiring'],u['release']))}.</p>
<table><tr><th>Product</th><th>Module</th><th>Feature</th><th>Now enabled</th><th>Impact</th><th>Action</th><th>Introduced</th></tr>{exp or '<tr><td colspan=7>None listed.</td></tr>'}</table></div>{hr_box(u['release'],'../../',check=True)}
<div class="box"><h2>4. Read Oracle's "IMPORTANT Actions and Considerations" per product</h2><ul>{imp}</ul></div>{nl_form()}"""
    return page(f"{u['release']} what-to-test checklist", body, 2, desc=f"Oracle Fusion {u['release']} what-to-test checklist: baseline regression, changes delivered switched on, former opt-ins now standard, and Oracle's IMPORTANT actions per product.", path=f"updates/{u['release'].lower()}/checklist.html",og=(f"Oracle Fusion Cloud {u['release']} · what to test","Baseline regression, switched-on changes, former opt-ins"))
def is_next(rel): return bool(UPCOMING and UPCOMING.get('tracked') and UPCOMING['release']==rel)
def render(updates, dist, upcoming=None, generated='', current=None):
    global NAV, NEXT_REL, UPCOMING, CURRENT
    UPCOMING=upcoming; CURRENT=current or sorted(updates)[-1]; UPD_KEYS[:]=list(updates)
    if upcoming: NEXT_REL=upcoming['release']
    OG_SPECS.clear()
    NAV=''.join((f'<a href="@{k.lower()}/">{k} (next)</a>' if is_next(k) else f'<a href="@updates/{k.lower()}/index.html">{k}{" (current)" if k==CURRENT else ""}</a>') for k in sorted(updates,reverse=True))
    if os.path.exists(dist): shutil.rmtree(dist)
    os.makedirs(dist); open(os.path.join(dist,'style.css'),'w').write(CSS)
    for k,u in updates.items():
        d=os.path.join(dist,'updates',k.lower()); os.makedirs(d)
        open(os.path.join(d,'index.html'),'w').write(update_page(u)); open(os.path.join(d,'checklist.html'),'w').write(checklist_page(u))
    order=sorted(updates, reverse=True)  # newest first, e.g. 26D > 26C > 26B; 27A > 26D
    cur=updates[CURRENT]; ck=CURRENT.lower()
    hi=sum(1 for i in cur['items'] if i['impact']=='high'); auto=sum(1 for i in cur['items'] if i['enablement'].startswith('Automatically'))
    hero=f"""<section class="current"><span class="tag">Current update</span><h2>Oracle Fusion Cloud {cur['release']}</h2>
<p class="lead">The current quarterly update. Start here: what changed, what switches on automatically, and which former opt-ins are now standard.</p>
<div class="stats"><div><b>{len(cur['items'])}</b><span>changes we track</span></div><div><b>{len(cur['expiring'])}</b><span>former opt-ins now standard across all Fusion modules: {E(exp_scope(cur['expiring'],cur['release']))}.</span></div><div><b>{hi}</b><span>tracked changes rated high impact</span></div><div><b>{auto}</b><span>tracked changes delivered switched on</span></div></div>
<p class="small">We track up to 25 changes per module family, out of {cur['total_features']} features (our count) in the {cur['release']} What's New documents for these modules. The opt-in figure is Oracle's own Current Opt-In Expirations list, which covers all Fusion modules, not only the ones we track.</p>
<p class="small">HCM is listed separately: Oracle announces HCM changes as Redwood default switches, not opt-in expirations. <a style="color:#ff8a70" href="{HCMR_PATH}">HCM pages switching to Redwood ({len(hr_items(cur['release']))} in {cur['release']}, {len([i for i in HCMR['items'] if hr_group(i['release'])=='26d'])} announced for 26D) →</a></p>
<p><a class="btn" href="updates/{ck}/index.html">Browse {cur['release']} changes →</a> <a class="btn alt" href="updates/{ck}/checklist.html">{cur['release']} what-to-test checklist →</a> <a class="btn alt" href="{ck}/former-opt-ins-now-standard/">{cur['release']} former opt-ins now standard →</a></p></section>"""
    prev=''.join(f"""<div class="card"><h3>Update {k}</h3><p class="muted">{len(updates[k]['items'])} changes we track · {updates[k]['total_features']} features in the What's New documents (our count) · {len(updates[k]['expiring'])} opt-ins expiring</p>
<p><a href="updates/{k.lower()}/index.html">Browse changes →</a><br><a href="updates/{k.lower()}/checklist.html">What to test →</a></p></div>""" for k in order if k<CURRENT)
    prevsec=f'<h2>Previous updates</h2><div class="cards">{prev}</div>' if prev else ''
    fams=sorted(set(i['family'] for u in updates.values() for i in u['items']))
    famlinks=''.join(f"<p><b>{E(FNAME[f])}:</b> "+' · '.join(f'<a href="{k.lower()}/{FSLUG[f]}/">{k}</a>' for k in order)+"</p>" for f in fams)
    upsec=f'<div class="box"><h3 style="margin-top:0">Coming next: {upcoming["release"]}</h3><p>Oracle has published its {upcoming["release"]} What\'s New documents. <a href="{upcoming["release"].lower()}/">Oracle Fusion {upcoming["release"]} opt-in expiration list and what to expect →</a></p></div>' if upcoming else ''
    if upcoming and is_next(upcoming['release']):
        nu=updates[upcoming['release']]; nk=nu['release'].lower(); bc=bucket_counts(nu['all'])
        upsec=(f'<div class="box"><h3 style="margin-top:0">Coming next: {nu["release"]}, what&#39;s new</h3><p>Oracle has published its {nu["release"]} What&#39;s New documents. Their Feature Summary tables list <b>{len(nu["all"])} features</b> across the modules we cover: {bc["on"]} on by default, {bc["pot"]} on by default with potential setup, {bc["setup"]} needing setup, {bc["opt"]} opt-in and {bc["other"]} needing another action, per Oracle&#39;s "Action to Enable" column. {len(nu["expiring"])} opt-ins also end with {nu["release"]}.</p>'
               f'<p>By module: '+' · '.join(f'<a href="{nk}/{FSLUG[f]}/">{E(FNAME[f])}</a> ({sum(1 for r in nu["all"] if r["family"]==f)})' for f in sorted(set(r['family'] for r in nu['all'])))+'</p>'
               f'<p><a class="btn" href="{nk}/">{nu["release"]}: what&#39;s new and the opt-in list →</a> <a class="btn alt" style="border:1px solid var(--line)" href="updates/{nk}/index.html">{nu["release"]} changes we track ({len(nu["items"])}) →</a> <a class="btn alt" style="border:1px solid var(--line)" href="updates/{nk}/checklist.html">{nu["release"]} what-to-test checklist →</a></p></div>')
    home=f"""<div class="hero"><h1>Every Oracle Fusion quarterly update, in plain English.</h1>
<p class="lead">What changed in Financials, Procurement, Supply Chain, Logistics, Project Management and HCM, what switches on automatically, which opt-ins are becoming standard features, and what to test before it hits production.</p></div>
{hero}{upsec}{prevsec}<div class="box"><h3 style="margin-top:0">Covered module families</h3>{famlinks}</div>{nl_form(latest=True)}"""
    open(os.path.join(dist,'index.html'),'w').write(page('Oracle Fusion Cloud quarterly update tracker',home,desc='Every Oracle Fusion Cloud quarterly update in plain English: what changed by module, what switches on automatically, former opt-ins now standard, and what to test.',path='',og=('Oracle Fusion Cloud quarterly updates',f"{cur['release']} now, {NEXT_REL} next: what changed and what to test"),head=jsonld({"@context":"https://schema.org","@graph":[{"@type":"WebSite","@id":BASE+"/#website","url":BASE+"/","name":SITE,"description":"Plain-English tracker of Oracle Fusion Cloud quarterly updates.","publisher":{"@id":BASE+"/#org"}},{"@type":"Organization","@id":BASE+"/#org","name":SITE,"url":BASE+"/","logo":BASE+"/logo.png","email":CONTACT}]})))
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
    # release hubs stay up after a release stops being "next" (e.g. /26d/ is linked from outside the site)
    for k in sorted(updates):
        if k>=HUB_FROM and not (upcoming and upcoming['release']==k):
            u=updates[k]; d=os.path.join(dist,k.lower()); os.makedirs(d,exist_ok=True)
            open(os.path.join(d,'index.html'),'w').write(upcoming_page(dict(release=k,tracked=True,books=u['books'],expiring=u['expiring']),updates)); extra.append(f"{k.lower()}/")
    if ISSUES:
        os.makedirs(os.path.join(dist,'newsletter'),exist_ok=True)
        open(os.path.join(dist,'newsletter','index.html'),'w').write(issues_index_page()); extra.append('newsletter/')
        for it in ISSUES:
            d=os.path.join(dist,'newsletter',it['slug']); os.makedirs(d,exist_ok=True)
            open(os.path.join(d,'index.html'),'w').write(issue_page(it)); extra.append(f"newsletter/{it['slug']}/")
    if HCMR['items']:
        d=os.path.join(dist,'hcm-redwood'); os.makedirs(d,exist_ok=True)
        open(os.path.join(d,'index.html'),'w').write(hcm_redwood_page(cur['release'])); extra.append(HCMR_PATH)
    import longtail; extra+=longtail.build(dist)  # long-tail SEO pages (growth plan tactic #3)
    d=os.path.join(dist,'downloads'); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w').write(downloads_page()); extra.append('downloads/')
    if os.path.exists(os.path.join(ASSETS,LEAD['pdf'])): extra.append(LEAD['pdf'])
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
    open(os.path.join(dist,'newsletter.html'),'w').write(page('Newsletter',desc='Free quarterly briefing on Oracle Fusion Cloud updates: the changes that matter by module, opt-in expirations and a test checklist.',path='newsletter.html',og=('Newsletter','One plain-English email per Oracle Fusion quarterly update'),top_form=False,body='<div class="hero"><h1>The quarterly briefing</h1><p class="lead">Before each Oracle Fusion update reaches your test environment: the changes that matter, by module, the opt-ins about to expire, and a ready-to-use test checklist. Free.</p>'+(f'<p><a class="btn alt" style="border:1px solid var(--line)" href="newsletter/{ISSUES[0]["slug"]}/">Read issue #{ISSUES[0]["number"]} →</a> <a href="newsletter/">All issues</a></p>' if ISSUES else '')+'</div>'+nl_form(top=True)))
    if SHOW_SPONSORS: open(os.path.join(dist,'sponsor.html'),'w').write(page('Sponsor',desc='Sponsor Fusion Updates to reach people who plan, test and run Oracle Fusion Cloud quarterly updates.',path='sponsor.html',body="""<div class="hero"><h1>Sponsor Fusion Updates</h1><p class="lead">Reach the people who plan, test and run Oracle Fusion Cloud updates: application owners, functional leads, testers and consultants across Financials, Procurement, SCM, Projects and HCM.</p></div>
<div class="cards"><div class="card"><h3>Newsletter sponsor</h3><p class="muted">One sponsor slot per quarterly briefing, sent before each update's test window.</p></div>
<div class="card"><h3>Update page sponsor</h3><p class="muted">"Presented by" placement on an update's change list and test checklist.</p></div>
<div class="card"><h3>Module sponsor</h3><p class="muted">Placement on one module family (e.g. Supply Chain or HCM) across updates.</p></div></div>
<div class="box"><p>Good fits: test automation, data loading and migration tools, Oracle partners and add-on vendors. Sponsors never influence summaries or ratings, and sponsored placements are always labeled.</p><p><b>Rates and audience numbers:</b> available on request. """+(f"Write to {contact_html()}." if CONTACT else '<span class="muted small">(Contact address to be added.)</span>')+"""</p></div>"""))
    open(os.path.join(dist,'about.html'),'w').write(page('About',desc='About Fusion Updates: an independent, plain-English tracker of Oracle Fusion Cloud quarterly updates, and how it is built.',path='about.html',body="""<div class="hero"><h1>About</h1><p class="lead">Fusion Updates (fusionupdates.com) turns Oracle's quarterly readiness documentation into a filterable, plain-English list of changes across Oracle Fusion Cloud, with impact ratings and a what-to-test checklist for every update.</p></div>
<div class="box"><p>It is run by an experienced Oracle consultant. Every entry links back to its Oracle source page. Summaries are condensed from Oracle's text, and impact ratings are editorial judgment, so always check the Oracle page and your own configuration.</p>
<p>This is an independent site, not affiliated with or endorsed by Oracle.</p><p class="small muted">Method: features come from the "Feature Summary" tables in Oracle's What's New documents. Enablement comes from Oracle's "Action to Enable" column plus the Current Opt-In Expirations list. Impact: high means users have to change how they work, or it's a large UI or process change, a former opt-in that becomes standard and affects users, or it touches payments, accounting, integrations or security. Medium means visible but contained, or switched on automatically and noticeable. Low means minor, cosmetic, reporting-only, or it needs setup before anyone gets it. Each rating is checked against Oracle's feature page (description, action to enable, scale and opt-in status).</p></div>"""))

    finish_assets(dist)

ASSETS=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'assets')
def finish_assets(dist):
    """Draw any new/changed OG cards into assets/og (cached), then copy assets/ (og/, downloads/) into dist."""
    import og as _og
    _og.generate(OG_SPECS, os.path.join(ASSETS,'og'))
    for sub in ('og','downloads'):
        src=os.path.join(ASSETS,sub)
        if os.path.isdir(src): shutil.copytree(src,os.path.join(dist,sub),dirs_exist_ok=True,ignore=shutil.ignore_patterns('manifest.json'))
def downloads_page():
    path='downloads/'; title='Free downloads: 26D readiness checklist and update calendar'
    cl=[('Home',''),('Free downloads',path)]
    pdf=LEAD['pdf'].split('/')[-1]; ics=LEAD['ics'].split('/')[-1]
    body=f"""{crumbs_html(cl,'../')}<div class="hero"><h1>Free downloads</h1><p class="lead">Two free files for planning the next Oracle Fusion quarterly update. Both are built from Oracle's published documents and link back to them. No signup needed, though subscribers get the next ones by email.</p></div>
<div class="box"><h2 style="margin-top:0">{LEAD['rel']} readiness checklist (PDF)</h2><p>A printable checklist for the {LEAD['rel']} update: the baseline regression checks, the opt-ins Oracle lists as ending with {LEAD['rel']}, the HCM pages that switch to Redwood by default in {LEAD['rel']} (with the profile option names Oracle gives), and links to Oracle's {LEAD['rel']} What's New documents.</p>
<p class="small muted">Oracle's {LEAD['rel']} What's New documents are still being revised, so treat this checklist as preliminary and confirm details on the linked Oracle pages.</p>
<p><a class="btn" href="{pdf}" download>Download the {LEAD['rel']} checklist (PDF)</a> <a href="../{LEAD['rel'].lower()}/">Or read the {LEAD['rel']} page on the site →</a></p></div>
<div class="box"><h2 style="margin-top:0">Fusion quarterly update calendar (.ics)</h2><p>Calendar entries for the 26D and 27A test and production update windows for cohorts A, B and C. Import it into Outlook, Google Calendar or Apple Calendar and delete the cohorts you're not in.</p>
<p class="small muted">Oracle publishes the rule rather than a public list of dates: test environments update on the first Friday of the update month and production on the third Friday (in Middle East regions, on the Thursday before). The dates in this file follow that rule and are labelled as typical. Your own dates are in the Oracle Cloud Console. Source: <a href="https://blogs.oracle.com/fusioninsider/quarterly-updates-made-easy" target=_blank rel=noopener>Oracle Fusion Insider, "Quarterly updates made easy"</a>.</p>
<p><a class="btn" href="{ics}" download>Download the calendar (.ics)</a></p></div>{nl_form()}"""
    ld=jsonld({"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":BASE+'/'+path,"url":BASE+'/'+path,"name":title,"inLanguage":"en","isPartOf":{"@type":"WebSite","@id":BASE+"/#website","name":SITE,"url":BASE+"/"}},crumbs(cl)]})
    return page(title,body,1,f"Free {LEAD['rel']} readiness checklist (PDF) and a Fusion quarterly update calendar (.ics) for 26D and 27A, built from Oracle's published documents.",path,ld,og=('Free downloads',f"{LEAD['rel']} readiness checklist (PDF) and update calendar (.ics)"))

# ---------------- SEO pages ----------------
FSLUG={'Financials':'financials','Procurement':'procurement','Supply Chain & Manufacturing':'supply-chain-manufacturing','Logistics (OTM/GTM/WMS)':'logistics','Project Management':'project-management','HCM':'hcm'}
FNAME={'Financials':'Financials','Procurement':'Procurement','Supply Chain & Manufacturing':'Supply Chain & Manufacturing','Logistics (OTM/GTM/WMS)':'Logistics (OTM, GTM, WMS)','Project Management':'Project Management','HCM':'HCM'}
# ---------------- Oracle Feature Summary rows, as Oracle states them ----------------
# Buckets follow Oracle's "Action to Enable" column only. Oracle's legend: features with an "Impact to Existing Processes"
# of None "are not delivered enabled"; Potential Setup means "there is prerequisite or optional configuration to consider".
BUCKETS=[('on','On by default','Action to Enable: None'),('pot','On by default, potential setup','Action to Enable: Potential Setup'),
         ('setup','Setup required','Action to Enable: Setup Required'),('opt','Opt-in','Action to Enable: Opt In, or Opt In plus Setup'),
         ('other','Other action required','Another action Oracle names, e.g. Visual Builder or Service Request Required')]
def bucket(action):
    if action=='None': return 'on'
    if action=='Potential Setup': return 'pot'
    if action=='Setup Required': return 'setup'
    if action.startswith('Opt In'): return 'opt'
    return 'other'
def bucket_counts(rows):
    c=collections.Counter(bucket(r['action']) for r in rows); return {k:c.get(k,0) for k,_,_ in BUCKETS}
BLABEL={k:l for k,l,_ in BUCKETS}
BCLS={'on':'e-auto','pot':'e-auto','opt':'e-exp'}
def bucket_sentence(rows):
    c=bucket_counts(rows)
    return f"{c['on']} on by default, {c['pot']} on by default with potential setup, {c['setup']} setup required, {c['opt']} opt-in" + (f", {c['other']} needing another action" if c['other'] else '')
def all_features_html(u,f):
    """Every row of Oracle's Feature Summary tables for one module family, grouped by Oracle product (What's New book)."""
    rows=[r for r in u.get('all',[]) if r['family']==f]
    if not rows: return ''
    rel=u['release']; byp=collections.OrderedDict()
    for r in rows: byp.setdefault(r['product'],[]).append(r)
    jump=' · '.join(f'<a href="#all-{n}">{E(p)} ({len(x)})</a>' for n,(p,x) in enumerate(byp.items()))
    out=(f'<div class="box" id="all-features"><h2 style="margin-top:0">All {len(rows)} {E(FNAME[f])} features in Oracle&#39;s {rel} What&#39;s New</h2>'
         f'<p class="small muted">Every row of the Feature Summary tables in Oracle&#39;s {rel} What&#39;s New documents for this area, with Oracle&#39;s own "Impact to Existing Processes" and "Action to Enable" columns as Oracle states them: {bucket_sentence(rows)}. Oracle&#39;s legend: features whose impact is "None" are not delivered enabled and need steps to use; "Potential Setup" means there is prerequisite or optional configuration to consider. Each title links to Oracle&#39;s feature page.</p>'
         f'<p class="small"><b>By product:</b> {jump}</p>')
    for n,(p,x) in enumerate(byp.items()):
        out+=(f'<h3 id="all-{n}" style="font-size:17px">{E(p)} ({len(x)})</h3><table><tr><th>Feature (Oracle title)</th><th>Module</th><th>Impact to Existing Processes</th><th>Action to Enable</th><th>Status</th></tr>'+
              ''.join(f'<tr><td><a href="{E(r["url"])}" target=_blank rel=noopener>{E(r["title"])}</a></td><td>{E(r["module"])}</td><td>{E(r["oracle_impact"])}</td><td>{E(r["action"])}</td><td><span class="pill {BCLS.get(bucket(r["action"]),"")}">{E(BLABEL[bucket(r["action"])])}</span></td></tr>' for r in x)+'</table>')
    return out+'</div>'
def unpub_note(u,f=None):
    x=[b['product'] for b in u.get('unpublished',[]) if f is None or b['family']==f]
    if not x: return ''
    return f'<p class="small muted">Oracle had not published {u["release"]} What&#39;s New documents for {E(_and(x))} when we last checked, so {"they are" if len(x)>1 else "it is"} not included yet. We check every week and add {"them" if len(x)>1 else "it"} once Oracle publishes.</p>'
def pillar_groups(es):
    """Opt-in expiration rows grouped by Oracle's own Pillar column (Oracle's grouping, not ours)."""
    g=collections.OrderedDict()
    for e in es: g.setdefault(e['pillar'] or 'Other',[]).append(e)
    return g
def jsonld(o): return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False).replace('</','<\\/')+'</script>'
def crumbs(lst): return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":n+1,"name":nm,"item":BASE+'/'+u} for n,(nm,u) in enumerate(lst)]}
def crumbs_html(lst,p): return '<p class="small muted">'+' › '.join(f'<a href="{p}{u}">{E(nm)}</a>' if n<len(lst)-1 else E(nm) for n,(nm,u) in enumerate(lst))+'</p>'
def item_html(i):
    return f"""<div class="item" data-family="{E(i['family'])}" data-product="{E(i['product'])}" data-impact="{i['impact']}" data-en="{E(i['enablement'])}" data-text="{E((i['title']+' '+i['summary']+' '+i['module']).lower())}">
<h4><a href="{E(i['url'])}" target="_blank" rel="noopener">{E(i['title'])}</a></h4>
<div class="meta"><span class="pill i-{i['impact']}">Impact: {i['impact']}</span><span class="pill {enc(i['enablement'])}">{E(i['enablement'])}</span><span class="pill">{E(i['family'])}</span><span class="pill">{E(i['product'])} · {E(i['module'])}</span>{'<span class="pill">'+E(i['tags'])+'</span>' if i.get('tags') else ''}</div>
<div>{E(i['summary']) or '<span class="muted">See the Oracle page for details.</span>'}</div>
<div class="small muted">Oracle's own impact label: {E(i['oracle_impact'])} · Action to enable: {E(i['action'])} · <a href="{E(i['url'])}" target="_blank" rel="noopener">Oracle source</a></div></div>"""
def exp_family(e):
    pl,pr=e['pillar'],e['product']
    if pl.startswith('Enterprise Resource'): return 'Project Management' if pr.startswith('Project') else 'Financials'
    if pl.startswith('Supply Chain'): return 'Procurement' if pr.startswith('Procurement') or 'Sourcing' in pr or 'Supplier' in pr else 'Supply Chain & Manufacturing'
    if pl.startswith('Human Capital') or pl=='HCM': return 'HCM'
    if 'Logistics' in pl: return 'Logistics (OTM/GTM/WMS)'
    return None
CORE_SHORT={'Financials':'Financials','Project Management':'Projects','Procurement':'Procurement','Supply Chain & Manufacturing':'Supply Chain','Logistics (OTM/GTM/WMS)':'Logistics','HCM':'HCM'}
def exp_other_label(e):
    return e['product'] if e['pillar']=='Industry' else e['pillar']
def _and(xs): return xs[0] if len(xs)==1 else ', '.join(xs[:-1])+' and '+xs[-1]
def exp_scope(es,rel):
    """Plain-English split of Oracle's opt-in expiration list: modules we track vs the rest."""
    core=[e for e in es if exp_family(e)]
    have={CORE_SHORT.get(exp_family(e),exp_family(e)) for e in core}
    areas=[a for a in CORE_SHORT.values() if a in have]
    cl=_and(areas) if areas else ''
    oth=collections.OrderedDict()
    for e in es:
        if not exp_family(e): oth.setdefault(exp_other_label(e),[]).append(e)
    if not oth: return f"all {len(es)} across {cl}" if core else ''
    parts=([f"{len(core)} across {cl}"] if core else [])+[f"{len(x)} in {k}" for k,x in oth.items()]
    return ', '.join(parts)
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
    nxt=is_next(rel); allf=[r for r in u.get('all',[]) if r['family']==f]
    title=f"Oracle Fusion {fn} {rel}: what's new" if nxt else f"Oracle Fusion {fn} {rel}: what changed"
    desc=f"What changed in Oracle Fusion {fn} {rel}, in plain English: {len(its)} changes we track, {len(auto)} delivered switched on, and {len(exps)} former opt-in{'s' if len(exps)!=1 else ''} now standard. Every item links to Oracle's docs."
    if nxt: desc=f"What's new in Oracle Fusion {fn} {rel}: all {len(allf)} features in Oracle's {rel} What's New, {bucket_sentence(allf)} per Oracle, plus {len(its)} changes in plain English. Every item links to Oracle's docs."
    path=f"{rk}/{fn and FSLUG[f]}/"
    cl=[('Home',''),(f'{rel}',f'{rk}/' if nxt else f'updates/{rk}/'),(fn,path)]
    others=' · '.join(f'<a href="../{FSLUG[g]}/">{E(FNAME[g])}</a>' for g in sorted(set(i['family'] for i in u['items'])) if g!=f)
    otherrel=' · '.join(f'<a href="../../{k.lower()}/{FSLUG[f]}/">{fn} {k}</a>' for k in sorted(updates,reverse=True) if k!=rel and any(i['family']==f for i in updates[k]['items']))
    booklinks=' · '.join(f'<a href="{E(b["url"])}" target=_blank rel=noopener>{E(b["product"])} {rel} What\'s New</a>' for b in books)
    body=f"""{crumbs_html(cl,'../../')}<div class="hero"><h1>{E(title)}</h1>
{f'<p class="lead">{rel} is the next Oracle Fusion Cloud quarterly update. Oracle&#39;s {rel} What&#39;s New documents for this area list {len(allf)} features: {bucket_sentence(allf)}, per Oracle&#39;s "Action to Enable" column. <a href="#all-features">See all {len(allf)} →</a></p>' if nxt and allf else ''}<p class="lead">We track {len(its)} {E(fn)} changes in {rel}{f', out of {tot} features (our count) in Oracle&#39;s {rel} What&#39;s New documents for this area' if tot else ''}. {len(auto)} of them are delivered switched on; {len(rest)} need setup or an opt-in before anyone can use them.</p>
<p class="small muted">Oracle sources: {booklinks}</p>{unpub_note(u,f) if nxt else ''}<p class="note">Impact ratings are our editorial view of how much a change affects day-to-day users and testing. Always confirm details on the linked Oracle page.</p></div>
<div class="box"><h2 style="margin-top:0">Former opt-ins now standard in {rel}</h2><p class="small muted">From Oracle's <a href="https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html" target=_blank rel=noopener>Current Opt-In Expirations</a> list: features whose opt-in period {'ends' if nxt else 'ended'} with {rel}. If you already opted in and finished setup, nothing changes.{' Oracle&#39;s list groups these under its own Pillar column; here they are shown by product.' if exps else ''} <a href="../former-opt-ins-now-standard/">All former opt-ins now standard in {rel} →</a></p>{exp_table(exps)}</div>
{hr_box(rel,'../../') if f=='HCM' else ''}<h2>Delivered switched on ({len(auto)})</h2>{''.join(item_html(i) for i in auto) or '<p class="muted">None among the changes we track.</p>'}
<h2>Needs setup or opt-in ({len(rest)})</h2>{''.join(item_html(i) for i in rest) or '<p class="muted">None among the changes we track.</p>'}
{all_features_html(u,f)}
<div class="box"><p><b>More {rel}:</b> {f'<a href="../">{rel} hub: what&#39;s new and the opt-in list</a> · ' if nxt else ''}<a href="../../updates/{rk}/">All {len(u['items'])} tracked {rel} changes</a> · <a href="../../updates/{rk}/checklist.html">{rel} what-to-test checklist</a> · <a href="../former-opt-ins-now-standard/">{rel} former opt-ins now standard</a></p><p><b>Other module families in {rel}:</b> {others}</p>{f'<p><b>Other releases:</b> {otherrel}</p>' if otherrel else ''}</div>{nl_form()}"""
    ld=jsonld({"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":BASE+'/'+path,"url":BASE+'/'+path,"name":title,"description":desc,"inLanguage":"en","isPartOf":{"@type":"WebSite","@id":BASE+"/#website","name":SITE,"url":BASE+"/"},"about":{"@type":"SoftwareApplication","name":f"Oracle Fusion Cloud {fn}","softwareVersion":rel,"applicationCategory":"BusinessApplication"},"dateModified":None},
        crumbs(cl),{"@type":"ItemList","name":f"{fn} {rel} changes we track","numberOfItems":len(its),"itemListElement":[{"@type":"ListItem","position":n+1,"name":i['title'],"url":i['url']} for n,i in enumerate(its)]}]})
    ld=ld.replace(',"dateModified":null','')
    return page(title,body,2,desc,path,ld,og=(f"Oracle Fusion Cloud {rel} · {fn}",(f"{len(allf)} features in Oracle's {rel} What's New, with Oracle's status" if nxt and allf else f"{len(its)} changes we track · {len(auto)} delivered switched on")))
def standard_page(u):
    rel=u['release']; rk=rel.lower(); es=u['expiring']
    on=sum(1 for e in es if e['now_enabled']=='Yes'); st=len(es)-on
    grp=collections.OrderedDict((f"Oracle pillar: {k}",x) for k,x in pillar_groups(es).items())
    oth=[e for e in es if exp_family(e) is None]
    core=len(es)-len(oth)
    title=f"Oracle Fusion {rel}: former opt-ins now standard"
    desc=f"The {len(es)} Oracle Fusion features, across all modules, whose opt-in period ended with {rel}, from Oracle's opt-in expiration list: {on} switched on automatically, {st} need setup if you want them. Plain English, with Oracle links."
    path=f"{rk}/former-opt-ins-now-standard/"; cl=[('Home',''),(rel,f'updates/{rk}/'),('Former opt-ins now standard',path)]
    faq=standard_faq(u)
    body=f"""{crumbs_html(cl,'../../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">Oracle's <a href="https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html" target=_blank rel=noopener>Current Opt-In Expirations</a> list names {len(es)} features whose opt-in period ended with {rel}. They are now standard: {on} are switched on automatically, and {st} need setup if you want to use them.{f' By area: {E(exp_scope(es,rel))}.' if es else ''}</p>
<p class="small muted">HCM changes are not on this list: Oracle announces them as Redwood default switches. See <a href="../../{HCMR_PATH}">HCM pages switching to Redwood</a>.</p>
<p class="small muted">Oracle's note: if you already opted in and finished the setup, nothing changes for you. "Now enabled" and "Oracle's impact" are Oracle's own columns, and the groups below follow Oracle's own Pillar column.</p></div>
{''.join(f'<div class="box"><h2 style="margin-top:0">{E(g)} ({len(x)})</h2>{exp_table(x)}</div>' for g,x in grp.items())}
{faq_html(faq)}<div class="box"><p><b>More {rel}:</b> <a href="../../updates/{rk}/">All tracked {rel} changes</a> · <a href="../../updates/{rk}/checklist.html">{rel} what-to-test checklist</a> · {' · '.join(f'<a href="../{FSLUG[f]}/">{E(FNAME[f])} {rel}</a>' for f in sorted(set(i['family'] for i in u['items'])))}</p></div>{nl_form()}"""
    ld=jsonld({"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":BASE+'/'+path,"url":BASE+'/'+path,"name":title,"description":desc,"inLanguage":"en","isPartOf":{"@type":"WebSite","@id":BASE+"/#website","name":SITE,"url":BASE+"/"}},crumbs(cl),
        {"@type":"ItemList","name":title,"numberOfItems":len(es),"itemListElement":[{"@type":"ListItem","position":n+1,"name":e['title'],"url":e['url']} for n,e in enumerate(es) if e['url']]},faq_ld(faq)]})
    return page(title,body,2,desc,path,ld,og=(f"Oracle Fusion Cloud {rel}",f"{len(es)} former opt-ins now standard, with Oracle links"))
NEXTREL={'26B':'26C','26C':'26D','26D':'27A','27A':'27B'}
def standard_faq(u):
    """FAQ for a former-opt-ins page: (question, answer HTML) built only from Oracle's opt-in list and the site's data."""
    rel=u['release']; es=u['expiring']; on=sum(1 for e in es if e['now_enabled']=='Yes'); st=len(es)-on
    nx=NEXTREL.get(rel); OL='<a href="https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html">Current Opt-In Expirations</a>'
    q=[(f"What does \"former opt-in now standard\" mean in {rel}?",
        f"Oracle first delivered these features as opt-ins: you had to choose to switch them on. Oracle's {OL} list names {rel} as the update where that opt-in step is removed, so from {rel} they are part of the standard product."),
       (f"How many features stopped being opt-in with {rel}?",
        f"{len(es)}, according to Oracle's list. {on} are switched on for all users (Oracle's \"Now enabled\" column says Yes), and {st} need setup before anyone can use them."),
       (f"Which modules do the {rel} former opt-ins cover?", E(exp_scope(es,rel)[0:1].upper()+exp_scope(es,rel)[1:])+"." if es else "None are listed."),
       ("Do I need to do anything if I already opted in?","No. Oracle says that if you opted in earlier and completed the setup, no further action is needed."),
       (f"What happens to the {st} features that need setup?","Nothing changes for your users until you do the setup. If you want to use one, follow the steps on its linked Oracle page."),
       (f"Why are there no HCM features in the {rel} list?",f"Oracle's opt-in expiration list doesn't cover HCM. Oracle announces HCM changes as pages switching to Redwood by default instead. See <a href=\"{BASE}/{HCMR_PATH}\">HCM pages switching to Redwood</a>.")]
    if nx=='26D' and UPCOMING and UPCOMING['release']==nx:
        q.append((f"Which opt-ins end with {nx}?",f"Oracle's list names {len(UPCOMING['expiring'])} features whose opt-in ends with {nx}. See the <a href=\"{BASE}/{nx.lower()}/\">{nx} opt-in expiration list, in plain English</a>."))
    return q
def faq_html(faq):
    return '<div class="box" id="faq"><h2 style="margin-top:0">Frequently asked questions</h2>'+''.join(f'<h3 style="font-size:17px;margin:16px 0 4px">{E(qq)}</h3><p style="margin:0">{a}</p>' for qq,a in faq)+'</div>'
def faq_ld(faq):
    import re as _re
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":qq,"acceptedAnswer":{"@type":"Answer","text":html.unescape(_re.sub(r'<[^>]+>','',a))}} for qq,a in faq]}
def upcoming_page(up,updates):
    rel=up['release']; rk=rel.lower(); es=up['expiring']
    on=sum(1 for e in es if e['now_enabled']=='Yes'); st=len(es)-on
    byf=collections.defaultdict(list)
    for b in up['books']: byf[FNAME.get(b['family'],b['family'])].append(b)
    ann=[i for k in updates for i in updates[k]['items'] if rel in i['title']]
    grp=collections.OrderedDict((f"Oracle pillar: {k}",x) for k,x in pillar_groups(es).items())
    tu=updates.get(rel) if up.get('tracked') else None
    title=f"Oracle Fusion {rel} opt-in expiration list, in plain English"
    desc=f"The {len(es)} Oracle Fusion features whose opt-in ends with {rel}, in plain English: {on} switched on for everyone, {st} need setup if you want them. Grouped by module with Oracle links, plus what else to expect in {rel}."
    path=f"{rk}/"; cl=[('Home',''),(f'{rel} opt-in expiration list',path)]
    wn=''
    if tu:
        allr=tu['all']; fams=[f for f in FSLUG if any(r['family']==f for r in allr)]
        title=f"Oracle Fusion {rel}: what's new by module, and the opt-in expiration list"
        desc=f"What's new in Oracle Fusion {rel}: all {len(allr)} features in Oracle's {rel} What's New for Financials, Procurement, SCM, Projects and HCM, with Oracle's enablement status, plus the {len(es)} opt-ins that end with {rel}."
        cl=[('Home',''),(rel,path)]
        def _row(f):
            x=[r for r in allr if r['family']==f]; c=bucket_counts(x)
            return f'<tr><td><a href="{FSLUG[f]}/">{E(FNAME[f])} {rel}</a></td><td>{len(x)}</td><td>{c["on"]}</td><td>{c["pot"]}</td><td>{c["setup"]}</td><td>{c["opt"]}</td><td>{c["other"]}</td></tr>'
        tc=bucket_counts(allr)
        wn=(f'<div class="box" id="whats-new"><h2 style="margin-top:0">What&#39;s new in {rel}, by module ({len(allr)} features)</h2>'
            f'<p class="small muted">Counts of the rows in the Feature Summary tables of Oracle&#39;s {rel} What&#39;s New documents, by Oracle&#39;s "Action to Enable" column. Each module page lists every feature with Oracle&#39;s own columns and a link to Oracle&#39;s feature page, plus the changes we summarise in plain English.</p>'
            '<table><tr><th>Module family</th><th>Features</th><th>On by default</th><th>On by default, potential setup</th><th>Setup required</th><th>Opt-in</th><th>Other action</th></tr>'+''.join(_row(f) for f in fams)+
            f'<tr><td><b>Total</b></td><td><b>{len(allr)}</b></td><td><b>{tc["on"]}</b></td><td><b>{tc["pot"]}</b></td><td><b>{tc["setup"]}</b></td><td><b>{tc["opt"]}</b></td><td><b>{tc["other"]}</b></td></tr></table>'
            f'<p class="small muted">"On by default" = Action to Enable: None. "Potential setup" = Oracle flags prerequisite or optional configuration to consider. "Other action" = an action such as Visual Builder or Service Request Required, shown on each module page.</p>'+unpub_note(tu)+
            f'<p><a class="btn" href="../updates/{rk}/index.html">{rel} changes in plain English ({len(tu["items"])}) →</a> <a class="btn alt" style="border:1px solid var(--line)" href="../updates/{rk}/checklist.html">{rel} what-to-test checklist →</a> <a class="btn alt" style="border:1px solid var(--line)" href="#opt-ins">{rel} opt-in expiration list ({len(es)}) →</a></p></div>')
    hr=[i for i in HCMR['items'] if hr_group(i['release'])==rk]
    import longtail
    hcm=(f'<div class="box"><h2 style="margin-top:0">HCM in {rel}: Redwood default switches instead</h2><p>HCM isn&#39;t on Oracle&#39;s opt-in expiration list. Oracle announces HCM changes as pages switching to Redwood by default; {len(hr)} are announced for {rel}. '
         f'<a href="../{HCMR_PATH}#r{rk}">All HCM changes for {rel} →</a></p>'+(longtail.hcm_links('../').replace('<div class="box">','<div>',1) if rel=='26D' else '')+'</div>') if hr else ''
    optlead=f"""Oracle&#39;s <a href="https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html" target=_blank rel=noopener>Current Opt-In Expirations</a> list names {len(es)} features whose opt-in period ends with the {rel} update. From {rel} they are standard features: {on} are switched on for everyone, and {st} need setup before anyone can use them.{f' By area: {E(exp_scope(es,rel))}.' if es else ''}"""
    if tu:
        hero=f"""<p class="lead">{rel} {'is the next' if is_next(rel) else ('is the current' if rel==CURRENT else 'was an')} Oracle Fusion Cloud quarterly update. Oracle&#39;s {rel} What&#39;s New documents list {len(tu['all'])} features across the modules we cover: {bucket_sentence(tu['all'])}, per Oracle&#39;s "Action to Enable" column. <a href="#whats-new">See them by module →</a></p>
<p class="lead">{optlead} <a href="#opt-ins">See the opt-in list →</a></p>
<p class="small muted">Oracle can revise its {rel} documents and this list, and we recheck them every week.</p></div>{wn}
<div id="opt-ins"><h2>{rel} opt-in expiration list ({len(es)})</h2></div>"""
    else:
        hero=f"""<p class="lead">{optlead}</p>
<p class="small muted">{rel} is the next Oracle Fusion Cloud quarterly update. Oracle can update this list, and we recheck it every week.</p></div>"""
    body=f"""{crumbs_html(cl,'../')}<div class="hero"><h1>{E(title)}</h1>
{hero}
<div class="box"><h2 style="margin-top:0">What this means, in plain English</h2><ul>
<li><b>An opt-in expiration</b> means Oracle first delivered the feature as something you had to opt in to. With the update in Oracle&#39;s list, the opt-in step is removed and the feature becomes part of the standard product.</li>
<li><b>"Now enabled: Yes"</b> ({on} here): the feature is on for all users from {rel}. Nothing to switch on, but test it, because users will see it.</li>
<li><b>"Now enabled: No"</b> ({st} here): nothing changes for users until you do the setup on the linked Oracle page.</li>
<li><b>Already opted in?</b> Per Oracle, if you opted in earlier and finished the setup, there&#39;s nothing more to do.</li>
<li><b>Grouping:</b> the groups below follow Oracle&#39;s own Pillar column. For example, Oracle lists Supplier Registration (product: Procurement Common) under Supply Chain &amp; Manufacturing.</li></ul></div>
{''.join(f'<div class="box"><h2 style="margin-top:0">{E(g)} ({len(x)})</h2>{exp_table(x)}</div>' for g,x in grp.items()) or '<p class="muted">None in Oracle&#39;s list.</p>'}
{hcm}
<h2>What else to expect in {rel}</h2>
<div class="box"><h3 style="margin-top:0">When it arrives</h3><p>Oracle updates environments in cohorts. Per Oracle, Cohort A gets quarterly updates in February, May, August and November, Cohort B in March, June, September and December, and Cohort C in April, July, October and January. Test environments update on the first Friday of the update month and production two weeks later, on the third Friday. Your cohort is shown in the Oracle Cloud Console. <span class="small muted">Source: <a href="https://blogs.oracle.com/fusioninsider/quarterly-updates-made-easy" target=_blank rel=noopener>Oracle Fusion Insider, "Quarterly updates made easy"</a></span></p></div>
<div class="box"><h3 style="margin-top:0">Oracle's {rel} What's New documents</h3><p class="small muted">{'Oracle has published them. Every feature in their Feature Summary tables is listed on our module pages above.' if tu else f"Oracle has published them. We haven't added {rel} to the tracker yet; plain-English summaries follow."}</p>{''.join(f'<p><b>{E(g)}:</b> '+' · '.join(f'<a href="{E(b["url"])}" target=_blank rel=noopener>{E(b["product"])}</a>' for b in bs)+'</p>' for g,bs in byf.items())}</div>
{f'<div class="box"><h3 style="margin-top:0">Already announced for {rel} in earlier What&#39;s New documents</h3><ul>'+''.join(f'<li><a href="{E(i["url"])}" target=_blank rel=noopener>{E(i["title"])}</a> <span class="small muted">({E(i["product"])}, from the {i["_rel"]} What&#39;s New)</span></li>' for i in ann)+'</ul></div>' if ann else ''}{nl_form()}"""
    ld=jsonld({"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":BASE+'/'+path,"url":BASE+'/'+path,"name":title,"description":desc,"inLanguage":"en","isPartOf":{"@type":"WebSite","@id":BASE+"/#website","name":SITE,"url":BASE+"/"}},crumbs(cl),
        {"@type":"ItemList","name":f"Oracle Fusion opt-ins ending with {rel}","numberOfItems":len(es),"itemListElement":[{"@type":"ListItem","position":n+1,"name":e['title'],"url":e['url']} for n,e in enumerate(es) if e['url']]}]})
    return page(title,body,1,desc,path,ld,og=((f"Next update · {rel}" if (is_next(rel) or not tu) else f"Oracle Fusion Cloud {rel}"),(f"What's new: {len(tu['all'])} features by module, with Oracle's status · {len(es)} opt-ins end" if tu else f"{len(es)} opt-ins end with {rel}: {on} switched on, {st} need setup")))

# ---------------- HCM pages switching to Redwood ----------------
_HR=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'data','hcm_redwood.json')
HCMR=json.load(open(_HR)) if os.path.exists(_HR) else {'items':[],'checked':''}
HCMR_PATH='hcm-redwood/'
HR_TYPE={'Redwood by default':'Switches to Redwood by default','End of support':'End of support','Mandatory migration':'Migration','Removal':'Removal','Switched on automatically':'Switches on automatically'}
def hr_group(rel):
    return 'later' if rel>='27A' else rel.lower()
def hr_items(rel): return [i for i in HCMR['items'] if hr_group(i['release'])==hr_group(rel)]
HR_NOTE="Oracle announces these HCM changes in its HCM What's New documents as Redwood default switches (and a few end-of-support, migration or removal notices), not as opt-in expirations. They are not on Oracle's Current Opt-In Expirations list and are not part of the former opt-ins counts on this site."
def hr_item_html(i,check=False):
    src=' · '.join(f'<a href="{E(u)}" target=_blank rel=noopener>Oracle source{(" "+str(n+1)) if len(i["urls"])>1 else ""}</a>' for n,u in enumerate(i['urls']))
    ot=f'<p class="small muted">Oracle&#39;s title: &ldquo;{E(i["oracle_title"])}&rdquo;</p>' if i.get('oracle_title') else ''
    pg=', '.join(i['pages'])
    po=f'<p class="small muted">Profile options named on Oracle&#39;s page: <code style="font-size:12px">{"</code>, <code style=\"font-size:12px\">".join(E(c) for c in i["profile_options"])}</code></p>' if i.get('profile_options') and i['type']=='Redwood by default' else ''
    head=f'<label><input type=checkbox> {E(i["title"])}</label>' if check else E(i['title'])
    return (f'<div class="item"><h4>{head}</h4><div class="meta"><span class="pill">{E(i["area"])}</span><span class="pill e-auto">{E(HR_TYPE.get(i["type"],i["type"]))}</span>'
            f'<span class="pill">From {E(i["release"])}</span><span class="pill">Revert: {E(i["revert"])}</span></div>'
            f'<p style="margin:4px 0">{E(i["summary"])}</p><p class="small muted">Pages affected: {E(pg)}</p>{po}{ot}<p class="small">{src}</p></div>')
def hr_counts():
    c=collections.Counter(hr_group(i['release']) for i in HCMR['items']); return c
def hcm_redwood_page(cur_rel):
    c=hr_counts()
    groups=[('26b','26B'),('26c','26C'),('26d','26D'),('later','27A and later')]
    groups=[(g,lbl) for g,lbl in groups if c.get(g)]
    lab=lambda g,lbl: lbl+(' (current update)' if lbl==cur_rel else (' (next update, already announced)' if g=='26d' and cur_rel=='26C' else ''))
    title='Oracle Fusion HCM: pages switching to Redwood'
    desc=f"Oracle Fusion HCM pages that switch to Redwood by default in 26B, 26C, 26D and 27A, plus related end-of-support notices, in plain English with Oracle links: {len(HCMR['items'])} changes."
    cl=[('Home',''),('HCM pages switching to Redwood',HCMR_PATH)]
    jump=' · '.join(f'<a href="#r{g}">{E(lbl)} ({c[g]})</a>' for g,lbl in groups)
    secs=''.join(f'<h2 id="r{g}">{E(lab(g,lbl))} <span class="muted small">({c[g]})</span></h2>'+''.join(hr_item_html(i) for i in HCMR['items'] if hr_group(i['release'])==g) for g,lbl in groups)
    body=f"""{crumbs_html(cl,'../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">HCM pages that switch to Redwood by default, by release, with the other HCM end-of-support and removal notices Oracle has published. Where Oracle says so, you can still set the profile option back to No.</p>
<p class="small muted">{E(HR_NOTE)} Checked against each Oracle page on {E(HCMR.get('checked',''))}.</p>
<p class="note">Impact ratings are our editorial view of how much a change affects day-to-day users and testing. Always confirm details on the linked Oracle page.</p>
<p><b>Jump to:</b> {jump}</p></div>{__import__('longtail').hcm_links('../')}{secs}
<div class="box"><p><b>More HCM:</b> {' · '.join(f'<a href="../{k}/hcm/">HCM {k.upper()} changes we track</a>' for k in [r.lower() for r in sorted(UPD_KEYS,reverse=True)])} · <a href="../updates/{cur_rel.lower()}/checklist.html">{cur_rel} what-to-test checklist</a></p></div>{nl_form()}"""
    ld=jsonld({"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":BASE+'/'+HCMR_PATH,"url":BASE+'/'+HCMR_PATH,"name":title,"description":desc,"inLanguage":"en","isPartOf":{"@type":"WebSite","@id":BASE+"/#website","name":SITE,"url":BASE+"/"}},crumbs(cl),
        {"@type":"ItemList","name":title,"numberOfItems":len(HCMR['items']),"itemListElement":[{"@type":"ListItem","position":n+1,"name":i['title'],"url":i['urls'][0]} for n,i in enumerate(HCMR['items'])]}]})
    return page(title,body,1,desc,HCMR_PATH,ld,og=('HCM · Redwood',f"{len(HCMR['items'])} HCM changes, 26B to 27A, with Oracle links"))
def hr_box(rel,depth_prefix,check=False):
    its=hr_items(rel)
    nxt={'26C':'26d'}.get(rel); nn=len([i for i in HCMR['items'] if hr_group(i['release'])==nxt]) if nxt else 0
    if not its and not nn: return ''
    more=f' {nn} more are already announced for {nxt.upper()}.' if nn else ''
    lst=''.join(hr_item_html(i,check) for i in its) or '<p class="muted">None announced for this release.</p>'
    return (f'<div class="box" id="hcm-redwood"><h2 style="margin-top:0">HCM: pages switching to Redwood in {rel} ({len(its)})</h2>'
            f'<p class="small muted">{E(HR_NOTE)}{more} <a href="{depth_prefix}{HCMR_PATH}#r{rel.lower()}">All HCM pages switching to Redwood →</a></p>{lst}</div>')

# ---------------- Newsletter archive (web copies written by the newsletter build) ----------------
_ID=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'newsletter','issues')
ISSUES=sorted([json.load(open(os.path.join(_ID,f))) for f in os.listdir(_ID) if f.endswith('.json')],key=lambda i:-i['number']) if os.path.isdir(_ID) else []
def issue_page(it):
    path=f"newsletter/{it['slug']}/"; title=it['subject']
    cl=[('Home',''),('Newsletter','newsletter/'),(f"Issue #{it['number']}",path)]
    body=f"""{crumbs_html(cl,'../../')}<p class="small muted" style="margin-top:24px">Fusion Updates newsletter · Issue #{it['number']} · {E(it['date_label'])} · <a href="../">All issues</a></p>
{nl_compact(*cta_for(path))}
<div class="box" style="padding:0;max-width:760px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="color:#14202b">{it['body_html']}<tr><td style="padding:0 28px 24px"></td></tr></table></div>
<p class="note">Summaries are condensed from Oracle's public readiness documentation. Always confirm details on the linked Oracle page. Questions or a change we missed: <a href="mailto:{CONTACT}">{CONTACT}</a></p>
{nl_form()}"""
    ld=jsonld({"@context":"https://schema.org","@graph":[{"@type":"Article","@id":BASE+'/'+path,"url":BASE+'/'+path,"headline":title,"description":it['preheader'],"datePublished":it['date'],"inLanguage":"en","publisher":{"@id":BASE+"/#org"},"isPartOf":{"@type":"WebSite","@id":BASE+"/#website","name":SITE,"url":BASE+"/"}},crumbs(cl)]})
    return page(title,body,2,it['preheader'],path,ld,og=(f"Newsletter · Issue #{it['number']}",f"Oracle Fusion {it['release']} · {it['date_label']}"),top_form=False)
def issues_index_page():
    path='newsletter/'; title='Fusion Updates newsletter: all issues'
    cl=[('Home',''),('Newsletter',path)]
    lst=''.join(f'<div class="item"><h4><a href="{it["slug"]}/">Issue #{it["number"]}: {E(it["subject"])}</a></h4><p class="small muted" style="margin:2px 0">{E(it["date_label"])} · Oracle Fusion {E(it["release"])}</p><p style="margin:4px 0">{E(it["preheader"])}</p></div>' for it in ISSUES)
    body=f"""{crumbs_html(cl,'../')}<div class="hero"><h1>{E(title)}</h1><p class="lead">Past issues of the quarterly briefing on Oracle Fusion Cloud updates. Subscribe to get the next one by email.</p></div>{lst}{nl_form()}"""
    ld=jsonld({"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","@id":BASE+'/'+path,"url":BASE+'/'+path,"name":title,"inLanguage":"en","isPartOf":{"@type":"WebSite","@id":BASE+"/#website","name":SITE,"url":BASE+"/"}},crumbs(cl)]})
    return page(title,body,1,'Archive of the Fusion Updates quarterly newsletter on Oracle Fusion Cloud updates.',path,ld,og=('Newsletter','All issues of the quarterly briefing'))

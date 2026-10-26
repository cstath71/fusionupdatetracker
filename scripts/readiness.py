"""Release-readiness pages (growth plan, Days 1-30: release-readiness content for ERP and HCM admins).
Cross-module views of the rows in Oracle's Feature Summary tables (data/updates.json 'all'), as Oracle states them:
  /<rel>/opt-in-features/   every feature whose Action to Enable is Opt In or Opt In plus Setup
  /<rel>/on-by-default/     every feature whose Action to Enable is None (Oracle delivers it ready to use)
  /<rel>/redwood-erp-scm/   every feature outside HCM with "Redwood" in Oracle's title
Nothing here is our own rating: titles, modules, Impact to Existing Processes and Action to Enable are Oracle's columns.
Called from render.render(); returns the sitemap paths it wrote."""
import os, collections
import render as R
E=R.E
FAM_ORDER=list(R.FSLUG)
def _ext(u,t): return f'<a href="{E(u)}" target=_blank rel=noopener>{E(t)}</a>'
def _by_family(rows):
    g=collections.OrderedDict()
    for f in FAM_ORDER:
        x=[r for r in rows if r['family']==f]
        if x: g[f]=x
    return g
def _table(rows,show_status=True):
    h='<table><tr><th>Feature (Oracle title)</th><th>Product · module</th><th>Oracle scale (Impact to Existing Processes)</th><th>Action to Enable</th></tr>'
    return h+''.join(f'<tr><td>{_ext(r["url"],r["title"])}</td><td>{E(r["product"])} · {E(r["module"])}</td><td>{E(r["oracle_impact"])}</td><td><span class="pill {R.BCLS.get(R.bucket(r["action"]),"")}">{E(r["action"])}</span></td></tr>' for r in rows)+'</table>'
def _groups(rows,rel,depth):
    g=_by_family(rows)
    jump=' · '.join(f'<a href="#f-{R.FSLUG[f]}">{E(R.FNAME[f])} ({len(x)})</a>' for f,x in g.items())
    out=f'<p class="small"><b>Jump to:</b> {jump}</p>'
    for f,x in g.items():
        out+=(f'<div class="box" id="f-{R.FSLUG[f]}"><h2 style="margin-top:0">{E(R.FNAME[f])} ({len(x)})</h2>{_table(x)}'
              f'<p class="small"><a href="{depth}{rel.lower()}/{R.FSLUG[f]}/">All {E(R.FNAME[f])} features in {rel}, with plain-English summaries →</a></p></div>')
    return out
def _counts(rows): return R._and([f'{len(x)} in {R.FNAME[f]}' for f,x in _by_family(rows).items()])
def _src(u,rows=None):
    fams={r['family'] for r in rows} if rows else None
    bs=[b for b in u['books'] if fams is None or b['family'] in fams]
    return '<p class="small muted">Oracle sources: '+' · '.join(_ext(b['url'],f"{b['product']} {u['release']} What's New") for b in bs)+'</p>'
def _related(rel,cur,depth='../../'):
    P={'opt-in-features/':f'{rel} opt-in features','on-by-default/':f'{rel} features on by default','redwood-erp-scm/':f'{rel} Redwood changes outside HCM'}
    lk=' · '.join(f'<a href="{depth}{rel.lower()}/{p}">{E(n)}</a>' for p,n in P.items() if p!=cur)
    return (f'<div class="box"><p><b>More {rel} readiness:</b> {lk} · <a href="{depth}{rel.lower()}/">{rel} what&#39;s new by module and opt-in expiration list</a> · '
            f'<a href="{depth}updates/{rel.lower()}/checklist.html">{rel} what-to-test checklist</a> · <a href="{depth}{R.HCMR_PATH}">HCM pages switching to Redwood</a></p></div>')
def _ld(path,title,desc,cl,rows,faq):
    g=[{"@type":"WebPage","@id":R.BASE+'/'+path,"url":R.BASE+'/'+path,"name":title,"description":desc,"inLanguage":"en",
        "isPartOf":{"@type":"WebSite","@id":R.BASE+"/#website","name":R.SITE,"url":R.BASE+"/"}},R.crumbs(cl),
       {"@type":"ItemList","name":title,"numberOfItems":len(rows),"itemListElement":[{"@type":"ListItem","position":n+1,"name":r['title'],"url":r['url']} for n,r in enumerate(rows)]}]
    if faq: g.append(R.faq_ld(faq))
    return R.jsonld({"@context":"https://schema.org","@graph":g})
LEGEND=('<p class="small muted">Every row comes from the Feature Summary tables in Oracle&#39;s {rel} What&#39;s New documents, with Oracle&#39;s own "Impact to Existing Processes" and "Action to Enable" columns as Oracle states them. '
        'Each title links to Oracle&#39;s feature page. Oracle can revise its documents; we recheck them every week. Always confirm on the linked Oracle page.</p>')

def opt_in_page(u):
    rel=u['release']; rk=rel.lower(); rows=[r for r in u['all'] if R.bucket(r['action'])=='opt']
    if not rows: return None
    plain=sum(1 for r in rows if r['action']=='Opt In'); plus=len(rows)-plain
    path=f'{rk}/opt-in-features/'
    title=f'Oracle Fusion {rel} opt-in features: all {len(rows)}, by module'
    desc=f"The {len(rows)} features in Oracle Fusion {rel} that stay off until you opt in: {_counts(rows)}. Oracle's own Action to Enable and Impact columns, with a link to each Oracle feature page."
    cl=[('Home',''),(rel,f'{rk}/'),('Opt-in features',path)]
    faq=[(f"How many {rel} features need an opt-in?",f"{len(rows)} of the {len(u['all'])} features in Oracle's {rel} What's New documents for the modules we cover: {plain} are \"Opt In\" and {plus} are \"Opt In plus Setup\", per Oracle's Action to Enable column."),
         (f"Do {rel} opt-in features change anything for users if I do nothing?","No. Per Oracle's Action to Enable column, these features stay off until you opt in, and \"Opt In plus Setup\" features also need configuration before anyone can use them."),
         ("Is this the same as the opt-in expiration list?",f"No. This page lists new {rel} features you can choose to switch on. The <a href=\"{R.BASE}/{rk}/#opt-ins\">{rel} opt-in expiration list</a> is Oracle's list of older opt-ins that become standard features with {rel}.")]
    body=f"""{R.crumbs_html(cl,'../../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">Oracle&#39;s {rel} What&#39;s New documents list {len(rows)} features you have to opt in to before anyone can use them: {plain} marked "Opt In" and {plus} marked "Opt In plus Setup". By area: {E(_counts(rows))}. Nothing below changes for your users until you opt in.</p>
{LEGEND.format(rel=rel)}{_src(u,rows)}</div>
<div class="box"><h2 style="margin-top:0">How to use this list</h2><ul class="check">
<li>Shortlist the opt-ins your business owners asked for, and read each one&#39;s Oracle page for prerequisites and setup steps.</li>
<li>Opt in and set up in a test environment first, then test the end-to-end flow the feature touches.</li>
<li>"Opt In plus Setup" features need configuration after the opt-in, so plan time for both.</li>
<li>Some of today&#39;s opt-ins later become standard features. Oracle&#39;s <a href="https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html" target=_blank rel=noopener>Current Opt-In Expirations</a> list says which, and when.</li></ul></div>
{_groups(rows,rel,'../../')}{R.faq_html(faq)}{_related(rel,'opt-in-features/')}{R.nl_form()}"""
    return path,R.page(title,body,2,desc,path,_ld(path,title,desc,cl,rows,faq),og=(f'Oracle Fusion Cloud {rel} · readiness',f"{len(rows)} opt-in features, by module, with Oracle's status"))

def on_default_page(u):
    rel=u['release']; rk=rel.lower(); rows=[r for r in u['all'] if R.bucket(r['action'])=='on']
    if not rows: return None
    big=[r for r in rows if r['oracle_impact']=='Larger scale']
    path=f'{rk}/on-by-default/'
    title=f'Oracle Fusion {rel} features on by default: all {len(rows)}, by module'
    desc=f"The {len(rows)} Oracle Fusion {rel} features with no action to enable, so users can see them from {rel}: {_counts(rows)}. {len(big)} are larger scale per Oracle. Oracle links for each."
    cl=[('Home',''),(rel,f'{rk}/'),('On by default',path)]
    faq=[(f"Which {rel} features switch on without any action?",f"{len(rows)} features in Oracle's {rel} What's New documents for the modules we cover have \"None\" in Oracle's Action to Enable column: {_counts(rows)}."),
         (f"Which {rel} on-by-default changes are the biggest?",f"Oracle rates {len(big)} of them \"Larger scale\" in its Impact to Existing Processes column. They are marked in the tables below, and they are the first ones to test."),
         ("Can I switch these features off?","Oracle's feature page for each one says whether there is anything to configure or turn off. This page only repeats Oracle's Action to Enable column.")]
    bigtab=f'<div class="box"><h2 style="margin-top:0">Test first: {len(big)} rated "Larger scale" by Oracle</h2>{_table(big)}</div>' if big else ''
    body=f"""{R.crumbs_html(cl,'../../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">These {len(rows)} features need no action to enable, per Oracle&#39;s {rel} What&#39;s New documents, so your users can meet them as soon as {rel} reaches your environment. By area: {E(_counts(rows))}. Oracle rates {len(big)} of them "Larger scale".</p>
{LEGEND.format(rel=rel)}{_src(u,rows)}</div>{bigtab}
<div class="box"><h2 style="margin-top:0">How to use this list</h2><ul class="check">
<li>Start with the "Larger scale" rows above, then work through your own modules below.</li>
<li>Tell the users of each changed page what they will see, before {rel} reaches production.</li>
<li>Re-run the flows, reports and integrations that touch these pages in your test environment.</li></ul></div>
{_groups(rows,rel,'../../')}{R.faq_html(faq)}{_related(rel,'on-by-default/')}{R.nl_form()}"""
    return path,R.page(title,body,2,desc,path,_ld(path,title,desc,cl,rows,faq),og=(f'Oracle Fusion Cloud {rel} · readiness',f"{len(rows)} features on by default, by module, with Oracle's status"))

def redwood_erp_page(u):
    rel=u['release']; rk=rel.lower(); rows=[r for r in u['all'] if r['family']!='HCM' and 'redwood' in r['title'].lower()]
    if not rows: return None
    path=f'{rk}/redwood-erp-scm/'
    fams=R._and([R.FNAME[f] for f in _by_family(rows)])
    title=f'Redwood changes in Oracle Fusion {rel} for ERP, Procurement and Supply Chain'
    desc=f"The {len(rows)} features in Oracle's {rel} What's New for {fams} with Redwood in the title, with Oracle's Action to Enable for each: {R.bucket_sentence(rows)}."
    cl=[('Home',''),(rel,f'{rk}/'),('Redwood outside HCM',path)]
    body=f"""{R.crumbs_html(cl,'../../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">Outside HCM, Oracle&#39;s {rel} What&#39;s New documents name Redwood in {len(rows)} feature titles: {E(_counts(rows))}. Per Oracle&#39;s Action to Enable column: {E(R.bucket_sentence(rows))}.</p>
<p class="small muted">We list every row whose Oracle title contains "Redwood". Oracle delivers other Redwood work under titles that don&#39;t use the word, so check your module pages too. For HCM, see <a href="../../{R.HCMR_PATH}">HCM pages switching to Redwood</a>.</p>
{LEGEND.format(rel=rel)}{_src(u,rows)}</div>
{_groups(rows,rel,'../../')}{_related(rel,'redwood-erp-scm/')}{R.nl_form()}"""
    return path,R.page(title,body,2,desc,path,_ld(path,title,desc,cl,rows,None),og=(f'Oracle Fusion Cloud {rel} · Redwood',f"{len(rows)} Redwood changes outside HCM, with Oracle's status"))

def build(dist,updates):
    out=[]
    for k in sorted(updates):
        u=updates[k]
        if k<R.HUB_FROM or not u.get('all'): continue
        for fn in (opt_in_page,on_default_page,redwood_erp_page):
            r=fn(u)
            if not r: continue
            path,htm=r; d=os.path.join(dist,path); os.makedirs(d,exist_ok=True)
            open(os.path.join(d,'index.html'),'w').write(htm); out.append(path)
    return out
def links(rel,depth):
    """Link strip for the release hub."""
    rk=rel.lower()
    return (f'<div class="box"><h3 style="margin-top:0">{rel} readiness lists across modules</h3><p><a href="{depth}{rk}/opt-in-features/">{rel} opt-in features</a> · '
            f'<a href="{depth}{rk}/on-by-default/">{rel} features on by default</a> · <a href="{depth}{rk}/redwood-erp-scm/">{rel} Redwood changes outside HCM</a></p></div>')

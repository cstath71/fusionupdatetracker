"""Long-tail SEO pages (growth plan tactic #3): one page per search question, built from
data/longtail.json (tables checked against Oracle's readiness pages) and data/hcm_redwood.json.
Called from render.render(); returns the sitemap paths it wrote."""
import os, json
import render as R
E=R.E
_LT=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'data','longtail.json')
LT=json.load(open(_LT)) if os.path.exists(_LT) else None
P_PERSON='26d/redwood-person-pages/'; P_EMPL='26d/redwood-employment-pages/'; P_WFS='26d/redwood-workforce-structures-pages/'; P_27A='27a/redwood-defaults/'
PAGES={P_PERSON:'Redwood person pages in 26D',P_EMPL:'Redwood employment pages in 26D',P_WFS:'Redwood workforce structures pages in 26D',P_27A:'27A Redwood defaults announced so far'}
def ext(u,t): return f'<a href="{E(u)}" target=_blank rel=noopener>{E(t)}</a>'
def srcs(sec): return '<p class="small muted">Oracle sources: '+' · '.join(ext(u,t) for t,u in sec['sources'])+'</p>'
def table(rows,first_label='Redwood page first delivered'):
    return ('<table><tr><th>Page</th><th>Profile option code</th><th>'+E(first_label)+'</th></tr>'+
            ''.join(f'<tr><td>{E(p)}</td><td><code style="font-size:12px">{E(c)}</code></td><td>{E(f)}</td></tr>' for p,c,f in rows)+'</table>')
def revert_box(extra=''):
    return f"""<div class="box"><h2 style="margin-top:0">How to keep the older pages for now</h2>
<p>Oracle lets you switch each page back by setting its profile option to No:</p>
<ol><li>In Setup and Maintenance, open the <b>Manage Administrator Profile Values</b> task.</li><li>Search for the profile option code from the table above.</li><li>In Profile Values, enter <b>No</b> and save.</li></ol>
{extra}<p class="small muted">Oracle keeps the full list of HCM Redwood profile options in My Oracle Support: {E(LT['mos_doc'])}.</p></div>"""
POD_NOTE='<p>Per Oracle, if you set a profile option to Yes in a test pod and then back to No to stay on the older page, that No is kept when the pod moves to 26D. The setting is held separately in each pod, so check production as well as every test pod.</p>'
def related(cur,depth='../../'):
    lk=' · '.join(f'<a href="{depth}{p}">{E(n)}</a>' for p,n in PAGES.items() if p!=cur)
    return (f'<div class="box"><p><b>Related:</b> {lk} · <a href="{depth}{R.HCMR_PATH}">All HCM pages switching to Redwood</a> · '
            f'<a href="{depth}26d/">26D opt-in expiration list</a></p></div>')
def ld(path,title,desc,cl,extra=None):
    g=[{"@type":"WebPage","@id":R.BASE+'/'+path,"url":R.BASE+'/'+path,"name":title,"description":desc,"inLanguage":"en","dateModified":LT['checked'],
        "isPartOf":{"@type":"WebSite","@id":R.BASE+"/#website","name":R.SITE,"url":R.BASE+"/"}},R.crumbs(cl)]
    if extra: g.append(extra)
    return R.jsonld({"@context":"https://schema.org","@graph":g})
def itemlist(name,rows): return {"@type":"ItemList","name":name,"numberOfItems":len(rows),"itemListElement":[{"@type":"ListItem","position":n+1,"name":f"{p} ({c})"} for n,(p,c,_) in enumerate(rows)]}
def chk(): return f'<p class="small muted">Checked against Oracle&#39;s pages on {E(LT["checked"])}. Oracle can revise its What&#39;s New pages; always confirm on the linked Oracle page.</p>'

def person_page():
    s=LT['person_26d']; rows=s['rows']; path=P_PERSON
    codes=sorted(set(c for _,c,_ in rows)); shared=[p for p,c,_ in rows if c==rows[0][1]]
    title='Redwood person pages by default in 26D: pages and profile option codes'
    desc=f"From Oracle Fusion HCM 26D, {len(rows)} person pages open in Redwood by default. The pages, the {len(codes)} profile option codes behind them, and how to keep the responsive pages for now, with Oracle links."
    cl=[('Home',''),('HCM pages switching to Redwood',R.HCMR_PATH),('Person pages in 26D',path)]
    body=f"""{R.crumbs_html(cl,'../../')}<div class="hero"><h1>Redwood person pages by default in 26D</h1>
<p class="lead">From the 26D update, {len(rows)} Oracle Fusion HCM person pages open in Redwood by default, and the older responsive pages are no longer shown by default. You can still go back to a responsive page by setting its profile option to No. Oracle first planned this for 26C and moved it to 26D.</p>
{srcs(s)}{chk()}</div>
<div class="box"><h2 style="margin-top:0">The {len(rows)} person pages and their profile options</h2>
<p class="small muted">{len(rows)} pages, {len(codes)} profile option codes. One code, <code style="font-size:12px">{E(rows[0][1])}</code>, covers {len(shared)} pages ({E(R._and(shared))}), so setting it to No keeps all {len(shared)} on the responsive pages. "First delivered" is the update in which Oracle released the Redwood version of the page.</p>
{table(rows)}</div>
{revert_box(POD_NOTE)}
<div class="box"><h2 style="margin-top:0">What to check before 26D reaches your test pod</h2><ul class="check">
<li>Decide, page by page, whether you move to Redwood in 26D or set the profile option to No for now. Because of the shared code, Personal Details, Contact Info, Identification Info and Family and Emergency Contacts move together.</li>
<li>Access: per Oracle, the roles that could open the responsive pages can open the Redwood pages too.</li>
<li>Custom roles: Oracle points to a 24D change to the privileges for managing addresses on Redwood pages. Check it if you use custom roles.</li>
<li>Run the person flows your HR team uses most on the Redwood pages in your test environment.</li></ul></div>
{related(path)}{R.nl_form()}"""
    return path,R.page(title,body,2,desc,path,ld(path,title,desc,cl,itemlist('Redwood person pages in 26D and their profile options',rows)),og=('HCM · Redwood · 26D',f"{len(rows)} person pages switch to Redwood by default, with profile option codes"))

def employment_page():
    s=LT['employment_26d']; rows=s['rows']; path=P_EMPL; nx=LT['employment_27a']['rows']
    title=f'Redwood employment pages in 26D: all {len(rows)} pages and profile options'
    desc=f"From Oracle Fusion HCM 26D, {len(rows)} employment pages, from Hire an Employee to Promote and Transfer, open in Redwood by default. Every page with its profile option code and first Redwood release, plus the {len(nx)} that follow in 27A."
    cl=[('Home',''),('HCM pages switching to Redwood',R.HCMR_PATH),('Employment pages in 26D',path)]
    body=f"""{R.crumbs_html(cl,'../../')}<div class="hero"><h1>Redwood employment pages in 26D: all {len(rows)} pages and profile options</h1>
<p class="lead">From the 26D update, Oracle turns on the Redwood profile option by default for {len(rows)} Oracle Fusion HCM employment pages. You don't need to do anything to get them. If you want to stay on an older page for now, set its profile option to No.</p>
{srcs(s)}{chk()}</div>
<div class="box"><h2 style="margin-top:0">The {len(rows)} employment pages and their profile options</h2>
<p class="small muted">Each page has its own profile option, so you can move page by page. "First delivered" is the update in which Oracle released the Redwood version of the page.</p>{table(rows)}</div>
{revert_box()}
<div class="box"><h2 style="margin-top:0">Next: {len(nx)} more employment pages in 27A</h2><p>Oracle has also announced that these switch to Redwood by default in 27A. Per Oracle, the Redwood Mass Assignment Change page itself only arrives in 26D.</p>{table(nx)}{srcs(LT['employment_27a'])}<p><a href="../../{P_27A}">Everything announced for 27A so far →</a></p></div>
<div class="box"><h2 style="margin-top:0">What to check before 26D reaches your test pod</h2><ul class="check">
<li>List which of the {len(rows)} pages your HR users and managers use, and run those flows (hire, add assignment, change manager, promote, transfer) on the Redwood pages in your test environment.</li>
<li>Decide whether any page needs its profile option set to No for now, and in which pods.</li>
<li>Oracle mentions that users can reach these Redwood pages through the quick action for each page.</li></ul></div>
{related(path)}{R.nl_form()}"""
    return path,R.page(title,body,2,desc,path,ld(path,title,desc,cl,itemlist('Redwood employment pages in 26D and their profile options',rows)),og=('HCM · Redwood · 26D',f"{len(rows)} employment pages switch to Redwood by default, with profile option codes"))

def wfs_page():
    s=LT['wfs_26d']; rows=s['rows']; path=P_WFS; prev=LT['wfs_26c']['rows']
    names=R._and([p for p,_,_ in rows])
    title='Redwood workforce structures pages in 26D: Jobs, Departments, Locations and more'
    desc=f"From Oracle Fusion HCM 26D, {len(rows)} workforce structures pages open in Redwood by default: {names}. Profile option codes, how to keep the older pages, and the {len(prev)} that switched in 26C."
    cl=[('Home',''),('HCM pages switching to Redwood',R.HCMR_PATH),('Workforce structures pages in 26D',path)]
    body=f"""{R.crumbs_html(cl,'../../')}<div class="hero"><h1>Redwood workforce structures pages in 26D</h1>
<p class="lead">From the 26D update, {len(rows)} Oracle Fusion HCM workforce structures pages open in Redwood by default: {E(names)}. The older responsive or classic pages are no longer shown by default, but you can still use them by setting the profile option to No.</p>
{srcs(s)}{chk()}</div>
<div class="box"><h2 style="margin-top:0">The {len(rows)} pages switching in 26D</h2><p class="small muted">"First delivered" is the update in which Oracle released the Redwood version of the page.</p>{table(rows)}</div>
{revert_box(POD_NOTE)}
<div class="box"><h2 style="margin-top:0">Already Redwood by default since 26C ({len(prev)})</h2><p>Oracle switched the first set of workforce structures pages to Redwood by default in 26C. Their profile options work the same way.</p>{table(prev)}{srcs(LT['wfs_26c'])}</div>
<div class="box"><h2 style="margin-top:0">What to check before 26D reaches your test pod</h2><ul class="check">
<li>Access: per Oracle, the roles that could open the responsive and classic pages can open the Redwood pages too.</li>
<li>Have the people who maintain jobs, departments and locations run their usual create and update tasks on the Redwood pages in your test environment.</li>
<li>Decide whether any page needs its profile option set to No for now, in each pod.</li></ul></div>
{related(path)}{R.nl_form()}"""
    return path,R.page(title,body,2,desc,path,ld(path,title,desc,cl,itemlist('Redwood workforce structures pages in 26D and their profile options',rows)),og=('HCM · Redwood · 26D',f"{len(rows)} workforce structures pages switch to Redwood by default"))

def a27_page():
    path=P_27A
    its=[i for i in R.HCMR['items'] if i['release']=='27A']
    cd=[i for i in R.HCMR['items'] if 'Career Development' in i['title']]
    red=[i for i in its if i['type']=='Redwood by default']; only=[i for i in its if i['type']=='End of support' and 'Redwood' in i['title']]
    other=[i for i in its if i not in red and i not in only]
    em=LT['employment_27a']; po=LT['positions_27a']
    title='Oracle Fusion HCM 27A: Redwood defaults announced so far'
    desc=f"What Oracle has already announced for HCM in 27A: Resign, Terminate and Mass Assignment Change and the Positions pages switch to Redwood by default, Redwood-only payroll calculation cards, and other 27A changes. Profile option codes and Oracle links."
    cl=[('Home',''),('HCM pages switching to Redwood',R.HCMR_PATH),('27A Redwood defaults',path)]
    l27b=''.join(f'<div class="item"><h4>{E(x["title"])}</h4><div class="meta"><span class="pill">From 27B</span></div><p style="margin:4px 0">{E(x["summary"])}</p><p class="small">{ext(x["url"],"Oracle source")}</p></div>' for x in LT['later_27b'])
    l27b+=''.join(R.hr_item_html(i) for i in R.HCMR['items'] if i['release']=='27B')
    body=f"""{R.crumbs_html(cl,'../../')}<div class="hero"><h1>Oracle Fusion HCM 27A: Redwood defaults announced so far</h1>
<p class="lead">Oracle hasn't published its 27A What's New documents yet, but its 26C and 26D documents already announce several HCM changes for 27A. Here is everything we've found, with the profile option codes Oracle gives and a link to each Oracle page. We add new 27A announcements as Oracle publishes them.</p>{chk()}</div>
<div class="box"><h2 style="margin-top:0">Employment pages: Redwood by default in 27A ({len(em['rows'])})</h2><p>Each page has its own profile option, and you can set it back to No to keep the older page. Per Oracle, the Redwood Mass Assignment Change page itself arrives in 26D.</p>{table(em['rows'])}{srcs(em)}</div>
<div class="box"><h2 style="margin-top:0">Positions pages and guided processes: Redwood by default in 27A</h2><p>The Positions pages and the Request a New Position and Request a Position Change guided processes switch together: Oracle says the one profile option <code style="font-size:12px">{E(po['rows'][0][1])}</code> covers all of them. Setting it to No keeps the older pages.</p>{table(po['rows'])}{srcs(po)}</div>
<div class="box"><h2 style="margin-top:0">Payroll: only the Redwood calculation cards supported from 27A ({len(only)})</h2>{''.join(R.hr_item_html(i) for i in only)}</div>
<div class="box"><h2 style="margin-top:0">Learning: responsive Career Development pages</h2>{''.join(R.hr_item_html(i) for i in cd)}</div>
<div class="box"><h2 style="margin-top:0">Other HCM changes Oracle has announced for 27A ({len(other)})</h2>{''.join(R.hr_item_html(i) for i in other)}</div>
<div class="box"><h2 style="margin-top:0">Looking further: 27B</h2>{l27b}</div>
<div class="box"><p>Before 27A: the 26D switches come first. <a href="../../{P_PERSON}">Person pages in 26D</a> · <a href="../../{P_EMPL}">Employment pages in 26D</a> · <a href="../../{P_WFS}">Workforce structures pages in 26D</a></p></div>
{related(path)}{R.nl_form()}"""
    rows=em['rows']+po['rows']
    return path,R.page(title,body,2,desc,path,ld(path,title,desc,cl,itemlist('HCM pages switching to Redwood by default in 27A',rows)),og=('HCM · Redwood · 27A','Redwood defaults Oracle has announced for 27A so far'))

def build(dist):
    if not LT: return []
    out=[]
    for fn in (person_page,employment_page,wfs_page,a27_page):
        path,htm=fn(); d=os.path.join(dist,path); os.makedirs(d,exist_ok=True)
        open(os.path.join(d,'index.html'),'w').write(htm); out.append(path)
    return out
def hcm_links(depth):
    """Short link list for the HCM Redwood page and the next-update page."""
    if not LT: return ''
    return '<div class="box"><h3 style="margin-top:0">Deep dives with every profile option code</h3><p>'+' · '.join(f'<a href="{depth}{p}">{E(n)}</a>' for p,n in PAGES.items())+'</p></div>'

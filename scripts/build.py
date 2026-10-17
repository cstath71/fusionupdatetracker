"""Build Fusion Updates (fusionupdates.com) static site from Oracle readiness data.
Usage: python3 scripts/build.py   -> writes ./dist
Data: scripts/crawl.py writes /workspace/fut-raw/summaries.json (Oracle Feature Summary tables)."""
import json, re, html, os, sys, shutil, datetime, collections
# Public contact address (used on privacy, sponsor and footer). Override with env FUT_CONTACT if ever needed.
CONTACT_DEFAULT='hello@fusionupdates.com'
os.environ['FUT_CONTACT']=os.environ.get('FUT_CONTACT') or CONTACT_DEFAULT
sys.path.insert(0, os.path.dirname(__file__))
from crawl import get, txt
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW='/workspace/fut-raw'; DIST=os.path.join(ROOT,'dist'); DATA=os.path.join(ROOT,'data')
PER_FAMILY=int(os.environ.get('PER_FAMILY','25'))
FAM={'fins':'Financials','risk':'Financials','ssfin':'Financials','ppm':'Project Management','proc':'Procurement','ssproc':'Procurement',
     'gtm':'Logistics (OTM/GTM/WMS)','otm':'Logistics (OTM/GTM/WMS)','wms':'Logistics (OTM/GTM/WMS)'}
def family(path):
    b=re.sub(r'-?26[a-d]$','',path.split('/')[-1])
    if path.startswith('hcm/'): return 'HCM'
    return FAM.get(b,'Supply Chain & Manufacturing')
def product(title): return re.sub(r"^Oracle Fusion Cloud |\s*26[A-D] What's New$|\s*What's New.*$","",title).strip()
# opt-in expirations (Oracle "Current Opt-In Expirations" table)
oh=get('https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html')
EXP=[]; EXPMAP={}
for tr in re.findall(r'<tr>(.*?)</tr>',oh,re.S):
    td=re.findall(r'<td[^>]*>(.*?)</td>',tr,re.S)
    if len(td)<9: continue
    m=re.search(r'href="([^"]+)"',td[4]); link=html.unescape(m.group(1)) if m else ''
    if link.startswith('/'): link='https://docs.oracle.com'+link
    elif link and not link.startswith('http'): link='https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/'+link
    mm=re.search(r'/wn/([a-z]+)/releases/(\d\d[A-D])/.*#F(\d+)',link)  # old webfolder links now 404: use Oracle's lookup service
    if mm: link=f'https://docs.oracle.com/pls/topic/lookup?ctx=saas-readiness&id={mm.group(1)}{mm.group(2).lower()}-f{mm.group(3)}'
    r=dict(expires=txt(td[0]),pillar=txt(td[1]),product=txt(td[2]),module=txt(td[3]),title=txt(td[4]),now_enabled=txt(td[5]),impact=txt(td[6]),action=txt(td[7]),introduced=txt(td[8]),url=link)
    EXP.append(r); EXPMAP[r['title'].lower()]=r['expires']
def norm(s): return re.sub(r'\s+',' ',s).strip().lower()
def enablement(r):
    e=EXPMAP.get(norm(r['title']))
    a=r['action']
    if a.startswith('Opt In'):
        return ('Opt-in, expires '+e) if e else ('Opt-in plus setup' if 'Setup' in a else 'Opt-in')
    if a in ('None',) : return 'Automatically on'
    if a=='Potential Setup': return 'Automatically on (setup may apply)'
    if a=='Setup Required': return 'Off until set up'
    return 'Off until set up ('+a+')'
def draft_impact(r,en):
    oi=r['oracle_impact']
    if oi=='Larger scale': return 'high'
    if en.startswith('Opt-in, expires'): return 'high' if (en.endswith(r['_rel']) or en.endswith(r['_relnext'])) else 'medium'
    if oi=='Small scale': return 'medium'
    if 'Redwood' in r['title'] and en.startswith('Automatically'): return 'medium'
    return 'low'
SCORE={'high':3,'medium':2,'low':1}
def summary(url):
    h=get(url); h=re.sub(r'<script.*?</script>|<style.*?</style>','',h,flags=re.S)
    i=h.find('<h1'); h=h[i:] if i>=0 else h
    ps=[txt(p) for p in re.findall(r'<p[^>]*>(.*?)</p>',h,re.S)]
    ps=[p for p in ps if len(p)>40 and not p.startswith('Copyright')]
    if not ps: return ''
    sents=re.split(r'(?<=[.!?])\s+',' '.join(ps[:2]))
    out=sents[0]
    if len(out)<160 and len(sents)>1: out+=' '+sents[1]
    return out[:420].rstrip()+('…' if len(out)>420 else '')
def prodname(title,path):
    prod=product(title)
    if '$' in prod or not prod: prod={'risk':'Risk Management','ssfin':'Financials (Shared)','hcom':'HCM Common','wohs':'Workforce Health and Safety','woli':'Work Life'}.get(re.sub(r'-?2\d[a-d]$','',path.split('/')[-1]),path.split('/')[-1])
    return prod
raw=json.load(open(os.path.join(RAW,'summaries.json')))
nextrel={'26b':'26C','26c':'26D'}
updates={}
for rel,books in raw.items():
    items=[]; important=[]
    for b in books:
        fam=family(b['path']); prod=prodname(b['title'],b['path'])
        if b.get('important'): important.append(dict(product=prod,family=fam,url=b['important']))
        for r in b['rows']:
            r=dict(r); r['family']=fam; r['product']=prod; r['_rel']=rel.upper(); r['_relnext']=nextrel[rel]
            r['enablement']=enablement(r); r['impact']=draft_impact(r,r['enablement']); items.append(r)
    sel=[]
    for fam in sorted(set(i['family'] for i in items)):
        fi=[i for i in items if i['family']==fam]
        fi.sort(key=lambda i:(-SCORE[i['impact']], 0 if i['enablement'].startswith('Automatically') else 1, i['product'], i['title']))
        sel+=fi[:PER_FAMILY]
    import concurrent.futures as cf
    with cf.ThreadPoolExecutor(8) as ex:
        for r,s in zip(sel,ex.map(lambda r:summary(r['url']),sel)): r['summary']=s
    for r in sel: r.pop('_relnext',None)
    books=[dict(product=prodname(b['title'],b['path']),family=family(b['path']),url=f"https://docs.oracle.com/en/cloud/saas/readiness/{b['path']}/index.html",features=len(b['rows'])) for b in books if b['rows']]
    updates[rel.upper()]=dict(release=rel.upper(),items=sel,total_features=len(items),important=important,
        family_totals=dict(collections.Counter(i['family'] for i in items)),books=books,
        expiring=[e for e in EXP if e['expires']==rel.upper()])
# Next release: only listed if Oracle has published its What's New documents (checked via each book's toc.htm)
from crawl import BOOKS
_last=sorted(raw)[-1]; _nxt=nextrel[_last] if _last in nextrel else None
upcoming=None
if _nxt:
    nb=[]
    for path in BOOKS[_last].split():
        np_=path.replace(_last,_nxt.lower())
        toc=get(f'https://docs.oracle.com/en/cloud/saas/readiness/{np_}/toc.htm')
        if '<title>' in toc:
            t=txt(re.search(r'<title>(.*?)</title>',toc,re.S).group(1))
            if t.startswith('Cloud Applications Readiness'): continue  # generic landing page, book not published
            nb.append(dict(product=prodname(t,np_),family=family(np_),url=f'https://docs.oracle.com/en/cloud/saas/readiness/{np_}/index.html'))
    if nb: upcoming=dict(release=_nxt,books=nb,expiring=[e for e in EXP if e['expires']==_nxt])
os.makedirs(DATA,exist_ok=True)
json.dump(dict(generated=datetime.date.today().isoformat(),updates=updates,upcoming=upcoming),open(os.path.join(DATA,'updates.json'),'w'),indent=1)
import render; render.render(updates, DIST, upcoming=upcoming, generated=datetime.date.today().isoformat())
for k,u in updates.items():
    import collections; print(k,'total in Oracle docs:',u['total_features'],'selected:',dict(collections.Counter(i['family'] for i in u['items'])),'expiring:',len(u['expiring']))

"""Build the free downloads into assets/downloads/:
 - fusion-26d-readiness-checklist.pdf: only from data we already track (Oracle's 26D What's New book list,
   Oracle's opt-in expiration list, data/hcm_redwood.json), printed with headless Chrome.
 - fusion-quarterly-update-calendar.ics: typical 26D/27A windows from Oracle's published cohort rule.
Run: python3 scripts/leadmagnets.py  (then python3 scripts/build.py)"""
import os, sys, json, html, datetime, subprocess, tempfile, collections, calendar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
E=html.escape
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'assets','downloads'); os.makedirs(OUT,exist_ok=True)
U=json.load(open(os.path.join(ROOT,'data','updates.json'))); UP=U['upcoming']
if not UP or UP['release']!=R.LEAD['rel']:  # e.g. once 26D is the current update and 27A isn't published yet
    _u=U['updates'].get(R.LEAD['rel']); UP=dict(release=_u['release'],books=_u['books'],expiring=_u['expiring']) if _u else UP
REL=UP['release']
assert REL==R.LEAD['rel'], (REL, R.LEAD['rel'])
TODAY=datetime.date.today()
FI='https://blogs.oracle.com/fusioninsider/quarterly-updates-made-easy'
OPTIN='https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html'

# ---- Typical update dates from Oracle's published rule (first Friday = test, third Friday = production) ----
COH={'A':(2,5,8,11),'B':(3,6,9,12),'C':(4,7,10,1)}
QIDX={'A':0,'B':1,'C':2,'D':3}
def fridays(y,m):
    fs=[d for d in range(1,calendar.monthrange(y,m)[1]+1) if datetime.date(y,m,d).weekday()==4]
    return datetime.date(y,m,fs[0]),datetime.date(y,m,fs[2])
def windows(rel):
    y=2000+int(rel[:2]); q=QIDX[rel[2]]; res=[]
    for c,ms in COH.items():
        m=ms[q]; yy=y+1 if (c=='C' and q==3) else y
        t,p=fridays(yy,m); res.append((c,t,p))
    return res
HOL={datetime.date(2027,1,1):"This date is New Year's Day. Oracle may schedule this cohort differently, so check your own date."}

# ---- PDF ----
def bygroup(es):  # Oracle's own Pillar column
    return collections.OrderedDict((f"Oracle pillar: {k}",x) for k,x in R.pillar_groups(es).items())
ACT={'None':'Nothing to do: on for everyone','Setup':'Set up if you want to use it'}
hr=[i for i in R.HCMR['items'] if i['release']==REL]
later=[i for i in R.HCMR['items'] if i['release']>REL]
es=UP['expiring']; on=sum(1 for e in es if e['now_enabled']=='Yes')
def cb(): return '<span class="cb"></span>'
rows_exp=''.join(f'<h3>{E(g)} ({len(x)})</h3><table><tr><th></th><th>Feature (Oracle source)</th><th>Product · module</th><th>Now enabled</th><th>What this means</th></tr>'+''.join(
    f"<tr><td>{cb()}</td><td>{'<a href=\"'+E(e['url'])+'\">' if e['url'] else ''}{E(e['title'])}{'</a>' if e['url'] else ''}</td><td>{E(e['product'])} · {E(e['module'])}</td><td>{E(e['now_enabled'])}</td><td>{E(ACT.get(e['action'],e['action']))}</td></tr>" for e in x)+'</table>' for g,x in bygroup(es).items())
def hr_row(i):
    po=('<div class="po">Profile options named on Oracle\'s page: '+', '.join(f'<code>{E(c)}</code>' for c in i.get('profile_options',[]))+'</div>') if i.get('profile_options') and i['type']=='Redwood by default' else ''
    src=' · '.join(f'<a href="{E(u)}">Oracle source{(" "+str(n+1)) if len(i["urls"])>1 else ""}</a>' for n,u in enumerate(i['urls']))
    return (f'<div class="it">{cb()}<div><b>{E(i["title"])}</b> <span class="pill">{E(i["area"])}</span> <span class="pill">{E(R.HR_TYPE.get(i["type"],i["type"]))}</span><br>{E(i["summary"])}'
            f'<div class="mut">Pages affected ({len(i["pages"])}): {E(", ".join(i["pages"]))} · Revert: {E(i["revert"])} · {src}</div>{po}</div></div>')
win=''.join(f'<tr><td>Cohort {c}</td><td>{t:%a %d %b %Y}</td><td>{p:%a %d %b %Y}</td><td>{E(HOL.get(t,""))}</td></tr>' for c,t,p in windows(REL))
byf=collections.OrderedDict()
for b in UP['books']: byf.setdefault(R.FNAME.get(b['family'],b['family']),[]).append(b)
books=''.join(f'<p><b>{E(g)}:</b> '+' · '.join(f'<a href="{E(b["url"])}">{E(b["product"])}</a>' for b in bs)+'</p>' for g,bs in byf.items())
SITE='https://fusionupdates.com'
doc=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Oracle Fusion {REL} readiness checklist | Fusion Updates</title><style>
@font-face{{font-family:I;src:url("file://{'/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf'}");font-weight:100 900}}
@page{{size:A4;margin:14mm 14mm 16mm}}
body{{font-family:I,Arial,sans-serif;font-size:10.2pt;line-height:1.42;color:#14202b;margin:0}}
a{{color:#1f5fa8;text-decoration:none}}
.head{{background:#14202b;color:#fff;padding:16px 20px;border-left:8px solid #c74634;border-radius:6px}}
.head .b{{font-weight:800;font-size:15pt}}.head .b span{{color:#ff8a70}}.head h1{{font-size:21pt;margin:6px 0 2px;letter-spacing:-.01em}}.head p{{margin:2px 0;color:#d6dee6;font-size:9.5pt}}
h2{{font-size:13.5pt;margin:16px 0 6px;border-bottom:2px solid #c74634;padding-bottom:3px;page-break-after:avoid}}h3{{font-size:11pt;margin:10px 0 4px;page-break-after:avoid}}
.note{{background:#fff6ec;border:1px solid #f3d4b5;border-radius:6px;padding:8px 10px;font-size:9.3pt;margin:10px 0}}
table{{border-collapse:collapse;width:100%;font-size:9pt;page-break-inside:auto}}tr{{page-break-inside:avoid}}td,th{{border-bottom:1px solid #e3e6ea;padding:4px 6px;text-align:left;vertical-align:top}}th{{background:#f6f7f9}}
.cb{{display:inline-block;width:10px;height:10px;border:1.3px solid #5b6875;border-radius:2px;margin-top:2px;flex:none}}
ul.ck{{list-style:none;padding:0;margin:4px 0}}ul.ck li{{display:flex;gap:8px;margin:4px 0}}
.it{{display:flex;gap:8px;margin:7px 0;page-break-inside:avoid}}.mut{{color:#5b6875;font-size:8.6pt;margin-top:2px}}.po{{color:#5b6875;font-size:8.2pt;margin-top:2px;word-break:break-all}}
code{{font-family:Menlo,Consolas,monospace;font-size:7.8pt;background:#f1f3f5;padding:0 2px;border-radius:2px}}
.pill{{font-size:7.8pt;background:#eef1f4;border-radius:99px;padding:1px 7px;color:#33414e}}
.foot{{color:#5b6875;font-size:8.3pt;border-top:1px solid #e3e6ea;margin-top:16px;padding-top:6px}}
</style></head><body>
<div class="head"><div class="b">Fusion<span>Updates</span></div><h1>Oracle Fusion {REL} readiness checklist</h1><p>Preliminary · built {TODAY:%d %b %Y} from Oracle's published {REL} What's New documents, Oracle's opt-in expiration list and the HCM Redwood changes tracked at fusionupdates.com</p></div>
<div class="note"><b>Preliminary.</b> Oracle's {REL} What's New documents are still being revised. Oracle's note on them: "This document will continue to evolve as existing sections change and new information is added." Check each linked Oracle page before you rely on an item. The latest version of this checklist is at {SITE}/{R.LEAD['pdf']}</div>

<h2>When {REL} arrives (typical dates)</h2>
<p>Oracle's published rule: test environments update on the <b>first Friday</b> of the update month and production on the <b>third Friday</b>, two weeks later. In Middle East regions, updates happen on the Thursday before. The dates below follow that rule. Oracle doesn't publish them as a list, so confirm yours in the Oracle Cloud Console. Source: <a href="{FI}">Oracle Fusion Insider, "Quarterly updates made easy"</a>.</p>
<table><tr><th>Cohort</th><th>Test environments</th><th>Production</th><th>Note</th></tr>{win}</table>

<h2>1. Before the update: baseline regression</h2>
<p class="mut">Based on Oracle's guidance: <a href="https://docs.oracle.com/en/cloud/saas/transportation/26b/otmpt/what-should-i-test-after-a-quarterly-update.html">What Should I Test After a Quarterly Update?</a></p>
<ul class="ck">{''.join(f'<li>{cb()}<span>{x}</span></li>' for x in [y.replace(' (section 2) and former opt-ins that are now standard (section 3)',', and the former opt-ins that become standard (section 2 below)') for y in R.BASELINE])}<li>{cb()}<span>Refresh your test environment from production before the test-environment update, as Oracle recommends</span></li></ul>

<h2>2. Opt-ins Oracle lists as ending with {REL} ({len(es)})</h2>
<p>From Oracle's <a href="{OPTIN}">Current Opt-In Expirations</a> list. With {REL} these become standard features. Oracle's "Now enabled" column shows Yes for {on} of them, and the rest need setup if you want to use them. If you already opted in and finished setup, nothing changes. By area: {E(R.exp_scope(es,REL))}. Oracle can update this list.</p>
{rows_exp}

<h2>3. HCM: pages switching to Redwood and other HCM notices in {REL} ({len(hr)})</h2>
<p>{E(R.HR_NOTE)} Where Oracle says so, you can still set the profile option back to No.</p>
{''.join(hr_row(i) for i in hr)}
{f'<h3>Already announced for 27A and later ({len(later)})</h3><ul class="ck">'+''.join(f'<li>{cb()}<span>{E(i["release"])}: {E(i["title"])} <span class="mut">({E(i["area"])}, <a href="{E(i["urls"][0])}">Oracle source</a>)</span></span></li>' for i in later)+'</ul>' if later else ''}

<h2>4. Read Oracle's {REL} What's New documents</h2>
<p class="mut">Check each product's "IMPORTANT Actions and Considerations" section and the features delivered switched on. Plain-English {REL} summaries by module follow on <a href="{SITE}/{REL.lower()}/">{SITE.replace('https://','')}/{REL.lower()}/</a>.</p>
{books}

<div class="foot">Fusion Updates (fusionupdates.com) is independent and not affiliated with or endorsed by Oracle. Oracle and Oracle Fusion are trademarks of Oracle and/or its affiliates. Items are condensed from Oracle's public readiness documentation; always confirm details on the linked Oracle page and in your own environment. Free quarterly briefing: {SITE}/newsletter.html</div>
</body></html>"""
pdf=os.path.join(OUT,R.LEAD['pdf'].split('/')[-1])
with tempfile.TemporaryDirectory() as td:
    f=os.path.join(td,'c.html'); open(f,'w').write(doc); open('/workspace/growth/26d-checklist-source.html','w').write(doc)
    subprocess.run([R.__dict__.get('CHROME') or 'google-chrome','--headless=new','--no-sandbox','--disable-gpu','--no-pdf-header-footer',f'--print-to-pdf={pdf}',f'file://{f}'],check=True,capture_output=True,timeout=120)
print('PDF',pdf,os.path.getsize(pdf))
# page-1 preview image for the signup boxes (render.LEAD_THUMB); skipped if poppler's pdftoppm isn't installed
try:
    th=os.path.join(ROOT,'assets',R.LEAD_THUMB)
    subprocess.run(['pdftoppm','-png','-f','1','-l','1','-singlefile','-scale-to-x','224','-scale-to-y','-1',pdf,th[:-4]],check=True,capture_output=True,timeout=60)
    print('THUMB',th,os.path.getsize(th))
except Exception as e: print('THUMB skipped:',e)

# ---- ICS ----
def fold(line):
    b=line.encode('utf-8'); out=[]
    while len(b)>75:
        cut=75 if not out else 74
        while (b[cut] & 0xC0)==0x80: cut-=1
        out.append(b[:cut]); b=b[cut:]
    out.append(b); return b'\r\n '.join(out).decode('utf-8')
def esc(t): return t.replace('\\','\\\\').replace(';','\\;').replace(',','\\,').replace('\n','\\n')
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
L=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Fusion Updates//Quarterly update calendar//EN','CALSCALE:GREGORIAN','METHOD:PUBLISH',
   'X-WR-CALNAME:Oracle Fusion quarterly updates (typical dates)','X-WR-CALDESC:'+esc('Typical Oracle Fusion Cloud test and production update dates for 26D and 27A, from Oracle\'s published cohort rule. Delete the cohorts you are not in. From fusionupdates.com (independent, not affiliated with Oracle).')]
RULE=("Typical date, not an Oracle-published date for your environment. Oracle's published rule: test environments update on the first Friday of the update month and production on the third Friday "
      "(Middle East regions: the Thursday before). Confirm your own dates in the Oracle Cloud Console. Source: "+FI)
n_ev=0
for rel in ('26D','27A'):
    link=f'{SITE}/{rel.lower()}/' if rel==REL else f'{SITE}/'
    for c,t,p in windows(rel):
        for kind,d in (('test environments',t),('production',p)):
            extra=''
            if kind=='production' and rel==REL: extra=f"\n\nWith {rel}, the {len(es)} opt-ins Oracle lists as ending with {rel} become standard. Checklist: {SITE}/{R.LEAD['pdf']}"
            if kind=='test environments': extra+=("\n\nTwo-week test window until the production update." )
            if d in HOL: extra+="\n\n"+HOL[d]
            L+=['BEGIN:VEVENT',f'UID:fut-{rel.lower()}-{c.lower()}-{"test" if kind.startswith("test") else "prod"}@fusionupdates.com',f'DTSTAMP:{stamp}',
                f'DTSTART;VALUE=DATE:{d:%Y%m%d}',f'DTEND;VALUE=DATE:{d+datetime.timedelta(days=1):%Y%m%d}',
                'SUMMARY:'+esc(f'Oracle Fusion {rel}: {kind} update, Cohort {c} (typical date)'),
                'DESCRIPTION:'+esc(RULE+extra+f'\n\nPlain-English briefing: {link}'),f'URL:{link}','TRANSP:TRANSPARENT','END:VEVENT']; n_ev+=1
L.append('END:VCALENDAR')
ics=os.path.join(OUT,R.LEAD['ics'].split('/')[-1])
open(ics,'w',newline='').write('\r\n'.join(fold(x) for x in L)+'\r\n')
print('ICS',ics,n_ev,'events')
for rel in ('26D','27A'): print(rel,[(c,str(t),str(p)) for c,t,p in windows(rel)])

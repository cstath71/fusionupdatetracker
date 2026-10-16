import re, json, html, urllib.request, concurrent.futures as cf, os
B='https://docs.oracle.com/en/cloud/saas/readiness'
BOOKS={'26b':"""erp/26b/fins26b erp/26b/ppm26b erp/26b/risk26b erp/26b/ssfin26b hcm/26b/amg-26b hcm/26b/benf-26b hcm/26b/comp-26b hcm/26b/hcom-26b hcm/26b/hure-26b hcm/26b/lear-26b hcm/26b/payr-26b hcm/26b/recr-26b hcm/26b/tama-26b hcm/26b/tila-26b hcm/26b/wohs-26b hcm/26b/wosc-26b logistics/26b/gtm26b logistics/26b/otm26b logistics/26b/wms26b scm/26b/demand26b scm/26b/inv26b scm/26b/maint26b scm/26b/mfg26b scm/26b/order26b scm/26b/plm26b scm/26b/proc26b scm/26b/sccv26b scm/26b/scp26b scm/26b/sop26b scm/26b/ssproc26b""",
'26c':"""erp/26c/fins26c erp/26c/ppm26c erp/26c/risk26c erp/26c/ssfin26c hcm/26c/amg-26c hcm/26c/benf-26c hcm/26c/comp-26c hcm/26c/hure-26c hcm/26c/lear-26c hcm/26c/payr-26c hcm/26c/recr-26c hcm/26c/tama-26c hcm/26c/tila-26c hcm/26c/woli-26c hcm/26c/wosc-26c logistics/26c/gtm26c logistics/26c/otm26c logistics/26c/wms26c scm/26c/demand26c scm/26c/inv26c scm/26c/maint26c scm/26c/mfg26c scm/26c/order26c scm/26c/plm26c scm/26c/proc26c scm/26c/sccv26c scm/26c/scp26c scm/26c/sop26c scm/26c/ssproc26c"""}
CACHE='/workspace/fut-raw/cache'; os.makedirs(CACHE,exist_ok=True)
def get(u):
    p=os.path.join(CACHE,re.sub(r'[^a-zA-Z0-9]','_',u)[-180:])
    if os.path.exists(p): return open(p).read()
    try: t=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read().decode('utf-8','ignore')
    except Exception as e: t=''
    open(p,'w').write(t); return t
def txt(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s))).replace('\xa0',' ').strip()
def book(path):
    base=f'{B}/{path}'; toc=get(base+'/toc.htm')
    title=txt(re.search(r'<title>(.*?)</title>',toc,re.S).group(1)) if '<title>' in toc else path
    links=re.findall(r'href="([^"#]+\.htm)[^"]*"[^>]*>(.*?)</a>',toc,re.S)
    fs=[a for a,b in links if txt(b)=='Feature Summary']; imp=[a for a,b in links if 'IMPORTANT' in txt(b)]
    rows=[]
    if fs:
        h=get(base+'/'+fs[0])
        seen=set()
        for tb in re.findall(r'<table class="rfs_table[^"]*".*?</table>',h,re.S):
            hd=[txt(x) for x in re.findall(r'<th[^>]*>(.*?)</th>',tb,re.S)]
            if 'Action to Enable' not in hd: continue
            ix={k:hd.index(k) for k in hd}
            for tr in re.findall(r'<tr>(.*?)</tr>',tb,re.S):
                td=re.findall(r'<td[^>]*>(.*?)</td>',tr,re.S)
                if len(td)<4: continue
                m=re.search(r'href="([^"#]+)',td[ix['Feature']])
                if not m or m.group(1) in seen: continue
                seen.add(m.group(1))
                rows.append(dict(module=txt(td[ix['Module']]),title=txt(td[ix['Feature']]),tags=' '.join(txt(x) for x in td[2:-2]),oracle_impact=txt(td[-2]),action=txt(td[-1]),url=base+'/'+m.group(1)))
    return dict(path=path,title=title,rows=rows,important=(base+'/'+imp[0]) if imp else None)
if __name__=='__main__':
  out={}
  for r,bs in BOOKS.items():
    with cf.ThreadPoolExecutor(8) as ex: out[r]=list(ex.map(book,bs.split()))
    print(r,[(b['path'].split('/')[-1],len(b['rows'])) for b in out[r]])
  json.dump(out,open('/workspace/fut-raw/summaries.json','w'),indent=1)

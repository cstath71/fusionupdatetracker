"""Weekly refresh checks (used by .github/workflows/weekly-refresh.yml). Read-only; exits 1 when the new data looks broken.

  python3 scripts/weekly_check.py crawl     after crawl.py: no tracked book may lose all its Feature Summary rows and no
                                            release may lose more than 2% of its rows, compared with data/updates.json in git HEAD
                                            (guards against Oracle blocking or changing its pages; then nothing is published)
  python3 scripts/weekly_check.py build     after build.py: no release may lose summaries or opt-in expirations, and prints
                                            CHANGED / UNCHANGED (data/updates.json compared with HEAD, ignoring 'generated')
"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.environ.get('FUT_RAW', '/workspace/fut-raw')
B = 'https://docs.oracle.com/en/cloud/saas/readiness'

def head():
    return json.loads(subprocess.check_output(['git', '-C', ROOT, 'show', 'HEAD:data/updates.json']))

def crawl():
    old, new = head()['updates'], json.load(open(os.path.join(RAW, 'summaries.json')))
    bad = []
    for rel, u in old.items():
        books = {f"{B}/{b['path']}/index.html": len(b['rows']) for b in new.get(rel.lower(), [])}
        total = sum(books.values())
        print(f"{rel}: {total} rows now, {u['total_features']} on the site")
        if total < u['total_features'] * 0.98: bad.append(f"{rel}: {total} rows vs {u['total_features']} on the site")
        for b in u['books']:
            if b['features'] and not books.get(b['url']): bad.append(f"{rel}: {b['product']} had {b['features']} rows, now none ({b['url']})")
    return bad

def build():
    old, new = head(), json.load(open(os.path.join(ROOT, 'data', 'updates.json')))
    bad = []
    for rel, u in old['updates'].items():
        n = new['updates'].get(rel)
        if not n: bad.append(f"{rel}: missing from the new build"); continue
        e0 = sum(1 for i in u['items'] if not i.get('summary')); e1 = sum(1 for i in n['items'] if not i.get('summary'))
        if e1 > e0: bad.append(f"{rel}: {e1} items without a summary (was {e0})")
        if len(n['expiring']) < len(u['expiring']) * 0.8: bad.append(f"{rel}: {len(n['expiring'])} opt-in expirations (was {len(u['expiring'])})")
        print(f"{rel}: {n['total_features']} features (was {u['total_features']}), {len(n['items'])} picked, {len(n['expiring'])} expirations")
    old.pop('generated', None); new.pop('generated', None)
    print('CHANGED' if old != new else 'UNCHANGED')
    return bad

if __name__ == '__main__':
    bad = {'crawl': crawl, 'build': build}[sys.argv[1]]()
    for b in bad: print('PROBLEM:', b)
    sys.exit(1 if bad else 0)

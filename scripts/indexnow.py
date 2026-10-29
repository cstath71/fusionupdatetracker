"""Ping IndexNow (Bing and others) for changed Fusion Updates URLs after a deploy.
Usage: python3 scripts/indexnow.py [url ...]
With no args, submits every URL in dist/sitemap.xml.
"""
import json, os, sys, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')
KEY = '888d7949179eeef4627d8a943b3068a4'
HOST = 'fusionupdates.com'
BASE = f'https://{HOST}'

def urls_from_sitemap():
    import re
    sm = open(os.path.join(DIST, 'sitemap.xml')).read()
    return re.findall(r'<loc>(.*?)</loc>', sm)

def ping(urls):
    body = json.dumps({
        'host': HOST,
        'key': KEY,
        'keyLocation': f'{BASE}/{KEY}.txt',
        'urlList': urls,
    }).encode()
    req = urllib.request.Request(
        'https://api.indexnow.org/indexnow',
        data=body,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read()

if __name__ == '__main__':
    urls = sys.argv[1:] or urls_from_sitemap()
    print(f'Pinging IndexNow for {len(urls)} URL(s)…')
    status, raw = ping(urls)
    print(status, raw[:200])

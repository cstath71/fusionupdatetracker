"""Answer-first 26D summaries, FAQPage text, dateModified and the Fusion Updates publisher.
Run after python3 scripts/rerender.py.
"""
import os, re, json, html, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')
R = lambda p: open(os.path.join(DIST, p), encoding='utf-8').read()

def lds(h):
    return [json.loads(m) for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)]

def nodes(h):
    out = []
    for o in lds(h):
        out.extend(o.get('@graph', [o]))
    return out

def visible(fragment):
    t = re.sub(r'<[^>]+>', ' ', fragment)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()

def block(h, eid):
    m = re.search(r'id="%s"[^>]*>(.*?)(?=<div class="(?:box|filters|nlc|hero)"|</main>)' % eid, h, re.S)
    # summary is a div.answer; faq is a div.box. Take the element itself more tightly.
    return m.group(0) if m else ''

def element(h, eid):
    m = re.search(r'<div[^>]*id="%s"[^>]*>' % eid, h)
    if not m:
        return ''
    i = m.start(); depth = 0
    for mm in re.finditer(r'<div\b|</div>', h[i:]):
        depth += 1 if mm.group(0) != '</div>' else -1
        if depth == 0:
            return h[i:i+mm.end()]
    return ''

def faq_visible(h):
    box = element(h, 'faq')
    qs = re.findall(r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>', box, re.S)
    return [(norm(visible(q)), norm(visible(a))) for q, a in qs]

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

def faq_ld(h):
    pages = [n for n in nodes(h) if n.get('@type') == 'FAQPage']
    if not pages:
        return []
    return [(norm(q['name']), norm(q['acceptedAnswer']['text'])) for q in pages[0]['mainEntity']]

OWNER = re.compile(r'\b(primelogic|stathopoulos|switzerland)\b', re.I)
DASH = re.compile('[\u2013\u2014]')

@unittest.skipUnless(os.path.exists(os.path.join(DIST, 'index.html')), 'dist not built')
class GeoAnswers(unittest.TestCase):
    def test_homepage_date_and_publisher(self):
        h = R('index.html')
        types = {n.get('@type'): n for n in nodes(h)}
        self.assertIn('WebPage', types)
        self.assertEqual(types['WebPage'].get('dateModified'), '2026-11-09')
        self.assertEqual(types['WebSite'].get('dateModified'), '2026-11-09')
        self.assertEqual(types['Organization'].get('name'), 'Fusion Updates')
        self.assertNotIn('author', json.dumps(nodes(h)))
        self.assertIn('Published by Fusion Updates.', h)
        self.assertIn('As of 9 November 2026', visible(h))
        self.assertIsNone(OWNER.search(visible(h)))

    def test_about_names_the_publisher_only(self):
        h = R('about.html')
        v = visible(h)
        self.assertIn('Published by Fusion Updates.', v)
        self.assertIsNone(OWNER.search(v))
        org = [n for n in nodes(h) if n.get('@type') == 'Organization']
        self.assertEqual(org[0]['name'], 'Fusion Updates')
        self.assertEqual([n for n in nodes(h) if n.get('@type') == 'WebPage'][0].get('dateModified'), '2026-11-09')
        self.assertNotIn('author', json.dumps(nodes(h)))

    def test_overview_financials_and_hcm_open_with_dated_answers(self):
        pages = {
            '26d/index.html': ('789', '23 former opt-ins now standard', '34 pages'),
            '26d/financials/index.html': ('73', 'Revenue Equipment Leases', '16 of the 25'),
            '26d/hcm/index.html': ('34 pages', '30 profile option codes', '1 migration notice'),
            'hcm-redwood/index.html': ('34 pages', '30 profile option codes', 'ORA_CMP_SPOTLIGHT_REDWOOD_ENABLED'),
        }
        for path, bits in pages.items():
            h = R(path)
            summary = visible(element(h, 'summary'))
            faq = visible(element(h, 'faq'))
            self.assertTrue(summary.startswith('In short: As of 9 November 2026'), path)
            self.assertGreaterEqual(len(faq_visible(h)), 3, path)
            self.assertEqual(faq_visible(h), faq_ld(h), path)
            blob = summary + ' ' + faq
            for bit in bits:
                self.assertIn(bit, blob, path)
            self.assertNotIn('mandatory', blob.lower(), path)
            self.assertIsNone(DASH.search(blob), path)
            self.assertIsNone(OWNER.search(blob), path)
            self.assertIn('now standard', blob, path)
            page = [n for n in nodes(h) if n.get('@type') == 'WebPage'][0]
            self.assertEqual(page.get('dateModified'), '2026-11-09', path)
            pub = page.get('publisher') or {}
            self.assertEqual(pub.get('name'), 'Fusion Updates', path)
            self.assertIn('Published by Fusion Updates.', h, path)
            self.assertNotIn('"author"', json.dumps(nodes(h)), path)

    def test_llms_lists_key_26d_counts(self):
        ll = R('llms.txt'); full = R('llms-full.txt')
        for text in (ll, full):
            self.assertIn('https://fusionupdates.com/26d/', text)
            self.assertIn('https://fusionupdates.com/26d/financials/', text)
            self.assertIn('https://fusionupdates.com/26d/hcm/', text)
            self.assertIn('https://fusionupdates.com/hcm-redwood/', text)
            self.assertIn('789 features', text)
            self.assertIn('23 former opt-ins now standard', text)
            self.assertIn('34 pages', text)
            self.assertIn('73 features', text)
            self.assertIn('Revenue Equipment Leases', text)
            self.assertIn('30 profile option codes', text)
            self.assertIn('Published by Fusion Updates.', text)
            self.assertNotIn('mandatory', text.lower())
            self.assertIsNone(OWNER.search(text))
            self.assertIsNone(DASH.search(text))
        self.assertIn('What changed in Oracle Fusion 26D?', full)
        self.assertIn('What are the new features in Oracle Fusion Financials 26D?', full)
        self.assertIn('How many Oracle HCM pages switch to Redwood by default in 26D?', full)

if __name__ == '__main__':
    unittest.main()

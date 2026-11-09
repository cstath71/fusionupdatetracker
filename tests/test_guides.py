"""Offline checks for the gap SEO/AEO guide pages (scripts/guides.py). Run after python3 scripts/build.py."""
import os, re, json, html, unittest, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')
R = lambda p: open(os.path.join(DIST, p), encoding='utf-8').read()
T = lambda h: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h))).strip()

def lds(h):
    return [json.loads(m) for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)]

PAGES = [
    '26d/dates/index.html',
    '26d/fusion-claw-ai-agent-studio/index.html',
    'guides/opt-in-and-enablement/index.html',
    'redwood-defaults/index.html',
    'guides/prepare-for-quarterly-update/index.html',
]
# Our voice never says updates/opt-ins are "mandatory" (Gus: say "now standard").
# Oracle's own feature titles may contain "Mandatory Migration" — those quotes stay.
OWN_MANDATORY = re.compile(r'\b(updates? are mandatory|quarterly updates? (are )?mandatory|mandatory (for|to) (all )?customers)\b', re.I)
OWNER = re.compile(r'\b(primelogic|stathopoulos|switzerland)\b', re.I)

@unittest.skipUnless(os.path.exists(os.path.join(DIST, 'index.html')), 'dist not built')
class Guides(unittest.TestCase):
    def test_pages_exist_with_summary_faq_and_one_h1(self):
        for p in PAGES:
            h = R(p)
            self.assertEqual(len(re.findall(r'<h1[ >]', h)), 1, p)
            self.assertIn('id="summary"', h, p)
            self.assertIn('id="faq"', h, p)
            self.assertIn('In short:', h, p)
            faq = [x for o in lds(h) for x in o.get('@graph', [o]) if x.get('@type') == 'FAQPage']
            self.assertTrue(faq, p)
            self.assertGreaterEqual(len(faq[0]['mainEntity']), 3, p)
            self.assertIn('hello@fusionupdates.com', h, p)  # newsletter signup present
            self.assertIn('class="brand"', h, p)  # logo/brand on the left via header
            self.assertIsNone(OWN_MANDATORY.search(T(h)), p)
            self.assertIsNone(OWNER.search(T(h)), p)

    def test_dates_cite_oracle_and_do_not_invent_days(self):
        h = R('26d/dates/index.html'); v = T(h)
        self.assertIn('blogs.oracle.com/fusioninsider/quarterly-updates-made-easy', h)
        self.assertIn('release-planning1.html', h)
        self.assertIn('docs.oracle.com/en/cloud/saas/readiness/index.html', h)
        for c in ('Cohort A', 'Cohort B', 'Cohort C'):
            self.assertIn(c, v)
        self.assertIn('Oracle Cloud Console', v)
        self.assertIn('November', v)
        self.assertIn('December', v)
        self.assertIn('January', v)
        self.assertIn('10 Dec 2025', v)  # publication date of the Oracle article, not a 26D window
        # Calculated 26D Fridays are not on the page.
        self.assertIsNone(re.search(r'\b(?:Fri|Mon|Tue|Wed|Thu|Sat|Sun)\b', v))
        for bad in ('6 Nov', '20 Nov', '4 Dec', '18 Dec', '1 Jan', '15 Jan', 'Nov 2026', 'Dec 2026', 'Jan 2027'):
            self.assertNotIn(bad, v)
        with open(os.path.join(ROOT, 'data', 'updates.json'), encoding='utf-8') as _f:
            u = json.load(_f)['updates']['26D']
        self.assertIn(str(len(u['all'])), v)

    def test_ai_page_lists_only_verified_rows(self):
        h = R('26d/fusion-claw-ai-agent-studio/index.html'); v = T(h)
        with open(os.path.join(ROOT, 'data', 'updates.json'), encoding='utf-8') as _f:
            updates = json.load(_f)['updates']
        pat = re.compile(r'\b(?:fusion claw|ai agent studio|agent studio)\b', re.I)
        urls = []
        for rel, u in updates.items():
            seen = set()
            for r in (u.get('items') or []) + (u.get('all') or []):
                blob = ' '.join(r.get(k) or '' for k in ('title', 'module', 'tags'))
                if pat.search(blob) and r.get('url') and r['url'] not in seen:
                    seen.add(r['url']); urls.append(r['url'])
        self.assertGreaterEqual(len(urls), 1)
        for url in urls:
            self.assertIn(url, h, url)
        self.assertIn('26D-procurement-wn-f51463.htm', h)
        self.assertIn('Fusion AI Agent Studio Support', v)
        self.assertIn('AI Agent Studio - Seeded Business Objects', v)
        self.assertNotIn('Asset Additions Assistant', v)
        self.assertNotIn('Storage location assistant', v)
        self.assertIsNone(re.search(r'\b(AI unit budget|guardrail budget|\d+\s+guardrail)\b', v, re.I))
        self.assertIn('do not publish', v)
        self.assertNotIn('mandatory', v.lower())

    def test_optin_guide_uses_26d_bucket_counts(self):
        with open(os.path.join(ROOT, 'data', 'updates.json'), encoding='utf-8') as _f: u = json.load(_f)['updates']['26D']
        h = R('guides/opt-in-and-enablement/index.html'); v = T(h)
        self.assertIn(str(len(u['all'])), v)
        self.assertIn('now standard', v)
        self.assertIn('Action to Enable', v)

    def test_prepare_replaces_old_guides_url(self):
        stub = R('guides/how-oracle-fusion-updates-work/index.html')
        self.assertIn('http-equiv="refresh"', stub)
        self.assertIn('/guides/prepare-for-quarterly-update/', stub)
        self.assertIn('rel="canonical"', stub)
        self.assertIn('noindex', stub)
        self.assertIn('class="brand"', stub)
        h = R('guides/prepare-for-quarterly-update/index.html')
        self.assertIn('what-to-test checklist', T(h))
        self.assertIn('26d/dates/', h)

    def test_sitemap_llms_and_hub_links(self):
        sm = R('sitemap.xml'); ll = R('llms.txt'); home = R('index.html'); hub = R('26d/index.html')
        for path in ('26d/dates/', '26d/fusion-claw-ai-agent-studio/', 'guides/opt-in-and-enablement/',
                     'redwood-defaults/', 'guides/prepare-for-quarterly-update/'):
            self.assertIn(f'<loc>https://fusionupdates.com/{path}</loc>', sm)
            self.assertIn(f'https://fusionupdates.com/{path}', ll)
            self.assertIn(path, home)
            self.assertIn(path, hub)
        # old 404 path is a redirect stub, not in sitemap
        self.assertNotIn('how-oracle-fusion-updates-work', sm)

    def test_redwood_calendar_lists_releases(self):
        h = R('redwood-defaults/index.html'); v = T(h)
        self.assertIn('26D', v)
        self.assertIn('hcm-redwood', h)
        self.assertIn('Redwood', v)
        self.assertIn('id="r27a"', h)
        self.assertIn('id="r27b"', h)
        self.assertIn('id="r27c"', h)
        self.assertIn('Oracle has not published a full 27A', v)
        self.assertIn('Oracle has not published a full 27B', v)
        self.assertIn('Oracle has not published a full 27C', v)
        self.assertNotIn('mandatory', v.lower())

    def test_no_ics_and_dataset_labels_26d_current(self):
        self.assertFalse(os.path.exists(os.path.join(DIST, 'downloads', 'fusion-quarterly-update-calendar.ics')))
        self.assertFalse(os.path.exists(os.path.join(ROOT, 'assets', 'downloads', 'fusion-quarterly-update-calendar.ics')))
        dl = T(R('downloads/index.html'))
        self.assertNotIn('.ics', dl)
        self.assertIn('does not list calculated calendar dates', dl)
        self.assertIn('does not offer one', dl)
        self.assertIn('first Friday', dl)
        self.assertIn('third Friday', dl)
        for bad in ('6 Nov', '20 Nov', '4 Dec', '18 Dec', '1 Jan', '15 Jan'):
            self.assertNotIn(bad, dl)
        home = R('index.html')
        self.assertIn('26D (current)', home)
        self.assertNotIn('26D (next)', home)
        self.assertNotIn('26C (current)', home)
        self.assertNotIn('typical 26D test and production dates', home)
        pdf = os.path.join(ROOT, 'assets', 'downloads', 'fusion-26d-readiness-checklist.pdf')
        self.assertTrue(os.path.exists(pdf))
        out = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True, check=True)
        pdf_text = re.sub(r'\s+', ' ', out.stdout)
        for bad in ('20 Nov', '4 Dec', '18 Dec', '1 Jan', '15 Jan', 'Jan 2027', 'typical dates'):
            self.assertNotIn(bad, pdf_text, bad)
        self.assertIn('first Friday', pdf_text)
        self.assertIn('does not print a Friday', pdf_text)

    def test_prepare_does_not_print_calculated_fridays(self):
        v = T(R('guides/prepare-for-quarterly-update/index.html'))
        self.assertIsNone(re.search(r'\b(?:Fri|Mon|Tue|Wed|Thu|Sat|Sun)\b', v))
        self.assertNotIn('6 Nov', v)
        self.assertIn('now standard', v)
        self.assertNotIn('mandatory', v.lower())

if __name__ == '__main__':
    unittest.main()

"""Offline checks for the gap SEO/AEO guide pages (scripts/guides.py). Run after python3 scripts/build.py."""
import os, re, json, html, unittest
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

    def test_dates_cite_oracle_insider_and_show_cohorts(self):
        h = R('26d/dates/index.html'); v = T(h)
        self.assertIn('blogs.oracle.com/fusioninsider/quarterly-updates-made-easy', h)
        for c in ('Cohort A', 'Cohort B', 'Cohort C'):
            self.assertIn(c, v)
        self.assertIn('Oracle Cloud Console', v)
        # derived 26D windows (rule: first/third Friday)
        self.assertIn('Nov 2026', v)
        self.assertIn('Dec 2026', v)
        self.assertIn('Jan 2027', v)

    def test_ai_page_is_honest_about_claw_and_agent_studio(self):
        h = R('26d/fusion-claw-ai-agent-studio/index.html'); v = T(h)
        self.assertIn('do not currently include a row titled Fusion Claw', v)
        self.assertIn("What's New", v)
        # must not invent AI-unit / guardrail numbers
        self.assertIsNone(re.search(r'\b(AI unit|guardrail budget)\b', v, re.I))

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

if __name__ == '__main__':
    unittest.main()

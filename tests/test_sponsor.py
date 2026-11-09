"""Sponsor stays hidden (SHOW_SPONSORS off) but /sponsor.html is a noindex redirect, not a 404.
The stub follows the retired-guides redirect and stays out of the sitemap and nav.
Run after python3 scripts/rerender.py (the dist checks) ; the writer checks do not need a full rebuild.
"""
import os, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import render  # noqa: E402
import guides  # noqa: E402

HOME = 'https://fusionupdates.com/'

def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def assert_stub(testcase, html):
    testcase.assertIn('<meta http-equiv="refresh" content="0;url=https://fusionupdates.com/">', html)
    testcase.assertIn("location.replace('https://fusionupdates.com/')", html)
    testcase.assertIn('<a href="https://fusionupdates.com/">Fusion Updates home page</a>', html)
    testcase.assertIn('<meta name="robots" content="noindex">', html)
    testcase.assertIn('<link rel="canonical" href="https://fusionupdates.com/">', html)
    testcase.assertIn('class="brand"', html)
    testcase.assertNotIn('Sponsor Fusion Updates', html)
    testcase.assertNotIn('<nav', html)
    testcase.assertNotIn('\u2014', html)
    testcase.assertNotIn('\u2013', html)

class SponsorRedirect(unittest.TestCase):
    def test_flag_off_writes_home_redirect(self):
        self.assertFalse(render.SHOW_SPONSORS)
        with tempfile.TemporaryDirectory() as d:
            render.write_sponsor(d)
            html = read(os.path.join(d, 'sponsor.html'))
        assert_stub(self, html)

    def test_flag_on_writes_the_real_page(self):
        prev = render.SHOW_SPONSORS
        render.SHOW_SPONSORS = True
        try:
            with tempfile.TemporaryDirectory() as d:
                render.write_sponsor(d)
                html = read(os.path.join(d, 'sponsor.html'))
            self.assertIn('<h1>Sponsor Fusion Updates</h1>', html)
            self.assertIn('href="sponsor.html">Sponsor</a>', html)
            self.assertNotIn('name="robots" content="noindex"', html)
            self.assertNotIn('http-equiv="refresh"', html)
        finally:
            render.SHOW_SPONSORS = prev

    def test_guides_redirect_still_uses_the_same_writer(self):
        with tempfile.TemporaryDirectory() as d:
            guides._redirect_stub(
                d, 'guides/how-oracle-fusion-updates-work',
                HOME + 'guides/prepare-for-quarterly-update/',
                'Prepare for an Oracle Fusion Cloud quarterly update')
            html = read(os.path.join(d, 'guides/how-oracle-fusion-updates-work/index.html'))
        self.assertIn('http-equiv="refresh" content="0;url=/guides/prepare-for-quarterly-update/"', html)
        self.assertIn("location.replace('/guides/prepare-for-quarterly-update/')", html)
        self.assertIn('rel="canonical" href="https://fusionupdates.com/guides/prepare-for-quarterly-update/"', html)
        self.assertIn('name="robots" content="noindex"', html)
        self.assertIn('href="../../style.css"', html)
        self.assertIn('class="brand" href="../../"', html)
        live = os.path.join(DIST, 'guides/how-oracle-fusion-updates-work/index.html')
        if os.path.exists(live):
            self.assertEqual(html, read(live))

    @unittest.skipUnless(os.path.exists(os.path.join(DIST, 'index.html')), 'dist not built')
    def test_dist_stub_is_out_of_sitemap_and_nav(self):
        assert_stub(self, read(os.path.join(DIST, 'sponsor.html')))
        sitemap = read(os.path.join(DIST, 'sitemap.xml'))
        self.assertNotIn('sponsor.html', sitemap)
        for page in ('index.html', 'about.html', '26d/index.html', 'llms.txt'):
            self.assertNotIn('sponsor.html', read(os.path.join(DIST, page)), page)

if __name__ == '__main__':
    unittest.main()

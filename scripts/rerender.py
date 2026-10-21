#!/usr/bin/env python3
"""Re-render dist/ from the saved data/updates.json without fetching anything from Oracle (template-only changes).
Keeps the data's own 'generated' date, so the footer date, dateModified and sitemap lastmod stay the date of the last refresh.
Usage: python3 scripts/rerender.py [outdir]   (default: dist)"""
import json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE); sys.path.insert(0,HERE)
os.environ.setdefault('FUT_CONTACT','hello@fusionupdates.com')
import render
d=json.load(open(os.path.join(ROOT,'data','updates.json')))
render.render(d['updates'],sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,'dist'),upcoming=d['upcoming'],generated=d['generated'],current=d['current'])

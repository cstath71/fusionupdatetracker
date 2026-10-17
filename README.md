# Fusion Updates (fusionupdates.com), repo: fusionupdatetracker

A static site that tracks Oracle Fusion Cloud quarterly updates (26B, 26C) across Financials, Procurement, SCM, Logistics, Project Management and HCM.

- `scripts/crawl.py` reads the Feature Summary tables from Oracle readiness docs into `/workspace/fut-raw/summaries.json` (HTTP responses are cached in `/workspace/fut-raw/cache`).
- `scripts/build.py` picks the top changes per module family (`PER_FAMILY=25`), pulls 1-2 sentence summaries from each Oracle feature page, sets draft impact and enablement, and writes `data/updates.json` and `dist/`.
- `scripts/render.py` holds the HTML templates (home, update pages, checklists, newsletter, sponsor, about).

Rebuild: `python3 scripts/crawl.py && python3 scripts/build.py`
Preview: `cd dist && python3 -m http.server 4321`, then open http://localhost:4321
Add an update: add its book paths to `BOOKS` in crawl.py and a link in the render.py nav.

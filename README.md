# Fusion Updates (fusionupdates.com), repo: fusionupdatetracker

A static site that tracks Oracle Fusion Cloud quarterly updates (26B, 26C) across Financials, Procurement, SCM, Logistics, Project Management and HCM.

- `scripts/crawl.py` reads the Feature Summary tables from Oracle readiness docs into `/workspace/fut-raw/summaries.json` (HTTP responses are cached in `/workspace/fut-raw/cache`).
- `scripts/build.py` picks the top changes per module family (`PER_FAMILY=25`), pulls 1-2 sentence summaries from each Oracle feature page, sets an automatic first-pass impact and enablement, applies the reviewed ratings and summaries in `data/editorial.json`, and writes `data/updates.json` and `dist/`.
- `scripts/render.py` holds the HTML templates (home, update pages, checklists, newsletter, sponsor, about).

Rebuild: `python3 scripts/crawl.py && python3 scripts/build.py`
Preview: `cd dist && python3 -m http.server 4321`, then open http://localhost:4321
Add an update: add its book paths to `BOOKS` in crawl.py and a link in the render.py nav.

Free downloads and share cards:
- `python3 scripts/leadmagnets.py` builds `assets/downloads/` (the 26D readiness checklist PDF and the quarterly update calendar .ics). It uses only `data/updates.json`, `data/hcm_redwood.json` and Oracle's published cohort rule. Run it before `build.py`.
- `scripts/og.py` draws the 1200x627 Open Graph cards into `assets/og/` with headless Chrome during `build.py`. Cards are cached by content hash, so only new or changed ones are redrawn.
- Each page gets a compact signup box under its H1/intro, with copy written for that page (`cta_for` in render.py), plus the footer form and a sticky "Subscribe" link on mobile. All forms post to the same `fut-subscribe` function.

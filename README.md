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
- Newsletter sync is automatic: `fut-subscribe` (`supabase/functions/fut-subscribe/`) stores the row in `fut_subscribers`, then adds the email to the Resend segment FusionUpdateTracker (`a3689e22-cd3d-4f0a-98cb-dd7f195a081b`) and stamps `synced_to_resend_at`. Existing Resend contacts are added without changing their unsubscribe status. The Resend key and segment id come from function secrets if set, else from Supabase Vault via `public.fut_resend_config()` (service_role only; `supabase/migrations/20261017_fut_resend_config.sql`). New subscribed contacts get the welcome email automatically: the function fires `fut.subscribed` (Vault secret `fut_welcome_enabled` = `true`, on since 17 Oct 2026; never for existing contacts or test domains). The daily manual sync is retired; a quick check (unsubscribe pull-back) runs before each broadcast. Unsubscribes are pulled back manually (`/workspace/newsletter/sync_subscribers.md` Step 3).

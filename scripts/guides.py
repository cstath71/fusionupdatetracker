"""Gap SEO/AEO guide pages (keyword research 29 Oct 2026):
  /26d/dates/                              26D cohort dates from Oracle's published rule
  /26d/fusion-claw-ai-agent-studio/        AI/agent rows from our What's New extract only
  /guides/opt-in-and-enablement/           evergreen enablement explainer (26D figures as examples)
  /redwood-defaults/                       consolidated Redwood defaults calendar
  /guides/prepare-for-quarterly-update/    prepare / test-window playbook
Also writes a redirect stub at /guides/how-oracle-fusion-updates-work/ (404 on live; no internal linker found).
Called from render.render(); returns sitemap paths (redirect stub is omitted from sitemap).
"""
import os, re, calendar, datetime, collections
import render as R
E = R.E

FI = 'https://blogs.oracle.com/fusioninsider/quarterly-updates-made-easy'
OPTIN = 'https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html'
COH = {'A': (2, 5, 8, 11), 'B': (3, 6, 9, 12), 'C': (4, 7, 10, 1)}
QIDX = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
HOL = {datetime.date(2027, 1, 1): "This date is New Year's Day. Oracle may schedule this cohort differently, so confirm yours in the Oracle Cloud Console."}
AI_TITLE = re.compile(r'\b(ai agent|agentic|agent studio|fusion claw|\bclaw\b|assistant)\b', re.I)

def _fridays(y, m):
    fs = [d for d in range(1, calendar.monthrange(y, m)[1] + 1) if datetime.date(y, m, d).weekday() == 4]
    return datetime.date(y, m, fs[0]), datetime.date(y, m, fs[2])

def windows(rel):
    """Typical test/production Fridays from Oracle's published cohort rule (same as leadmagnets.py)."""
    y = 2000 + int(rel[:2]); q = QIDX[rel[2]]; res = []
    for c, ms in COH.items():
        m = ms[q]; yy = y + 1 if (c == 'C' and q == 3) else y
        t, p = _fridays(yy, m); res.append((c, t, p))
    return res

def _fmt(d):
    return f"{d:%a %-d %b %Y}" if os.name != 'nt' else d.strftime('%a %d %b %Y').replace(' 0', ' ')

def _fmt_safe(d):
    return f"{d.strftime('%a')} {d.day} {d.strftime('%b %Y')}"

def _ld(path, title, desc, cl, faq=None, extra=None):
    g = [{"@type": "WebPage", "@id": R.BASE + '/' + path, "url": R.BASE + '/' + path, "name": title,
          "description": desc, "inLanguage": "en", "isPartOf": {"@type": "WebSite", "@id": R.BASE + "/#website", "name": R.SITE, "url": R.BASE + "/"}},
         R.crumbs(cl)]
    if faq: g.append(R.faq_ld(faq))
    if extra: g.append(extra)
    return R.jsonld({"@context": "https://schema.org", "@graph": g})

def _related_guides(cur, depth='../../'):
    pages = [
        ('26d/dates/', '26D release dates and cohorts'),
        ('guides/opt-in-and-enablement/', 'How opt-in and enablement work'),
        ('redwood-defaults/', 'Redwood defaults calendar'),
        ('guides/prepare-for-quarterly-update/', 'Prepare for a quarterly update'),
        ('26d/fusion-claw-ai-agent-studio/', 'AI and agentic features in 26D'),
    ]
    lk = ' · '.join(f'<a href="{depth}{p}">{E(n)}</a>' for p, n in pages if p != cur)
    return f'<div class="box"><p><b>Related guides:</b> {lk} · <a href="{depth}26d/">26D hub</a> · <a href="{depth}downloads/">Free downloads</a></p></div>'

def _oracle_rule_note():
    return (f'<p class="small muted">Source for the cohort rule: <a href="{FI}" target=_blank rel=noopener>Oracle Fusion Insider, '
            f'"Quarterly updates made easy"</a> (published 10 Dec 2025). Oracle publishes the rule rather than a public '
            f'list of dates for every environment. Confirm your own dates in the Oracle Cloud Console. Middle East regions '
            f'update on the Thursday before each Friday.</p>')

# ---------- 1. /26d/dates/ ----------
def dates_page(updates):
    rel = '26D'; path = '26d/dates/'; u = updates[rel]
    wins = windows(rel)
    on = sum(1 for e in u['expiring'] if e['now_enabled'] == 'Yes')
    st = len(u['expiring']) - on
    rows = ''.join(
        f'<tr><td>Cohort {c}</td><td>{_fmt_safe(t)}</td><td>{_fmt_safe(p)}</td><td>{E(HOL.get(t, "—"))}</td></tr>'
        for c, t, p in wins)
    title = 'Oracle Fusion 26D release dates and cohorts'
    desc = ('Typical Oracle Fusion Cloud 26D test and production update dates for Cohorts A, B and C, derived from '
            'Oracle\'s published cohort rule, plus links to what changes in 26D.')
    cl = [('Home', ''), ('26D', '26d/'), ('Release dates', path)]
    summary = (f'Oracle Fusion Cloud <b>26D</b> is the fourth 2026 quarterly update. Per Oracle\'s published rule, '
               f'test environments take the update on the <b>first Friday</b> of the cohort month and production on the '
               f'<b>third Friday</b>, two weeks later. Typical dates: Cohort A {_fmt_safe(wins[0][1])} / {_fmt_safe(wins[0][2])}, '
               f'Cohort B {_fmt_safe(wins[1][1])} / {_fmt_safe(wins[1][2])}, Cohort C {_fmt_safe(wins[2][1])} / {_fmt_safe(wins[2][2])}. '
               f'These are derived from Oracle\'s rule, not a published per-environment calendar — confirm yours in the Oracle Cloud Console. '
               f'On the content side, Oracle\'s 26D What\'s New lists <b>{len(u["all"])}</b> features across the modules we cover: '
               f'<b>{sum(1 for r in u["all"] if R.bucket(r["action"])=="on")}</b> on by default, '
               f'<b>{sum(1 for r in u["all"] if R.bucket(r["action"])=="opt")}</b> opt-in, and '
               f'<b>{len(u["expiring"])}</b> former opt-ins that are now standard with 26D '
               f'(<b>{on}</b> switch on for everyone, <b>{st}</b> need setup).')
    faq = [
        ('When does Oracle Fusion 26D update my environments?',
         f'It depends on your cohort. Applying Oracle\'s published rule (test on the first Friday of the update month, production on the third) gives Cohort A {_fmt_safe(wins[0][1])} / {_fmt_safe(wins[0][2])}, Cohort B {_fmt_safe(wins[1][1])} / {_fmt_safe(wins[1][2])}, and Cohort C {_fmt_safe(wins[2][1])} / {_fmt_safe(wins[2][2])}. Confirm your cohort and exact dates in the Oracle Cloud Console. Source: <a href="{FI}" target=_blank rel=noopener>Oracle Fusion Insider</a>.'),
        ('Which months are Cohorts A, B and C?',
         'Per Oracle Fusion Insider: Cohort A is February, May, August and November; Cohort B is March, June, September and December; Cohort C is April, July, October and January. 26D is the fourth 2026 release, so those months are November 2026, December 2026 and January 2027.'),
        ('Are these Oracle-published dates for my pod?',
         'No. Oracle publishes the cohort rule; it does not publish a public list of every environment\'s date. The table on this page applies that rule. Always confirm your own dates in the Oracle Cloud Console.'),
        ('What should I do in the two-week test window?',
         f'Start with the <a href="../../updates/26d/checklist.html">26D what-to-test checklist</a>, review <a href="../on-by-default/">features on by default</a> and <a href="../opt-in-features/">opt-ins</a>, and decide which of the <a href="../former-opt-ins-now-standard/">{len(u["expiring"])} former opt-ins now standard</a> need setup. See also <a href="../../guides/prepare-for-quarterly-update/">Prepare for a quarterly update</a>.'),
    ]
    body = f"""{R.crumbs_html(cl, '../../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">Typical test and production Fridays for Oracle Fusion Cloud 26D, by cohort, from Oracle&#39;s published update rule. Use them to plan the two-week window; confirm your own dates in the Oracle Cloud Console.</p>
{R.summary_html(summary)}{_oracle_rule_note()}</div>
<div class="box"><h2 style="margin-top:0">Typical 26D dates by cohort</h2>
<table><tr><th>Cohort</th><th>Test environments</th><th>Production</th><th>Note</th></tr>{rows}</table>
<p class="small muted">Cohort months for 26D (fourth 2026 release): A = November 2026, B = December 2026, C = January 2027.</p></div>
<div class="box"><h2 style="margin-top:0">What changes when 26D lands</h2>
<p>Oracle&#39;s 26D What&#39;s New documents list <b>{len(u['all'])}</b> features across the modules Fusion Updates covers. Use these lists for the content of the update:</p>
<ul class="check">
<li><a href="../">26D hub: what&#39;s new by module and the opt-in expiration list</a></li>
<li><a href="../on-by-default/">Features on by default</a> · <a href="../opt-in-features/">Opt-in features</a> · <a href="../former-opt-ins-now-standard/">Former opt-ins now standard ({len(u['expiring'])})</a></li>
<li><a href="../../updates/26d/checklist.html">26D what-to-test checklist</a> · <a href="../../downloads/">Free checklist PDF and calendar (.ics)</a></li>
</ul></div>
{R.faq_html(faq)}{_related_guides(path)}{R.nl_form()}"""
    return path, R.page(title, body, 2, desc, path, _ld(path, title, desc, cl, faq),
                        og=('Oracle Fusion Cloud 26D · dates', 'Typical Cohort A/B/C test and production Fridays'))

# ---------- 2. /26d/fusion-claw-ai-agent-studio/ ----------
def _ai_rows(u):
    """Rows whose Oracle title mentions AI agent / agentic / assistant / claw / agent studio. Deduped by title+family."""
    seen, out = set(), []
    for r in u['all']:
        if not AI_TITLE.search(r.get('title', '')): continue
        k = (r['title'].lower(), r['family'])
        if k in seen: continue
        seen.add(k); out.append(r)
    return out

def ai_page(updates):
    rel = '26D'; path = '26d/fusion-claw-ai-agent-studio/'; u = updates[rel]
    rows = _ai_rows(u)
    # Agent Studio / Claw specifically
    claw = [r for r in rows if re.search(r'\bclaw\b|agent studio', r['title'], re.I)]
    # Cross-release Agent Studio from our extract (honest cross-link, still our data)
    studio_prior = []
    for k in ('26C', '26B'):
        if k not in updates: continue
        for r in updates[k]['all']:
            if 'agent studio' in r['title'].lower() or re.search(r'\bclaw\b', r['title'], re.I):
                studio_prior.append(dict(r, _rel=k))
    # dedupe prior by title+rel
    seen, prior = set(), []
    for r in studio_prior:
        k = (r['title'].lower(), r['_rel'])
        if k in seen: continue
        seen.add(k); prior.append(r)

    byf = collections.OrderedDict()
    for f in R.FSLUG:
        x = [r for r in rows if r['family'] == f]
        if x: byf[f] = x
    def _tbl(rs):
        return ('<table><tr><th>Feature (Oracle title)</th><th>Product · module</th><th>Action to Enable</th><th>Oracle scale</th></tr>' +
                ''.join(f'<tr><td><a href="{E(r["url"])}" target=_blank rel=noopener>{E(r["title"])}</a></td>'
                        f'<td>{E(r["product"])} · {E(r["module"])}</td>'
                        f'<td><span class="pill">{E(r["action"])}</span></td><td>{E(r["oracle_impact"])}</td></tr>' for r in rs) + '</table>')
    groups = ''.join(f'<div class="box" id="f-{R.FSLUG[f]}"><h2 style="margin-top:0">{E(R.FNAME[f])} ({len(x)})</h2>{_tbl(x)}'
                     f'<p class="small"><a href="../{R.FSLUG[f]}/">All {E(R.FNAME[f])} features in 26D →</a></p></div>'
                     for f, x in byf.items())
    prior_html = ''
    if prior:
        prior_html = ('<div class="box"><h2 style="margin-top:0">AI Agent Studio in earlier releases we track</h2>'
                      '<p class="small muted">These rows are in our What\'s New extract for 26B/26C (not 26D). Titles and Action to Enable are Oracle\'s.</p>'
                      '<table><tr><th>Release</th><th>Feature (Oracle title)</th><th>Action to Enable</th></tr>' +
                      ''.join(f'<tr><td>{E(r["_rel"])}</td><td><a href="{E(r["url"])}" target=_blank rel=noopener>{E(r["title"])}</a></td>'
                              f'<td><span class="pill">{E(r["action"])}</span></td></tr>' for r in prior) + '</table></div>')

    honest = ('Oracle\'s 26D What\'s New Feature Summary tables for the modules we cover do <b>not</b> currently include a row titled '
              '<b>Fusion Claw</b> or <b>AI Agent Studio</b>. Partner writeups often use those names; this page only lists rows that '
              f'already appear in our extract. We found <b>{len(rows)}</b> 26D features whose Oracle title mentions an AI agent, '
              f'an agentic app, or an assistant'
              + (f', and none titled Fusion Claw or AI Agent Studio' if not claw else f', including {len(claw)} titled Fusion Claw or AI Agent Studio')
              + '.')

    title = 'AI agents and agentic apps in Oracle Fusion 26D'
    desc = (f'{len(rows)} Oracle Fusion 26D features whose titles mention an AI agent, agentic app or assistant, '
            f'from the Feature Summary tables for the modules Fusion Updates covers. No invented AI metrics.')
    cl = [('Home', ''), ('26D', '26d/'), ('AI and agentic features', path)]
    summary = (f'<b>Honest scope:</b> {honest} Enablement below is Oracle\'s Action to Enable column. '
               f'Start from the <a href="../../updates/26d/">26D changes list</a> and confirm behaviour in your test pod before production.')
    faq = [
        ('Does Fusion Updates list Fusion Claw in 26D?',
         'Not under that title. As of our current 26D What\'s New extract for Financials, Procurement, SCM, Logistics, Projects and HCM, no Feature Summary row is titled Fusion Claw. If Oracle publishes one later for a module we cover, the weekly refresh will pick it up.'),
        ('Does Fusion Updates list AI Agent Studio in 26D?',
         f'Not in the 26D Feature Summary tables for the modules we cover. Our extract does include AI Agent Studio rows in earlier releases ({", ".join(sorted({r["_rel"] for r in prior}) or ["none yet"])}). See the earlier-releases section on this page.'),
        (f'How many 26D features mention AI agents or assistants?',
         f'{len(rows)} unique features (by title and module family) in Oracle\'s 26D What\'s New for the modules we cover, matching titles that contain AI agent, agentic, assistant, claw or agent studio.'),
        ('Where do the enablement labels come from?',
         'Oracle\'s Action to Enable column on each feature\'s What\'s New row. We copy it; we do not invent AI-unit budgets or guardrail counts.'),
    ]
    body = f"""{R.crumbs_html(cl, '../../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">What our 26D What&#39;s New extract actually contains for AI agents, agentic apps and assistants — and what it does not.</p>
{R.summary_html(summary)}
<p class="small muted">Every row below comes from Oracle&#39;s Feature Summary tables in the 26D What&#39;s New documents for the modules we cover. Titles and Action to Enable are Oracle&#39;s. We recheck them every week.</p></div>
<div class="box"><h2 style="margin-top:0">26D rows we can verify ({len(rows)})</h2>
<p class="small muted">Matched on Oracle&#39;s feature title containing &quot;AI agent&quot;, &quot;agentic&quot;, &quot;assistant&quot;, &quot;claw&quot; or &quot;agent studio&quot;. Duplicate titles that appear in more than one book of the same family are listed once.</p></div>
{groups if groups else '<div class="box"><p>No matching rows in the current extract.</p></div>'}
{prior_html}
{R.faq_html(faq)}{_related_guides(path)}{R.nl_form()}"""
    return path, R.page(title, body, 2, desc, path, _ld(path, title, desc, cl, faq),
                        og=('Oracle Fusion Cloud 26D · AI', f'{len(rows)} AI agent / agentic / assistant rows from our extract'))

# ---------- 3. /guides/opt-in-and-enablement/ ----------
def optin_guide(updates):
    path = 'guides/opt-in-and-enablement/'
    u = updates['26D']; allr = u['all']; es = u['expiring']
    bc = R.bucket_counts(allr)
    on = sum(1 for e in es if e['now_enabled'] == 'Yes'); st = len(es) - on
    title = 'How Oracle Fusion opt-in and enablement work'
    desc = ('Plain-English guide to Oracle Fusion Cloud Action to Enable: on by default, opt-in, setup required, and former opt-ins that are now standard, illustrated with current 26D counts.')
    cl = [('Home', ''), ('Opt-in and enablement', path)]
    summary = (f'Each Oracle Fusion Cloud What\'s New row has an <b>Action to Enable</b>. '
               f'<b>On by default</b> (Action: None) means users can meet it when the update lands. '
               f'<b>Opt-in</b> stays off until an admin enables it; <b>Opt-in plus Setup</b> also needs configuration. '
               f'Some older opt-ins expire and become <b>now standard</b> — a subset switches on for everyone, others need setup if you want them. '
               f'For <b>26D</b>, across the modules we cover, Oracle\'s Feature Summary tables list '
               f'<b>{bc["on"]}</b> on by default, <b>{bc["pot"]}</b> on by default with potential setup, '
               f'<b>{bc["opt"]}</b> opt-in, <b>{bc["setup"]}</b> setup required and <b>{bc["other"]}</b> needing another action '
               f'(out of <b>{len(allr)}</b> features). Oracle also lists <b>{len(es)}</b> opt-ins that are now standard with 26D '
               f'(<b>{on}</b> automatic, <b>{st}</b> setup).')
    faq = [
        ('What does "on by default" mean?',
         'Oracle\'s Action to Enable column says None: the feature is delivered ready for users when the update reaches the environment. Some rows are "Potential Setup" — still delivered enabled, but Oracle flags prerequisite or optional configuration.'),
        ('What does "opt-in" mean?',
         'The feature stays off until an administrator opts in. "Opt In plus Setup" also needs configuration before anyone can use it. Nothing changes for end users if you do nothing.'),
        ('What does "now standard" mean?',
         f'Oracle first shipped the feature as an opt-in. Its Current Opt-In Expirations list names a release where that opt-in step ends, so from that release the feature is part of the standard product. Some switch on for everyone; others still need setup. See <a href="../../26d/former-opt-ins-now-standard/">26D former opt-ins now standard</a>.'),
        ('Where do the 26D counts on this page come from?',
         f'From Oracle\'s 26D What\'s New Feature Summary tables for Financials, Procurement, SCM, Logistics, Projects and HCM (our extract: {len(allr)} rows), plus Oracle\'s Current Opt-In Expirations list for the {len(es)} that end with 26D. Counts are examples for the current release, not permanent facts.'),
    ]
    body = f"""{R.crumbs_html(cl, '../../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">A short glossary of Oracle&#39;s Action to Enable labels, with live 26D figures as examples. The labels come from Oracle; the counts come from our weekly extract of Oracle&#39;s What&#39;s New tables.</p>
{R.summary_html(summary)}</div>
<div class="box"><h2 style="margin-top:0">Action to Enable, in plain English</h2>
<table><tr><th>Oracle label</th><th>What it means for you</th><th>26D count (modules we cover)</th></tr>
<tr><td>None</td><td>On by default when the update lands</td><td>{bc['on']}</td></tr>
<tr><td>Potential Setup</td><td>On by default; Oracle flags setup you may need</td><td>{bc['pot']}</td></tr>
<tr><td>Opt In</td><td>Stays off until an admin opts in</td><td>{sum(1 for r in allr if r['action']=='Opt In')}</td></tr>
<tr><td>Opt In plus Setup</td><td>Opt-in, then configuration</td><td>{sum(1 for r in allr if r['action']=='Opt In plus Setup')}</td></tr>
<tr><td>Setup Required</td><td>Off until set up (no separate opt-in step)</td><td>{bc['setup']}</td></tr>
<tr><td>Other (e.g. Visual Builder, Service Request Required)</td><td>Follow the action named on Oracle&#39;s feature page</td><td>{bc['other']}</td></tr>
</table>
<p class="small muted">Source: Feature Summary &quot;Action to Enable&quot; column in Oracle&#39;s 26D What&#39;s New documents. Total rows in our extract: {len(allr)}.</p></div>
<div class="box"><h2 style="margin-top:0">Former opt-ins that are now standard</h2>
<p>Oracle&#39;s <a href="{OPTIN}" target=_blank rel=noopener>Current Opt-In Expirations</a> list names features whose opt-in period ends with a given release. From that release they are <b>now standard</b>. For 26D that is <b>{len(es)}</b> features: <b>{on}</b> switch on for everyone (Oracle&#39;s &quot;Now enabled&quot; = Yes) and <b>{st}</b> need setup if you want them.</p>
<p><a href="../../26d/former-opt-ins-now-standard/">26D former opt-ins now standard →</a> · <a href="../../26d/opt-in-features/">26D new opt-in features →</a> · <a href="../../26d/on-by-default/">26D on by default →</a></p></div>
<div class="box"><h2 style="margin-top:0">How to use this each quarter</h2><ul class="check">
<li>Read the release hub for counts by Action to Enable (for 26D: <a href="../../26d/">26D hub</a>).</li>
<li>Shortlist opt-ins your business owners asked for; leave the rest off until you need them.</li>
<li>For features that are now standard, check whether Oracle&#39;s &quot;Now enabled&quot; is Yes or whether setup is still required.</li>
<li>Test in the pod that receives the update first, then confirm production matches what you signed off.</li>
</ul></div>
{R.faq_html(faq)}{_related_guides(path)}{R.nl_form()}"""
    return path, R.page(title, body, 2, desc, path, _ld(path, title, desc, cl, faq),
                        og=('Oracle Fusion · enablement', 'On by default, opt-in, and now standard — illustrated with 26D'))

# ---------- 4. /redwood-defaults/ ----------
def redwood_calendar(updates):
    path = 'redwood-defaults/'
    items = R.HCMR['items']
    by_rel = collections.OrderedDict()
    for rel in sorted({i['release'] for i in items}):
        by_rel[rel] = [i for i in items if i['release'] == rel]
    # longtail deep dives
    import longtail
    deep = ''
    if longtail.LT:
        deep = ('<div class="box"><h2 style="margin-top:0">26D page-level lists with profile option codes</h2><p>' +
                ' · '.join(f'<a href="../{p}">{E(n)}</a>' for p, n in longtail.PAGES.items()) +
                f' · <a href="../26d/redwood-erp-scm/">26D Redwood changes outside HCM</a></p></div>')
    def _sec(rel, rows):
        red = [i for i in rows if i['type'] == 'Redwood by default']
        other = [i for i in rows if i not in red]
        bits = []
        if red:
            bits.append(f'<h3 style="margin:12px 0 6px">Redwood by default ({len(red)})</h3>' +
                        ''.join(R.hr_item_html(i) for i in red))
        if other:
            bits.append(f'<h3 style="margin:12px 0 6px">Other HCM notices ({len(other)})</h3>' +
                        ''.join(R.hr_item_html(i) for i in other))
        note = ''
        if rel >= '27A':
            note = ('<p class="small muted">Announced in Oracle\'s 26C/26D documents; Oracle has not published a full 27A What\'s New yet. '
                    'Treat these as announced, and re-check when 27A documents appear.</p>')
        return (f'<div class="box" id="r{rel.lower()}"><h2 style="margin-top:0">{E(rel)} ({len(rows)})</h2>{note}' +
                ''.join(bits) + '</div>')
    secs = ''.join(_sec(rel, rows) for rel, rows in by_rel.items())
    n26d = len(by_rel.get('26D', [])); n27a = len(by_rel.get('27A', []))
    title = 'Oracle Fusion Redwood defaults calendar'
    desc = (f'HCM Redwood default switches and related notices by release (26B–27C), plus links to 26D page-level lists '
            f'and ERP/SCM Redwood rows. {n26d} items announced for 26D; {n27a} early 27A announcements.')
    cl = [('Home', ''), ('Redwood defaults', path)]
    summary = (f'Oracle is moving selected Fusion pages to <b>Redwood by default</b> on a published schedule. '
               f'Fusion Updates groups those default switches and related HCM notices by release '
               f'({", ".join(f"{rel} ({len(rows)})" for rel, rows in by_rel.items())}). '
               f'Where Oracle says so, a profile option can still be set back to No. '
               f'Drill into the 26D person, employment and workforce-structures lists for every profile option code, '
               f'and into <a href="../27a/redwood-defaults/">27A Redwood defaults</a> for early announcements.')
    faq = [
        ('Can I keep an older page instead of Redwood?',
         'Where Oracle provides a profile option, set it to No in Manage Administrator Profile Values. Oracle\'s feature page for each switch says whether that is available.'),
        ('Is HCM on the opt-in expiration list?',
         'No. Oracle announces HCM Redwood default switches separately. That is why this calendar exists alongside the former-opt-ins pages.'),
        ('Are 27A items final?',
         'They are announced in Oracle\'s 26C/26D documents. Oracle has not published full 27A What\'s New books yet, so re-check when those appear.'),
    ]
    body = f"""{R.crumbs_html(cl, '../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">One place for HCM Redwood default switches and related notices across releases, with links to the detailed profile-option lists.</p>
{R.summary_html(summary)}
<p class="small muted">{E(R.HCMR.get('note',''))} Checked {E(R.HCMR.get('checked',''))}.</p></div>
{deep}{secs}
<p><a href="../{R.HCMR_PATH}">Full HCM Redwood hub →</a></p>
{R.faq_html(faq)}{_related_guides(path, '../')}{R.nl_form()}"""
    return path, R.page(title, body, 1, desc, path, _ld(path, title, desc, cl, faq),
                        og=('Oracle Fusion · Redwood', 'Defaults calendar by release, with profile-option deep dives'))

# ---------- 5. /guides/prepare-for-quarterly-update/ ----------
def prepare_page(updates):
    path = 'guides/prepare-for-quarterly-update/'
    u = updates['26D']; wins = windows('26D')
    on = sum(1 for e in u['expiring'] if e['now_enabled'] == 'Yes'); st = len(u['expiring']) - on
    title = 'Prepare for an Oracle Fusion Cloud quarterly update'
    desc = ('Playbook for the Fusion Cloud quarterly update test window: when your cohort updates, what changed, and what to test, with links to Fusion Updates checklists and lists.')
    cl = [('Home', ''), ('Prepare for a quarterly update', path)]
    summary = (f'Plan Fusion Cloud quarterly updates in three layers: (1) <b>when</b> your cohort\'s test and production Fridays fall, '
               f'(2) <b>what</b> changed — on by default, opt-in, and opt-ins that are now standard — and '
               f'(3) <b>what to test</b> in the roughly two-week pod window. For <b>26D</b>, start with the '
               f'<a href="../../26d/dates/">dates page</a> (Cohort A {_fmt_safe(wins[0][1])} / {_fmt_safe(wins[0][2])}), the '
               f'<a href="../../26d/">26D hub</a> (<b>{len(u["all"])}</b> features in modules we cover), and the '
               f'<a href="../../updates/26d/checklist.html">what-to-test checklist</a>. '
               f'Tick Financials, HCM, SCM, Procurement, Logistics and Projects pages that match your offerings; '
               f'confirm every opt-in decision before production.')
    faq = [
        ('How long is the test window?',
         'About two weeks: Oracle updates test environments on the first Friday of the cohort month and production on the third Friday. Source: <a href="' + FI + '" target=_blank rel=noopener>Oracle Fusion Insider</a>.'),
        ('What should I test first?',
         'Baseline regression (current configuration, key end-to-end flows, integrations, reports, custom workflows, security), then features delivered switched on, then former opt-ins that are now standard. Our checklists follow that order.'),
        ('Where do I get 26D dates?',
         f'<a href="../../26d/dates/">26D release dates and cohorts</a> applies Oracle\'s published rule. Confirm your own dates in the Oracle Cloud Console.'),
        ('Is this the same as the old /guides/how-oracle-fusion-updates-work/ URL?',
         'That path returned 404. This page is the replacement; requests to the old path redirect here.'),
    ]
    baseline = ''.join(f'<li>{x}</li>' for x in R.BASELINE)
    body = f"""{R.crumbs_html(cl, '../../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">A repeatable playbook for each Fusion Cloud quarterly update: when it lands, what changed, and what to test before production.</p>
{R.summary_html(summary)}{_oracle_rule_note()}</div>
<div class="box"><h2 style="margin-top:0">1. When: your cohort&#39;s Fridays</h2>
<p>Find your cohort in the Oracle Cloud Console. Typical 26D Fridays:</p>
<ul class="check">
<li>Cohort A — test {_fmt_safe(wins[0][1])}, production {_fmt_safe(wins[0][2])}</li>
<li>Cohort B — test {_fmt_safe(wins[1][1])}, production {_fmt_safe(wins[1][2])}</li>
<li>Cohort C — test {_fmt_safe(wins[2][1])}, production {_fmt_safe(wins[2][2])}{(' — ' + HOL[wins[2][1]]) if wins[2][1] in HOL else ''}</li>
</ul>
<p><a href="../../26d/dates/">Full 26D dates page →</a> · <a href="../../downloads/">Download the .ics calendar →</a></p></div>
<div class="box"><h2 style="margin-top:0">2. What: on by default, opt-in, now standard</h2>
<p>For 26D across the modules we cover:</p>
<ul class="check">
<li><a href="../../26d/on-by-default/">On by default</a> — users may see these when the update lands</li>
<li><a href="../../26d/opt-in-features/">Opt-in features</a> — stay off until you choose them</li>
<li><a href="../../26d/former-opt-ins-now-standard/">Former opt-ins now standard ({len(u['expiring'])})</a> — {on} switch on for everyone, {st} need setup</li>
<li><a href="../../guides/opt-in-and-enablement/">How opt-in and enablement work</a> (evergreen glossary)</li>
</ul></div>
<div class="box"><h2 style="margin-top:0">3. What to test</h2>
<p class="small muted">Baseline items follow Oracle&#39;s published guidance: <a href="https://docs.oracle.com/en/cloud/saas/transportation/26b/otmpt/what-should-i-test-after-a-quarterly-update.html" target=_blank rel=noopener>What Should I Test After a Quarterly Update?</a></p>
<ul class="check">{baseline}
<li>Features delivered switched on (see the release checklist)</li>
<li>Former opt-ins that are now standard</li>
<li>Refresh your test environment from production before the test-environment update, as Oracle recommends</li>
</ul>
<p><a class="btn" href="../../updates/26d/checklist.html">Open the 26D what-to-test checklist →</a>
<a class="btn alt" style="border:1px solid var(--line)" href="../../downloads/">Get the printable PDF →</a></p></div>
<div class="box"><h2 style="margin-top:0">Module hubs for 26D</h2>
<p>{' · '.join(f'<a href="../../26d/{R.FSLUG[f]}/">{E(R.FNAME[f])}</a>' for f in R.FSLUG)}</p>
<p><a href="../../26d/">26D hub</a> · <a href="../../redwood-defaults/">Redwood defaults calendar</a> · <a href="../../26d/fusion-claw-ai-agent-studio/">AI and agentic features in 26D</a></p></div>
{R.faq_html(faq)}{_related_guides(path)}{R.nl_form()}"""
    return path, R.page(title, body, 2, desc, path, _ld(path, title, desc, cl, faq),
                        og=('Oracle Fusion · prepare', 'When, what changed, and what to test each quarter'))

def _redirect_stub(dist, old_path, new_url, label):
    """Minimal HTML redirect for a retired URL (same pattern as ShopBot Index store stubs). Not added to the sitemap."""
    d = os.path.join(dist, old_path)
    os.makedirs(d, exist_ok=True)
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0;url={new_url}">
<link rel="canonical" href="{new_url}">
<title>Moved: {E(label)}</title></head>
<body><p>This guide has moved to <a href="{new_url}">{E(new_url)}</a>.</p></body></html>
"""
    open(os.path.join(d, 'index.html'), 'w').write(html)

def build(dist, updates):
    if '26D' not in updates or not updates['26D'].get('all'):
        return []
    out = []
    for fn in (dates_page, ai_page, optin_guide, redwood_calendar, prepare_page):
        path, htm = fn(updates)
        depth = path.count('/')
        # redwood-defaults/ is depth 1; others depth 2
        d = os.path.join(dist, path)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w').write(htm)
        out.append(path)
    _redirect_stub(dist, 'guides/how-oracle-fusion-updates-work',
                   R.BASE + '/guides/prepare-for-quarterly-update/',
                   'Prepare for an Oracle Fusion Cloud quarterly update')
    return out

def hub_links(depth=''):
    """Short strip for the 26D hub and home."""
    return (f'<div class="box"><h3 style="margin-top:0">Guides</h3><p>'
            f'<a href="{depth}26d/dates/">26D release dates and cohorts</a> · '
            f'<a href="{depth}guides/opt-in-and-enablement/">How opt-in and enablement work</a> · '
            f'<a href="{depth}guides/prepare-for-quarterly-update/">Prepare for a quarterly update</a> · '
            f'<a href="{depth}redwood-defaults/">Redwood defaults calendar</a> · '
            f'<a href="{depth}26d/fusion-claw-ai-agent-studio/">AI and agentic features in 26D</a></p></div>')

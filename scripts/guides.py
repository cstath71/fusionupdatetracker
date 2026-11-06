"""Gap SEO/AEO guide pages (keyword research 29 Oct 2026, rechecked at publish):
  /26d/dates/                              cohort months and official Oracle links; no calculated day-level dates
  /26d/fusion-claw-ai-agent-studio/        Fusion Claw and AI Agent Studio rows from our extract only
  /guides/opt-in-and-enablement/           evergreen enablement explainer (26D figures counted from the dataset)
  /redwood-defaults/                       consolidated Redwood defaults calendar
  /guides/prepare-for-quarterly-update/    prepare / test-window playbook
Also writes a redirect stub at /guides/how-oracle-fusion-updates-work/ (404 on the live site).
Called from render.render(); returns sitemap paths (redirect stub is omitted from sitemap).
"""
import os, re, collections
import render as R
E = R.E

FI = 'https://blogs.oracle.com/fusioninsider/quarterly-updates-made-easy'
CLAW = 'https://blogs.oracle.com/fusioninsider/introducing-fusion-claw-for-complex-autonomous-work'
OPTIN = 'https://docs.oracle.com/en/cloud/saas/readiness/common/opt-in-features/optincurrent.html'
READINESS = 'https://docs.oracle.com/en/cloud/saas/readiness/index.html'
RELEASE_PLANNING = 'https://docs.oracle.com/en/cloud/customer-success/cloud-success-navigator/navigator-user-guide/release-planning1.html'
# Oracle title, module, or feature-summary tag. Not a general "assistant" / "agentic" match.
AI_VERIFIED = re.compile(r'\b(?:fusion claw|ai agent studio|agent studio)\b', re.I)

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
        ('26d/fusion-claw-ai-agent-studio/', 'Fusion Claw and AI Agent Studio'),
    ]
    lk = ' · '.join(f'<a href="{depth}{p}">{E(n)}</a>' for p, n in pages if p != cur)
    return f'<div class="box"><p><b>Related guides:</b> {lk} · <a href="{depth}26d/">26D hub</a> · <a href="{depth}downloads/">Free downloads</a></p></div>'

def _oracle_rule_note():
    return (f'<p class="small muted">Official schedule: <a href="{FI}" target=_blank rel=noopener>Oracle Fusion Insider, '
            f'"Quarterly updates made easy"</a> (10 Dec 2025). That article states the cohort months and the first-Friday / '
            f'third-Friday rule. It does not list calendar dates for 26D. Per-environment dates are in the '
            f'<a href="{RELEASE_PLANNING}" target=_blank rel=noopener>Oracle Cloud Success Navigator Release Planning</a> page '
            f'(sign-in) and in the Oracle Cloud Console. Middle East regions update on the Thursday before each Friday.</p>')

def _cohort_table():
    """Months Oracle publishes, plus where release D falls in that list. No calculated Fridays."""
    rows = (
        ('A', 'February, May, August, November', 'November'),
        ('B', 'March, June, September, December', 'December'),
        ('C', 'April, July, October, January', 'January, after the November and December updates'),
    )
    body = ''.join(f'<tr><td>Cohort {c}</td><td>{m}</td><td>{d}</td></tr>' for c, m, d in rows)
    return ('<table><tr><th>Cohort</th><th>Update months Oracle publishes</th>'
            '<th>Where 26D falls in that list</th></tr>' + body + '</table>'
            '<p class="small muted">Oracle names 26A, 26B, 26C and 26D as the four 2026 releases, in that order, and lists '
            'four months for each cohort. The third column is that order applied to 26D. It is not a dated Oracle calendar, '
            'and this page does not calculate the Friday inside the month.</p>')

# ---------- 1. /26d/dates/ ----------
def dates_page(updates):
    rel = '26D'; path = '26d/dates/'; u = updates[rel]
    on = sum(1 for e in u['expiring'] if e['now_enabled'] == 'Yes')
    st = len(u['expiring']) - on
    bc = R.bucket_counts(u['all'])
    title = 'Oracle Fusion 26D release dates and cohorts'
    desc = ('Oracle Fusion Cloud 26D cohort months and the official schedule links. Oracle publishes the cohort rule, not a public day-by-day 26D calendar, so this page does not print calculated dates.')
    cl = [('Home', ''), ('26D', '26d/'), ('Release dates', path)]
    summary = (f'Oracle Fusion Cloud <b>26D</b> is the fourth 2026 quarterly update. Oracle publishes which months each cohort updates, '
               f'and that test environments update on the <b>first Friday</b> of that month and production on the <b>third Friday</b>. '
               f'Oracle has not published a public list of those Fridays for 26D, so this page does not calculate or print them. '
               f'Use the official links below and confirm your environment in the Oracle Cloud Console. '
               f'On the content side, Oracle\'s 26D What\'s New lists <b>{len(u["all"])}</b> features across the modules we cover: '
               f'<b>{bc["on"]}</b> on by default, <b>{bc["pot"]}</b> on by default with potential setup, '
               f'<b>{bc["opt"]}</b> opt-in, and <b>{len(u["expiring"])}</b> former opt-ins that are now standard with 26D '
               f'(<b>{on}</b> switch on for everyone, <b>{st}</b> need setup).')
    faq = [
        ('When does Oracle Fusion 26D update my environments?',
         f'It depends on your cohort. Oracle\'s published rule puts test environments on the first Friday of the cohort\'s update month and production on the third Friday. For 26D, the fourth 2026 release, those months are November (Cohort A), December (Cohort B) and the following January (Cohort C). Oracle has not published the Fridays themselves on a public calendar, so confirm your dates in the Oracle Cloud Console. Source: <a href="{FI}" target=_blank rel=noopener>Oracle Fusion Insider</a>.'),
        ('Which months are Cohorts A, B and C?',
         'Per Oracle Fusion Insider: Cohort A is February, May, August and November; Cohort B is March, June, September and December; Cohort C is April, July, October and January.'),
        ('Why does this page not list a Friday for 26D?',
         f'We rechecked <a href="{FI}" target=_blank rel=noopener>Oracle\'s quarterly-updates article</a> and the public readiness site. They state the cohort months and the Friday rule. They do not list a dated 26D calendar. Calculated Fridays would be unverified, so they are not on this page. Your dates are in the Oracle Cloud Console and in <a href="{RELEASE_PLANNING}" target=_blank rel=noopener>Release Planning</a>.'),
        ('What should I do in the two-week test window?',
         f'Start with the <a href="../../updates/26d/checklist.html">26D what-to-test checklist</a>, review <a href="../on-by-default/">features on by default</a> and <a href="../opt-in-features/">opt-ins</a>, and decide which of the <a href="../former-opt-ins-now-standard/">{len(u["expiring"])} former opt-ins now standard</a> need setup. See also <a href="../../guides/prepare-for-quarterly-update/">Prepare for a quarterly update</a>.'),
    ]
    body = f"""{R.crumbs_html(cl, '../../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">Cohort months for Oracle Fusion Cloud 26D, with links to Oracle&#39;s schedule. Day-level dates are not printed here, because Oracle has not published them on a public calendar we could recheck.</p>
{R.summary_html(summary)}{_oracle_rule_note()}</div>
<div class="box"><h2 style="margin-top:0">Cohorts and where 26D falls</h2>
{_cohort_table()}
<p>Inside the month, Oracle\'s rule is: test environments on the first Friday, production on the third Friday, two weeks later. Middle East regions use the Thursday before. If that Friday is a holiday, confirm the date Oracle assigned to your environment.</p></div>
<div class="box"><h2 style="margin-top:0">Official Oracle links</h2>
<ul class="check">
<li><a href="{FI}" target=_blank rel=noopener>Quarterly updates made easy</a> (Oracle Fusion Insider) — cohort months and the Friday rule</li>
<li><a href="{RELEASE_PLANNING}" target=_blank rel=noopener>Release Planning</a> in Oracle Cloud Success Navigator — Oracle&#39;s in-product calendar by cohort (sign-in)</li>
<li><a href="{READINESS}" target=_blank rel=noopener>Oracle Cloud Readiness</a> — What&#39;s New documents for the update</li>
<li>Oracle Cloud Console — your environment&#39;s cohort and maintenance dates</li>
</ul></div>
<div class="box"><h2 style="margin-top:0">What changes when 26D lands</h2>
<p>Oracle&#39;s 26D What&#39;s New documents list <b>{len(u['all'])}</b> features across the modules Fusion Updates covers. Counts are taken from our current extract, not from an older research note. Use these lists for the content of the update:</p>
<ul class="check">
<li><a href="../">26D hub: what&#39;s new by module and the opt-in expiration list</a></li>
<li><a href="../on-by-default/">Features on by default</a> · <a href="../opt-in-features/">Opt-in features</a> · <a href="../former-opt-ins-now-standard/">Former opt-ins now standard ({len(u['expiring'])})</a></li>
<li><a href="../../updates/26d/checklist.html">26D what-to-test checklist</a> · <a href="../../downloads/">Free checklist PDF</a></li>
</ul></div>
{R.faq_html(faq)}{_related_guides(path)}{R.nl_form()}"""
    return path, R.page(title, body, 2, desc, path, _ld(path, title, desc, cl, faq),
                        og=('Oracle Fusion Cloud 26D · dates', 'Cohort months and official Oracle schedule links'))

# ---------- 2. /26d/fusion-claw-ai-agent-studio/ ----------
def _ai_blob(r):
    return ' '.join(r.get(k) or '' for k in ('title', 'module', 'tags'))

def verified_ai(updates):
    """Rows whose Oracle title, module, or feature-summary tag names Fusion Claw or AI Agent Studio.
    Curated items are preferred (they carry Oracle's tag). Deduped by Oracle URL. No title-keyword guesses."""
    out, seen = [], set()
    for rel in sorted(updates, reverse=True):
        u = updates[rel]
        for r in list(u.get('items') or []) + list(u.get('all') or []):
            if not AI_VERIFIED.search(_ai_blob(r)): continue
            url = r.get('url') or ''
            if not url or url in seen: continue
            seen.add(url); out.append((rel, r))
    return out

def ai_page(updates):
    path = '26d/fusion-claw-ai-agent-studio/'
    rows = verified_ai(updates)
    d26 = [r for rel, r in rows if rel == '26D']
    claw = [r for r in d26 if re.search(r'\bfusion claw\b', _ai_blob(r), re.I)]
    prior = [(rel, r) for rel, r in rows if rel != '26D']
    def _why(r):
        blob = _ai_blob(r)
        bits = []
        if re.search(r'\bfusion claw\b', blob, re.I): bits.append('Fusion Claw')
        if re.search(r'\bagent studio\b', blob, re.I): bits.append('AI Agent Studio')
        return ', '.join(bits) or '—'
    def _tr(rel, r, with_rel=False):
        relc = f'<td>{E(rel)}</td>' if with_rel else ''
        tag = r.get('tags') or '—'
        return (f'<tr>{relc}<td><a href="{E(r["url"])}" target=_blank rel=noopener>{E(r["title"])}</a></td>'
                f'<td>{E(r.get("product") or "")} · {E(r.get("module") or "")}</td>'
                f'<td><span class="pill">{E(r.get("action") or "")}</span></td>'
                f'<td>{E(tag)}</td><td>{E(_why(r))}</td></tr>')
    d26_html = ('<table><tr><th>Feature (Oracle title)</th><th>Product · module</th><th>Action to Enable</th><th>Oracle tag</th><th>Matched as</th></tr>'
                + ''.join(_tr('26D', r) for r in d26) + '</table>') if d26 else '<p>No 26D row in the current extract is titled or tagged Fusion Claw or AI Agent Studio.</p>'
    prior_html = ''
    if prior:
        prior_html = ('<div class="box"><h2 style="margin-top:0">AI Agent Studio in earlier releases we track (' + str(len(prior)) + ')</h2>'
                      '<p class="small muted">These rows are in our What\'s New extract for earlier releases. Titles and Action to Enable are Oracle\'s. '
                      'OTM and GTM publish the same feature as separate books, so both Oracle links are listed.</p>'
                      '<table><tr><th>Release</th><th>Feature (Oracle title)</th><th>Product · module</th><th>Action to Enable</th><th>Oracle tag</th><th>Matched as</th></tr>'
                      + ''.join(_tr(rel, r, True) for rel, r in prior) + '</table></div>')
    title = 'Fusion Claw and AI Agent Studio in Oracle Fusion 26D'
    desc = (f'{len(d26)} Oracle Fusion 26D row(s) tagged or titled Fusion Claw or AI Agent Studio in the modules Fusion Updates covers, '
            f'plus {len(prior)} earlier AI Agent Studio rows from the same extract. No other AI rows and no AI-unit counts.')
    cl = [('Home', ''), ('26D', '26d/'), ('Fusion Claw and AI Agent Studio', path)]
    summary = (f'Fusion Updates lists only What\'s New rows whose Oracle title, module, or feature-summary tag says <b>Fusion Claw</b> or <b>AI Agent Studio</b>. '
               f'In the current 26D extract that is <b>{len(d26)}</b> row{"s" if len(d26)!=1 else ""}'
               + (': ' + '; '.join(E(r['title']) for r in d26) + '. ' if d26 else '. ')
               + (f'None of those 26D titles is "AI Agent Studio". ' if d26 and not any(re.search(r'agent studio', _ai_blob(r), re.I) for r in d26) else '')
               + f'Earlier releases we track include <b>{len(prior)}</b> AI Agent Studio rows, linked below. '
               f'Other AI agents and agentic apps are not listed here. We do not publish AI-unit budgets or guardrail counts; those figures are not fields in our extract. '
               f'Enablement is Oracle\'s Action to Enable column. Confirm each linked Oracle page in your test pod before production.')
    faq = [
        ('Does Fusion Updates list Fusion Claw in 26D?',
         (f'The current 26D extract has {len(claw)} row{"s" if len(claw)!=1 else ""} whose feature-summary tag or title says Fusion Claw'
          + (': ' + '; '.join(E(r['title']) for r in claw) + '. ' if claw else '. ')
          + 'No 26D row is titled Fusion Claw. If Oracle adds another tagged row for a module we cover, the weekly refresh picks it up.')),
        ('Does Fusion Updates list AI Agent Studio in 26D?',
         'Not as a 26D Feature Summary title or tag in the modules we cover. '
         + (f'Our extract does include {len(prior)} AI Agent Studio rows in earlier releases ({", ".join(sorted({rel for rel, _ in prior}))}).' if prior else 'Earlier releases we track do not include one either.')
         + ' Open the linked Oracle page for any 26D Fusion Claw row to see whether that page also describes AI Agent Studio setup.'),
        ('Why are other AI agents not on this page?',
         'A title that merely says "assistant" or "agentic app" is not Fusion Claw or AI Agent Studio. Those features stay on the module pages. This page does not invent rows to fill a gap.'),
        ('Where do the enablement labels come from?',
         'Oracle\'s Action to Enable column, copied from the What\'s New row. We do not add AI-unit budgets or guardrail counts.'),
    ]
    fam_links = ' · '.join(f'<a href="../{R.FSLUG[f]}/">{E(R.FNAME[f])} in 26D</a>'
                           for f in R.FSLUG if any(r.get('family') == f for r in d26))
    more = (' · ' + fam_links) if fam_links else ''
    body = f"""{R.crumbs_html(cl, '../../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">Only the What&#39;s New rows we can verify as Fusion Claw or AI Agent Studio. Nothing else is added to make the list look complete.</p>
{R.summary_html(summary)}
<p class="small muted">Oracle describes Fusion Claw in <a href="{CLAW}" target=_blank rel=noopener>this Fusion Insider article</a>. This page does not repeat counts from that article. The tables are rows already in our What&#39;s New extract. We recheck them every week.</p></div>
<div class="box"><h2 style="margin-top:0">26D rows we can verify ({len(d26)})</h2>
<p class="small muted">A row is included only when Oracle&#39;s feature title, module name, or feature-summary tag contains &quot;Fusion Claw&quot; or &quot;AI Agent Studio&quot;. Assistants and agentic apps that do not say those names are left off.</p>
{d26_html}
<p class="small"><a href="../../updates/26d/">26D changes we track</a>{more}</p></div>
{prior_html}
{R.faq_html(faq)}{_related_guides(path)}{R.nl_form()}"""
    return path, R.page(title, body, 2, desc, path, _ld(path, title, desc, cl, faq),
                        og=('Oracle Fusion Cloud 26D · AI', f'{len(d26)} verified Fusion Claw / AI Agent Studio row(s) in 26D'))

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
    def _src_rels(rows):
        found = []
        for i in rows:
            for u in i.get('urls') or []:
                m = re.search(r'/(\d\d[a-d])/', u, re.I)
                if m and m.group(1).upper() not in found:
                    found.append(m.group(1).upper())
        return found
    def _future_note(rel, rows):
        if rel < '27A': return ''
        src = _src_rels(rows)
        src_txt = ' and '.join(src) if src else 'earlier'
        return ('<p class="small muted">Announced in Oracle\'s ' + E(src_txt) + ' documents. '
                'Oracle has not published a full ' + E(rel) + ' What\'s New yet. '
                'Treat these as announced, and re-check when the ' + E(rel) + ' documents appear.</p>')
    def _sec(rel, rows):
        red = [i for i in rows if i['type'] == 'Redwood by default']
        other = [i for i in rows if i not in red]
        bits = []
        if red:
            bits.append(f'<h3 style="margin:12px 0 6px">Redwood by default ({len(red)})</h3>' +
                        ''.join(R.hr_item_html(i, show_oracle_title=False) for i in red))
        if other:
            bits.append(f'<h3 style="margin:12px 0 6px">Other HCM notices ({len(other)})</h3>' +
                        ''.join(R.hr_item_html(i, show_oracle_title=False) for i in other))
        return (f'<div class="box" id="r{rel.lower()}"><h2 style="margin-top:0">{E(rel)} ({len(rows)})</h2>{_future_note(rel, rows)}' +
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
        ('Are 27A, 27B and 27C items final?',
         'No. Each future release on this page is marked with the Oracle documents that announced it. Oracle has not published a full What\'s New for that release yet, so re-check when those documents appear. A profile option can still be set back to No where Oracle says so.'),
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
    u = updates['26D']
    on = sum(1 for e in u['expiring'] if e['now_enabled'] == 'Yes'); st = len(u['expiring']) - on
    bc = R.bucket_counts(u['all'])
    title = 'Prepare for an Oracle Fusion Cloud quarterly update'
    desc = ('Playbook for the Fusion Cloud quarterly update test window: when your cohort updates, what changed, and what to test, with links to Fusion Updates checklists and lists.')
    cl = [('Home', ''), ('Prepare for a quarterly update', path)]
    summary = (f'Plan Fusion Cloud quarterly updates in three layers: (1) <b>when</b> your cohort\'s test and production windows fall, '
               f'(2) <b>what</b> changed — on by default, opt-in, and opt-ins that are now standard — and '
               f'(3) <b>what to test</b> in the roughly two-week pod window. For <b>26D</b>, start with the '
               f'<a href="../../26d/dates/">dates and cohorts page</a> (official Oracle links; no calculated calendar dates), the '
               f'<a href="../../26d/">26D hub</a> (<b>{len(u["all"])}</b> features in modules we cover: '
               f'{bc["on"]} on by default, {bc["opt"]} opt-in), and the '
               f'<a href="../../updates/26d/checklist.html">what-to-test checklist</a>. '
               f'Tick Financials, HCM, SCM, Procurement, Logistics and Projects pages that match your offerings; '
               f'confirm every opt-in decision before production.')
    faq = [
        ('How long is the test window?',
         'About two weeks: Oracle updates test environments on the first Friday of the cohort month and production on the third Friday. Source: <a href="' + FI + '" target=_blank rel=noopener>Oracle Fusion Insider</a>.'),
        ('What should I test first?',
         'Baseline regression (current configuration, key end-to-end flows, integrations, reports, custom workflows, security), then features delivered switched on, then former opt-ins that are now standard. Our checklists follow that order.'),
        ('Where do I get 26D dates?',
         f'<a href="../../26d/dates/">26D release dates and cohorts</a> links Oracle\'s published schedule and states the cohort months. It does not print calculated Fridays, because Oracle has not published a public day-by-day 26D calendar. Confirm your own dates in the Oracle Cloud Console.'),
        ('Is this the same as the old /guides/how-oracle-fusion-updates-work/ URL?',
         'That path returned 404. This page is the replacement; requests to the old path redirect here.'),
    ]
    baseline = ''.join(f'<li>{x}</li>' for x in R.BASELINE)
    body = f"""{R.crumbs_html(cl, '../../')}<div class="hero"><h1>{E(title)}</h1>
<p class="lead">A repeatable playbook for each Fusion Cloud quarterly update: when it lands, what changed, and what to test before production.</p>
{R.summary_html(summary)}{_oracle_rule_note()}</div>
<div class="box"><h2 style="margin-top:0">1. When: your cohort&#39;s window</h2>
<p>Find your cohort in the Oracle Cloud Console. Oracle&#39;s published months, and where 26D falls in them:</p>
{_cohort_table()}
<p>The test window is the time between the first Friday (test) and the third Friday (production) of that month. This page does not print those Fridays.</p>
<p><a href="../../26d/dates/">26D dates and official Oracle links →</a> · <a href="../../downloads/">Free 26D checklist PDF →</a></p></div>
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
<p><a href="../../26d/">26D hub</a> · <a href="../../redwood-defaults/">Redwood defaults calendar</a> · <a href="../../26d/fusion-claw-ai-agent-studio/">Fusion Claw and AI Agent Studio in 26D</a></p></div>
{R.faq_html(faq)}{_related_guides(path)}{R.nl_form()}"""
    return path, R.page(title, body, 2, desc, path, _ld(path, title, desc, cl, faq),
                        og=('Oracle Fusion · prepare', 'When, what changed, and what to test each quarter'))

def _redirect_stub(dist, old_path, new_url, label):
    """Static redirect for GitHub Pages (no server rewrite). Canonical + refresh, noindex, site stylesheet. Not in the sitemap."""
    d = os.path.join(dist, old_path)
    os.makedirs(d, exist_ok=True)
    dest = '/guides/prepare-for-quarterly-update/'
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="0;url={dest}">
<link rel="canonical" href="{new_url}">
<meta name="robots" content="noindex">
<title>Moved: {E(label)} | {E(R.SITE)}</title>
<link rel="stylesheet" href="../../style.css">
<script>location.replace({dest!r});</script></head>
<body>
<header><div class="w"><a class="brand" href="../../">Fusion<span>Updates</span></a></div></header>
<main class="w"><div class="hero"><h1>This guide has moved</h1>
<p class="lead"><a href="{dest}">{E(label)}</a> is the page that replaced /guides/how-oracle-fusion-updates-work/.</p></div></main>
</body></html>
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
            f'<a href="{depth}26d/fusion-claw-ai-agent-studio/">Fusion Claw and AI Agent Studio</a></p></div>')

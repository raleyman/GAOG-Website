#!/usr/bin/env python3
"""
Regenerates the parts of this site that are driven by the JSON files in /content.

Run this any time content/services.json, content/team.json,
content/articles.json, or content/insights.json changes:

    python3 generate.py

It rewrites the marked blocks in index.html and team-biographies.html,
rebuilds insights.html (the combined "Insights" feed: original articles +
curated industry-watch entries) and services.html (the services index),
and writes one page per full-length article under insights/<slug>.html and
one page per service under services/<slug>.html. It also refreshes
sitemap.xml.

Nothing else on the site is touched — hand-written pages (contact.html,
START-HERE.md, styles.css) are left alone.
"""
import json
import re
import os
from datetime import datetime

SITE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(SITE, "content")
DOMAIN = "https://www.globalairoperations.com"
OG_IMAGE = f"{DOMAIN}/assets/og-image.jpg"
OG_IMAGE_TAGS = (
    f'<meta property="og:image" content="{OG_IMAGE}" />\n'
    '<meta property="og:image:width" content="1200" />\n'
    '<meta property="og:image:height" content="630" />\n'
    f'<meta name="twitter:image" content="{OG_IMAGE}" />'
)


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def load(name):
    with open(os.path.join(CONTENT, name)) as f:
        return json.load(f)


def replace_between(text, start_marker, end_marker, new_inner):
    pattern = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker), re.DOTALL)
    replacement = start_marker + new_inner + end_marker
    new_text, count = pattern.subn(lambda m: replacement, text, count=1)
    if count == 0:
        raise ValueError(f"Markers not found: {start_marker} ... {end_marker}")
    return new_text


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


# ---------------------------------------------------------------- services
def render_service_card(svc):
    bg_html = ""
    if svc.get("card_bg_image"):
        bg_html = f'<img class="service-card-bg" src="{esc(svc["card_bg_image"])}" alt="" aria-hidden="true" />\n          '
    return f"""        <a class="service-card" href="/services/{svc['slug']}">
          {bg_html}<h3>{esc(svc['title'])}</h3>
          <p>{esc(svc['description'])}</p>
          <span class="service-more">Learn more &rarr;</span>
        </a>
"""


def render_svc_index_card(svc):
    bg_html = ""
    if svc.get("card_bg_image"):
        bg_html = f'<img class="svc-card-bg" src="{esc(svc["card_bg_image"])}" alt="" aria-hidden="true" />\n          '
    return f"""        <a class="svc-card" href="/services/{svc['slug']}">
          {bg_html}<div class="svc-card-body">
            <h3>{esc(svc['title'])}</h3>
            <p>{esc(svc.get('summary') or svc['description'])}</p>
            <span class="svc-card-more">Learn more &rarr;</span>
          </div>
        </a>
"""


def render_included_list(items):
    if not items:
        return ""
    lis = "".join(
        f'          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6L9 17l-5-5"/></svg>{esc(item)}</li>\n'
        for item in items
    )
    return f"""        <h3>What's Included</h3>
        <ul class="included-list">
{lis}        </ul>
"""


def build_services_index(services):
    cards = "\n".join(render_svc_index_card(s) for s in services)
    nav = NAV.format(insights_active="", svc_active=' class="is-active"')
    return f"""<!doctype html>
<html lang="en">
<head>
<script>document.documentElement.classList.add('js');</script>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />

<!-- PRE-LAUNCH: remove once live on www.globalairoperations.com -->
<meta name="robots" content="noindex, nofollow" />

<title>Services | Global Air Operations Group</title>
<meta name="description" content="Consulting services from Global Air Operations Group: operational strategy and incident support, policy and program development, training and exercises, after-action review, and business consulting." />
<link rel="canonical" href="{DOMAIN}/services" />

<meta property="og:type" content="website" />
<meta property="og:site_name" content="Global Air Operations Group" />
<meta property="og:title" content="Services | Global Air Operations Group" />
<meta property="og:description" content="Consulting services built around aviation operations, program and business development." />
<meta property="og:url" content="{DOMAIN}/services" />
{OG_IMAGE_TAGS}
<meta name="twitter:card" content="summary_large_image" />

<link rel="icon" type="image/png" href="/assets/favicon.png" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,500&amp;display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/styles.css" />
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

{nav}

<main id="main">

  <div class="page-header page-header-photo">
    <img class="page-header-photo-img" src="/assets/services-hero.jpg" alt="" aria-hidden="true" />
    <div class="container">
      <p class="eyebrow">What We Do</p>
      <h1>Consulting Services</h1>
      <p>Services built around aviation operations, program and business development, led by consultants who have done the work themselves.</p>
    </div>
  </div>

  <section>
    <div class="container">
      <div class="grid-svc reveal-group">
{cards}      </div>
    </div>
  </section>

  <section class="section-alt" aria-labelledby="svc-contact-heading">
    <div class="container">
      <div class="cta-band">
        <div class="cta-copy">
          <p class="eyebrow">Get In Touch</p>
          <h2 id="svc-contact-heading">Tell us about your program, business, goals, and needs</h2>
          <p>Not sure which service fits? Reach out and we'll help point you in the right direction.</p>
        </div>
        <a class="btn btn-primary" href="/contact">Go to Contact Page</a>
      </div>
    </div>
  </section>

</main>

<script src="/scroll-reveal.js" defer></script>
{FOOTER}
"""


# Each service detail page gets its own header photo instead of the generic
# services-hero.jpg, so the five pages stop feeling like one templated page
# repeated five times (see stylistic review, Aug 2026).
SERVICE_HERO_PHOTOS = {
    "operational-strategy-incident-support": "/assets/services/operational-strategy-bg.jpg",
    "policy-program-development": "/assets/services/policy-program-bg.jpg",
    "training-exercises": "/assets/services/training-exercises-bg.jpg",
    "aar-continuous-improvement": "/assets/services/aar-continuous-improvement-bg.jpg",
    "business-consulting": "/assets/services/business-consulting-bg.jpg",
}

def build_service_page(svc, articles_by_slug, all_services):
    body_html = "".join(f"        <p>{esc(p)}</p>\n" for p in svc["body"])
    included_html = render_included_list(svc.get("included"))
    credentials_html = ""
    if svc.get("credentials_note"):
        credentials_html = f'        <div class="credentials-note">{esc(svc["credentials_note"])}</div>\n'
    related_html = ""
    related_pub = articles_by_slug.get(svc.get("related_publication"))
    if related_pub:
        related_html = f"""        <div class="related-link">
          <span class="related-link-label">Related Reading</span>
          <a href="/insights/{related_pub['slug']}">{esc(related_pub['title'])} &rarr;</a>
        </div>
"""
    nav = NAV.format(insights_active="", svc_active=' class="is-active"')

    # A right-hand rail so the page isn't just a narrow content card floating
    # in a wide field — a CTA, a team link, and the other services (see
    # stylistic review, Aug 2026).
    other_services_html = "".join(
        f'            <li><a href="/services/{s["slug"]}">{esc(s["title"])}</a></li>\n'
        for s in all_services if s["slug"] != svc["slug"]
    )
    sidebar_html = f"""        <aside class="svc-sidebar">
          <div class="svc-sidebar-card">
            <h4>Ready to talk about this?</h4>
            <p>Tell us about your program, business, goals, and needs.</p>
            <a class="btn btn-primary" href="/contact">Go to Contact Page</a>
          </div>
          <div class="svc-sidebar-card">
            <h4>Meet the Team</h4>
            <p>Senior consultants and principals with careers built at CAL FIRE, the U.S. Forest Service, Orange County Fire Authority, and the U.S. Coast Guard.</p>
            <a class="svc-sidebar-link" href="/team-biographies">View Full Team Biographies &rarr;</a>
          </div>
          <div class="svc-sidebar-card">
            <h4>Other Services</h4>
            <ul class="svc-sidebar-list">
{other_services_html}            </ul>
          </div>
        </aside>
"""

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />

<!-- PRE-LAUNCH: remove once live on www.globalairoperations.com -->
<meta name="robots" content="noindex, nofollow" />

<title>{esc(svc['title'])} | Global Air Operations Group</title>
<meta name="description" content="{esc(svc.get('summary') or svc['description'])}" />
<link rel="canonical" href="{DOMAIN}/services/{svc['slug']}" />

<meta property="og:type" content="website" />
<meta property="og:site_name" content="Global Air Operations Group" />
<meta property="og:title" content="{esc(svc['title'])} | Global Air Operations Group" />
<meta property="og:description" content="{esc(svc.get('summary') or svc['description'])}" />
<meta property="og:url" content="{DOMAIN}/services/{svc['slug']}" />
{OG_IMAGE_TAGS}
<meta name="twitter:card" content="summary_large_image" />

<link rel="icon" type="image/png" href="/assets/favicon.png" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,500&amp;display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/styles.css" />

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": {json.dumps(svc['title'])},
  "provider": {{ "@type": "Organization", "name": "Global Air Operations Group" }},
  "description": {json.dumps(svc.get('summary') or svc['description'])}
}}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

{nav}

<main id="main">

  <div class="page-header page-header-photo">
    <img class="page-header-photo-img" src="{SERVICE_HERO_PHOTOS.get(svc['slug'], '/assets/services-hero.jpg')}" alt="" aria-hidden="true" />
    <div class="container">
      <p class="eyebrow"><a href="/services" style="color:inherit;">Services</a></p>
      <h1>{esc(svc['title'])}</h1>
      <p>{esc(svc.get('summary') or svc['description'])}</p>
    </div>
  </div>

  <section class="section-alt">
    <div class="container svc-detail-layout">
      <article class="article-body">
{body_html}{included_html}{credentials_html}{related_html}        <p class="article-signature"><a href="/team-biographies">Meet the consultants behind our work &rarr;</a></p>
      </article>
{sidebar_html}    </div>
  </section>

  <section aria-labelledby="svc-cta-heading">
    <div class="container">
      <div class="cta-band">
        <div class="cta-copy">
          <h2 id="svc-cta-heading">Ready to talk about {esc(svc['title'])}?</h2>
          <p>Tell us about your program, business, goals, and needs. We typically reply within one business day.</p>
        </div>
        <a class="btn btn-primary" href="/contact">Go to Contact Page</a>
      </div>
    </div>
  </section>

</main>

{FOOTER}
"""


def build_services_block(services):
    return "\n" + "".join(render_service_card(s) for s in services)


# ---------------------------------------------------------------- team
def render_team_card(person):
    bio_id = f"bio-{slugify(person['name'])}"
    has_full = bool(person.get("full_bio"))
    readmore = (
        f'\n            <button type="button" class="team-readmore" data-bio-open="{bio_id}">Read Full Biography &rarr;</button>'
        if has_full else ""
    )
    photo_attrs = f' data-bio-open="{bio_id}" role="button" tabindex="0" aria-label="Read full biography for {esc(person["name"])}"' if has_full else ""
    if person.get("photo"):
        photo_inner = f'<img src="{esc(person["photo"])}" alt="{esc(person["name"])}" loading="lazy" />'
    else:
        photo_inner = esc(person["initials"])
    return f"""
        <article class="team-card">
          <div class="team-photo"{photo_attrs}>{photo_inner}</div>
          <div class="team-body">
            <h3>{esc(person['name'])}</h3>
            <div class="team-role">{esc(person['role'])}</div>
            <p class="team-bio clamp">{esc(person['bio'])}</p>{readmore}
          </div>
        </article>
"""


def build_team_block(team):
    return "".join(render_team_card(p) for p in team) + "\n        "


def render_team_strip_item(person):
    """Small circular-crop entry for the homepage team strip — links out to
    the full bios page rather than trying to open the bio modal, since that
    modal's templates only live on team-biographies.html (see stylistic
    review round 2, Aug 2026)."""
    if person.get("photo"):
        photo_inner = f'<img src="{esc(person["photo"])}" alt="{esc(person["name"])}" loading="lazy" />'
    else:
        photo_inner = esc(person["initials"])
    return f"""        <a class="team-strip-item" href="/team-biographies">
          <span class="team-strip-photo">{photo_inner}</span>
          <span class="team-strip-name">{esc(person['name'])}</span>
          <span class="team-strip-role">{esc(person['role'])}</span>
        </a>
"""


def build_team_strip(team):
    return "\n" + "".join(render_team_strip_item(p) for p in team) + "        "


def render_bio_template(person):
    bio_id = f"bio-{slugify(person['name'])}"
    edu = esc(person["education"]) if person.get("education") else ""
    photo = esc(person["photo"]) if person.get("photo") else ""
    paragraphs = person.get("full_bio") or [person["bio"]]
    body = "".join(f"<p>{esc(p)}</p>" for p in paragraphs)
    return (
        f'<template id="{bio_id}" data-name="{esc(person["name"])}" '
        f'data-role="{esc(person["role"])}" data-initials="{esc(person["initials"])}" '
        f'data-photo="{photo}" data-edu="{edu}">{body}</template>\n'
    )


def build_bio_templates(team):
    return "\n" + "".join(render_bio_template(p) for p in team if p.get("full_bio")) + "        "


def build_team_ld(team):
    graph = [{
        "@type": "ProfessionalService",
        "name": "Global Air Operations Group",
        "url": f"{DOMAIN}/",
        "email": "info@globalairoperations.com",
    }]
    for p in team:
        graph.append({
            "@type": "Person",
            "name": p["name"],
            "jobTitle": p["role"],
            "worksFor": {"@type": "Organization", "name": "Global Air Operations Group"},
        })
    payload = {"@context": "https://schema.org", "@graph": graph}
    return "\n<script type=\"application/ld+json\">\n" + json.dumps(payload, indent=2) + "\n</script>\n"


# ---------------------------------------------------------------- insights
NAV = """<header class="site-header">
  <nav class="nav container">
    <a class="nav-brand" href="/">
      <img src="/assets/logo-icon.png" alt="Global Air Operations Group logo" class="logo-mark logo-mark-dark" />
      <img src="/assets/logo-icon-reverse.png" alt="" aria-hidden="true" class="logo-mark logo-mark-light" />
      <span class="nav-brand-text">Global Air Operations Group</span>
      <span class="nav-brand-short">GAOG</span>
    </a>
    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
    <ul class="nav-links">
      <li><a href="/" data-path="/">Home</a></li>
      <li><a href="/services" data-path="/services"{svc_active}>Services</a></li>
      <li><a href="/insights" data-path="/insights"{insights_active}>Insights</a></li>
      <li><a href="/team-biographies" data-path="/team-biographies">Team Biographies</a></li>
      <li class="nav-cta"><a class="btn btn-primary" href="/contact">Contact Us</a></li>
    </ul>
  </nav>
</header>"""

FOOTER = """<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div>
        <div class="footer-brand"><img class="footer-logo" src="/assets/logo-icon-reverse.png" alt="Global Air Operations Group logo" /> Global Air Operations Group</div>
        <p class="footer-tagline">Strategic Consulting&nbsp;&middot;&nbsp;Operational Planning&nbsp;&middot;&nbsp;Incident Support</p>
      </div>
      <div class="footer-links">
        <div class="footer-col">
          <h4>Site</h4>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/services">Services</a></li>
            <li><a href="/insights">Insights</a></li>
            <li><a href="/team-biographies">Team Biographies</a></li>
            <li><a href="/contact">Contact</a></li>
            <li><a href="/privacy">Privacy Policy</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Contact</h4>
          <ul>
            <li><a href="mailto:info@globalairoperations.com">info@globalairoperations.com</a></li>
            <li><a href="tel:+15309499868">530-949-9868</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Services</h4>
          <ul>
            <li><a href="/services/operational-strategy-incident-support">Operational Strategy &amp; Incident Support</a></li>
            <li><a href="/services/policy-program-development">Policy &amp; Program Development</a></li>
            <li><a href="/services/training-exercises">Training &amp; Exercises</a></li>
            <li><a href="/services/aar-continuous-improvement">AAR &amp; Continuous Improvement</a></li>
            <li><a href="/services/business-consulting">Business Consulting</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="year">2026</span> Global Air Operations Group. All Rights Reserved.</span>
    </div>
  </div>
</footer>

<script src="/script.js"></script>
<script>document.getElementById("year").textContent = new Date().getFullYear();</script>
</body>
</html>"""


INSIGHT_CATEGORY_LABELS = {"article": "Article", "blog": "Blog Post", "business": "Business Highlight"}


def parse_insight_date(date_str):
    return datetime.strptime(date_str, "%b %d, %Y")


def sort_insights_entries(entries):
    """Featured entries always float to the top, in whatever relative order
    they're listed in insights.json (so you control it just by reordering
    them there, or by adding/removing "featured": true). Everything else is
    sorted newest-first by its date, regardless of JSON order."""
    featured = [e for e in entries if e.get("featured")]
    rest = sorted(
        (e for e in entries if not e.get("featured")),
        key=lambda e: parse_insight_date(e["date"]),
        reverse=True,
    )
    return featured + rest



# Per-article card image for the Insights feed's "featured analysis" treatment —
# lets our own original writing read as the flagship piece it is, instead of
# looking like a rectangle identical to nine curated link summaries
# (see stylistic review, Aug 2026).
ARTICLE_CARD_IMAGES = {
    "retardant-is-not-just-for-airtankers-anymore": "/assets/publications/retardant-featured-card.jpg",
}


def render_insight_item(entry, articles_by_slug):
    """One entry in the unified Insights feed — either our own full-length
    article (type: article; links out to wherever it was actually published
    if entry['url'] is set, otherwise to its page on this site) or a curated
    external story (type: watch, always links out to the source). Watch
    entries carry a 'category' — article, blog, or business — shown as a
    small badge next to the outlet name; business-highlight entries also
    swap the "Why we think it matters" label for "Why we think it's worth
    a look" (see stylistic follow-up, Aug 2026 — personalized both labels
    so they read as the team's own commentary rather than a generic,
    Axios-style subhead)."""
    take_label = "Why we think it matters:"
    item_class = "watch-item"
    image_html = ""
    if entry["type"] == "article":
        article = articles_by_slug[entry["slug"]]
        title = article["title"]
        badge = '<span class="watch-source watch-source-own">Our Analysis</span>'
        card_image = ARTICLE_CARD_IMAGES.get(entry["slug"])
        if card_image:
            item_class = "watch-item watch-item-featured"
            image_html = f'          <img class="watch-item-image" src="{card_image}" alt="" aria-hidden="true" />\n'
        if entry.get("url"):
            href = entry["url"]
            link_attrs = ' target="_blank" rel="noopener"'
            icon = ' <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17L17 7M7 7h10v10"/></svg>'
        else:
            href = f"/insights/{entry['slug']}"
            link_attrs = ""
            icon = ""
    else:
        title = entry["title"]
        href = entry["url"]
        category = entry.get("category", "article")
        category_label = INSIGHT_CATEGORY_LABELS.get(category, "Article")
        badge = (f'<span class="watch-category watch-category-{category}">{category_label}</span> '
                 f'<span class="watch-source-name">{esc(entry["source"])}</span>')
        link_attrs = ' target="_blank" rel="noopener"'
        icon = ' <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17L17 7M7 7h10v10"/></svg>'
        if category == "business":
            take_label = "Why we think it's worth a look:"

    # Own-analysis entries never show the Featured pill — the tier heading
    # and the "Our Analysis" badge already say that, and stacking a third
    # label on the only entry in that tier said nothing extra. Curated watch
    # entries keep it since it still distinguishes one story among several
    # (see stylistic review, Aug 2026).
    featured_html = '<span class="watch-featured">Featured</span> ' if (entry.get("featured") and entry["type"] != "article") else ""

    # Byline: only our own analysis pieces carry one — the curated "watch"
    # entries already credit the outlet via the source-name badge instead
    # (see two-tier Insights restructuring, Aug 2026).
    byline_html = ""
    if entry["type"] == "article":
        authors = article.get("authors") or []
        if authors:
            if len(authors) == 1:
                names = authors[0]
            elif len(authors) == 2:
                names = f"{authors[0]} & {authors[1]}"
            else:
                names = ", ".join(authors[:-1]) + f", & {authors[-1]}"
            byline = f"By {names}"
            if article.get("featured_in"):
                byline += f", as featured in {article['featured_in']}"
            byline_html = f'\n            <p class="watch-byline">{esc(byline)}</p>'

    return f"""        <article class="{item_class}">
{image_html}          <div class="watch-item-content">
            <div class="watch-meta">
              {featured_html}{badge}
              <span class="watch-date">{esc(entry['date'])}</span>
            </div>
            <h3><a href="{esc(href)}"{link_attrs}>{esc(title)}{icon}</a></h3>
            <p class="watch-take"><strong>{take_label}</strong> {esc(entry['take'])}</p>{byline_html}
          </div>
        </article>
"""


def build_insights_index(insights_entries, articles_by_slug):
    analysis_entries = sort_insights_entries([e for e in insights_entries if e["type"] == "article"])
    curated_entries = sort_insights_entries([e for e in insights_entries if e["type"] == "watch"])

    analysis_items = "\n".join(render_insight_item(e, articles_by_slug) for e in analysis_entries) if analysis_entries else \
        '        <div class="pub-empty">More original analysis is on the way.</div>\n'
    curated_items = "\n".join(render_insight_item(e, articles_by_slug) for e in curated_entries) if curated_entries else \
        '        <div class="pub-empty">More entries are on the way.</div>\n'

    tiers_html = f"""      <div class="watch-tier watch-tier-analysis">
        <div class="watch-tier-head">
          <h2>Original Analysis</h2>
          <p class="watch-tier-note">Written by our own consultants</p>
        </div>
        <div class="watch-list reveal-group">
{analysis_items}      </div>
      </div>

      <div class="watch-tier watch-tier-curated">
        <div class="watch-tier-head">
          <h2>Industry Watch</h2>
          <p class="watch-tier-note">Curated news &amp; announcements worth your attention</p>
        </div>
        <div class="watch-list reveal-group">
{curated_items}      </div>
      </div>
"""

    nav = NAV.format(insights_active=' class="is-active"', svc_active="")
    return f"""<!doctype html>
<html lang="en">
<head>
<script>document.documentElement.classList.add('js');</script>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />

<!-- PRE-LAUNCH: remove once live on www.globalairoperations.com -->
<meta name="robots" content="noindex, nofollow" />

<title>Insights | Global Air Operations Group</title>
<meta name="description" content="Original analysis from Global Air Operations Group, plus a running, curated watch on the wildfire, aviation, and business news we think is worth your attention." />
<link rel="canonical" href="{DOMAIN}/insights" />

<meta property="og:type" content="website" />
<meta property="og:site_name" content="Global Air Operations Group" />
<meta property="og:title" content="Insights | Global Air Operations Group" />
<meta property="og:description" content="Original analysis, plus a running, curated watch on the wildfire, aviation, and business news we think is worth your attention." />
<meta property="og:url" content="{DOMAIN}/insights" />
{OG_IMAGE_TAGS}
<meta name="twitter:card" content="summary_large_image" />

<link rel="icon" type="image/png" href="/assets/favicon.png" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,500&amp;display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/styles.css" />
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

{nav}

<main id="main">

  <div class="page-header">
    <div class="container">
      <p class="eyebrow">Insights</p>
      <h1>Wildfire, Aviation &amp; Business Insights</h1>
      <p>Original analysis from our consultants, plus a running, curated watch on the industry news, reports, and business moves we think are worth your time.</p>
    </div>
    <img class="page-header-watermark" src="/assets/logo-icon-reverse.png" alt="" aria-hidden="true" />
  </div>

  <section aria-labelledby="watch-list-heading">
    <div class="container">
      <h2 id="watch-list-heading" class="visually-hidden">Latest Insights</h2>
{tiers_html}    </div>
  </section>

</main>

<script src="/scroll-reveal.js" defer></script>
{FOOTER}
"""


def render_body_block(block):
    if block["type"] == "h3":
        return f"        <h2>{esc(block['text'])}</h2>\n"
    if block["type"] == "quote":
        return f'        <blockquote class="pull-quote article-pull-quote">{esc(block["text"])}</blockquote>\n'
    if block["type"] == "stat":
        return (
            f'        <div class="article-stat-callout">'
            f'<span class="stat-value">{esc(block["value"])}</span>'
            f'<span class="stat-detail">{esc(block["detail"])}</span>'
            f'</div>\n'
        )
    return f"        <p>{esc(block['text'])}</p>\n"


def build_article_page(pub):
    byline = " and ".join(pub["authors"])
    body_html = "".join(render_body_block(b) for b in pub["body"])
    featured_line = f' &middot; Featured in {esc(pub["featured_in"])}' if pub.get("featured_in") else ""
    pdf_card = ""
    if pub.get("pdf"):
        pdf_card = f"""
      <div class="pub-list" style="margin-bottom:40px;">
        <a class="pub-item" href="/assets/{pub['pdf']}" target="_blank" rel="noopener">
          <span class="pub-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 2h9l5 5v15H6z"/><path d="M15 2v5h5"/><path d="M9 13h6M9 17h6M9 9h2"/></svg>
          </span>
          <div class="pub-meta">
            <h2>Download as PDF</h2>
            <span>Formatted with letterhead &middot; {esc(pub['date'])}</span>
          </div>
        </a>
      </div>"""

    authors_ld = json.dumps([{"@type": "Person", "name": a} for a in pub["authors"]])
    nav = NAV.format(insights_active=' class="is-active"', svc_active="")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />

<!-- PRE-LAUNCH: remove once live on www.globalairoperations.com -->
<meta name="robots" content="noindex, nofollow" />

<title>{esc(pub['title'])} | Global Air Operations Group</title>
<meta name="description" content="{esc(pub['description'])}" />
<link rel="canonical" href="{DOMAIN}/insights/{pub['slug']}" />

<meta property="og:type" content="article" />
<meta property="og:site_name" content="Global Air Operations Group" />
<meta property="og:title" content="{esc(pub['title'])}" />
<meta property="og:description" content="{esc(pub['description'])}" />
<meta property="og:url" content="{DOMAIN}/insights/{pub['slug']}" />
{OG_IMAGE_TAGS}
<meta name="twitter:card" content="summary_large_image" />

<link rel="icon" type="image/png" href="/assets/favicon.png" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,500&amp;display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/styles.css" />

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": {json.dumps(pub['title'])},
  "author": {authors_ld},
  "publisher": {{ "@type": "Organization", "name": "Global Air Operations Group" }},
  "mainEntityOfPage": "{DOMAIN}/insights/{pub['slug']}",
  "description": {json.dumps(pub['description'])}
}}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

{nav}

<main id="main">

  <div class="page-header page-header-photo">
    <img class="page-header-photo-img" src="/assets/publications/retardant-featured-card.jpg" alt="" aria-hidden="true" />
    <div class="container">
      <p class="eyebrow"><a href="/insights" style="color:inherit;">Insights</a></p>
      <h1>{esc(pub['title'])}</h1>
      <p>By {esc(byline)} &middot; {esc(pub['date'])}{featured_line}</p>
    </div>
  </div>

  <section class="section-alt">
    <div class="container">{pdf_card}
      <article class="article-body" id="full-article">
{body_html}        <p class="article-signature">Written by {esc(byline)}<br>Global Air Operations Group</p>
      </article>
    </div>
  </section>

</main>

{FOOTER}
"""


# ---------------------------------------------------------------- sitemap
def build_sitemap(articles, services):
    urls = [
        ("/", "1.0"),
        ("/services", "0.9"),
        ("/team-biographies", "0.8"),
        ("/insights", "0.8"),
        ("/contact", "0.7"),
        ("/privacy", "0.3"),
    ] + [(f"/services/{s['slug']}", "0.7") for s in services] \
      + [(f"/insights/{p['slug']}", "0.6") for p in articles]
    entries = "\n".join(
        f"  <url>\n    <loc>{DOMAIN}{path}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        for path, prio in urls
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n'


# ---------------------------------------------------------------- main
def main():
    services = load("services.json")
    team = load("team.json")
    articles = load("articles.json")
    insights_entries = load("insights.json")

    # index.html
    index_path = os.path.join(SITE, "index.html")
    with open(index_path) as f:
        index_html = f.read()
    index_html = replace_between(
        index_html, "<!-- SERVICES:START (generated from content/services.json — do not hand-edit, run generate.py) -->",
        "<!-- SERVICES:END -->", build_services_block(services)
    )
    index_html = replace_between(
        index_html, "<!-- TEAM_STRIP:START (generated from content/team.json — do not hand-edit, run generate.py) -->",
        "<!-- TEAM_STRIP:END -->", build_team_strip(team)
    )
    index_html = index_html.replace("{{TEAM_COUNT}}", str(len(team)))
    index_html = index_html.replace("{{SERVICE_COUNT}}", str(len(services)))
    with open(index_path, "w") as f:
        f.write(index_html)
    print(f"index.html: {len(services)} services, team count -> {len(team)}")

    # team-biographies.html
    team_path = os.path.join(SITE, "team-biographies.html")
    with open(team_path) as f:
        team_html = f.read()
    team_html = replace_between(
        team_html, "<!-- TEAM:START (generated from content/team.json — do not hand-edit, run generate.py) -->",
        "<!-- TEAM:END -->", build_team_block(team)
    )
    team_html = replace_between(
        team_html, "<!-- TEAM_LD:START (generated from content/team.json — do not hand-edit, run generate.py) -->",
        "<!-- TEAM_LD:END -->", build_team_ld(team)
    )
    team_html = replace_between(
        team_html, "<!-- BIO_TEMPLATES:START (generated from content/team.json — do not hand-edit, run generate.py) -->",
        "<!-- BIO_TEMPLATES:END -->", build_bio_templates(team)
    )
    team_html = team_html.replace("{{TEAM_COUNT}}", str(len(team)))
    with open(team_path, "w") as f:
        f.write(team_html)
    print(f"team-biographies.html: {len(team)} team members")

    # insights.html (the combined feed: our articles + curated industry watch)
    articles_by_slug = {a["slug"]: a for a in articles}
    insights_index_path = os.path.join(SITE, "insights.html")
    with open(insights_index_path, "w") as f:
        f.write(build_insights_index(insights_entries, articles_by_slug))
    print(f"insights.html: {len(insights_entries)} entrie(s) listed")

    # insights/<slug>.html — one full page per original article
    insights_dir = os.path.join(SITE, "insights")
    os.makedirs(insights_dir, exist_ok=True)
    # clean out any article pages for slugs no longer in the data
    valid_files = {f"{a['slug']}.html" for a in articles}
    for fname in os.listdir(insights_dir):
        if fname.endswith(".html") and fname not in valid_files:
            os.remove(os.path.join(insights_dir, fname))
    for article in articles:
        out_path = os.path.join(insights_dir, f"{article['slug']}.html")
        with open(out_path, "w") as f:
            f.write(build_article_page(article))
        print(f"  insights/{article['slug']}.html written")

    # retire the old /publications URLs (renamed to /insights, pre-launch)
    old_pubs_index = os.path.join(SITE, "publications.html")
    if os.path.exists(old_pubs_index):
        os.remove(old_pubs_index)
        print("removed stale publications.html")
    old_pubs_dir = os.path.join(SITE, "publications")
    if os.path.isdir(old_pubs_dir):
        for fname in os.listdir(old_pubs_dir):
            os.remove(os.path.join(old_pubs_dir, fname))
        os.rmdir(old_pubs_dir)
        print("removed stale publications/ directory")

    # services.html (services index)
    services_index_path = os.path.join(SITE, "services.html")
    with open(services_index_path, "w") as f:
        f.write(build_services_index(services))
    print(f"services.html: {len(services)} service(s) listed")

    # services/<slug>.html
    svc_dir = os.path.join(SITE, "services")
    os.makedirs(svc_dir, exist_ok=True)
    valid_svc_files = {f"{s['slug']}.html" for s in services}
    for fname in os.listdir(svc_dir):
        if fname.endswith(".html") and fname not in valid_svc_files:
            os.remove(os.path.join(svc_dir, fname))
    for svc in services:
        out_path = os.path.join(svc_dir, f"{svc['slug']}.html")
        with open(out_path, "w") as f:
            f.write(build_service_page(svc, articles_by_slug, services))
        print(f"  services/{svc['slug']}.html written")

    # sitemap.xml
    sitemap_path = os.path.join(SITE, "sitemap.xml")
    with open(sitemap_path, "w") as f:
        f.write(build_sitemap(articles, services))
    print("sitemap.xml refreshed")


if __name__ == "__main__":
    main()

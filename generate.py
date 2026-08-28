#!/usr/bin/env python3
"""
Regenerates the parts of this site that are driven by the JSON files in /content.

Run this any time content/services.json, content/team.json, or
content/publications.json changes:

    python3 generate.py

It rewrites the marked blocks in index.html and team-biographies.html,
rebuilds publications.html (the blog index), and writes one page per
publication under publications/<slug>.html. It also refreshes sitemap.xml.

Nothing else on the site is touched — hand-written pages (contact.html,
START-HERE.md, styles.css) are left alone.
"""
import json
import re
import os

SITE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(SITE, "content")
DOMAIN = "https://www.globalairoperations.com"


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
    return f"""        <article class="service-card">
          <div class="service-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">{svc['icon']}</svg>
          </div>
          <h3>{esc(svc['title'])}</h3>
          <p>{esc(svc['description'])}</p>
        </article>
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
            <p class="team-bio">{esc(person['bio'])}</p>{readmore}
          </div>
        </article>
"""


def build_team_block(team):
    return "".join(render_team_card(p) for p in team) + "\n        "


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


# ---------------------------------------------------------------- publications
NAV = """<header class="site-header">
  <nav class="nav container">
    <a class="nav-brand" href="/">
      <img src="/assets/logo-icon.png" alt="Global Air Operations Group logo" class="logo-mark" />
      Global Air Operations Group
    </a>
    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
    <ul class="nav-links">
      <li><a href="/" data-path="/">Home</a></li>
      <li><a href="/publications" data-path="/publications"{pub_active}>Publications</a></li>
      <li><a href="/team-biographies" data-path="/team-biographies">Team Biographies</a></li>
      <li class="nav-cta"><a class="btn btn-primary" href="/contact">Contact Us</a></li>
    </ul>
  </nav>
</header>"""

FOOTER = """<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div>
        <div class="footer-brand"><span class="logo-badge"><img src="/assets/logo-icon.png" alt="Global Air Operations Group logo" /></span> Global Air Operations Group</div>
        <p class="footer-tagline">Strategic Consulting &middot; Operational Planning &middot; Incident Support</p>
      </div>
      <div class="footer-links">
        <div class="footer-col">
          <h4>Site</h4>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/publications">Publications</a></li>
            <li><a href="/team-biographies">Team Biographies</a></li>
            <li><a href="/contact">Contact</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Contact</h4>
          <ul><li><a href="mailto:info@globalairoperations.com">info@globalairoperations.com</a></li></ul>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="year"></span> Global Air Operations Group. All Rights Reserved.</span>
    </div>
  </div>
</footer>

<script src="/script.js"></script>
<script>document.getElementById("year").textContent = new Date().getFullYear();</script>
</body>
</html>"""


def render_pub_card(pub):
    if pub.get("thumbnail"):
        thumb_inner = f'<img src="{esc(pub["thumbnail"])}" alt="" loading="lazy" />'
    else:
        thumb_inner = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 2h9l5 5v15H6z"/><path d="M15 2v5h5"/><path d="M9 13h6M9 17h6M9 9h2"/></svg>'
    featured = f'<span class="pub-featured">{esc(pub["featured_in"])}</span>' if pub.get("featured_in") else ""
    return f"""        <a class="pub-card" href="/publications/{pub['slug']}">
          <div class="pub-card-thumb">{thumb_inner}</div>
          <div class="pub-card-body">
            {featured}
            <h3>{esc(pub['title'])}</h3>
            <span class="pub-card-byline">{esc(' & '.join(pub['authors']))} &middot; {esc(pub['date'])}</span>
            <p class="pub-excerpt clamp">{esc(pub['excerpt'])}</p>
          </div>
        </a>
"""


def build_publications_index(publications):
    cards = "\n".join(render_pub_card(p) for p in publications) if publications else \
        '        <div class="pub-empty">More publications are on the way.</div>\n'
    nav = NAV.format(pub_active=' class="is-active"')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />

<!-- PRE-LAUNCH: remove once live on www.globalairoperations.com -->
<meta name="robots" content="noindex, nofollow" />

<title>Publications | Global Air Operations Group</title>
<meta name="description" content="Field-informed writing from Global Air Operations Group on aviation operations, incident management, and emergency response." />
<link rel="canonical" href="{DOMAIN}/publications" />

<meta property="og:type" content="website" />
<meta property="og:site_name" content="Global Air Operations Group" />
<meta property="og:title" content="Publications | Global Air Operations Group" />
<meta property="og:description" content="Field-informed writing from Global Air Operations Group on aviation operations, incident management, and emergency response." />
<meta property="og:url" content="{DOMAIN}/publications" />
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
      <p class="eyebrow">Resources</p>
      <h1>Publications</h1>
      <p>Field-informed writing on aviation operations, incident management, and emergency response — from consultants who have done the work.</p>
    </div>
    <img class="page-header-watermark" src="/assets/logo-icon.png" alt="" aria-hidden="true" />
  </div>

  <section>
    <div class="container">
      <div class="grid-pubs">
{cards}      </div>
    </div>
  </section>

</main>

{FOOTER}
"""


def render_body_block(block):
    if block["type"] == "h3":
        return f"        <h3>{esc(block['text'])}</h3>\n"
    return f"        <p>{esc(block['text'])}</p>\n"


def build_publication_page(pub):
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
            <h3>Download as PDF</h3>
            <span>Formatted with letterhead &middot; {esc(pub['date'])}</span>
          </div>
        </a>
      </div>"""

    authors_ld = json.dumps([{"@type": "Person", "name": a} for a in pub["authors"]])
    nav = NAV.format(pub_active=' class="is-active"')

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />

<!-- PRE-LAUNCH: remove once live on www.globalairoperations.com -->
<meta name="robots" content="noindex, nofollow" />

<title>{esc(pub['title'])} | Global Air Operations Group</title>
<meta name="description" content="{esc(pub['description'])}" />
<link rel="canonical" href="{DOMAIN}/publications/{pub['slug']}" />

<meta property="og:type" content="article" />
<meta property="og:site_name" content="Global Air Operations Group" />
<meta property="og:title" content="{esc(pub['title'])}" />
<meta property="og:description" content="{esc(pub['description'])}" />
<meta property="og:url" content="{DOMAIN}/publications/{pub['slug']}" />
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
  "mainEntityOfPage": "{DOMAIN}/publications/{pub['slug']}",
  "description": {json.dumps(pub['description'])}
}}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

{nav}

<main id="main">

  <div class="page-header">
    <div class="container">
      <p class="eyebrow"><a href="/publications" style="color:inherit;">Publications</a></p>
      <h1>{esc(pub['title'])}</h1>
      <p>By {esc(byline)} &middot; {esc(pub['date'])}{featured_line}</p>
    </div>
    <img class="page-header-watermark" src="/assets/logo-icon.png" alt="" aria-hidden="true" />
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
def build_sitemap(publications):
    urls = [
        ("/", "1.0"),
        ("/team-biographies", "0.8"),
        ("/publications", "0.8"),
        ("/contact", "0.7"),
    ] + [(f"/publications/{p['slug']}", "0.6") for p in publications]
    entries = "\n".join(
        f"  <url>\n    <loc>{DOMAIN}{path}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        for path, prio in urls
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n'


# ---------------------------------------------------------------- main
def main():
    services = load("services.json")
    team = load("team.json")
    publications = load("publications.json")

    # index.html
    index_path = os.path.join(SITE, "index.html")
    with open(index_path) as f:
        index_html = f.read()
    index_html = replace_between(
        index_html, "<!-- SERVICES:START (generated from content/services.json — do not hand-edit, run generate.py) -->",
        "<!-- SERVICES:END -->", build_services_block(services)
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

    # publications.html (blog index)
    pubs_index_path = os.path.join(SITE, "publications.html")
    with open(pubs_index_path, "w") as f:
        f.write(build_publications_index(publications))
    print(f"publications.html: {len(publications)} post(s) listed")

    # publications/<slug>.html
    pubs_dir = os.path.join(SITE, "publications")
    os.makedirs(pubs_dir, exist_ok=True)
    # clean out any post pages for slugs no longer in the data
    valid_files = {f"{p['slug']}.html" for p in publications}
    for fname in os.listdir(pubs_dir):
        if fname.endswith(".html") and fname not in valid_files:
            os.remove(os.path.join(pubs_dir, fname))
    for pub in publications:
        out_path = os.path.join(pubs_dir, f"{pub['slug']}.html")
        with open(out_path, "w") as f:
            f.write(build_publication_page(pub))
        print(f"  publications/{pub['slug']}.html written")

    # sitemap.xml
    sitemap_path = os.path.join(SITE, "sitemap.xml")
    with open(sitemap_path, "w") as f:
        f.write(build_sitemap(publications))
    print("sitemap.xml refreshed")


if __name__ == "__main__":
    main()

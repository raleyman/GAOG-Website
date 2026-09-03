# Your site — what's here and how to grow it

This folder is your whole website: Home, Services, Insights (original articles plus a curated industry-news feed), Team Biographies, and Contact — styled and optimized for search engines. You don't need to open or understand any of these files. For almost everything below, the fastest path is: tell Claude what you want added or changed, and hand over this folder (or the live GitHub/Vercel project once it's connected).

## What's new in this round

- **Publications is now "Insights"** (`/insights`, was `/publications`) — one combined, running feed instead of a separate blog section. It holds two kinds of entries in a single list, newest/most-important at the top: your own original articles (badged "Our Analysis," link to a full page on this site, same as before) and short curated entries about outside news you think is worth flagging (a source tag, a link that opens the original story in a new tab, and a couple of sentences in your own voice on why it matters). See `content/insights.json` below — this is the file for your weekly "add a link and a sentence or two" routine.
- **Services now have their own real page and their own page per service** (`/services`, and `/services/<its-name>` for each one). The homepage still shows the five short teaser cards, but each one now links to a full page with real depth: a proper explanation, a "What's Included" bullet list, and (where there's something real and specific to say) a short credentials line and a link to the related published article. Every service page ends with a "talk to us" button, and there's a new "View All Services" link on the homepage.
- **Scalable content system.** Consultants, services, articles, and curated insights now live in simple data files instead of being hand-typed into the page HTML. Adding one is a small, safe edit — not a rebuild.
- **New service: Business Consulting** — "Considering starting a business in the fire space? We help vet your idea and get you started."
- **New Contact page** (`/contact`) — a proper form (name, email, organization, topic dropdown, message) plus your email and response-time info, separate from the homepage.
- **CAL FIRE and USFS given equal billing** on the homepage, and the positioning broadened from "statewide" to national fireline leadership and global reach — so the language doesn't read as California-only or favor one agency.
- **New homepage hero photo** — the flat dark background is replaced with a full-bleed black-and-white aerial wildfire photo, with the logo large and glowing on the right side (`assets/hero-photo.jpg`). Every other page's header banner still carries the smaller watermark version of the icon.

## How to add things later (the easy way)

Just tell Claude (or whoever's helping you) what you want, for example:
- "Add a new consultant, [name], [title], here's their bio..."
- "We're now offering a new service called X, here's the description..."
- "Here's a new article we wrote, can you publish it as a blog post?"
- "Add this to Insights: [link], and here's why it matters: [a sentence or two]."

That person edits one of the files below and runs one command (`pnpm build`) to rebuild the site — nothing else needs to change, and nothing gets accidentally broken.

### The files that drive the site (all in `content/`)

- **`content/team.json`** — one entry per consultant: name, role, a short teaser bio (shown on the card), education, `photo` (path to their headshot), and `full_bio` — a list of paragraphs for their complete biography. Clicking a consultant's photo, or the "Read Full Biography" link, opens their full bio in a popup right on the page. Add a new entry to add a new consultant; removing one takes them off the site. If a person has no `photo`, their card just shows colored initials instead — still works fine, just less personal. If a person has no `full_bio`, the card just won't be clickable — no popup, no broken link.
- **`content/services.json`** — one entry per service. `icon`, `title`, and `description` still power the short homepage teaser card, same as before. New fields power the service's own full page: `slug` (its URL), `summary` (a one-sentence intro for the top of the page), `body` (a list of paragraphs — the real explanation), `included` (a bulleted list of what's specifically covered), and two optional fields — `credentials_note` (a short line naming a real, specific qualification or agency tie, if there's one worth calling out) and `related_publication` (the slug of an article in `content/articles.json` to cross-link, if one applies). Add a new entry with all of these to add a new service with its own page.
- **`content/articles.json`** — one entry per full-length original article: title, authors, date, short excerpt, and the full body text (broken into paragraphs/subheadings). Add an entry to write a new full article; it automatically gets its own page. Optional fields: `thumbnail`, `pdf`, and `featured_in` (e.g. `"AerialFire Magazine"`, for pieces published somewhere else first). Writing one of these is the rare, occasional case — most updates to Insights are the file below instead.
- **`content/insights.json`** — **this is the one you'll touch most often.** It's the ordered list that drives the whole `/insights` page, top to bottom. Two kinds of entries:
  - `"type": "article"` — points at an entry in `content/articles.json` by its `slug`, plus your own `date` and `take` ("why it matters") for how it should read on the feed. Use this to feature one of your full articles.
  - `"type": "watch"` — a curated outside story: `source` (the outlet's name), `url` (link to the original story — opens in a new tab), `date`, `title` (the headline, written or copied as-is), and `take` (a sentence or two, in your own voice, on why it matters to someone in this field). This is the weekly routine: find a story, add one of these entries at the top of the list, write your one or two sentences, done.
  - A couple of ground rules for `take`: don't copy the source article's own text into it — write your own reaction; and don't reproduce the source's paragraphs anywhere on the site, since that's their copyrighted work. A link plus your own short commentary is exactly the right amount to use.
  - Featured entries stay at the top; everything else is sorted newest-first by date automatically at build time.

### The one command: `pnpm build`

After any of those files change, running:

```
pnpm install   # first time only, or after dependencies change
pnpm build
```

from inside this folder rebuilds the whole site (homepage, services, team page, Insights feed, every article and service page) and refreshes the sitemap automatically. For local preview while editing, use `pnpm dev` and open the local address it prints. If you're not comfortable running this yourself, just ask Claude to do it for you — that's the normal way this will work going forward.

## Team photos

Every consultant now has a real headshot on the Team Biographies page (`public/assets/team/`), cropped square and optimized for the web. To swap a photo or add one for a new hire, drop the image anywhere handy, ask Claude to crop and add it, and it'll update `content/team.json`'s `photo` field and re-run the build.

I also noticed the GAOG Google Drive has some internal files unrelated to the website (an operations/billing workbook and a Perimeter Solutions field binder marked proprietary) sitting in the same shared folder as the site assets. I didn't use or touch those — just flagging in case you want the website assets kept in a more separate folder going forward.

## How to get this live on Vercel (no coding required)

1. Go to vercel.com and sign up for a free account (you can sign up with just an email or a GitHub account).
2. Once logged in, click **"Add New Project"**.
3. Vercel will offer to import from GitHub. Connect the repo — Vercel detects Astro automatically and runs `pnpm build`, outputting the `dist/` folder.
4. Click Deploy. Within about a minute you'll get a free web address like `global-air-operations.vercel.app` — that's your staging link. Share that with me or anyone else to preview it before it's public.
5. **Important:** the pages currently have a "noindex" tag in them so Google doesn't index the staging link. Tell me when you're ready to go live and I'll remove that before the final switch.

## Swapping over your real domain (globalairoperations.com)

When you're happy with the staging version:

1. In the Vercel project, go to **Settings → Domains** and add `www.globalairoperations.com`.
2. Vercel will give you one or two DNS records to add (usually a CNAME or an A record).
3. Log into GoDaddy, find that domain's DNS settings, and add the records Vercel gave you. I can walk you through this step-by-step when you're there — just share your screen or paste what GoDaddy shows you.
4. DNS changes usually go live within a few minutes to a few hours.
5. Once it's live, tell me and I'll remove the "noindex" tags and submit the sitemap to Google Search Console so it starts getting indexed properly.

## Making changes later

Once it's live, you never need to touch code. Just come back and tell me what you want changed — new consultant, new service, new blog post, updated bio, different wording — and I'll edit the content files, run the build, and push the update (or send you the updated version to re-deploy).

# Friends & Co mockup site — handoff brief

Everything a new assistant needs to pick this up. Read this file first, then
`styleguide.html` in a browser, then `build.py`.

---

## 1. What this project is

`friendsco-theme-mockups` is a **complete parallel mock-website** for Friends & Co
(friendsco.org), a Minnesota nonprofit that runs free friendship programs for adults 62+.

It is a set of static HTML files. It is **not** WordPress, and nothing in this folder
touches, publishes to, or modifies the live site.

**The commercial purpose matters, because it drives the technical constraints.**
Mari (Up Top Studio) is redesigning the site for the client, Paul. The plan is to show him
the finished design for free, and charge only for build time. For that offer to work, the
mockup must be convincing enough to approve as-is.

That produces the single hardest requirement:

> **A mockup page must render identically to what the finished Elementor build will look
> like.** Not "similar". If a heading is 44px on the live site, it is 44px here.

---

## 2. Where things are

### 2.1 The root

Everything for this client lives under one Google Drive folder, synced locally on macOS:

```
/Users/marnie/My Drive - Up Top/friends-and-co/
```

`My Drive - Up Top` is the Google Drive mount for Up Top Studio. `friends-and-co` is the
client folder. **Everything below is relative to that path.**

### 2.2 The redesign root

```
friends-and-co/friendsco-theme-mockups/
```

This is the only folder you normally need to write to. It is a **git repo**:

- remote: `https://github.com/shafferma08/friendsco-theme-mockups.git`
- branch: `main`
- published via GitHub Pages, e.g.
  `https://shafferma08.github.io/friendsco-theme-mockups/home-mockup.html`

That published URL is how Paul reviews the mockups, which is why every internal link must
resolve to a local file in this repo.

### 2.3 Reference material in the parent folder

Read-only. Don't reorganise these — Mari and the client both rely on the structure.

| Path | What's in it |
|---|---|
| `FriendsCo Identity Guidelines_5-21-22.pdf` | **The brand guide.** Colour palette p.9, logo colours p.7, typography p.8. |
| `Website Sitemap - friendsco.docx` | Current sitemap, navigation and content-type overview. |
| `Sitemap for Friends & Co.docx` | Earlier sitemap draft. |
| `Friends & Co Audit.docx` | Original site audit. |
| `Friends & Co Website Redesign_ Project Outline & Payment Plan.pdf` | Scope and commercials. |
| `heading-fix-checklist.md` | Heading-tag punch list. ⚠️ Type sizes in it are the *plan*, not what was saved. |
| `home-page-checklist.md`, `action-plan-today.md` | Working notes. |
| `Logins.docx` | Credentials. Do not read unless explicitly asked. |
| `friendsco-font-guide.docx` | Font notes. |
| `Website Fixes & Edits.docx` | Running client fix list. |
| `template-exports/elementor-4935-2026-03-17.json` | **Elementor export — search results template only.** Not the giving pages. |
| `Design/` | 743MB of design assets, incl. `branding assets/`, `assets from website/`, `albiol/`, `placeholder pics/`, and PDF mockups. |
| `Friendship Services & Be a Friend/` | Programme photography (AdobeStock originals, 8–13MB each). |
| `branding assets/`, `assets from website/`, `web assets/` | Logos, patterns, accreditation badges, site imagery. |
| `Friends & Co/` | Misc working docs, incl. `Phone-Companions-Elementor-Build.md` ⚠️ **stale, see §5**. |
| `friendsco-project-hub/` | `index.html` + `timeline.html` — a small client-facing project hub. |
| `Meeting Minutes/`, `Phase 1/`, `screenshots/`, `team photos/`, `popups/`, `footer/`, `code/`, `Canva Videos/`, `ig-pics/` | Supporting material. |
| `homepage-mockup/`, `F&CO Website Redesign-.../`, `300ppi-.../` | Older mockup and asset drops, largely superseded. |

**Where to find images:** check `assets/img/` in the repo first. If it isn't there, look in
`Design/branding assets/`, `Design/assets from website/`, `assets from website/`, or
`Friendship Services & Be a Friend/`. Originals are often 8–13MB — resize to ~1600px
before adding them to the repo. Client has approved referencing images directly from
friendsco.org where no local copy exists.

### 2.4 Inside the redesign folder

```
friendsco-theme-mockups/            ← git repo, published to GitHub Pages
├── HANDOFF.md                  ← this file
├── styleguide.html             ← the design system, rendered. Also the artifact for Paul.
├── _template.html              ← starter page, house rules in comments
├── build.py                    ← page generator. Most pages are defined here.
├── lint.py                     ← consistency + link checker. Run before you finish.
├── *.html                      ← 26 mockup pages
├── _archive/                   ← 12 superseded originals. Ignore. Do not revive.
└── assets/
    ├── css/
    │   ├── friendsco.css       ← THE design system. All tokens live here.
    │   ├── chrome.css          ← header, nav, footer, trust strip
    │   ├── pages/*.css         ← page-specific only (home, donate)
    │   └── global.css          ← ORPHANED, contradicts the system. Ignore.
    ├── js/
    │   ├── chrome.js           ← header + footer markup, injected into every page
    │   └── home.js             ← home page hero video + tabs
    ├── img/                    ← local images
    └── fonts/Albiol.ttf        ← display/word-art only, never body or UI
```

---

## 3. Architecture

**Three layers, in cascade order:**

1. `friendsco.css` — every design token (colour, type, spacing, radius) plus base
   elements and shared components (buttons, cards, steps, FAQ, forms, heroes, stats…).
2. `chrome.css` — header, navigation, footer.
3. `assets/css/pages/<page>.css` — only if a page genuinely needs something unique.

**Header and footer are injected by JavaScript.** A page contains:

```html
<body data-page="support">
  <div data-chrome="header"></div>
  <main> … </main>
  <div data-chrome="footer"></div>
  <script src="assets/js/chrome.js"></script>
```

`data-page` sets the active nav item. Valid values:
`home | programs | volunteer | about | support` (or empty for none).

Chrome is delivered as JS rather than fetched HTML partials so the mockups work both on
GitHub Pages **and** when opened directly from disk (`fetch()` is blocked on `file://`,
`<script src>` is not).

**Most pages are generated.** `build.py` defines each page as a short spec composed of
section helpers, then writes the HTML. Run `python3 build.py` to rebuild all, or
`python3 build.py donate` for one. Two pages are hand-written and NOT in build.py:
`home-mockup.html` and `donate.html` — edit those directly.

### Section helpers in `build.py`

General purpose: `hero`, `prose`, `statement`, `cards`, `checklist`, `steps`, `faq`,
`factbox`, `media`, `cta`, `closing`, `notice`, `raw`.

Matched to the live giving pages — prefer these when mirroring:

| Helper | Where it comes from |
|---|---|
| `pattern_hero` | Support: graphic pattern + teal wash, photo card left, white card right |
| `pattern_page_hero` | Planned giving / corporate / other ways: pattern, centred, white type |
| `pattern_cta` | Closing band on the pattern, white type, white button |
| `split_hero` | Phone Companions: photo one side, solid accent panel with ampersand watermark |
| `colour_cards` | Support "Ways to support": 2×2, icon+heading+button share one accent |
| `colour_stats` | Support "Impact at a glance": solid filled discs, coloured numbers |
| `option_grid` / `option_card` | Other ways to give: 2-col cards, accent rule on top |
| `icon_steps` | Phone Companions "How it works": centred discs, blue headings |
| `faq_cards` | Phone Companions FAQ: blue band, flower watermark, tinted cards |
| `choice_band` | Phone Companions "Get connected": tilted photo + stacked choice cards |
| `split` | Planned giving / corporate: body copy beside an accented panel |
| `jumpnav` | Anchor bar |
| `quote` | Testimonial band |

### Per-page accent identity

Each giving page has its own colour, applied as the wash over the pattern and through
its components. This is deliberate — do not normalise it.

| Page | Accent |
|---|---|
| Support Friends & Co | teal hero wash; cards magenta / lime / orange / teal |
| Planned giving | teal wash, lime advisor panel |
| Corporate sponsorship | blue wash, magenta panel rule, teal icon |
| Other ways to give | magenta wash; cards blue / magenta / green / orange / teal / slate |
| Phone Companions | orange (solid panel, not a wash) |
| Donate | magenta band |

---

## 4. Hard rules — do not break these

These are not preferences. Each one was a real bug that made mockups unbuildable.

| Rule | Why |
|---|---|
| **No links to friendsco.org** | Paul must be able to click through the whole mockup without landing on the live site. Use local `.html` filenames. `mailto:` is fine. Images may be referenced from friendsco.org (client approved). `lint.py` enforces this. |
| **Open Sans only. No condensed face.** | The brand guide lists Akzidenz-Grotesk Pro Medium Condensed but says for external work "the Open Sans family is the preferred choice". Akzidenz is not licensed for web and is not on the live site. Earlier mockups used Roboto Condensed as a stand-in — that is the single biggest reason they didn't match. |
| **Never set `html{font-size}` above 100%** | Root stays 16px. Body is 1.3rem (20.8px). One old mockup set a 20px root, silently scaling every `rem` by 30%, so it could never be matched in Elementor. |
| **Sentence case everywhere. Never `text-transform: uppercase`.** | Standing client rule (Paul). Program names keep capitals — they're proper nouns (Coffee Talk, Cards Connect). This applies to the *literal* capitalisation too, not just the CSS: write "Planned giving", not "Planned Giving". **The live site uses title case on several giving pages; the mockups deliberately diverge.** Decided 2026-07-19 — internal consistency beats matching live on this one point. `lint.py` enforces it; add legitimate names to `PROPER_NOUNS` there. |
| **Never redefine tokens in a page** | All tokens live in `friendsco.css`. If a page needs something new, add it there so every page gets it. |
| **No raw hex outside the token block** | Raw hex bypasses the brand-tier labelling and is how off-brand colours crept in unnoticed. |
| **Content column is 1140px** | Elementor's default, and what the live site measures. Old mockups variously used 1180 / 1200 / 1250. |

---

## 5. The source of truth for type and colour

The client's Elementor kit is **post 1392**. Its compiled settings are at:

```
https://friendsco.org/wp-content/uploads/elementor/css/post-1392.css
```

To read it: open a browser tab on friendsco.org and `fetch()` the file same-origin, then
regex it. `cssRules` is CORS-blocked and `getComputedStyle(root)` returns empty for the
`--e-global-*` variables, so parsing the file text is the only reliable route.

**There are two separate typography systems in that file and they do not agree:**

- **Theme Style → Typography** — selectors `.elementor-kit-1392 h1 … h6`. This is what a
  plain heading tag inherits. This is what `friendsco.css` mirrors.
- **Global Fonts** — the `--e-global-typography-*` named styles (Hero Title, Section
  Heading, Card Title, Big Statement, Button, Eyebrow Label). "Big Statement" is 1.6rem
  and is *not* H4 (1.5rem). They look like a duplicate; both are intentional.

**Verified values (desktop):**

| | Size | Weight | Line height |
|---|---|---|---|
| H1 | 3.2rem / 51.2px | 700 | 1.3 |
| H2 | 2.75rem / 44px | 700 | 1.3 |
| H3 | 2rem / 32px | 600 | 1.3 |
| H4 | 1.5rem / 24px | 600 | 1.35 |
| H5 | 1.35rem / 21.6px | 600 | 1.4 |
| H6 | 1.25rem / 20px | 600 | 1.4 |
| Body | 1.3rem / 20.8px | 400 | 1.6 |

Breakpoints are **1024px and 575px** — not the usual 768px. Tablet steps: H1 3rem,
H2 2.4rem, H3 1.8rem, H4 1.4rem. Mobile: H1 2rem, H2 1.8rem, H3 1.5rem, H4 1.3rem.

⚠️ `heading-fix-checklist.md` in the parent folder is the *plan*, not what was saved.
It lists H2 at 2.5rem and H3 at 1.7rem; the live kit has 2.75 and 2. Always trust
`post-1392.css`.

⚠️ `Friends & Co/Phone-Companions-Elementor-Build.md` is **stale and wrong** — it
specifies Roboto Condensed uppercase headings, `#FAFAFA` background, 1200px container and
a 768px breakpoint. All four are incorrect. Do not follow it.

---

## 6. Colour, and the open decisions

`friendsco.css` sorts every colour into labelled tiers. Keep that labelling intact.

**Tier 1 — on brand** (Identity Guidelines p.9; all six are Elementor Global Colors, and
every HEX matches the guidelines exactly):
blue `#5E74B1` · magenta `#BA3F97` · lime `#B0D235` · teal `#00BBD3` · orange `#F9A41E` ·
slate `#7D91A0`

**Tier 2 — logo only:** green `#85C340` (PMS 2294). In the logo spec (p.7) but *not* the
p.9 palette, and not a Global Color. Currently used for buttons and tiles.

**Tier 3b — brand tints:** `#F7FDDF` (page background) and `#DFF0A8` (hairlines). These
are **tints of the brand lime**, hue 72°/74° against lime's 73° — PMS 2292 at ~7%
strength. Do not call this "cream": the old warm cream was `#FBF6EF` at hue 35°, an
orange, and the name caused real confusion. Canonical token is `--lime-tint`.

**Tier 4 — off brand:** navy `#1A2A42`, footer band `#4B5D91`, pale blue `#EEF2FB`.
In heavy use, absent from the guidelines, not tints of anything.

**Open decisions awaiting Paul** (documented in `styleguide.html`):
1. Green — promote to the palette, or restrict to the logo?
2. Navy, footer band, pale blue — approve as brand extensions, or replace?
3. The lime tints — should be near-automatic approvals, since they're tints of an
   existing palette colour.

**Page background:** Paul wants the site off white and onto the yellow-green. This is a
role token — `--surface` in `friendsco.css`, currently `var(--lime-tint)`. Point it at
`var(--white)` to flip the entire site back. Deliberately a one-line change.

Contrast is checked and holds: body `#333` reads 12.08:1 on the tint (AAA) vs 12.63:1 on
white. Caution — blue text drops to 4.35:1, fine at 20.8px body size but not smaller.

---

## 7. Status

**26 mockup pages built, all on the shared system, lint clean.**

Live pages already rebuilt in Elementor — these are mirrored, **not** restyled, because
they're the "already finished" proof for the pitch:
`donate` · `planned-giving` · `corporate-sponsorship` · `other-ways-to-give` ·
`phone-companions` · `support-friends-co`

Other pages: `home-mockup` · `friendship-services` · `coffee-talk` · `visiting-companions`
· `cards-connect` · `lets-do-events` · `spanish-language-programs` · `about` ·
`staff-and-board` · `annual-reports` · `news` · `contact` · `events` ·
`remembering-our-friends` · `get-involved` · `refer` · `join` · `volunteer-apply` ·
`search-results` · `404` · `styleguide`

**Built 2026-07-19** — the nine that used to be dead `#` links: the five volunteer role
pages (`volunteer-coffee-talk`, `-phone-companion`, `-visiting-companion`,
`-cards-connect`, `-admin`), `volunteer-portal`, `visiting-companions-match`,
`news-article` (single-post template) and `event-detail` (single-event template).

All five role pages use the Phone Companions visual language via the `role_page()`
builder — that page is the model for the modern look and the rest of the site should be
brought toward it.

⚠️ Only `volunteer-coffee-talk` has real copy. On the live site the other four role
pages say "Full details coming soon!", so their content in the mockups is **drafted, not
client-approved**. Flag that when showing Paul.

Only 3 placeholder `#` links remain: the portal sign-in button and two annual-report
downloads that need real files.

**All six giving pages have been verified against the live rendered pages** (2026-07-19)
and match: layout, imagery, per-page accent, component treatments. The invented closing
CTAs were removed from corporate sponsorship and phone-companions.

**Known gaps to fix before Paul sees it:**
- `staff-and-board.html` and `annual-reports.html` have real structure but **placeholder
  content** — no actual staff names or report links. These will read as unfinished.
- The live Phone Companions FAQ uses `h2` for three of four questions and `h3` for the
  first. The mockup uses `h3` throughout, which is structurally correct but diverges from
  live. Decision pending.
- The live "YES, SIGN ME UP!" button on Phone Companions is CSS-uppercased, breaking the
  sentence-case rule. Worth fixing on the live site.
- **The five other program pages do not match live.** Coffee talk, visiting companions,
  cards connect, let's do events, conexiones comunitarias were built as new-design
  proposals, on the assumption their live versions were the old design. That assumption
  is **wrong** — checked 2026-07-19. Coffee Talk at least is a fully designed page in a
  *third* visual language: split hero with a curved-edge teal panel, wave section divider,
  embedded video. Decide with Mari whether these should be mirrored like the giving pages
  or left as redesign proposals.

---

## 8. How to verify your work

```bash
cd "/Users/marnie/My Drive - Up Top/friends-and-co/friendsco-theme-mockups"
python3 build.py       # regenerate pages
python3 lint.py        # must report 0 issues
```

`lint.py` checks for: condensed fonts, redefined tokens, inflated root font size,
uppercase text, raw hex, inline header/footer markup, links to friendsco.org, and broken
internal links. It also counts placeholder `#` links.

**For visual/computed verification**, a headless browser is worth setting up:

```bash
pip install playwright --break-system-packages
playwright install chromium
```

On a sandboxed Linux host missing `libXdamage.so.1`, without root:
```bash
cd /tmp && apt-get download libxdamage1 && dpkg-deb -x libxdamage1*.deb libs
export LD_LIBRARY_PATH=/tmp/libs/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH
```

Serve with `python3 -m http.server 8899` and load pages from `http://localhost:8899/`.

**The definitive typography check:** inject bare `h1`–`h6` into the live friendsco.org
DOM, read computed styles, then render the mockup headless at 1200 / 900 / 480px and
compare. They should match to the pixel.

---

## 8b. Look at the rendered page, never just the DOM

This is the most expensive lesson from the build so far, learned five times in a row.

Reading a page's DOM structure tells you what widgets exist. It does **not** tell you what
the page looks like. Every one of the six giving pages was rebuilt wrong the first time
because the DOM said "hero section, image widget" and the actual page was something else
entirely — a brand pattern under a colour wash, a split panel, a card grid.

Concretely, what the DOM hid:

- The graphic pattern hero is a background image plus a `::before` colour wash at 69%
  opacity. Without the wash the pattern is far too vivid and white type is unreadable.
- The wash colour differs per page (teal / blue / magenta) and defines the page's identity.
- Other ways to give looked like six stacked full-width bands in the DOM. It's a
  two-column card grid.
- Phone Companions' hero is a split — photo one side, solid orange panel the other.

**Procedure:** navigate to the live page, take screenshots the whole way down, *then*
query computed styles for the exact values. Check `::before` and `::after` on every
section — that's where the washes live. Check `background-size` too; several sections use
a fixed `2704px` rather than `cover`.

## 9. Gotchas that will cost you time

- **Scraping live pages while logged in** pulls in the WordPress admin bar. Scope to
  `[data-elementor-type="wp-page"]`.
- **The browser tool blocks output containing query strings** ("Cookie/query string
  data"). Strip `?…` from image URLs before returning scraped content.
- **`build.py` content is authored as HTML** — it already contains `&amp;` and `&rsquo;`.
  The `e()` helper is deliberately a pass-through. Do not add escaping or you'll get
  "Friends &amp; Co" rendered literally.
- **Don't use `%`-formatting for CSS gradients** in build.py — they're full of percent
  signs. Use concatenation (see `photo_hero`).
- **SVG must stay `display: inline`** — a `display:block` reset drops nav carets and
  footer chevrons onto their own line.
- **Images from the client's Design folders are 8–13MB.** Resize to ~1600px before use.
- **Lazy-loaded images inside hidden tab panels** report `naturalWidth === 0`. That's not
  a broken image — force `loading="eager"` and remove `[hidden]` before checking.
- **US English.** This is a Minnesota nonprofit — "program", not "programme".

---

## 10. Working with Mari

- She goes by **Mari**, not Marnie.
- Prefers concise, direct answers. Minimal preamble.
- Wants to be challenged if an approach is wrong, not just followed.
- Wants research before "I can't" — check the live site, the brand guide, the kit CSS.
- Show visible progress. Infrastructure work that produces no viewable pages reads as no
  progress, even when it's the thing making later work fast. Ship a page early.
- Be straight about gaps. She'd rather hear "this section is placeholder" than find out
  when Paul does.

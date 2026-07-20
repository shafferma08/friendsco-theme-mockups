# Handoff prompt

Copy everything below the line into a new AI session.

---

I'm continuing work on a website redesign mockup. Read this whole message before acting.

## Where everything is

- **Client root:** `/Users/marnie/My Drive - Up Top/friends-and-co/`
- **Project root (work here):** `/Users/marnie/My Drive - Up Top/friends-and-co/friendsco-theme-mockups/`

The project root is a git repo (`main`, remote `github.com/shafferma08/friendsco-theme-mockups`)
published via GitHub Pages. That published URL is how the client reviews the work.

**First: read `HANDOFF.md` in the project root.** It's the full briefing — architecture,
rules, the Elementor source of truth, folder map, current status, and gotchas. Then open
`styleguide.html` in a browser and skim `build.py`. Don't skip this; several things in
this project are counter-intuitive and documented there.

## What this is

A complete static-HTML mock-website for Friends & Co (friendsco.org), a Minnesota
nonprofit running free friendship programs for adults 62+.

It is **not** WordPress. Nothing in this folder touches, publishes to, or modifies the
live site. If I ask you to change a page, you're changing local HTML.

**The commercial context drives everything technical:** Mari (Up Top Studio) is giving the
client the design for free and charging only for build time. For that to work, the client
has to be able to approve the mockup as-is. So:

> A mockup page must render **identically** to what the finished Elementor build will look
> like. Not "similar." If a heading is 44px on the live site, it's 44px here.

## Non-negotiable rules

1. **No links to friendsco.org.** The client must click through the entire mockup without
   landing on the live site. Use local `.html` filenames. `mailto:` and `tel:` are fine.
   Images *may* be referenced from friendsco.org — the client approved that.
2. **Open Sans only. No condensed face.** The brand guide lists Akzidenz-Grotesk Pro
   Medium Condensed but says Open Sans is preferred for external work. Akzidenz isn't
   licensed for web and isn't on the live site. Earlier mockups substituted Roboto
   Condensed — that's the single biggest reason they didn't match.
3. **Never set `html{font-size}` above 100%.** Root stays 16px; body is 1.3rem (20.8px).
   An old mockup used a 20px root and silently scaled every `rem` by 30%.
4. **Sentence case everywhere. Never `text-transform: uppercase`.** Standing client rule.
   Program names keep their capitals — they're proper nouns (Coffee Talk, Cards Connect).
5. **Never redefine design tokens in a page.** They all live in
   `assets/css/friendsco.css`. If a page needs something new, add it there.
6. **No raw hex outside the token block.** Raw hex bypasses the brand-tier labelling.
7. **Content column is 1140px** (Elementor's default, and what the live site measures).
8. **US English.** Minnesota nonprofit — "program", not "programme".

## How the code works

- Design system: `assets/css/friendsco.css` → `assets/css/chrome.css` →
  `assets/css/pages/<page>.css` (only if truly page-specific).
- Header and footer are **injected by `assets/js/chrome.js`**. Pages use
  `<div data-chrome="header">`, `<div data-chrome="footer">`, and
  `<body data-page="home|programs|volunteer|about|support">`.
- Most pages are **generated** from short specs in `build.py`. Run `python3 build.py`
  to rebuild all, or `python3 build.py donate` for one.
- **Two pages bypass build.py** and are edited directly: `home-mockup.html` and
  `donate.html`.
- `_archive/` holds 12 superseded originals. Ignore them. Don't revive them.
- `assets/css/global.css` is orphaned and contradicts the system. Ignore it.

## Always verify before you say you're done

```bash
cd "/Users/marnie/My Drive - Up Top/friends-and-co/friendsco-theme-mockups"
python3 build.py
python3 lint.py      # must report 0 issues
```

`lint.py` catches condensed fonts, redefined tokens, inflated root size, uppercase text,
raw hex, inline header/footer markup, links to friendsco.org, and broken internal links.

For visual work, set up headless Chromium (see §8 of HANDOFF.md, including the
`libXdamage` workaround for sandboxed Linux) and compare against the live site.

## Context you won't find in the files

These are judgment calls and observations from the previous session. Treat them as
starting positions, not settled facts — check with Mari before acting on any of them.

**Open decisions waiting on the client (Paul):**
- Green `#85C340` is in the logo spec but not the colour palette, and isn't an Elementor
  Global Color. It's used on buttons and tiles. Promote it, or restrict it to the logo?
- Navy `#1A2A42`, footer band `#4B5D91` and pale blue `#EEF2FB` are used heavily but
  appear nowhere in the brand guide. **My view: don't remove them** — the design would go
  flat. Approve them as brand extensions and register them as Global Colors instead. It's
  roughly 20 minutes of work and makes the whole palette editable from one screen. That's
  a concrete, demonstrable win to put in front of Paul.
- The yellow-green page background `#F7FDDF` and its hairline `#DFF0A8` should be easy
  approvals — they're tints of the brand lime (hue 72°/74° vs lime's 73°), not new
  colours. Frame them that way and the conversation is much shorter.

**Deliberate divergences from the live site — flag before "fixing" them:**
- The home hero `h1` uses weight 800 / line-height 1.1 versus the global 700 / 1.3. Kept
  as a deliberate hero exception because it reads better.
- `corporate-sponsorship.html` and `phone-companions.html` each have a closing CTA
  section that does **not** exist on the live pages. Added for consistency across the
  giving pages. Remove if strict fidelity wins.
- The live Phone Companions FAQ uses `h2` for three of four questions and `h3` for the
  first. The mockup uses `h3` throughout — structurally correct, but doesn't match live.

**Known gaps that will embarrass us if the client sees them first:**
- `staff-and-board.html` and `annual-reports.html` have real structure but **placeholder
  content** — no actual staff names, no real report links. These need Mari's content.
- 18 links currently resolve to `#` — the 5 volunteer role pages, volunteer portal,
  matching hub, individual news articles and event pages. Mostly login- or plugin-driven,
  so they were deliberately deferred.

**Worth raising with Mari at some point:**
- Now that the page background is the yellow-green tint, pale blue `#EEF2FB` gives you
  three light tones in rotation (tint, pale blue, white). Dropping pale blue would
  simplify the rhythm to tint + white, more in the spirit of "streamlining". It's a
  visible design change, so ask first.
- The live site's "YES, SIGN ME UP!" button on Phone Companions is CSS-uppercased, which
  breaks the client's own sentence-case rule. Worth fixing on the live site.
- There is **no Elementor JSON export** for the redesigned giving pages. The only export
  (`template-exports/elementor-4935-2026-03-17.json`) is the search-results template.
  That's why those pages were rebuilt by reading the live DOM. If Mari ever exports the
  real templates, future fidelity work gets much faster.

**Two documents in the parent folder are actively wrong. Do not follow them:**
- `heading-fix-checklist.md` — its type sizes are the *plan*, not what was saved. It says
  H2 2.5rem / H3 1.7rem; the live kit has 2.75 / 2.
- `Friends & Co/Phone-Companions-Elementor-Build.md` — specifies Roboto Condensed
  uppercase headings, `#FAFAFA` background, 1200px container, 768px breakpoint. All four
  incorrect.

Always trust `https://friendsco.org/wp-content/uploads/elementor/css/post-1392.css`
(the Elementor kit) over any document.

**Don't reorganise the parent folder.** Mari and the client both rely on its structure.
`Logins.docx` exists — don't open it unless explicitly asked.

## How to work with me

- I go by **Mari**, not Marnie.
- Be concise and direct. Skip the preamble.
- Challenge my approach if it's wrong. Don't just execute a bad plan.
- Research before saying you can't — check the live site, the brand guide, the kit CSS.
- **Show visible progress early.** Infrastructure that produces no viewable page reads as
  no progress, even when it's the thing making later work fast. Ship a page, then refactor.
- Be straight about gaps. I'd rather hear "this section is placeholder" from you than
  find out when the client does.

---

**My request for this session:** [describe what you want done]

#!/usr/bin/env python3
"""
Friends & Co mockup page generator.

Every page in the mock site is defined as a small spec below and rendered
through shared section helpers, so the design system is applied identically
everywhere and a page is a few lines rather than 400 of hand-written HTML.

    python3 build.py            # build every page
    python3 build.py donate     # build one page

Copy is pulled from the live friendsco.org pages so the mockups read as the
finished product rather than as placeholder.
"""

import html  # noqa: F401 — kept for future escaping needs
import os
import sys

# ---------------------------------------------------------------------------
# Page shell
# ---------------------------------------------------------------------------

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Friends &amp; Co — {title}</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- Shared design system — do not add page tokens or fonts below this line -->
<link rel="stylesheet" href="assets/css/friendsco.css">
<link rel="stylesheet" href="assets/css/chrome.css">
{extra_css}</head>

<body data-page="{nav}">

<div data-chrome="header"></div>

<main>
"""

FOOT = """</main>

<div data-chrome="footer"></div>

<script src="assets/js/chrome.js"></script>
</body>
</html>
"""

# Internal links point at local mockup files. Nothing in the mockup set links
# back to friendsco.org — Paul must be able to click through the whole thing
# without ever landing on the live WordPress site.
PAGE = {
    "/":                          "home-mockup.html",
    "/friendship-services/":      "friendship-services.html",
    "/visiting-companions/":      "visiting-companions.html",
    "/lets-do-events/":           "lets-do-events.html",
    "/spanish-language-programs/": "spanish-language-programs.html",
    "/coffee-talk/":              "coffee-talk.html",
    "/phone-companions/":         "phone-companions.html",
    "/cards-connect/":            "cards-connect.html",
    "/events/":                   "events.html",
    "/get-involved/":             "get-involved.html",
    "/refer/":                    "refer.html",
    "/join/":                     "join.html",
    "/volunteer/":                "volunteer-apply.html",
    "/about/":                    "about.html",
    "/annual-reports/":           "annual-reports.html",
    "/staff-and-board/":          "staff-and-board.html",
    "/news/":                     "news.html",
    "/contact/":                  "contact.html",
    "/support-friends-co/":       "support-friends-co.html",
    "/donate/":                   "donate.html",
    "/planned-giving/":           "planned-giving.html",
    "/corporate-sponsorship/":    "corporate-sponsorship.html",
    "/other-ways-to-give/":       "other-ways-to-give.html",
    "/remembering-our-friends/":  "remembering-our-friends.html",
    "/volunteer-portal/":         "volunteer-portal.html",
    "/visiting-companions-match/":"visiting-companions-match.html",
    "/volunteer-coffee-talk/":    "volunteer-coffee-talk.html",
    "/volunteer-phone-companion/":"volunteer-phone-companion.html",
    "/volunteer-visiting-companion/": "volunteer-visiting-companion.html",
    "/volunteer-cards-connect/":  "volunteer-cards-connect.html",
    "/volunteer-admin/":          "volunteer-admin.html",
}


class _Base(str):
    """Lets existing specs keep writing BASE + "/donate/" while resolving to a
    local file. Unknown paths become '#' rather than silently leaving the set."""

    def __add__(self, path):
        return PAGE.get(path, "#")


BASE = _Base("")


def e(s):
    """Pass content through unchanged.

    Copy in the page specs is authored as HTML, so it already carries its own
    entities (&amp;, &rsquo;) and occasional inline markup. Escaping here would
    double-encode them and render "Friends &amp; Co" literally on the page.
    """
    return s


# ---------------------------------------------------------------------------
# Section helpers — these are the vocabulary every page is written in
# ---------------------------------------------------------------------------

def hero(title, sub=None, eyebrow=None, tone="blue", ctas=None, watermark=True):
    """Page hero. tone: blue | magenta | navy | tint."""
    cls = {"blue": "section-blue", "magenta": "section-magenta",
           "navy": "section-navy", "tint": "section-tint"}[tone]
    dark = tone in ("blue", "magenta", "navy")
    out = ['<section class="page-hero %s">' % cls]
    if watermark and dark:
        out.append('  <img class="page-hero-watermark" src="assets/img/flower-icon-white.png" alt="">')
    out.append('  <div class="container page-hero-inner">')
    if eyebrow:
        out.append('    <p class="section-eyebrow">%s</p>' % e(eyebrow))
    out.append('    <h1%s>%s</h1>' % (' class="h-white"' if dark else '', e(title)))
    if sub:
        out.append('    <p class="lead measure">%s</p>' % e(sub))
    if ctas:
        out.append('    <div class="hero-actions">')
        for label, href, style in ctas:
            out.append('      <a class="btn %s" href="%s">%s</a>' % (style, href, e(label)))
        out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def prose(heading=None, paras=None, eyebrow=None, tone="tint", center=False,
          measure=True, ctas=None):
    """A block of body copy."""
    cls = {"tint": "section-tint", "white": "section-white",
           "blue": "section-blue", "navy": "section-navy"}[tone]
    out = ['<section class="section %s">' % cls,
           '  <div class="container%s">' % (" center" if center else "")]
    if eyebrow:
        out.append('    <p class="section-eyebrow">%s</p>' % e(eyebrow))
    if heading:
        out.append('    <h2>%s</h2>' % e(heading))
    if paras:
        out.append('    <div class="prose%s"%s>' % (
            " measure" if measure else "",
            ' style="margin-inline:auto"' if (center and measure) else ""))
        for p in paras:
            out.append('      <p>%s</p>' % e(p))
        out.append('    </div>')
    if ctas:
        out.append('    <div class="hero-actions">')
        for label, href, style in ctas:
            out.append('      <a class="btn %s" href="%s">%s</a>' % (style, href, e(label)))
        out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def cards(heading, items, eyebrow=None, sub=None, cols=3, tone="white"):
    """Grid of cards. items = [(title, body, link_label, href), ...]"""
    cls = {"tint": "section-tint", "white": "section-white",
           "blue": "section-blue", "navy": "section-navy"}[tone]
    out = ['<section class="section %s">' % cls, '  <div class="container">',
           '    <div class="section-head">']
    if eyebrow:
        out.append('      <p class="section-eyebrow">%s</p>' % e(eyebrow))
    out.append('      <h2>%s</h2>' % e(heading))
    if sub:
        out.append('      <p>%s</p>' % e(sub))
    out.append('    </div>')
    out.append('    <div class="grid grid-%d">' % cols)
    for title, body, label, href in items:
        out.append('      <article class="card">')
        out.append('        <div class="card-body">')
        out.append('          <h3 class="card-title">%s</h3>' % e(title))
        out.append('          <p>%s</p>' % e(body))
        if label:
            out.append('          <p class="card-action"><a class="btn btn-blue" href="%s">%s</a></p>'
                       % (href, e(label)))
        out.append('        </div>')
        out.append('      </article>')
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def checklist(heading, items, eyebrow=None, cols=2, tone="tint"):
    cls = {"tint": "section-tint", "white": "section-white"}[tone]
    out = ['<section class="section %s">' % cls, '  <div class="container">',
           '    <div class="section-head">']
    if eyebrow:
        out.append('      <p class="section-eyebrow">%s</p>' % e(eyebrow))
    out.append('      <h2>%s</h2>' % e(heading))
    out.append('    </div>')
    out.append('    <ul class="tick-list grid grid-%d">' % cols)
    for it in items:
        out.append('      <li><i class="fas fa-circle-check" aria-hidden="true"></i>'
                   '<span>%s</span></li>' % e(it))
    out.append('    </ul>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def factbox(heading, rows, body=None, tone="white"):
    """Definition-style panel, e.g. the planned-giving advisor details."""
    cls = {"tint": "section-tint", "white": "section-white"}[tone]
    out = ['<section class="section %s">' % cls, '  <div class="container">',
           '    <h2>%s</h2>' % e(heading)]
    if body:
        out.append('    <p class="measure" style="margin-top:12px">%s</p>' % e(body))
    out.append('    <dl class="factbox">')
    for k, v in rows:
        out.append('      <div><dt>%s</dt><dd>%s</dd></div>' % (e(k), v))
    out.append('    </dl>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def cta(heading, body=None, ctas=None, tone="navy"):
    cls = {"navy": "section-navy", "blue": "section-blue",
           "magenta": "section-magenta", "tint": "section-tint"}[tone]
    out = ['<section class="section %s">' % cls, '  <div class="container center">',
           '    <h2>%s</h2>' % e(heading)]
    if body:
        out.append('    <p class="lead measure" style="margin:14px auto 0">%s</p>' % e(body))
    if ctas:
        out.append('    <div class="hero-actions center-actions">')
        for label, href, style in ctas:
            out.append('      <a class="btn %s" href="%s">%s</a>' % (style, href, e(label)))
        out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def steps(heading, items, eyebrow="How it works", tone="white"):
    """Numbered "here's what to expect" sequence. items = [(title, body), ...]"""
    cls = {"tint": "section-tint", "white": "section-white"}[tone]
    out = ['<section class="section %s">' % cls, '  <div class="container">',
           '    <div class="section-head">',
           '      <p class="section-eyebrow">%s</p>' % e(eyebrow),
           '      <h2>%s</h2>' % e(heading),
           '    </div>',
           '    <ol class="steps grid grid-%d">' % min(len(items), 3)]
    for i, (t, b) in enumerate(items, 1):
        out.append('      <li class="step">')
        out.append('        <span class="step-num" aria-hidden="true">%d</span>' % i)
        out.append('        <h3>%s</h3>' % e(t))
        out.append('        <p>%s</p>' % e(b))
        out.append('      </li>')
    out.append('    </ol>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def faq(items, heading="Frequently asked questions",
        sub="Select a question to read the answer.", tone="tint"):
    cls = {"tint": "section-tint", "white": "section-white"}[tone]
    out = ['<section class="section %s">' % cls, '  <div class="container">',
           '    <div class="section-head">',
           '      <h2>%s</h2>' % e(heading)]
    if sub:
        out.append('      <p>%s</p>' % e(sub))
    out.append('    </div>')
    out.append('    <div class="faq measure" style="margin-inline:auto">')
    for q, a in items:
        out.append('      <details>')
        out.append('        <summary>%s</summary>' % e(q))
        out.append('        <div class="faq-body"><p>%s</p></div>' % e(a))
        out.append('      </details>')
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def notice(heading, paras, tone="orange"):
    """Prominent inline notice, e.g. the Visiting Companions application pause."""
    out = ['<section class="section-sm section-white">', '  <div class="container">',
           '    <div class="notice notice-%s">' % tone,
           '      <h2>%s</h2>' % e(heading)]
    for p in paras:
        out.append('      <p>%s</p>' % e(p))
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def photo_hero(title, sub, image, ctas=None, eyebrow=None, align="left"):
    """Hero with a full-bleed photograph behind a dark scrim.

    Used by the pages already rebuilt in Elementor, which all lead with a
    photograph rather than a flat colour band.
    """
    # Built by concatenation, not %-formatting: the gradient is full of percent
    # signs and would need escaping otherwise.
    scrim = ("linear-gradient(90deg,rgba(26,42,66,.88) 0%,"
             "rgba(26,42,66,.72) 45%,rgba(26,42,66,.45) 100%)")
    out = ['<section class="photo-hero" style="background-image:' + scrim +
           ",url('" + image + "');\">",
           '  <div class="container photo-hero-inner ' + align + '">']
    if eyebrow:
        out.append('    <p class="section-eyebrow">%s</p>' % e(eyebrow))
    out.append('    <h1 class="h-white">%s</h1>' % e(title))
    if sub:
        out.append('    <p class="lead measure">%s</p>' % e(sub))
    if ctas:
        out.append('    <div class="hero-actions">')
        for label, href, style in ctas:
            out.append('      <a class="btn %s" href="%s">%s</a>' % (style, href, e(label)))
        out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def statement(heading, paras, tone="tint", divider=True, heading_color=None,
              rule="lime"):
    """Centred statement block with the short rule under the heading that the
    live pages use."""
    cls = {"tint": "section-tint", "white": "section-white",
           "lime": "section-lime"}[tone]
    out = ['<section class="section %s">' % cls, '  <div class="container center">',
           '    <h2%s>%s</h2>' % (' class="h-%s"' % heading_color if heading_color else '',
                                  e(heading))]
    if divider:
        out.append('    <span class="rule rule-%s" aria-hidden="true"></span>' % rule)
    out.append('    <div class="prose measure" style="margin-inline:auto">')
    for p in paras:
        out.append('      <p>%s</p>' % e(p))
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def icon_cards(heading, items, cols=4, tone="tint-blue", eyebrow=None):
    """Cards led by a Font Awesome icon.
    items = [(icon_class, title, body, label, href), ...]"""
    cls = {"tint-blue": "section-tint-blue", "white": "section-white",
           "tint": "section-tint"}[tone]
    out = ['<section class="section %s">' % cls, '  <div class="container">',
           '    <div class="section-head">']
    if eyebrow:
        out.append('      <p class="section-eyebrow">%s</p>' % e(eyebrow))
    out.append('      <h2>%s</h2>' % e(heading))
    out.append('    </div>')
    out.append('    <div class="grid grid-%d">' % cols)
    for icon, title, body, label, href in items:
        out.append('      <article class="icon-card">')
        out.append('        <span class="icon-card-icon"><i class="%s" aria-hidden="true"></i></span>'
                   % icon)
        out.append('        <h3>%s</h3>' % e(title))
        out.append('        <p>%s</p>' % e(body))
        if label:
            out.append('        <a class="btn btn-blue" href="%s">%s</a>' % (href, e(label)))
        out.append('      </article>')
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def stats(heading, items, cta_label=None, cta_href=None, tone="white"):
    """Impact counters. items = [(icon, number, suffix, label), ...]"""
    cls = {"white": "section-white", "tint": "section-tint"}[tone]
    out = ['<section class="section %s">' % cls, '  <div class="container">',
           '    <div class="section-head"><h2>%s</h2></div>' % e(heading),
           '    <div class="grid grid-%d stats">' % len(items)]
    for icon, num, suffix, label in items:
        out.append('      <div class="stat">')
        out.append('        <span class="stat-icon"><i class="%s" aria-hidden="true"></i></span>'
                   % icon)
        out.append('        <span class="stat-num">%s<span class="stat-suffix">%s</span></span>'
                   % (num, suffix))
        out.append('        <span class="stat-label">%s</span>' % e(label))
        out.append('      </div>')
    out.append('    </div>')
    if cta_label:
        out.append('    <div class="section-footer-link">'
                   '<a class="btn btn-blue" href="%s">%s</a></div>' % (cta_href, e(cta_label)))
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def quote(text, attribution, tone="lime"):
    cls = {"lime": "section-lime", "navy": "section-navy"}[tone]
    return ("""<section class="section %s">
  <div class="container center">
    <span class="quote-mark" aria-hidden="true"><i class="fas fa-quote-left"></i></span>
    <blockquote class="pull-quote">%s</blockquote>
    <cite class="pull-cite">%s</cite>
  </div>
</section>""" % (cls, e(text), e(attribution)))


def closing(heading, sub, ctas, tone="tint"):
    """The 'Support Today' style closing block: small heading, rule, big line, button."""
    cls = {"tint": "section-tint", "white": "section-white"}[tone]
    out = ['<section class="section %s">' % cls, '  <div class="container center">',
           '    <h2>%s</h2>' % e(heading),
           '    <span class="rule" aria-hidden="true"></span>',
           '    <h3 class="closing-line measure" style="margin-inline:auto">%s</h3>' % e(sub),
           '    <div class="hero-actions center-actions">']
    for label, href, style in ctas:
        out.append('      <a class="btn %s btn-lg" href="%s">%s</a>' % (style, href, e(label)))
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def jumpnav(items):
    """'Jump to an option' anchor bar. items = [(label, anchor), ...]"""
    out = ['<section class="section-sm section-white jumpnav-wrap">',
           '  <div class="container center">',
           '    <p class="section-eyebrow">Jump to an option</p>',
           '    <div class="jumpnav">']
    for label, anchor in items:
        out.append('      <a class="btn btn-outline" href="#%s">%s</a>' % (anchor, e(label)))
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def option_card(anchor, accent, heading, icon, lede, body,
                action_head=None, action_body=None, contact=True):
    """One giving option on Other ways to give.

    On the live site these are cards in a two-column grid, not full-width
    bands: white, 12px radius, a thick accent rule along the top, the heading
    in slate at 44px with a faded accent icon top-right, and the sub-headings
    in the accent colour.
    """
    out = ['      <article class="option-card accent-%s" id="%s">' % (accent, anchor),
           '        <div class="option-card-head">',
           '          <h2>%s</h2>' % e(heading),
           '          <span class="option-card-icon"><i class="%s" aria-hidden="true"></i></span>' % icon,
           '        </div>',
           '        <p class="option-lede">%s</p>' % e(lede),
           '        <p class="option-text">%s</p>' % e(body)]
    if action_head:
        out.append('        <p class="option-lede">%s</p>' % e(action_head))
        out.append('        <p class="option-text">%s</p>' % e(action_body))
    if contact:
        out.append('        <p class="option-contact">'
                   '<a href="mailto:acarlson@friendsco.org">acarlson@friendsco.org</a><br>'
                   '<a href="tel:+16127460739">612-746-0739</a></p>')
    out.append('      </article>')
    return "\n".join(out)


def option_grid(cards, jump=None):
    """The lavender band holding the jump nav and the option cards."""
    out = ['<section class="section section-tint-blue">', '  <div class="container">']
    if jump:
        out.append('    <div class="center"><p class="section-eyebrow">Jump to an option</p>')
        out.append('      <div class="jumpnav">')
        for label, anchor in jump:
            out.append('        <a class="btn btn-white" href="#%s">%s</a>' % (anchor, e(label)))
        out.append('      </div>')
        out.append('    </div>')
    out.append('    <div class="grid grid-2 option-grid">')
    out.extend(cards)
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def split(main_heading, main_paras, aside_icon, aside_heading, aside_rows,
          aside_body=None, tone="tint", ratio="wide", aside_accent=None,
          main_heading_color="blue"):
    """Two columns: body copy on the left, an accented panel on the right.
    Matches the Legacy Giving / Advisor information band on planned giving."""
    cls = {"tint": "section-tint", "white": "section-white", "plain": ""}[tone]
    out = ['<section class="section %s">' % cls, '  <div class="container">',
           '    <div class="split split-%s">' % ratio,
           '      <div class="split-main">',
           '        <h2 class="h-%s">%s</h2>' % (main_heading_color, e(main_heading)),
           '        <div class="prose">']
    for p in main_paras:
        out.append('          <p>%s</p>' % e(p))
    out.append('        </div>')
    out.append('      </div>')
    out.append('      <aside class="split-aside%s">'
               % (' accent-' + aside_accent if aside_accent else ''))
    out.append('        <span class="split-icon"><i class="%s" aria-hidden="true"></i></span>'
               % aside_icon)
    out.append('        <h3>%s</h3>' % e(aside_heading))
    if aside_body:
        out.append('        <p class="split-note">%s</p>' % e(aside_body))
    out.append('        <dl class="split-rows">')
    for k, v in aside_rows:
        out.append('          <div><dt>%s</dt><dd>%s</dd></div>' % (e(k), v))
    out.append('        </dl>')
    out.append('      </aside>')
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def media(heading, paras, image, alt="", ctas=None, tone="tint-blue",
          reverse=False):
    """Image beside text. Used by the 'A future of belonging' band."""
    cls = {"tint-blue": "section-tint-blue", "white": "section-white",
           "tint": "section-tint"}[tone]
    out = ['<section class="section %s">' % cls, '  <div class="container">',
           '    <div class="media%s">' % (" media-reverse" if reverse else ""),
           '      <div class="media-img"><img src="%s" alt="%s" loading="lazy"></div>'
           % (image, e(alt)),
           '      <div class="media-body">',
           '        <h2>%s</h2>' % e(heading),
           '        <div class="prose">']
    for p in paras:
        out.append('          <p>%s</p>' % e(p))
    out.append('        </div>')
    if ctas:
        out.append('        <div class="hero-actions">')
        for label, href, style in ctas:
            out.append('          <a class="btn %s" href="%s">%s</a>' % (style, href, e(label)))
        out.append('        </div>')
    out.append('      </div>')
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def pattern_hero(title, sub, photo, ctas=None, title_color="teal"):
    """The Friends & Co graphic pattern behind a white content card.

    This is the hero the giving pages actually use — not a photograph with a
    scrim. A rounded photo sits left, the white card sits right.
    """
    out = ['<section class="pattern-hero">',
           '  <div class="container pattern-hero-inner">']
    if photo:
        out.append('    <figure class="pattern-hero-photo"><img src="%s" alt="" loading="lazy"></figure>'
                   % photo)
    out.append('    <div class="pattern-hero-card">')
    out.append('      <h1 class="h-%s">%s</h1>' % (title_color, e(title)))
    if sub:
        out.append('      <p>%s</p>' % e(sub))
    if ctas:
        out.append('      <div class="hero-actions">')
        for label, href, style in ctas:
            out.append('        <a class="btn %s btn-arrow" href="%s">%s</a>'
                       % (style, href, e(label)))
        out.append('      </div>')
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def pattern_cta(heading, sub=None, ctas=None, body=None, rule=True, wash="teal"):
    """Closing band on the graphic pattern, white type, white button.
    `wash` matches the page's hero — magenta on other ways to give."""
    out = ['<section class="pattern-cta wash-%s">' % wash,
           '  <div class="container center">',
           '    <h2 class="h-white">%s</h2>' % e(heading)]
    if rule:
        out.append('    <span class="rule rule-two" aria-hidden="true"></span>')
    if sub:
        out.append('    <h3 class="h-white closing-line measure" style="margin-inline:auto">%s</h3>'
                   % e(sub))
    if body:
        out.append('    <p class="pattern-body measure" style="margin-inline:auto">%s</p>'
                   % e(body))
    if ctas:
        out.append('    <div class="hero-actions center-actions">')
        for label, href, style in ctas:
            out.append('      <a class="btn %s" href="%s">%s</a>' % (style, href, e(label)))
        out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def pattern_page_hero(title, sub, eyebrow=None, ctas=None, wash="teal"):
    """Page hero on the graphic pattern: centred, white type, white button.

    `wash` is the colour laid over the pattern at 69% — teal on planned giving,
    blue on corporate sponsorship. It changes the whole feel of the band, so it
    is per-page rather than a single global.
    """
    out = ['<section class="pattern-cta pattern-page-hero wash-%s">' % wash,
           '  <div class="container center">']
    if eyebrow:
        out.append('    <p class="pattern-eyebrow">%s</p>' % e(eyebrow))
    out.append('    <h1 class="h-white">%s</h1>' % e(title))
    if sub:
        out.append('    <p class="pattern-lead measure" style="margin-inline:auto">%s</p>'
                   % e(sub))
    if ctas:
        out.append('    <div class="hero-actions center-actions">')
        for label, href, style in ctas:
            out.append('      <a class="btn %s" href="%s">%s</a>' % (style, href, e(label)))
        out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def colour_cards(heading, items, cols=2, tone="tint-blue", heading_color="blue"):
    """Cards where the icon, heading and button all share one accent colour.
    items = [(accent, icon, title, body, label, href), ...]
    accent is one of: magenta | lime | orange | teal | blue | green
    """
    cls = {"tint-blue": "section-tint-blue", "white": "section-white",
           "tint": "section-tint"}[tone]
    out = ['<section class="section %s">' % cls, '  <div class="container">',
           '    <div class="section-head"><h2 class="h-%s">%s</h2></div>'
           % (heading_color, e(heading)),
           '    <div class="grid grid-%d">' % cols]
    for accent, icon, title, body, label, href in items:
        out.append('      <article class="colour-card accent-%s">' % accent)
        out.append('        <span class="colour-card-icon"><i class="%s" aria-hidden="true"></i></span>' % icon)
        out.append('        <h3>%s</h3>' % e(title))
        out.append('        <p>%s</p>' % e(body))
        if label:
            out.append('        <a class="btn btn-%s btn-arrow" href="%s">%s</a>'
                       % (accent, href, e(label)))
        out.append('      </article>')
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def colour_stats(heading, items, cta_label=None, cta_href=None,
                 heading_color="blue"):
    """Impact counters with solid filled icon discs.
    items = [(accent, icon, number, suffix, label), ...]"""
    out = ['<section class="section section-white">', '  <div class="container">',
           '    <div class="section-head"><h2 class="h-%s">%s</h2></div>'
           % (heading_color, e(heading)),
           '    <div class="grid grid-%d stats">' % len(items)]
    for accent, icon, num, suffix, label in items:
        out.append('      <div class="stat accent-%s">' % accent)
        out.append('        <span class="stat-disc"><i class="%s" aria-hidden="true"></i></span>' % icon)
        out.append('        <span class="stat-num">%s<span class="stat-suffix">%s</span></span>'
                   % (num, suffix))
        out.append('        <span class="stat-label">%s</span>' % e(label))
        out.append('      </div>')
    out.append('    </div>')
    if cta_label:
        out.append('    <div class="section-footer-link">'
                   '<a class="btn btn-blue btn-arrow" href="%s">%s</a></div>'
                   % (cta_href, e(cta_label)))
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def split_hero(title, sub, image, eyebrow=None, ctas=None, accent="orange"):
    """Photo on the left, solid accent panel on the right with an ampersand
    watermark. The Phone Companions hero."""
    out = ['<section class="split-hero accent-%s">' % accent,
           '  <div class="split-hero-photo" style="background-image:url(\'%s\');"'
           ' role="img" aria-label=""></div>' % image,
           '  <div class="split-hero-panel">',
           '    <img class="split-hero-mark" src="assets/img/ampersand-icon.png" alt="">',
           '    <div class="split-hero-body">']
    if eyebrow:
        out.append('      <p class="split-hero-eyebrow">%s</p>' % e(eyebrow))
    out.append('      <h1 class="h-white">%s</h1>' % e(title))
    if sub:
        out.append('      <p class="split-hero-lead">%s</p>' % e(sub))
    if ctas:
        out.append('      <div class="hero-actions">')
        for label, href, style in ctas:
            out.append('        <a class="btn %s" href="%s">%s</a>' % (style, href, e(label)))
        out.append('      </div>')
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def icon_steps(heading, sub, items, accent="orange", tone="tint"):
    """Three centred icon-disc steps. items = [(icon, title, body), ...]"""
    cls = {"tint": "section-tint", "white": "section-white"}[tone]
    out = ['<section class="section %s">' % cls, '  <div class="container">',
           '    <div class="section-head">',
           '      <h2 class="h-magenta">%s</h2>' % e(heading)]
    if sub:
        out.append('      <p>%s</p>' % e(sub))
    out.append('    </div>')
    out.append('    <div class="grid grid-%d icon-steps accent-%s">' % (len(items), accent))
    for icon, title, body in items:
        out.append('      <div class="icon-step">')
        out.append('        <span class="icon-step-disc"><i class="%s" aria-hidden="true"></i></span>' % icon)
        out.append('        <h3>%s</h3>' % e(title))
        out.append('        <p>%s</p>' % e(body))
        out.append('      </div>')
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def faq_cards(heading, sub, items, cols=2):
    """Blue band with a flower watermark and tinted FAQ cards.
    items = [(icon, question, answer), ...]"""
    out = ['<section class="section faq-band">',
           '  <img class="faq-band-mark" src="assets/img/flower-icon-white.png" alt="">',
           '  <div class="container">',
           '    <h2 class="h-white">%s</h2>' % e(heading)]
    if sub:
        out.append('    <p class="faq-band-sub">%s</p>' % e(sub))
    out.append('    <div class="grid grid-%d faq-cards">' % cols)
    for icon, q, a in items:
        out.append('      <article class="faq-card">')
        out.append('        <h3><i class="%s" aria-hidden="true"></i>%s</h3>' % (icon, e(q)))
        out.append('        <p>%s</p>' % e(a))
        out.append('      </article>')
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def choice_band(heading, eyebrow, image, choices, alt=""):
    """Tilted photo left, stacked choice cards right.
    choices = [(accent, title, body, label, href), ...]"""
    out = ['<section class="section section-tint">', '  <div class="container">',
           '    <div class="media choice-band">',
           '      <div class="media-img tilted"><img src="%s" alt="%s" loading="lazy"></div>'
           % (image, e(alt)),
           '      <div class="media-body">']
    if eyebrow:
        out.append('        <p class="section-eyebrow">%s</p>' % e(eyebrow))
    out.append('        <h2 class="h-navy">%s</h2>' % e(heading))
    for accent, title, body, label, href in choices:
        out.append('        <div class="choice-card accent-%s">' % accent)
        out.append('          <h3>%s</h3>' % e(title))
        out.append('          <p>%s</p>' % e(body))
        out.append('          <a class="btn btn-%s btn-arrow" href="%s">%s</a>'
                   % (accent, href, e(label)))
        out.append('        </div>')
    out.append('      </div>')
    out.append('    </div>')
    out.append('  </div>')
    out.append('</section>')
    return "\n".join(out)


def raw(markup):
    return markup


WP = "https://friendsco.org/wp-content/uploads"


JOIN = BASE + "/join/"
REFER = BASE + "/refer/"


def program_ctas():
    return [("Join the program", JOIN, "btn-lime"),
            ("Refer an older adult", REFER, "btn-outline btn-on-dark")]


# ---------------------------------------------------------------------------
# Shared content
# ---------------------------------------------------------------------------

PROGRAMS = [
    ("Coffee Talk",
     "A commitment-free drop-in chat line when a friendly voice is needed the most.",
     "Learn more", BASE + "/coffee-talk/"),
    ("Phone Companions",
     "Weekly calls that spark meaningful, ongoing friendships.",
     "Learn more", BASE + "/phone-companions/"),
    ("Visiting Companions",
     "Friendly, in-home visits that build rapport, joy and wellbeing.",
     "Learn more", BASE + "/visiting-companions/"),
    ("Cards Connect",
     "Handmade cards created by people who care, sent seasonally.",
     "Learn more", BASE + "/cards-connect/"),
    ("Let’s Do Lunch &amp; Let’s Do Coffee",
     "Older LGBTQ+ adults connect over lunchtime educational presentations.",
     "Learn more", BASE + "/lets-do-events/"),
    ("Conexiones Comunitarias",
     "Gatherings for Spanish-speaking older adults to build friendship and community.",
     "Learn more", BASE + "/spanish-language-programs/"),
]


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

PAGES = {}

# --- Friendship services (programs hub) ------------------------------------
PAGES["friendship-services"] = dict(
    title="Friendship services", nav="programs", css=None,
    sections=[
        hero("Friendship services",
             "Our programs are, and will always be, free for older adults.",
             eyebrow="Belonging starts here", tone="blue",
             ctas=[("Refer an older adult", BASE + "/refer/", "btn-lime"),
                   ("Join the program", BASE + "/join/", "btn-outline btn-on-dark")]),
        prose(heading="Belonging starts here",
              paras=["At Friends &amp; Co, we offer programs designed to reduce loneliness "
                     "and build lasting connections. Whether you're seeking a friendly "
                     "voice, a one-on-one connection, or somewhere to belong, you're in "
                     "the right place."],
              tone="tint", center=True),
        prose(heading="What it means to be a part of Friends &amp; Co",
              paras=["When you participate in any of our programs — whether you're enjoying "
                     "a conversation, visiting a companion, attending a gathering, or "
                     "exchanging greeting cards — you become a member of our community."],
              tone="white"),
        checklist("What you can access", [
            "Friendly phone chats on your schedule",
            "One-to-one companion matching",
            "Greeting cards and handwritten notes",
            "Special events and gatherings",
            "Our Among Friends newsletter, full of stories and updates",
            "Ongoing support and more opportunities to connect",
        ], tone="tint"),
        cards("Our programs", PROGRAMS, eyebrow="Free for older adults",
              sub="Six ways to connect. Join as many as you like.", tone="white"),
        cta("Not sure which program fits?",
            "Tell us a little about yourself and we'll help you find the right one — "
            "or refer someone you're concerned about.",
            [("Join the program", BASE + "/join/", "btn-lime"),
             ("Refer an older adult", BASE + "/refer/", "btn-outline btn-on-dark")]),
    ])

# --- Planned giving --------------------------------------------------------
PAGES["planned-giving"] = dict(
    title="Planned giving", nav="support", css=None,
    sections=[
        pattern_page_hero("Planned giving",
                          "Leave a legacy of friendship and ensure meaningful connection "
                          "for generations to come.",
                          eyebrow="Enduring impact", wash="teal",
                          ctas=[("Back to support", BASE + "/support-friends-co/",
                                 "btn-white btn-arrow-left")]),
        split("Legacy giving", [
            "Friends &amp; Co accepts gifts of any size made in a will, a revocable trust "
            "agreement, an irrevocable trust agreement, or any other manner of non-probate "
            "disposition if they meet our contribution guidelines.",
            "Because Friends &amp; Co is deeply embedded in the community, providing vital "
            "services to older adults, we are positioned to absorb and distribute gifts of "
            "any size efficiently. We ensure every contribution directly supports our "
            "mission of alleviating loneliness.",
            "For planned gifts, we do not have specific requirements or language for bequest "
            "documents. A simple designation is often all that is needed to make a lasting "
            "difference.",
            "By including Friends &amp; Co in your estate plans, you are making a powerful "
            "statement about the value of connection. You are ensuring that no older adult "
            "has to face life alone.",
        ],
            "fas fa-file-signature", "Advisor information", [
                ("Legal name", "Friends &amp; Co"),
                ("Street address",
                 "2550 University Avenue W<br>Suite 260-S<br>Saint Paul, MN 55114"),
                ("Tax identification number (TIN)", "41-0986200"),
            ],
            aside_body="Your financial advisor may request our official street address and "
                       "tax identification number when drafting your documents.",
            tone="plain", aside_accent="lime"),
        media("A future of belonging", [
            "Your legacy doesn’t just fund programs; it funds laughter, shared stories, and "
            "the comfort of knowing someone cares. Click the button below to contact "
            "Amber Carlson to learn more about how you can make a difference.",
        ], WP + "/2026/01/support-hero-group.jpg",
            alt="Friends &amp; Co community members together",
            ctas=[("Join the Legacy Circle", "mailto:acarlson@friendsco.org",
                   "btn-lime btn-arrow")],
            tone="tint-blue"),
        pattern_cta("Get in touch", "Have questions about planned giving?",
                    body="Our team is here to help you or your advisor navigate the "
                         "process of leaving a legacy gift.",
                    ctas=[("Contact us", "mailto:acarlson@friendsco.org", "btn-white")]),
    ])


# --- Coffee Talk -----------------------------------------------------------
PAGES["coffee-talk"] = dict(
    title="Coffee Talk", nav="programs", css=None,
    sections=[
        split_hero("Coffee Talk", "A friendly voice to connect with.",
                   WP + "/2025/09/senior-woman-talking-over-the-phone-at-her-home-2024-10-18-05-19-09-utc-scaled-1-1024x683.jpg",
                   eyebrow="Tuesday &amp; Thursday, 9 a.m.\u2013Noon (CST)", accent="magenta",
                   ctas=[("Call 612-746-0728", "tel:+16127460728", "btn-tint-on-magenta"),
                         ("Request a callback", BASE + "/contact/", "btn-ghost-tint")]),
        statement("Brighten your day with a call \u2014 no signup needed", [
            "Coffee Talk is a free, drop-in phone line where older adults can connect "
            "with caring volunteers for friendly, one-on-one conversations. No forms. "
            "No pressure. Just warm conversation and connection when you need it.",
        ], tone="tint", heading_color="magenta", divider=False),
        icon_steps("Here\u2019s what to expect when you call", None, [
            ("fas fa-phone", "No signup needed",
             "No forms, no waitlists \u2014 just dial in when you\u2019re ready to chat."),
            ("fas fa-user", "Just use your first name",
             "You don\u2019t have to share personal info \u2014 just your first name is fine."),
            ("fas fa-comments", "Have a meaningful chat",
             "You can call in as often as once daily; chats are 20 minutes each."),
        ], accent="magenta"),
        statement("Coffee Talk is completely free and always open to older adults "
                  "looking for conversation.", [], tone="white",
                  heading_color="blue", divider=False),
        faq_cards("Frequently asked questions",
                  "Have questions? Read the answers below.", [
            ("fas fa-circle-check", "Who is Coffee Talk for?",
             "Coffee Talk is for older adults 62+ looking for connection, conversation, "
             "or simply someone to talk to during the day. There\u2019s no need to sign up "
             "\u2014 just pick up the phone and call."),
            ("fas fa-comments", "What can I talk about?",
             "Our volunteers are here to have casual, friendly conversations. You can "
             "talk about your day, your favorite shows, memories, hobbies \u2014 whatever\u2019s "
             "on your mind. Note: we are not a crisis line. If you need mental health or "
             "emotional support, call or text 988."),
            ("fas fa-clock", "When is Coffee Talk available?",
             "Coffee Talk is open on Tuesday and Thursday, from 9 to noon (CST)."),
            ("fas fa-phone-volume", "What number should I call?",
             "Local numbers \u2014 Twin Cities: 612-746-0728 or 651-204-0129. Western "
             "Wisconsin: 715-406-4871. Duluth: 218-293-4412. Rochester: 507-936-0317. "
             "St. Cloud / Central MN: 320-300-2683. Toll free: 877-238-2282."),
            ("fas fa-envelope", "Still have questions?",
             "We are happy to answer any questions you have about this commitment-free "
             "drop-in chat line. Send your question or comment to info@friendsco.org."),
        ]),
        choice_band("Want us to give you a call?", "Get connected",
                    WP + "/2025/09/senior-woman-talking-over-the-phone-at-her-home-2024-10-18-05-19-09-utc-scaled-1-1024x683.jpg",
                    alt="An older adult talking on the phone",
                    choices=[
                        ("magenta", "Call us now",
                         "Coffee Talk is open on Tuesday and Thursday, from 9 to noon (CST).",
                         "Call 612-746-0728", "tel:+16127460728"),
                        ("blue", "Request a callback",
                         "Request a callback and we\u2019ll reach out during an upcoming "
                         "Coffee Talk session.",
                         "Contact us", BASE + "/contact/"),
                    ]),
    ])

# --- Visiting Companions ---------------------------------------------------
PAGES["visiting-companions"] = dict(
    title="Visiting Companions", nav="programs", css=None,
    sections=[
        split_hero("Visiting Companions", "Visits that spark joy and connection.",
                   WP + "/2026/01/support-hero-connection.jpg",
                   eyebrow="One-to-one, in person", accent="magenta",
                   ctas=[("Explore our programs", BASE + "/friendship-services/",
                          "btn-tint-on-magenta"),
                         ("Refer an older adult", REFER, "btn-ghost-tint")]),
        notice("Please note", [
            "We are temporarily pausing new applications for the Visiting Companion "
            "program so we can match those currently waiting.",
            "We look forward to reopening applications as soon as possible. "
            "Thank you for your understanding.",
            "We are still accepting referrals and applications for other programs \u2014 "
            "<a href=\"friendship-services.html\">click here to explore our programs</a>.",
        ]),
        statement("Bringing friendship into your life", [
            "Visiting Companions pairs older adults with background-checked, trained "
            "volunteers for meaningful, in-person visits. Based on location, you and your "
            "companion can create a schedule that works for you. Most companions visit "
            "1\u20132 times per month.",
        ], tone="tint", heading_color="magenta", divider=False),
        icon_steps("Here\u2019s what to expect when you sign up", None, [
            ("fas fa-house", "Welcome call and home visit",
             "We\u2019ll start with a warm welcome call to arrange a visit, then pop by to "
             "answer your questions and discover what matters most to you in a new "
             "friendship."),
            ("fas fa-user-group", "Matching process",
             "We match based on friendship fit and travel distance that accommodates "
             "regular, meaningful visits."),
            ("fas fa-calendar-check", "Scheduled visits",
             "Your new companion calls to arrange a first visit. Together you decide on "
             "a regular schedule."),
        ], accent="magenta"),
        statement("Volunteers and older adults are background-checked and volunteers are "
                  "trained by Friends &amp; Co staff.", [
            "Older adult participants, like volunteers, must submit and pass a "
            "background check.",
        ], tone="white", heading_color="blue", divider=False),
        faq_cards("Frequently asked questions",
                  "Have questions? Read the answers below.", [
            ("fas fa-circle-check", "Who can sign up for Visiting Companions?",
             "People 70+ years who live in the Twin Cities seven-county metro seeking a "
             "meaningful connection."),
            ("fas fa-list-check", "What happens after I sign up?",
             "First, we will call you to introduce ourselves, answer your questions and "
             "make sure in-person visits feel right for you. Second, we will visit you "
             "in-person to get to know you. Next, we will look for a volunteer who is a "
             "good fit for you. Then, we will call you to share about the volunteer, so "
             "you can decide if you would like to move forward with the match. Finally, "
             "if you choose to move forward, the volunteer will call you to introduce "
             "themselves and to arrange your first visit."),
            ("fas fa-clock", "How long does it take to be matched with a volunteer?",
             "We do our best to make matches quickly, but some factors are outside our "
             "control. Geographic proximity: when older adults and volunteers live near "
             "each other, matches often happen quickly. If they\u2019re farther apart, wait "
             "times can be longer. High demand: many people are eager to join, which can "
             "also lengthen the time it takes to find the right match."),
            ("fas fa-users", "Who are the volunteers?",
             "Our volunteers come from all ages and backgrounds, from college students to "
             "older adults, and all share the desire to be a friend to someone in the "
             "community. Each volunteer completes a background check and training before "
             "being matched, ensuring they are well-prepared to provide meaningful "
             "connection."),
            ("fas fa-mug-saucer", "What do Visiting Companions do during visits?",
             "Every friendship is different! Some friends meet in the community; others "
             "meet at home. Some companions chat over coffee, take walks, play cards, or "
             "simply enjoy quiet time together. Visiting Companions do not provide "
             "transportation, run errands, handle medical or personal care, or perform "
             "household chores."),
            ("fas fa-envelope", "Still have questions?",
             "Email us at companions@friendsco.org or call (612) 746-0737."),
        ]),
        choice_band("Know an older adult who would love a visit?", "Get connected",
                    WP + "/2026/01/support-hero-connection.jpg",
                    alt="An older adult and a volunteer talking at home",
                    choices=[
                        ("magenta", "Explore our other programs",
                         "We are still accepting referrals and applications for other "
                         "programs.",
                         "Explore our programs", BASE + "/friendship-services/"),
                        ("blue", "I have a question",
                         "Email companions@friendsco.org or call (612) 746-0737.",
                         "Contact us", BASE + "/contact/"),
                    ]),
    ])

# --- Cards Connect ---------------------------------------------------------
PAGES["cards-connect"] = dict(
    title="Cards Connect", nav="programs", css=None,
    sections=[
        split_hero("Cards Connect", "Mail that makes your day.",
                   WP + "/2026/01/support-hero-group.jpg",
                   eyebrow="Handmade, four times a year", accent="teal",
                   ctas=[("Join the program", JOIN, "btn-tint-on-teal"),
                         ("Refer an older adult", REFER, "btn-ghost-tint")]),
        statement("Thoughtful cards mailed seasonally", [
            "Cards Connect brings smiles through the mail. Older adults receive handmade "
            "cards created by caring volunteers several times a year \u2014 in fall, winter, "
            "spring, and on Valentine\u2019s Day. The messages are free, heartfelt, and "
            "always appreciated.",
        ], tone="tint", heading_color="magenta", divider=False),
        icon_steps("Here\u2019s what to expect when you sign up", None, [
            ("fas fa-pen-to-square", "Sign up online",
             "Sign up online \u2014 it\u2019s quick and easy."),
            ("fas fa-palette", "Volunteers create your cards",
             "Volunteers create personalized, heartfelt cards."),
            ("fas fa-envelope-open-text", "Cards arrive through the year",
             "You\u2019ll receive cards several times a year, no cost, no catch. Four times "
             "per year: fall, winter, Valentine\u2019s Day, and late spring."),
        ], accent="teal"),
        faq_cards("Frequently asked questions",
                  "Have questions? Read the answers below.", [
            ("fas fa-circle-check", "Who can sign up for Cards Connect?",
             "You must be 62 years or older, live in Minnesota, and enjoy receiving cards "
             "in the mail."),
            ("fas fa-calendar-days", "How often will I receive cards?",
             "Cards are mailed four times per year: in the fall, during the winter "
             "holiday season, for Valentine\u2019s Day, and in spring."),
            ("fas fa-palette", "Who makes the cards?",
             "Our cards are made by volunteers of all ages \u2014 from students to artists to "
             "community groups \u2014 each one created with care and love."),
            ("fas fa-truck", "What if I move?",
             "Please let us know your new address so we can continue sending cards to "
             "you. You can email companions@friendsco.org or call (612) 746-0737."),
            ("fas fa-envelope", "Still have questions?",
             "Email jkapp@friendsco.org or call (612) 746-0737."),
        ]),
        choice_band("Get started", "Get connected",
                    WP + "/2026/01/support-hero-group.jpg",
                    alt="Handmade cards made by Friends &amp; Co volunteers",
                    choices=[
                        ("teal", "I want to receive cards",
                         "I\u2019m an older adult and want to receive cards from "
                         "Friends &amp; Co.", "Join the program", JOIN),
                        ("blue", "I want to refer someone",
                         "I know someone 62+ who would love to receive cards.",
                         "Refer an older adult", REFER),
                    ]),
    ])

# --- Let's Do Coffee / Let's Do Lunch --------------------------------------
PAGES["lets-do-events"] = dict(
    title="Let\u2019s Do Coffee &amp; Let\u2019s Do Lunch Caf\u00e9", nav="programs", css=None,
    sections=[
        split_hero("You\u2019re welcome at our table",
                   "Free monthly coffee &amp; lunch gatherings for LGBTQ+ adults ages 62+",
                   WP + "/2026/01/support-hero-group.jpg",
                   eyebrow="Let\u2019s Do Coffee &amp; Let\u2019s Do Lunch Caf\u00e9 \U0001F3F3\uFE0F\u200D\U0001F308",
                   accent="magenta",
                   ctas=[("See upcoming dates", BASE + "/events/", "btn-tint-on-magenta"),
                         ("Refer an older adult", REFER, "btn-ghost-tint")]),
        statement("What to expect", [
            "Free, drop-in gatherings for older LGBTQ+ adults to relax, talk, laugh and "
            "connect. Held at various locations across the Twin Cities. Enjoy "
            "complimentary coffee, pastries, or lunch.",
            "No pressure. No explaining yourself. Just socializing and friendship!",
        ], tone="tint", heading_color="magenta", divider=False),
        colour_cards("Two ways to gather \u2014 all month long", [
            ("magenta", "fas fa-mug-saucer", "Let\u2019s Do Coffee",
             "Casual come-as-you-are coffee and pastry meet-ups throughout the month. "
             "Small, and designed for easy conversations and getting to know others "
             "without pressure.",
             "See upcoming dates", BASE + "/events/"),
            ("teal", "fas fa-utensils", "Let\u2019s Do Lunch Caf\u00e9",
             "Casual caf\u00e9-style meal with a touch of intention. Gatherings include a "
             "short talk from a guest speaker offering new ideas, perspectives, and "
             "something to take with you beyond the table.",
             "See upcoming dates", BASE + "/events/"),
        ], cols=2, tone="tint-blue"),
        statement("As seen in", [
            "Let\u2019s Do Lunch Caf\u00e9 has been featured by local media for building "
            "community and reducing social isolation among LGBTQ+ older adults.",
        ], tone="white", heading_color="blue", divider=False),
        cards("Upcoming events", [
            ("Coffee Talk \u2014 free drop-in phone line",
             "A commitment-free drop-in chat line, Tuesday and Thursday mornings.",
             "Event details", "event-detail.html"),
            ("Let\u2019s Do Lunch Caf\u00e9: Wilder Foundation, St. Paul",
             "A caf\u00e9-style lunch with a short talk from a guest speaker.",
             "Event details", "event-detail.html"),
            ("Caf\u00e9 y Conversaciones",
             "A free monthly gathering for Spanish-speaking older adults.",
             "Event details", "event-detail.html"),
        ], tone="tint"),
        notice("Photos &amp; video notice \u2014 your comfort matters", [
            "When you enter any Friends &amp; Co event or program, you enter an area where "
            "photography, audio, and video recording may occur.",
            "We\u2019re a fun community and love capturing good moments \u2014 but we completely "
            "understand that some people prefer not to be photographed or recorded. From "
            "bad-hair days to privacy concerns, every reason is valid.",
            "If you prefer not to be included in photos or videos at any time, feel free "
            "to step aside or let a staff member know \u2014 no explanation needed.",
        ], tone="blue"),
        choice_band("Ready to join us?", "Get connected",
                    WP + "/2026/01/support-hero-group.jpg",
                    alt="A Let\u2019s Do Lunch Caf\u00e9 gathering",
                    choices=[
                        ("magenta", "Sign up and come along",
                         "Sign up and come to an upcoming gathering.",
                         "See upcoming dates", BASE + "/events/"),
                        ("blue", "Refer someone",
                         "Know an older LGBTQ+ adult who would enjoy these gatherings?",
                         "Refer an older adult", REFER),
                    ]),
    ])

# --- Conexiones Comunitarias -----------------------------------------------
PAGES["spanish-language-programs"] = dict(
    title="Conexiones Comunitarias", nav="programs", css=None,
    sections=[
        split_hero("Conexiones Comunitarias",
                   "Free monthly gatherings for Spanish-speaking older adults.",
                   WP + "/2026/01/support-hero-group.jpg",
                   eyebrow="In person gatherings", accent="teal",
                   ctas=[("View event calendar", BASE + "/events/", "btn-tint-on-teal"),
                         ("Refer an older adult", REFER, "btn-ghost-tint")]),
        statement("Connect and build community at gatherings designed for "
                  "Spanish-speaking older adults.", [
            "Caf\u00e9 y Conversaciones (Coffee &amp; Conversations) is a free monthly "
            "gathering for Spanish-speaking older adults. A place to connect, socialize, "
            "and share in group learning and activities.",
        ], tone="tint", heading_color="magenta", divider=False),
        split("In person gatherings", [
            "RSVP required.",
            "This program is made possible by DARTS and Friends &amp; Co.",
        ],
            "fas fa-circle-info", "Questions", [
                ("Contact", "Jethra Kapp"),
                ("Email", '<a href="mailto:jkapp@friendsco.org">jkapp@friendsco.org</a>'),
                ("Phone", '<a href="tel:+16127460725">612.746.0725</a>'),
            ],
            aside_body="For questions, location, and to participate, please get in touch.",
            tone="plain", aside_accent="lime"),
        faq_cards("Group rules of engagement", None, [
            ("fas fa-handshake-angle", "Treat everyone with respect",
             "Let\u2019s treat everyone with respect. Healthy debates are natural, but "
             "kindness, respect, and understanding are required."),
            ("fas fa-lock", "What\u2019s shared stays here",
             "What\u2019s shared in the group should stay in the group. Being part of this "
             "group requires mutual trust."),
            ("fas fa-hand-holding-heart", "Give more than you take",
             "Give more than you take to this group. Authentic, expressive discussions "
             "make groups great but may also be sensitive and private."),
            ("fas fa-shield-heart", "Make sure everyone feels safe",
             "Bullying of any kind isn\u2019t allowed, and degrading comments about things "
             "like race, religion, culture, sexual orientation, gender, or identity will "
             "not be tolerated."),
        ]),
        notice("Photos &amp; video notice \u2014 your comfort matters", [
            "When you enter any Friends &amp; Co event or program, you enter an area where "
            "photography, audio, and video recording may occur.",
            "We\u2019re a fun community and love capturing good moments \u2014 but we completely "
            "understand that some people prefer not to be photographed or recorded. From "
            "bad-hair days to privacy concerns, every reason is valid.",
            "If you prefer not to be included in photos or videos at any time, feel free "
            "to step aside or let a staff member know \u2014 no explanation needed.",
        ], tone="blue"),
        choice_band("More ways to connect", "Get connected",
                    WP + "/2026/01/support-hero-group.jpg",
                    alt="Friends &amp; Co community gathering",
                    choices=[
                        ("teal", "See upcoming gatherings",
                         "Caf\u00e9 y Conversaciones and other events across the Twin Cities.",
                         "View event calendar", BASE + "/events/"),
                        ("blue", "Ask a question",
                         "Contact Jethra at jkapp@friendsco.org or 612.746.0725.",
                         "Contact us", BASE + "/contact/"),
                    ]),
    ])

# --- About -----------------------------------------------------------------
PAGES["about"] = dict(
    title="About", nav="about", css=None,
    sections=[
        hero("About Friends &amp; Co",
             "We believe meaningful connections are essential for older adults’ health "
             "and happiness.",
             eyebrow="Our mission", tone="blue"),
        prose(heading="Who we are", tone="tint", paras=[
            "Formerly Little Brothers – Friends of the Elderly Twin Cities, Friends &amp; Co "
            "is the new name for our Minnesota-based nonprofit committed to creating "
            "connection and belonging for older adults through friendship-centered programs "
            "that build community.",
            "Founded in 1972, our organization has spent over 50 years nurturing meaningful "
            "relationships to combat isolation and loneliness. In 2022, we became "
            "Friends &amp; Co to reflect our evolving focus on inclusive, community-based "
            "connection for all older adults.",
        ]),
        cards("Mission and vision", [
            ("Our mission",
             "Friends &amp; Co celebrates aging through community-led service that fosters "
             "meaningful connections for everyone.", None, None),
            ("Our vision",
             "We envision a world where every older adult thrives in meaningful relationships "
             "and belongs to a caring, vibrant community.", None, None),
        ], cols=2, tone="white"),
        cards("Learn more", [
            ("Our team", "Meet the staff and board who keep Friends &amp; Co running.",
             "Staff and board", BASE + "/staff-and-board/"),
            ("Annual reports", "See how we use the gifts entrusted to us each year.",
             "Read the reports", BASE + "/annual-reports/"),
            ("Latest news", "Stories from our staff, volunteers and community partners.",
             "Read the news", BASE + "/news/"),
        ], eyebrow="More about us", tone="tint"),
        cta("Be part of the story",
            "Volunteer, refer someone, or support the work with a gift.",
            [("Become a volunteer", BASE + "/get-involved/", "btn-lime"),
             ("Give today", BASE + "/donate/", "btn-outline btn-on-dark")]),
    ])

# --- Support hub — mirrors the live Elementor build -------------------------
PAGES["support-friends-co"] = dict(
    title="Support Friends &amp; Co", nav="support", css=None,
    sections=[
        pattern_hero("Support Friends &amp; Co",
                     "Together, we create meaningful connections for older adults. Your "
                     "support builds a community where everyone belongs.",
                     WP + "/2026/01/support-hero-connection.jpg",
                     ctas=[("Donate today", BASE + "/donate/", "btn-orange")],
                     title_color="teal"),
        statement("You belong with us", [
            "When you give the gift of friendship, you strengthen far more than one life. "
            "Your generosity brings connection to older adults, comfort to the people who "
            "love them, and warmth to the communities they call home. Every gift—of any "
            "size—helps build the kind of well-connected communities that are healthier, "
            "stronger, and better places for all of us to live. At Friends &amp; Co, "
            "fostering meaningful connection is at the heart of our mission, and we invite "
            "you to help us build a community where everyone belongs.",
        ], tone="white", heading_color="magenta", rule="orange"),
        colour_cards("Ways to support", [
            ("magenta", "fas fa-hand-holding-heart", "Give today",
             "Make a one-time or monthly gift to support meaningful connections.",
             "Learn more", BASE + "/donate/"),
            ("lime", "fas fa-scroll", "Planned giving",
             "Leave a legacy of friendship and belonging for years to come.",
             "Learn more", BASE + "/planned-giving/"),
            ("orange", "fas fa-briefcase", "Corporate sponsorship",
             "Partner with Friends &amp; Co to make a greater community impact.",
             "Learn more", BASE + "/corporate-sponsorship/"),
            ("teal", "fas fa-lightbulb", "Other ways to give",
             "Partner with Friends &amp; Co to make a greater community impact.",
             "Learn more", BASE + "/other-ways-to-give/"),
        ], cols=2, tone="tint-blue"),
        colour_stats("Impact at a glance", [
            ("orange", "fas fa-users", "1,200", "+", "older adults served each year"),
            ("magenta", "fas fa-face-smile", "90", "%", "report feeling less lonely"),
            ("lime", "fas fa-phone", "40,000", "+", "phone calls and visits made"),
        ], cta_label="Read the annual report", cta_href=BASE + "/annual-reports/"),
        quote("\"I give because I’ve seen how much a simple conversation or friendship can "
              "mean. Friends &amp; Co turns small acts of care into life-changing "
              "connection—and I’m proud to be part of that.\"", "— Alan"),
        pattern_cta("Support today",
                    "You can make the difference between loneliness and belonging.",
                    [("Give today", BASE + "/donate/", "btn-white")]),
    ])

# --- 404 -------------------------------------------------------------------
PAGES["404"] = dict(
    title="Page not found", nav="", css=None,
    sections=[
        hero("We couldn’t find that page",
             "The link may be out of date, or the page may have moved. Here are some places "
             "to pick up from.",
             eyebrow="404", tone="blue",
             ctas=[("Go to the homepage", BASE + "/", "btn-lime")]),
        cards("Popular destinations", [
            ("Friendship services", "See all six of our free programs for older adults.",
             "Explore programs", BASE + "/friendship-services/"),
            ("Volunteer", "Find a role that fits your time and interests.",
             "Get involved", BASE + "/get-involved/"),
            ("Support us", "Give today, or explore other ways to help.",
             "Ways to give", BASE + "/support-friends-co/"),
        ], tone="tint"),
        cta("Still stuck?",
            "Call us on 612-721-1400 or email info@friendsco.org and we'll point you "
            "in the right direction.",
            [("Contact us", BASE + "/contact/", "btn-lime")]),
    ])


# --- Corporate sponsorship (mirrors live) ----------------------------------
PAGES["corporate-sponsorship"] = dict(
    title="Corporate sponsorship", nav="support", css=None,
    sections=[
        pattern_page_hero("Corporate sponsorship",
                          "Show your commitment to community well-being by partnering "
                          "with Friends &amp; Co.",
                          eyebrow="Meaningful difference", wash="blue",
                          ctas=[("Back to support", BASE + "/support-friends-co/",
                                 "btn-white btn-arrow-left")]),
        # The live page is just the hero and this one band — no closing CTA.
        raw("""<section class="section">
  <div class="container">
    <div class="split split-wide">
      <div class="split-main">
        <h2 class="h-blue">Why partner with us?</h2>
        <div class="prose">
          <p>Corporate partners make a meaningful difference when they sponsor
             Friends &amp; Co. By investing in programs that reduce isolation and
             loneliness among older adults, companies demonstrate their commitment to
             community well-being and social responsibility.</p>
          <p>Sponsorship directly supports connection, belonging, and improved health
             outcomes for our neighbors—while also offering partners increased
             visibility, authentic community engagement opportunities, and alignment
             with a mission that drives real, measurable impact.</p>
        </div>
        <ul class="tick-list tick-list-blue grid grid-1" style="margin-top:28px">
          <li><i class="fas fa-circle-check" aria-hidden="true"></i><span>Increased brand visibility</span></li>
          <li><i class="fas fa-circle-check" aria-hidden="true"></i><span>Social responsibility impact</span></li>
          <li><i class="fas fa-circle-check" aria-hidden="true"></i><span>Community engagement</span></li>
        </ul>
      </div>
      <aside class="split-aside panel-topline panel-magenta center">
        <span class="panel-icon"><i class="fas fa-handshake" aria-hidden="true"></i></span>
        <h3>Become a partner</h3>
        <p class="panel-note">To learn more about how you can make a difference,
           contact our Philanthropy team.</p>
        <p class="panel-contact">Contact<br>
          <strong>Amber Carlson</strong><br>
          <a href="mailto:acarlson@friendsco.org">acarlson@friendsco.org</a></p>
      </aside>
    </div>
  </div>
</section>"""),
    ])

# --- Other ways to give — mirrors the live Elementor build ------------------
PAGES["other-ways-to-give"] = dict(
    title="Other ways to give", nav="support", css=None,
    sections=[
        pattern_page_hero("Other ways to give",
                          "Build a community where everyone belongs through stock "
                          "transfers, workplace matching, and other creative gifts.",
                          eyebrow="Gifts of belonging", wash="magenta",
                          ctas=[("Back to support", BASE + "/support-friends-co/",
                                 "btn-white btn-arrow-left")]),
        option_grid(
            jump=[("ACH", "ach"), ("Donor advised funds", "daf"),
                  ("Employee matching", "matching"), ("Thrivent funds", "thrivent"),
                  ("Stock/IRA", "stock"), ("Host event", "event")],
            cards=[
                option_card("ach", "blue", "ACH transfers", "fas fa-university",
                    "Support Friends &amp; Co with easy, direct bank transfers",
                    "Making a direct payment from your bank account via ACH is a secure "
                    "and efficient way to support Friends &amp; Co\u2019s mission of creating "
                    "meaningful connections for older adults. This method allows for "
                    "convenient one-time or recurring contributions without the need for "
                    "credit card processing.",
                    "Setting up an ACH transfer",
                    "For guidance on how to set up a direct bank transfer, including "
                    "necessary account details, please contact our Philanthropy team. "
                    "We\u2019ll be happy to assist you with a secure and seamless setup "
                    "process."),
                option_card("daf", "magenta", "Donor advised fund",
                    "fas fa-hand-holding-heart",
                    "Support meaningful connections with your donor-advised fund",
                    "A Donor-Advised Fund (DAF) is a popular and tax-efficient way to "
                    "support charitable organizations you care about, like Friends &amp; Co. "
                    "When you contribute to your DAF, you may qualify for an immediate "
                    "federal income tax charitable deduction, making it an excellent "
                    "vehicle for maximizing your generosity.",
                    "Recommend a grant",
                    "We would be honored to be a recipient of your DAF grant. Please "
                    "contact our Philanthropy team to get our official name, Federal ID "
                    "Number (EIN), and mailing address to ensure your grant is processed "
                    "smoothly."),
                option_card("matching", "green", "Employee matching", "fas fa-building",
                    "Double your impact: ask your employer about matching gifts",
                    "Many companies offer matching gift programs that can significantly "
                    "increase the value of your donation to Friends &amp; Co. If your "
                    "employer has such a program, they may match your contribution "
                    "dollar-for-dollar (or even more), effectively doubling the support "
                    "for older adults in our community.",
                    "Check for matching",
                    "Check with your company\u2019s HR or community relations department to "
                    "see if they have a matching gift program, or contact our Philanthropy "
                    "team for assistance."),
                option_card("thrivent", "orange", "Thrivent funds", "fas fa-coins",
                    "Direct your Thrivent Choice Dollars\u00ae to Friends &amp; Co",
                    "If you\u2019re a Thrivent financial member, you have a unique opportunity "
                    "to direct \u201cChoice Dollars\u00ae\u201d to support Friends &amp; Co at no cost "
                    "to you. This program allows eligible members to recommend where "
                    "Thrivent distributes its charitable funds.",
                    "Direct Choice Dollars\u00ae",
                    "Simply log in to your Thrivent account online, or contact your "
                    "Thrivent financial professional, to designate Friends &amp; Co as your "
                    "chosen charity."),
                option_card("stock", "teal", "Stock / IRA", "fas fa-chart-line",
                    "Make a meaningful impact by donating appreciated stocks",
                    "Many people choose to donate appreciated stocks to Friends &amp; Co "
                    "because it can offer significant tax advantages. Giving stock is an "
                    "easy way to maximize your impact on meaningful connections for older "
                    "adults. Donors aged 70\u00bd or older are also eligible to give tax-free "
                    "gifts directly from their IRA (Qualified Charitable Distributions).",
                    "Make a gift",
                    "For personalized guidance and the details needed to make a gift of "
                    "stock or from your IRA, please contact us."),
                option_card("event", "slate", "Host your event", "fas fa-glass-cheers",
                    "Turn your passion into purpose: host a fundraiser",
                    "Consider hosting your own fundraising event. Whether it\u2019s a small "
                    "gathering with friends, a community bake sale, a charity walk, or an "
                    "online campaign, your efforts can create meaningful connections.",
                    "Start planning",
                    "We\u2019d love to hear your ideas and help you make your event a success. "
                    "Please contact our Philanthropy team to discuss your event."),
            ]),
        pattern_cta("Better together", "Ready to change lives?", wash="magenta",
                    ctas=[("Give today", BASE + "/donate/", "btn-white")]),
    ])

# --- Get involved / volunteer ----------------------------------------------
VOLUNTEER_ROLES = [
    ("Coffee Talk volunteer",
     "Answer the drop-in phone line and have friendly, 20-minute conversations.",
     "Learn more", BASE + "/volunteer-coffee-talk/"),
    ("Phone Companion",
     "Call the same older adult each week and build a real, ongoing friendship.",
     "Learn more", BASE + "/volunteer-phone-companion/"),
    ("Visiting Companion",
     "Visit an older adult in their home once or twice a month.",
     "Learn more", BASE + "/volunteer-visiting-companion/"),
    ("Cards Connect volunteer",
     "Make handmade cards that get mailed to older adults four times a year.",
     "Learn more", BASE + "/volunteer-cards-connect/"),
    ("Admin volunteer",
     "Support the office team with the behind-the-scenes work that keeps us running.",
     "Learn more", BASE + "/volunteer-admin/"),
]

PAGES["get-involved"] = dict(
    title="Volunteer", nav="volunteer", css=None,
    sections=[
        hero("Start volunteering",
             "Give an hour a week, or an hour a month — whatever you have is enough.",
             eyebrow="Get involved", tone="blue",
             ctas=[("Apply to volunteer", BASE + "/volunteer/", "btn-lime"),
                   ("Refer an older adult", REFER, "btn-outline btn-on-dark")]),
        prose(heading="Volunteering with Friends &amp; Co", tone="tint", paras=[
            "Our volunteers are the reason the programs work. You don't need special "
            "training or experience — just a willingness to listen and show up.",
            "Every volunteer is screened, trained and supported by our team, and we match "
            "you thoughtfully so the friendship works for both of you.",
        ]),
        cards("Volunteer opportunities", VOLUNTEER_ROLES,
              sub="Five ways to help. Choose the one that fits your time and interests.",
              tone="white"),
        steps("How to get started", [
            ("Apply online", "Tell us a bit about yourself and what you'd like to do."),
            ("Screening and training",
             "We'll run a background check and give you the training you need."),
            ("Get matched",
             "We introduce you to an older adult whose interests line up with yours."),
        ], eyebrow="Getting started", tone="tint"),
        cta("Ready to volunteer?",
            "The application takes about ten minutes.",
            [("Apply to volunteer", BASE + "/volunteer/", "btn-lime"),
             ("Current volunteers portal", BASE + "/volunteer-portal/",
              "btn-outline btn-on-dark")]),
    ])

# --- Refer -----------------------------------------------------------------
PAGES["refer"] = dict(
    title="Refer an older adult", nav="programs", css=None,
    sections=[
        hero("Refer an older adult",
             "If you're worried someone is lonely, you can connect them with us.",
             eyebrow="For family, caregivers and professionals", tone="magenta",
             ctas=[("Start a referral", BASE + "/refer/", "btn-lime")]),
        prose(heading="Who can be referred?", tone="tint", paras=[
            "Anyone aged 62 or over living in Minnesota. They don't need to be a client of "
            "any other service, and there's no cost at any point.",
            "You can refer a parent, a neighbor, a client or a friend. We'll reach out to "
            "them directly and find the program that suits them best.",
        ]),
        steps("What happens after you refer", [
            ("You send us their details",
             "Name, contact details, and anything you think we should know."),
            ("We get in touch",
             "One of our team calls to introduce Friends &amp; Co and talk through the options."),
            ("They choose a program",
             "No obligation. They join whichever program feels right — or none at all."),
        ], tone="white"),
        cta("Know someone who could use a friend?",
            "A referral takes a few minutes and could change someone's year.",
            [("Start a referral", BASE + "/refer/", "btn-lime")]),
    ])

# --- Contact ---------------------------------------------------------------
PAGES["contact"] = dict(
    title="Contact", nav="about", css=None,
    sections=[
        hero("Contact us",
             "We'd love to hear from you — whether you're interested in a program, "
             "volunteering, or supporting the work.",
             eyebrow="Get in touch", tone="blue"),
        factbox("How to reach us", [
            ("Phone", '<a href="tel:+16127211400">612-721-1400</a>'),
            ("Email", '<a href="mailto:info@friendsco.org">info@friendsco.org</a>'),
            ("Fax", "612-721-5848"),
        ], tone="tint"),
        factbox("Visit us", [
            ("Address",
             "2550 University Avenue W<br>Suite 260-S<br>Saint Paul, MN 55114"),
            ("Please note",
             "Hwy 280 is closed for construction — allow extra time."),
            ("Office hours", "Monday to Friday, 9 a.m. to 4 p.m."),
        ], tone="white"),
        cards("You might be looking for", [
            ("Join a program", "Free friendship programs for adults 62+.",
             "Explore programs", BASE + "/friendship-services/"),
            ("Volunteer", "Find a role that fits your time.",
             "Get involved", BASE + "/get-involved/"),
            ("Give", "Support the work with a one-time or recurring gift.",
             "Donate", BASE + "/donate/"),
        ], tone="tint"),
    ])

# --- Staff and board -------------------------------------------------------
PAGES["staff-and-board"] = dict(
    title="Staff and board", nav="about", css=None,
    sections=[
        hero("Our team",
             "The staff and board who keep Friends &amp; Co running.",
             eyebrow="Staff and board", tone="blue"),
        prose(heading="Staff", tone="tint", paras=[
            "Our small staff team runs the programs, supports the volunteers, and keeps "
            "the organization on a steady footing.",
        ]),
        prose(heading="Board of directors", tone="white", paras=[
            "Our volunteer board provides governance, financial oversight and strategic "
            "direction for Friends &amp; Co.",
        ]),
        cta("Want to join us?",
            "We're always glad to hear from people who want to get involved.",
            [("Contact us", BASE + "/contact/", "btn-lime")]),
    ])

# --- Annual reports --------------------------------------------------------
PAGES["annual-reports"] = dict(
    title="Annual reports", nav="about", css=None,
    sections=[
        hero("Annual reports",
             "See how we use the gifts entrusted to us, and the impact they make.",
             eyebrow="Accountability", tone="blue"),
        cards("Reports and filings", [
            ("Annual report", "Our yearly summary of programs, people and impact.",
             "Read the latest", "news-article.html"),
            ("Form 990", "Our most recent IRS filing, in full.",
             "View the 990", BASE + "/wp-content/uploads/2026/04/Friends-FY25-Form-990.pdf"),
            ("Financial statements", "Audited statements for the most recent year.",
             "View statements", "#"),
        ], tone="tint"),
        prose(heading="Accredited and reviewed", tone="white", paras=[
            "Friends &amp; Co is a four-star rated charity on Charity Navigator and meets "
            "the Charities Review Council standards. Your gift is in good hands.",
        ]),
    ])

# --- Search results --------------------------------------------------------
PAGES["search-results"] = dict(
    title="Search results", nav="", css=None,
    sections=[
        hero("Search results",
             "Showing results for your search across programs, services, events "
             "and resources.",
             eyebrow="Site search", tone="blue"),
        cards("Results", [
            ("Phone Companions",
             "Weekly one-to-one calls that spark meaningful, ongoing friendships.",
             "View page", BASE + "/phone-companions/"),
            ("Coffee Talk",
             "A free, drop-in phone line open Tuesday and Thursday mornings.",
             "View page", BASE + "/coffee-talk/"),
            ("Volunteer opportunities",
             "Five ways to help, from phone calls to card making.",
             "View page", BASE + "/get-involved/"),
        ], sub="Three results found.", tone="tint"),
        cta("Didn't find what you needed?",
            "Call 612-721-1400 or email info@friendsco.org and we'll help.",
            [("Contact us", BASE + "/contact/", "btn-lime")]),
    ])


# --- Phone Companions (mirrors live) ---------------------------------------
PAGES["phone-companions"] = dict(
    title="Phone Companions", nav="programs", css=None,
    sections=[
        split_hero("A friendly voice every week",
                   "Pair with a trained volunteer for a meaningful weekly phone call "
                   "from the comfort of home.",
                   WP + "/2025/09/senior-woman-talking-over-the-phone-at-her-home-2024-10-18-05-19-09-utc-scaled-1-1024x683.jpg",
                   eyebrow="Phone companions", accent="orange",
                   ctas=[("Refer an older adult", REFER, "btn-tint-on-orange"),
                         ("Join the program", JOIN, "btn-ghost-tint")]),
        statement("Build a friendship from the comfort of your home", [
            "Phone Companions pair older adults with background-checked, trained "
            "volunteers for meaningful one-on-one phone conversations. Together, you and "
            "your companion can decide on a schedule that works best for you, with most "
            "choosing to connect weekly.",
        ], tone="tint", heading_color="magenta", divider=False),
        icon_steps("How it works", "Here\u2019s what to expect when you sign up:", [
            ("fas fa-mobile-screen", "Phone assessment",
             "We'll give you a friendly call to learn more about your interests and "
             "preferences."),
            ("fas fa-users", "Matching process",
             "We'll pair you with a volunteer based on availability, interests, and "
             "shared life details."),
            ("fas fa-comments", "Weekly calls",
             "You and your companion choose a schedule that works \u2014 most people chat "
             "once a week."),
        ], accent="orange"),
        faq_cards("Frequently asked questions", "All the answers you need to get started.", [
            ("fas fa-circle-check", "Who qualifies?",
             "You must be 62 or older and live in Minnesota or Western Wisconsin. This "
             "program is for older adults seeking meaningful phone-based companionship. "
             "(Not suited for dementia care.)"),
            ("fas fa-clock", "What happens next?",
             "A member of our team will reach out to schedule a friendly assessment call. "
             "This helps us understand your needs and match you with the best possible "
             "companion."),
            ("fas fa-headset", "Is support available?",
             "Yes! If you miss a call or haven\u2019t heard from your companion, please "
             "contact our office. We are here to ensure your connection stays strong."),
            ("fas fa-location-dot", "In-person options?",
             "Phone Companions is remote-only. If you prefer face-to-face visits, please "
             "check out our Visiting Companions program page."),
        ]),
        choice_band("Ready to make a new friend?", "Get connected",
                    WP + "/2025/09/senior-woman-talking-over-the-phone-at-her-home-2024-10-18-05-19-09-utc-scaled-1-1024x683.jpg",
                    alt="An older woman smiling while talking on the phone",
                    choices=[
                        ("orange", "I want a companion",
                         "I am an older adult (62+) and would like to be paired with a "
                         "volunteer for weekly calls.",
                         "Join the program", JOIN),
                        ("blue", "I want to refer someone",
                         "I know an older adult who would enjoy receiving friendly calls "
                         "from a volunteer.",
                         "Refer a senior", REFER),
                    ]),
    ])

# --- Events ----------------------------------------------------------------
PAGES["events"] = dict(
    title="Events", nav="programs", css=None,
    sections=[
        hero("Events and gatherings",
             "Gather with us in person or online. All are welcome.",
             eyebrow="Community", tone="magenta"),
        cards("Upcoming events", [
            ("Let’s Do Coffee: Queermunity",
             "Thursday, Jul 2 · 9:30 to 11 a.m. — Minneapolis. A gathering for LGBTQ+ older "
             "adults and friends at Queermunity.", "Event details", "event-detail.html"),
            ("Let’s Do Coffee: FamilyMeans",
             "Tuesday, Jul 8 · 9:30 to 11 a.m. — Stillwater. Coffee and connection for "
             "LGBTQ+ older adults and friends at FamilyMeans.", "Event details", "event-detail.html"),
            ("Let’s Do Lunch Café: Hennepin Ave UMC",
             "Monday, Jul 14 · 11:30 a.m. to 1:30 p.m. — Minneapolis. Monthly lunch gathering "
             "for LGBTQ+ older adults and friends.", "Event details", "event-detail.html"),
        ], tone="tint"),
        cta("Want to be told about new events?",
            "Join our mailing list and we'll send dates as they're confirmed.",
            [("Contact us", BASE + "/contact/", "btn-lime")]),
    ])

# --- News ------------------------------------------------------------------
PAGES["news"] = dict(
    title="Latest news", nav="about", css=None,
    sections=[
        hero("Latest news",
             "Stories from our staff, volunteers and community partners.",
             eyebrow="Stories", tone="blue"),
        cards("Recent stories", [
            ("Volunteer of the month — June 2026",
             "Ric Landers discovered Friends &amp; Co through a Let’s Do Coffee event and "
             "became one of our most engaged volunteers.", "Read the story", "news-article.html"),
            ("For some LGBTQ+ older adults, aging means going back into the closet",
             "LGBTQ+ older adults experienced decades of loneliness shaped by the need to "
             "hide their identities during less accepting times.", "Read the story", "news-article.html"),
            ("Pride, connection and community at Lavender’s summer kickoff",
             "Friends &amp; Co participated as a community partner at the Lavender Magazine "
             "2026 Summer of Pride kickoff party.", "Read the story", "news-article.html"),
        ], tone="tint"),
    ])

# --- Remembering our friends -----------------------------------------------
PAGES["remembering-our-friends"] = dict(
    title="Remembering our friends", nav="about", css=None,
    sections=[
        hero("Remembering our friends",
             "Honoring the older adults in our community who have died, and the "
             "friendships they made.",
             eyebrow="In memoriam", tone="navy"),
        prose(heading="A community remembers", tone="tint", paras=[
            "Friendship doesn't end when someone dies. This page honors the older adults in "
            "our community we have lost, and the volunteers who walked alongside them.",
            "Memorials are organized by year. If you would like someone added, please get in "
            "touch with our team.",
        ]),
        cta("Add a remembrance",
            "Contact us and we'll add your friend to this page.",
            [("Contact us", BASE + "/contact/", "btn-lime")]),
    ])


# --- Join a program --------------------------------------------------------
PAGES["join"] = dict(
    title="Join a program", nav="programs", css=None,
    sections=[
        hero("Join a program",
             "Tell us a little about yourself and we'll help you find the right fit. "
             "Every program is free.",
             eyebrow="For adults 62+ in Minnesota", tone="blue"),
        prose(heading="Before you start", tone="tint", paras=[
            "You'll need to be 62 or older and living in Minnesota. There is no cost at any "
            "point, and you can join more than one program.",
            "If you're filling this in on behalf of someone else, use the "
            "<a href=\"refer.html\">referral form</a> instead.",
        ]),
        raw("""<section class="section section-white">
  <div class="container">
    <h2>Your details</h2>
    <form class="form-panel" onsubmit="return false;">
      <div class="field-row">
        <label>First name<input type="text" autocomplete="given-name"></label>
        <label>Last name<input type="text" autocomplete="family-name"></label>
      </div>
      <div class="field-row">
        <label>Phone<input type="tel" autocomplete="tel"></label>
        <label>Email<input type="email" autocomplete="email"></label>
      </div>
      <label>Which program interests you?
        <select>
          <option>I'm not sure — help me choose</option>
          <option>Coffee Talk</option>
          <option>Phone Companions</option>
          <option>Visiting Companions</option>
          <option>Cards Connect</option>
          <option>Let's Do Coffee / Let's Do Lunch Caf&eacute;</option>
          <option>Conexiones Comunitarias</option>
        </select>
      </label>
      <label>Anything you'd like us to know?<textarea rows="4"></textarea></label>
      <button type="submit" class="btn btn-lime btn-lg">Send my request</button>
      <p class="form-note">We'll call you within a few days to talk it through.
        Nothing is confirmed until you've spoken to us.</p>
    </form>
  </div>
</section>"""),
        cta("Prefer to talk to someone?",
            "Call us on 612-721-1400, Monday to Friday, 9 a.m. to 4 p.m.",
            [("Contact us", BASE + "/contact/", "btn-lime")]),
    ])

# --- Volunteer application -------------------------------------------------
PAGES["volunteer-apply"] = dict(
    title="Apply to volunteer", nav="volunteer", css=None,
    sections=[
        hero("Apply to volunteer",
             "The application takes about ten minutes. We'll be in touch within a week.",
             eyebrow="Get involved", tone="blue"),
        steps("What happens next", [
            ("You apply", "Fill in the form below — it takes about ten minutes."),
            ("Screening and training",
             "We'll run a background check and give you the training you need."),
            ("Get matched",
             "We introduce you to an older adult whose interests line up with yours."),
        ], eyebrow="The process", tone="tint"),
        raw("""<section class="section section-white">
  <div class="container">
    <h2>Your details</h2>
    <form class="form-panel" onsubmit="return false;">
      <div class="field-row">
        <label>First name<input type="text" autocomplete="given-name"></label>
        <label>Last name<input type="text" autocomplete="family-name"></label>
      </div>
      <div class="field-row">
        <label>Phone<input type="tel" autocomplete="tel"></label>
        <label>Email<input type="email" autocomplete="email"></label>
      </div>
      <label>Which role interests you?
        <select>
          <option>I'm not sure — help me choose</option>
          <option>Coffee Talk volunteer</option>
          <option>Phone Companion</option>
          <option>Visiting Companion</option>
          <option>Cards Connect volunteer</option>
          <option>Admin volunteer</option>
        </select>
      </label>
      <label>How much time can you give?
        <select>
          <option>About an hour a week</option>
          <option>About an hour a month</option>
          <option>A few hours a month</option>
          <option>Flexible</option>
        </select>
      </label>
      <label>Tell us a bit about yourself<textarea rows="4"></textarea></label>
      <button type="submit" class="btn btn-lime btn-lg">Submit application</button>
      <p class="form-note">All volunteers are screened and trained before being matched.</p>
    </form>
  </div>
</section>"""),
        cta("Questions before you apply?",
            "Email info@friendsco.org or call 612-721-1400 — we're happy to talk it through.",
            [("Contact us", BASE + "/contact/", "btn-lime")]),
    ])


# ---------------------------------------------------------------------------
# Volunteer role pages
#
# On the live site these are posts under News, and only the Coffee Talker one
# has real content — the rest read "Full details coming soon!". The mockups
# build all five out properly, in the Phone Companions visual language, so
# Paul can see what the section becomes.
# ---------------------------------------------------------------------------

def role_page(slug, title, tagline, accent, photo, intro, steps_items,
              duties_head, duties_lede, duties, commitment_head, commitment,
              proposed=False):
    secs = [
        split_hero(title, tagline, photo, eyebrow="Volunteer", accent=accent,
                   ctas=[("Apply to volunteer", BASE + "/volunteer/",
                          "btn-tint-on-" + accent),
                         ("All opportunities", BASE + "/get-involved/",
                          "btn-ghost-tint")]),
        statement("What you’ll do", [intro], tone="tint",
                  heading_color="magenta", divider=False),
        icon_steps("Become a volunteer in three steps", None, steps_items,
                   accent=accent),
        faq_cards(duties_head, duties_lede, duties),
        choice_band(commitment_head, "Time commitment", photo,
                    alt="A Friends &amp; Co volunteer",
                    choices=[
                        (accent, "Ready to apply?", commitment,
                         "Apply to volunteer", BASE + "/volunteer/"),
                        ("blue", "Still deciding?",
                         "Have a question first? Call 612-721-1400 or email "
                         "info@friendsco.org and we’ll talk it through.",
                         "Contact us", BASE + "/contact/"),
                    ]),
    ]
    PAGES[slug] = dict(title=title, nav="volunteer", css=None, sections=secs)


role_page("volunteer-coffee-talk", "Volunteer as a Coffee Talker",
    "One short phone call can change the shape of someone’s day — and you’re "
    "never doing it alone.",
    "orange", WP + "/2025/09/senior-woman-talking-over-the-phone-at-her-home-"
                   "2024-10-18-05-19-09-utc-scaled-1-1024x683.jpg",
    "You’ll have friendly, one-on-one phone conversations with older adults who call "
    "into Coffee Talk during weekday mornings. Calls last up to 20 minutes, which keeps "
    "conversations focused, manageable and welcoming. There’s no counseling and no "
    "fixing things — just real conversation, reliable presence, and a simple way to "
    "help reduce isolation.",
    [("fas fa-file-pen", "Apply online",
      "Complete a short volunteer application, including a required background check."),
     ("fas fa-graduation-cap", "Complete training",
      "Once your background check is approved, you’ll complete our training so you feel "
      "confident and supported."),
     ("fas fa-calendar-check", "Choose your time slots",
      "After training, sign up for weekday morning shifts that work for you and join "
      "the Coffee Talk team.")],
    "During your shift, you’re part of a team",
    "Real conversations. Real people. Real mornings.",
    [("fas fa-mug-hot", "What a shift looks like",
      "You take calls as they come in during the morning window. Between calls you’re "
      "in a shared space with other volunteers and staff."),
     ("fas fa-users", "You’re never alone",
      "Staff are on hand throughout every shift. If a call raises something you’re "
      "unsure about, you hand it straight to us."),
     ("fas fa-clock", "Short and focused",
      "Calls last up to 20 minutes. That keeps them welcoming for the caller and "
      "manageable for you."),
     ("fas fa-heart", "No experience needed",
      "You don’t need a background in care or counseling. You need to be a warm, "
      "reliable listener — the training covers the rest.")],
    "Coffee Talk is structured and predictable",
    "Shifts are weekday mornings, and most volunteers are fully onboarded and ready to "
    "start within a short period of time.")

role_page("volunteer-phone-companion", "Volunteer as a Phone Companion",
    "Call the same older adult each week and build a real, lasting friendship.",
    "blue", WP + "/2025/09/senior-woman-talking-over-the-phone-at-her-home-"
                 "2024-10-18-05-19-09-utc-scaled-1-1024x683.jpg",
    "You’ll be matched with one older adult and call them each week from wherever you "
    "are. Unlike Coffee Talk, this is the same person every time — so the conversation "
    "builds, and a genuine friendship has room to grow.",
    [("fas fa-file-pen", "Apply online",
      "Complete a short volunteer application, including a required background check."),
     ("fas fa-graduation-cap", "Complete training",
      "We’ll prepare you for your first call and introduce you to your staff contact."),
     ("fas fa-user-group", "Get matched",
      "We pair you based on interests, availability and shared life details.")],
    "What being a Phone Companion involves",
    "One person, one call a week, an ongoing friendship.",
    [("fas fa-phone", "A weekly call",
      "You and your companion agree a time that suits you both. Most pairs talk once a "
      "week for around half an hour."),
     ("fas fa-comments", "Just conversation",
      "No care tasks, no counseling. You’re there as a friend."),
     ("fas fa-headset", "Support when you need it",
      "Your staff contact checks in regularly and is available whenever something "
      "comes up."),
     ("fas fa-calendar", "A real commitment",
      "Because someone is expecting your call, we ask for a consistent weekly slot "
      "over several months.")],
    "A weekly rhythm that fits around you",
    "About half an hour a week, from home, at a time you and your companion choose.",
    proposed=True)

role_page("volunteer-visiting-companion", "Volunteer as a Visiting Companion",
    "Visit an older adult at home and bring company, conversation and routine.",
    "magenta", WP + "/2026/01/support-hero-connection.jpg",
    "You’ll be matched with an older adult near you and visit them in their home once "
    "or twice a month. Visits are about company — a cup of tea, a conversation, a walk "
    "if they’re up for it.",
    [("fas fa-file-pen", "Apply online",
      "Complete a short volunteer application, including a required background check."),
     ("fas fa-house", "Welcome call and home visit",
      "We’ll meet you both, answer questions, and make sure the match feels right."),
     ("fas fa-user-group", "Get matched",
      "We pair you on location, interests and shared life details.")],
    "What visits look like",
    "Ordinary time together, which is exactly the point.",
    [("fas fa-mug-saucer", "One to two visits a month",
      "You and your companion agree a rhythm that suits you both."),
     ("fas fa-comments", "Company, not care",
      "No personal care, no household tasks. You’re there as a friend."),
     ("fas fa-shield-halved", "Screened and supported",
      "Every volunteer is background-checked and trained, with a staff contact "
      "throughout."),
     ("fas fa-location-dot", "Matched near you",
      "We match on location so visits stay easy to keep up.")],
    "A visit or two each month",
    "Most pairs meet one to two times a month, at a time that suits you both.",
    proposed=True)

role_page("volunteer-cards-connect", "Volunteer with Cards Connect",
    "Make handmade cards that arrive in someone’s mailbox four times a year.",
    "teal", WP + "/2026/01/support-hero-group.jpg",
    "You’ll create handmade cards that we mail to older adults in the fall, over the "
    "winter holidays, for Valentine’s Day and in late spring. It’s a way to help that "
    "fits entirely around your own schedule.",
    [("fas fa-file-pen", "Sign up",
      "Let us know you’d like to take part — no background check needed for card making."),
     ("fas fa-palette", "Make your cards",
      "Work at home, at your own pace, on your own timetable."),
     ("fas fa-envelope", "Send them in",
      "Drop your finished cards to the office and we handle the mailing.")],
    "What card making involves",
    "Creative, flexible, and entirely on your own schedule.",
    [("fas fa-clock", "No fixed hours",
      "Make cards whenever suits you, in the weeks before each mailing."),
     ("fas fa-users", "Alone or in a group",
      "Some volunteers make cards at home; others join a group session."),
     ("fas fa-pen-nib", "No particular skill needed",
      "Warmth matters more than artistry. We’ll share prompts and ideas."),
     ("fas fa-calendar-days", "Four mailings a year",
      "Fall, the winter holidays, Valentine’s Day and late spring.")],
    "As much or as little as you like",
    "There’s no minimum. Make one card or fifty, whenever it suits you.",
    proposed=True)

role_page("volunteer-admin", "Volunteer in the office",
    "Support the team behind the scenes and keep the programs running.",
    "orange", WP + "/2026/01/support-hero-group.jpg",
    "Office volunteers help with the work that keeps everything else possible — data "
    "entry, mailings, event preparation, and answering the phone. If you’d rather help "
    "without being matched one-to-one, this is the role.",
    [("fas fa-file-pen", "Apply online",
      "Complete a short volunteer application, including a required background check."),
     ("fas fa-comments", "Have a chat",
      "We’ll talk through what you enjoy and where you’d like to help."),
     ("fas fa-calendar-check", "Choose your hours",
      "Office shifts are weekdays; you pick what fits your week.")],
    "What office volunteers do",
    "Varied, practical work that keeps the programs moving.",
    [("fas fa-keyboard", "Data and records",
      "Keeping participant and volunteer records accurate and current."),
     ("fas fa-envelopes-bulk", "Mailings",
      "Preparing newsletters, cards and appeal letters for posting."),
     ("fas fa-champagne-glasses", "Event preparation",
      "Helping get everything ready for gatherings and luncheons."),
     ("fas fa-phone", "Reception",
      "Answering the phone and welcoming people to the office.")],
    "Weekday hours that suit you",
    "Most office volunteers give a few hours a week, on a schedule you set with us.",
    proposed=True)


# --- Volunteer portal ------------------------------------------------------
PAGES["volunteer-portal"] = dict(
    title="Volunteer portal", nav="volunteer", css=None,
    sections=[
        pattern_page_hero("Volunteer portal",
                          "Sign in to log your hours, view resources and update your "
                          "details.",
                          eyebrow="Current volunteers", wash="blue",
                          ctas=[("Sign in", "#", "btn-white")]),
        cards("Once you’re signed in", [
            ("Log your hours", "Record visits, calls and shifts so we can report our "
             "collective impact accurately.", None, None),
            ("Resources and training", "Refresher materials, guidance notes and the "
             "volunteer handbook.", None, None),
            ("Update your details", "Change your contact details, availability or "
             "emergency contact.", None, None),
        ], eyebrow="What's inside", tone="tint"),
        cta("Trouble signing in?",
            "Call 612-721-1400 or email info@friendsco.org and we'll get you back in.",
            [("Contact us", BASE + "/contact/", "btn-lime")]),
    ])

# --- Matching hub ----------------------------------------------------------
PAGES["visiting-companions-match"] = dict(
    title="Matching hub", nav="volunteer", css=None,
    sections=[
        pattern_page_hero("Matching hub",
                          "Read a little about the older adults waiting to be matched, "
                          "and tell us who you’d like to connect with.",
                          eyebrow="Choose who you’ll connect with", wash="magenta",
                          ctas=[("Back to volunteering", BASE + "/get-involved/",
                                 "btn-white btn-arrow-left")]),
        notice("This page is password protected", [
            "The matching hub contains personal details about the older adults in our "
            "programs, so it’s only available to volunteers who have completed "
            "screening and training.",
            "If you’ve been through training and don’t have the password, please "
            "<a href=\"contact.html\">get in touch</a>.",
        ], tone="blue"),
        cards("How matching works", [
            ("Read the profiles", "Each profile covers interests, background and what "
             "the person is hoping for from a companion.", None, None),
            ("Tell us your preference", "Let your staff contact know who you’d like to "
             "be matched with.", None, None),
            ("We make the introduction", "We check the match works both ways, then "
             "introduce you.", None, None),
        ], tone="tint"),
    ])

# --- Single news article template ------------------------------------------
PAGES["news-article"] = dict(
    title="News article", nav="about", css=None,
    sections=[
        pattern_page_hero("Volunteer of the month — June 2026",
                          "How one Let’s Do Coffee event turned into a year of "
                          "volunteering.",
                          eyebrow="Volunteers · June 2026", wash="teal",
                          ctas=[("Back to news", BASE + "/news/",
                                 "btn-white btn-arrow-left")]),
        media("Ric Landers", [
            "Ric Landers initially discovered Friends &amp; Co through a Let’s Do Coffee "
            "event designed for LGBTQ+ older adults seeking community.",
            "He subsequently became deeply engaged, taking on multiple volunteer "
            "positions including event support and handmade card preparation.",
            "“Helping others is the foundation of my life, and Friends &amp; Co gives me "
            "the chance to do that.”",
        ], WP + "/2026/01/support-hero-group.jpg",
            alt="Ric Landers at a Friends &amp; Co event", tone="tint"),
        cards("More stories", [
            ("For some LGBTQ+ older adults, aging means going back into the closet",
             "Decades of loneliness shaped by the need to hide their identities during "
             "less accepting times.", "Read the story", "news-article.html"),
            ("Pride, connection and community at Lavender’s summer kickoff",
             "Friends &amp; Co took part as a community partner at the 2026 Summer of "
             "Pride kickoff party.", "Read the story", "news-article.html"),
            ("Friends &amp; Co featured on KARE 11 news",
             "Our Pride celebration luncheon made the local evening news.",
             "Read the story", "news-article.html"),
        ], eyebrow="Related", tone="white"),
    ])

# --- Single event template -------------------------------------------------
PAGES["event-detail"] = dict(
    title="Event", nav="programs", css=None,
    sections=[
        pattern_page_hero("Let’s Do Coffee: Queermunity",
                          "Thursday, 2 July · 9:30 to 11 a.m. · Queermunity, Minneapolis",
                          eyebrow="Events &amp; gatherings", wash="magenta",
                          ctas=[("All events", BASE + "/events/",
                                 "btn-white btn-arrow-left")]),
        split("About this gathering", [
            "A free, drop-in gathering for older LGBTQ+ adults to relax, talk, laugh and "
            "connect over complimentary coffee and pastries.",
            "No pressure. No explaining yourself. Just socializing and friendship. You "
            "don’t need to register, and you’re welcome to bring a friend.",
        ],
            "fas fa-location-dot", "Details", [
                ("When", "Thursday, 2 July<br>9:30 to 11 a.m."),
                ("Where", "Queermunity<br>1121 Jackson St NE<br>Minneapolis, MN"),
                ("Cost", "Free — no registration needed"),
            ],
            tone="tint", aside_accent="lime"),
        cta("Can’t make this one?",
            "We hold Let’s Do Coffee and Let’s Do Lunch gatherings across the Twin "
            "Cities every month.",
            [("See all events", BASE + "/events/", "btn-lime")]),
    ])


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render(slug, spec):
    extra = ""
    if spec.get("css"):
        extra = '<link rel="stylesheet" href="assets/css/pages/%s.css">\n' % spec["css"]
    parts = [HEAD.format(title=spec["title"], nav=spec["nav"], extra_css=extra)]
    parts.append("\n\n".join("  " + s.replace("\n", "\n  ") for s in spec["sections"]))
    parts.append("\n\n" + FOOT)
    with open(slug + ".html", "w", encoding="utf-8") as fh:
        fh.write("".join(parts))
    return slug + ".html"


def main():
    want = sys.argv[1:] or list(PAGES)
    for slug in want:
        if slug not in PAGES:
            print("unknown page:", slug)
            continue
        print("built", render(slug, PAGES[slug]))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()

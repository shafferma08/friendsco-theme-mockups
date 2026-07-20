#!/usr/bin/env python3
"""
Friends & Co mockup consistency linter.

Run from the friendsco-theme-mockups folder:

    python3 lint.py

Catches the drift that made the mockup set stop matching the live build:
stray fonts, redefined tokens, inflated root font size, all-caps text,
hard-coded brand colours, competing container widths, and pages that paste
their own header or footer instead of using the shared one.

Exit code is 0 when every page is clean, 1 when something needs attention.
"""

import os
import re
import sys

SKIP_FILES = {'_template.html', 'styleguide.html'}
SKIP_DIRS = {'assets', '.git', '.claude', 'node_modules', '_archive'}

SHARED_CSS = 'assets/css/friendsco.css'

CHECKS = [
    # (label, regex, hint)
    ('condensed font',
     re.compile(r'Roboto\+?\s?Condensed|Akzidenz', re.I),
     'Headings are Open Sans. Akzidenz is print-only and Roboto Condensed was '
     'only ever a stand-in for it.'),

    ('redefined design token',
     re.compile(r'--(?:font|font-primary|font-display|container|container-width|'
                r'blue|magenta|lime|green|navy|cream|ink|teal|orange|slate)\s*:', re.I),
     'Tokens live in assets/css/friendsco.css. Delete the local :root block.'),

    ('inflated root font size',
     re.compile(r'html\s*\{[^}]*font-size\s*:\s*(?!100%)', re.I | re.S),
     'The root stays at 16px. Large type comes from --fs-body, not a bigger root.'),

    ('uppercase text',
     re.compile(r'text-transform\s*:\s*uppercase', re.I),
     'Sentence case everywhere — this is a standing client rule.'),

    ('hard-coded palette colour',
     re.compile(r'#(?:5E74B1|BA3F97|B0D235|00BBD3|F9A41E|7D91A0|85C340|'
                r'1A2A42|F7FDDF|4B5D91|EEF2FB|3F5591|9C2F7E|A8CC26|6FAA2C)\b', re.I),
     'Use the token (var(--blue) etc.). Raw hex bypasses the brand-tier '
     'labelling in friendsco.css, which is how off-brand colours crept in '
     'unnoticed the first time.'),

    ('inline header markup',
     re.compile(r'<header[^>]*class="[^"]*site-header', re.I),
     'The header is injected by assets/js/chrome.js. Use <div data-chrome="header"></div>.'),

    ('inline footer markup',
     re.compile(r'<footer[^>]*>\s*<div class="footer-newsletter"', re.I | re.S),
     'The footer is injected by assets/js/chrome.js. Use <div data-chrome="footer"></div>.'),

    ('link to the live WordPress site',
     re.compile(r'href\s*=\s*["\']https?://(?:www\.)?friendsco\.org', re.I),
     'Navigation must stay inside the mockup — clicking through it should never '
     'land on friendsco.org. Point at the local .html file instead. '
     '(mailto:info@friendsco.org is fine, and images may be referenced from '
     'friendsco.org by agreement — only href navigation is banned.)'),
]


# Words that legitimately keep their capital inside a heading: program names,
# organisations, places, people, and acronyms. Everything else in a heading
# should be lower case — the client's rule is sentence case throughout.
PROPER_NOUNS = {
    'Friends', 'Co', 'Coffee', 'Talk', 'Cards', 'Connect', 'Phone', 'Companion',
    'Companions', 'Visiting', 'Conexiones', 'Comunitarias', 'Café', 'Cafe',
    'Legacy', 'Circle', 'Charity', 'Navigator', 'Charities', 'Council',
    'Thrivent', 'Choice', 'Dollars', 'Among', 'Minnesota', 'Wisconsin',
    'Saint', 'Paul', 'Amber', 'Carlson', 'Alan', 'Ric', 'Landers', 'Lavender',
    'Magazine', 'Queermunity', 'FamilyMeans', 'Hennepin', 'UMC', 'Twin',
    'Cities', 'Elementor', 'Español', 'Pride', 'Philanthropy',
    'Spanish', 'English', 'DARTS', 'Jethra', 'Kapp', 'Wilder', 'Foundation',
    'Conversaciones', 'Comunitarias',
    # "Let's Do Coffee" / "Let's Do Lunch Café" are program names
    'Do', 'Lunch', 'Let', "Let's", 'Let’s', 'Ave', 'Talker',
    # months and days
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December', 'Monday', 'Tuesday',
    'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
    'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
}

# Headings are stripped of markup before checking, so this is a crude but
# effective test: any capitalised word after the first that isn't a known
# proper noun and isn't an acronym.
HEADING_RE = re.compile(r'<h[1-4][^>]*>(.*?)</h[1-4]>', re.I | re.S)
TAG_RE = re.compile(r'<[^>]+>')
WORD_RE = re.compile(r"[A-Za-zÀ-ÿ’'&+]+")


def title_case_offenders(text):
    """Yield (heading, [offending words]) for headings that look title-cased."""
    for raw in HEADING_RE.findall(text):
        heading = TAG_RE.sub('', raw).replace('&amp;', '&')
        heading = ' '.join(heading.split())
        if not heading or len(heading) > 120:
            continue
        words = WORD_RE.findall(heading)
        if len(words) < 3:
            continue
        def known(w):
            # accept possessives: Lavender’s -> Lavender
            stem = re.sub(r"[’']s$", '', w)
            return w in PROPER_NOUNS or stem in PROPER_NOUNS

        bad = [w for w in words[1:]
               if w[:1].isupper()
               and not known(w)
               and not w.isupper()          # acronyms: ACH, IRA, TIN, LGBTQ
               and len(w) > 2]
        if bad:
            yield heading, bad


def find_pages():
    pages = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for f in sorted(files):
            if f.endswith('.html') and f not in SKIP_FILES:
                pages.append(os.path.join(root, f))
    return sorted(pages)


def line_of(text, pos):
    return text.count('\n', 0, pos) + 1


def main():
    pages = find_pages()
    if not pages:
        print('No pages found. Run this from the friendsco-theme-mockups folder.')
        return 1

    total = 0
    unconverted = []

    for path in pages:
        with open(path, encoding='utf-8', errors='replace') as fh:
            text = fh.read()

        problems = []

        if SHARED_CSS not in text:
            unconverted.append(path)

        for label, pattern, hint in CHECKS:
            for m in pattern.finditer(text):
                problems.append((line_of(text, m.start()), label, m.group(0)[:60], hint))

        for heading, bad in title_case_offenders(text):
            pos = text.find(heading[:30])
            problems.append((
                line_of(text, pos) if pos > -1 else 0,
                'title case in a heading',
                '%s  [%s]' % (heading[:40], ', '.join(bad)),
                'Sentence case throughout — lower-case these unless they are '
                'program or organisation names. If a name is legitimate, add it '
                'to PROPER_NOUNS at the top of lint.py.'))

        if problems:
            total += len(problems)
            print('\n' + path)
            print('-' * len(path))
            seen_hints = set()
            for line, label, snippet, hint in sorted(problems)[:25]:
                print('  line %-5d %-26s %s' % (line, label, snippet.replace('\n', ' ')))
                if label not in seen_hints:
                    print('            -> %s' % hint)
                    seen_hints.add(label)
            if len(problems) > 25:
                print('  ... and %d more' % (len(problems) - 25))

    # --- link check --------------------------------------------------------
    href_re = re.compile(r'href\s*=\s*["\']([^"\']+)["\']')
    broken, placeholders = [], 0
    for path in pages:
        with open(path, encoding='utf-8', errors='replace') as fh:
            text = fh.read()
        for href in href_re.findall(text):
            if href == '#':
                placeholders += 1
                continue
            if href.startswith(('http', 'mailto:', 'tel:', '#', 'assets/')):
                continue
            target = href.split('#')[0].split('?')[0]
            if target and not os.path.exists(target):
                broken.append((path, href))

    if broken:
        print('\nBroken internal links (%d):' % len(broken))
        for src, href in broken[:20]:
            print('  %-32s -> %s' % (src, href))
    if placeholders:
        print('\n%d placeholder link(s) pointing at "#" — pages not built yet.'
              % placeholders)

    print('\n' + '=' * 64)
    if unconverted:
        print('Not yet on the shared system (%d):' % len(unconverted))
        for p in unconverted:
            print('  ' + p)
        print()

    converted = len(pages) - len(unconverted)
    print('%d of %d pages on the shared system.' % (converted, len(pages)))
    print('%d issue(s) found.' % total)

    return 1 if (total or unconverted) else 0


if __name__ == '__main__':
    sys.exit(main())

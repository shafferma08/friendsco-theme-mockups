"""Diff each mockup's prose against the live page's prose.
# Run:  python3 copycheck.py     (needs a local server on :8899 and playwright)

Anything in the mockup that isn't traceable to the live page gets flagged, so
invented copy can't slip through unnoticed again.
"""
import json, re, sys
from playwright.sync_api import sync_playwright

PAIRS = [
 ('coffee-talk','https://friendsco.org/coffee-talk/'),
 ('visiting-companions','https://friendsco.org/visiting-companions/'),
 ('cards-connect','https://friendsco.org/cards-connect/'),
 ('lets-do-events','https://friendsco.org/lets-do-events/'),
 ('spanish-language-programs','https://friendsco.org/spanish-language-programs/'),
]

def norm(t):
    return re.sub(r'\s+',' ', re.sub(r'[^a-z0-9 ]','', t.lower())).strip()

GRAB = """()=>[...document.querySelectorAll('main h1,main h2,main h3,main h4,main p,main li')]
    .map(e=>(e.textContent||'').replace(/\\s+/g,' ').trim()).filter(t=>t.length>12)"""
LIVEGRAB = """()=>{const r=document.querySelector('[data-elementor-type="wp-page"]'); if(!r) return [];
    return [...r.querySelectorAll('h1,h2,h3,h4,p,li,.e-n-accordion-item-title')]
      .map(e=>(e.textContent||'').replace(/\\s+/g,' ').trim()).filter(t=>t.length>12);}"""

with sync_playwright() as pw:
    b=pw.chromium.launch(args=["--no-sandbox"]); pg=b.new_page()
    for slug,url in PAIRS:
        pg.goto(url, wait_until="domcontentloaded"); pg.wait_for_timeout(700)
        live=[norm(x) for x in pg.evaluate(LIVEGRAB)]
        livejoined=' || '.join(live)
        pg.goto("http://localhost:8899/%s.html"%slug, wait_until="domcontentloaded"); pg.wait_for_timeout(250)
        mine=pg.evaluate(GRAB)
        unmatched=[]
        for m in mine:
            n=norm(m)
            if not n: continue
            # matched if the live page contains this text, or this text contains a live line
            if n in livejoined: continue
            if any(n in l or l in n for l in live): continue
            # allow near-matches: 80% of words present in some live line
            w=set(n.split())
            if any(len(w & set(l.split()))/max(len(w),1) >= .8 for l in live): continue
            unmatched.append(m)
        print('\n%-28s %d blocks, %d not traceable to live' % (slug, len(mine), len(unmatched)))
        for u in unmatched: print('    ! '+u[:100])
    b.close()

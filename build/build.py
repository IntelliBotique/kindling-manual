"""Build the Kindling edition into public/.

  build/.venv/bin/python build/build.py

Reads the four finished Kindling chapters in content/kindling/ and the wrapper copy in build/edition.py.
The chapters are rendered as written, with the Markdown settings the Field Manual's own pipeline uses.
Every table that carries a digit gets a "Figures checked" line, as the master does. The edition carries no
Field Manual text; it links to the Library edition on solo.joshwolf.net.
"""
import html, json, os, re, shutil, sys
import markdown

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edition as E

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')

md = markdown.Markdown(extensions=['tables', 'fenced_code', 'sane_lists', 'smarty'],
                       extension_configs={'smarty': {'smart_dashes': False, 'smart_quotes': False,
                                                     'smart_ellipses': False, 'smart_angled_quotes': False}})

def render(text):
    md.reset()
    return md.convert(text)

K = {}
for kid, meta in E.K_CHAPTERS.items():
    src = open(os.path.join(ROOT, 'content', 'kindling', meta['file']), encoding='utf-8').read()
    first, rest = src.split('\n', 1)
    m = re.match(r'^## Chapter (K\.\d): (.+)$', first)
    assert m and m.group(1) == kid, first
    K[kid] = {'title': m.group(2), 'md': rest, **meta}

RW = {}
for cid, meta in E.REWRITES.items():
    src = open(os.path.join(ROOT, 'content', 'kindling', 'rewrites', meta['file']), encoding='utf-8').read()
    first, rest = src.split('\n', 1)
    m = re.match(r'^## Chapter K-(\d+\.\d+): (.+)$', first)
    assert m and m.group(1) == cid, first
    RW[cid] = {'title': m.group(2), 'md': rest, **meta}

ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
PAGES = []

def esc(s):
    return html.escape(s, quote=True)

def k_href(kid, door=None):
    doors = E.K_CHAPTERS[kid]['doors']
    d = door if door in doors else doors[0]
    return f'/{d}/{E.K_CHAPTERS[kid]["slug"]}'

def rw_href(cid, door=None):
    doors = E.REWRITES[cid]['doors']
    d = door if door in doors else doors[0]
    return f'/{d}/{E.rw_slug(cid)}'

def heading_id(kid, text):
    slug = E.K_CHAPTERS[kid]['slug'] if kid in E.K_CHAPTERS else E.rw_slug(kid[2:])
    return slug + '-' + re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:60]

# ---------- text helpers ----------
SEC_RE = re.compile(r'§(\d+(?:\.\d+)?)')
CHREF_RE = re.compile(r'\b(Chapter|Ch\.?)\s+(\d+\.\d+)\b')
KREF_RE = re.compile(r'\b(?:Chapter\s+)?(K\.[1-4])\b')
KXREF_RE = re.compile(r'\b(?:Chapter\s+)?K-(\d+\.\d+)\b')
KW_RE = re.compile(r'\b(MUST NOT|MUST|SHOULD NOT|SHOULD|MAY)\b')

def sec_anchor(num):
    return E.SPEC_URL + '#s' + num.replace('.', '-')

def map_text_nodes(h, fn, skip=('a', 'code', 'pre', 'script', 'style')):
    """Apply fn to text outside tags, skipping text inside the named elements."""
    out, depth, pos = [], 0, 0
    for m in re.finditer(r'<(/?)([a-zA-Z0-9]+)[^>]*>', h):
        text = h[pos:m.start()]
        out.append(text if depth else fn(text))
        if m.group(2).lower() in skip and not m.group(0).endswith('/>'):
            depth = max(depth + (-1 if m.group(1) else 1), 0)
        out.append(m.group(0))
        pos = m.end()
    tail = h[pos:]
    out.append(tail if depth else fn(tail))
    return ''.join(out)

def link_sections(h, skip=('a', 'code', 'pre', 'script', 'style')):
    return map_text_nodes(h, skip=skip, fn=lambda t: SEC_RE.sub(lambda m: f'<a class="ed-sec" href="{sec_anchor(m.group(1))}">§{m.group(1)}</a>', t))

def link_chapters(h, door=None, self_src=None):
    """Chapter numbers. A rewritten Field Manual number links to its Kindling rewrite, except inside that rewrite,
    where it names the original (xrefs.md). Every other Field Manual number links to the Library edition.
    K.1 to K.4 and K-n.n link within this edition."""
    def fm(m):
        cid = m.group(2)
        if cid in E.REWRITES and cid != self_src:
            return f'<a class="ed-x" href="{rw_href(cid, door)}">{m.group(0)}</a>'
        return f'<a class="ed-x ed-out" href="{E.fm_url(cid)}">{m.group(0)}</a>'
    def kx(m):
        cid = m.group(1)
        if cid not in E.REWRITES:
            return m.group(0)
        return f'<a class="ed-x" href="{rw_href(cid, door)}">{m.group(0)}</a>'
    def fn(t):
        t = KXREF_RE.sub(kx, t)
        t = CHREF_RE.sub(fm, t)
        return KREF_RE.sub(lambda m: f'<a class="ed-x" href="{k_href(m.group(1), door)}">{m.group(0)}</a>', t)
    return map_text_nodes(h, fn)

def mark_keywords(h):
    return map_text_nodes(h, lambda t: KW_RE.sub(lambda m: f'<span class="ed-kw ed-kw-{m.group(1).lower().replace(" ", "-")}">{m.group(1)}</span>', t))

TABLE_RE = re.compile(r'<table>.*?</table>(\s*<p>Figures checked [^<]*</p>)?', re.S)

def stamp_tables(h):
    """Wrap every table. A table that carries a digit gets a "Figures checked" line, unless its text already
    carries one (the rewrites do); that line is kept as written and only given the class."""
    def rep(m):
        table = m.group(0)[:m.group(0).index('</table>') + len('</table>')]
        t = f'<div class="ed-table">{table}</div>'
        if m.group(1):
            return t + m.group(1).strip().replace('<p>', '<p class="ed-checked">', 1)
        if re.search(r'\d', re.sub(r'<[^>]+>', '', table)):
            t += '<p class="ed-checked">Figures checked October 2026.</p>'
        return t
    return TABLE_RE.sub(rep, h)

def inline(s, door=None):
    """Wrapper strings: backticks to code, then section and chapter links."""
    s = re.sub(r'`([^`]+)`', lambda m: '<code>' + html.escape(m.group(1)) + '</code>', s)
    return link_chapters(link_sections(s), door)

def chip(text, planned=False):
    return f'<span class="chip{" chip-planned" if planned else ""}">{text}</span>'

# ---------- page shell ----------
MARK = open(os.path.join(ROOT, 'build', 'mark.svg'), encoding='utf-8').read().strip()

def nav_html(current):
    items = [('/', 'The two doors', 'doors'), ('/builders', 'For builders', 'builders'),
             ('/curators', 'For curators', 'curators'), ('/tools', 'Tools', 'tools')]
    links = ''.join(f'<a href="{u}"' + (' aria-current="page"' if k == current else '') + f'>{t}</a>' for u, t, k in items)
    return links + '<a class="out" href="https://protocol.kindling.foundation/build.html">Build on it</a>'

def page(path, title, body, *, dress='charter', current=None, desc=None):
    cls = ' class="ed-proto"' if dress == 'c1' else ''
    body = link_sections(body, skip=('a', 'code', 'pre', 'script', 'style', 'label', 'title'))
    out = f'''<!doctype html>
<html lang="en"{cls}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc or 'The Solo Operator’s Field Manual, Kindling edition: for people building on the Kindling protocol and people keeping Pools on it.')}">
<meta name="theme-color" content="#16121F">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/fonts.css">
<link rel="stylesheet" href="/assets/charter.css">
<link rel="stylesheet" href="/assets/edition.css">
<link rel="stylesheet" href="https://unicornfactory.dev/assets/uf-credit.css">
<script src="/assets/edition.js"></script>
</head>
<body>
<a class="skip" href="#main">Skip to the page</a>
<div class="xbar"><div class="wrap">
<b>Kindling</b><span>the Field Manual edition</span>
<span class="dot" aria-hidden="true">·</span><span>Spec {E.SPEC_VERSION} · Stable</span>
<span class="dot" aria-hidden="true">·</span><a href="https://protocol.kindling.foundation/">The protocol site</a>
<span class="dot" aria-hidden="true">·</span><a href="{E.SPEC_URL}">The specification</a>
<span class="dot" aria-hidden="true">·</span><a href="https://kindling.foundation/">kindling.foundation</a>
</div></div>
<header class="site"><div class="wrap">
<a class="brand" href="/">{MARK}<span>Kindling<small>The Solo Operator’s Field Manual</small></span></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-menu"><svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M3 5.5h14M3 10h14M3 14.5h14" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>Menu</button>
<div class="site-menu" id="site-menu">
<nav class="nav" aria-label="This edition">{nav_html(current)}</nav>
<div class="tools">
<div class="tg" role="group" aria-label="Theme"><button type="button" data-theme-set="light" aria-pressed="false">Day</button><button type="button" data-theme-set="dark" aria-pressed="true">Night</button></div>
<button type="button" class="rl" data-font-set aria-pressed="false">Readable letters</button>
</div>
</div>
</div></header>
<main id="main" tabindex="-1">
{body}
</main>
<footer class="foot"><div class="wrap">
<p class="foot-note">This edition of The Solo Operator’s Field Manual is for the people building on Kindling and the people keeping Pools on it. Kindling is a real open protocol, published by TranquilTech. Nothing runs on it at TranquilTech yet. Every example here carries a label: invented by the Kindling sites, or invented for this edition.</p>
<nav class="foot-nav" aria-label="Kindling">
<a href="https://protocol.kindling.foundation/">The protocol site</a>
<a href="{E.SPEC_URL}">The specification</a>
<a href="https://protocol.kindling.foundation/build.html">Build on it</a>
<a href="https://kindling.foundation/">kindling.foundation</a>
<a href="https://kindling.foundation/intro.html">The handshake</a>
<a href="{E.LIBRARY}">The Field Manual, Library edition</a>
<a href="https://github.com/IntelliBotique/kindling-manual">This edition’s source</a>
</nav>
<p class="ed-license">{E.LICENSE_LINE}</p>
<p>{E.COOKIE_LINE}</p>
<p class="ed-colophon">{E.CREDIT}</p>
</div>
<div class="uf-credit-row"><span class="uf-credit"><span class="uf-dot"></span><a class="uf-k" href="https://unicornfactory.dev/sites/">a lever in</a><a class="uf-wm" href="https://unicornfactory.dev/">The Unicorn Factory</a></span></div>
</footer>
<div class="ed-care" role="region" aria-label="Crisis support"><div class="wrap">
<span>If you are in crisis:</span>
<a href="tel:988">Call or text 988</a>
<a href="sms:741741?&amp;body=HOME">Text HOME to 741741</a>
<a href="{E.fm_url('10.9')}">Chapter 10.9, crisis and support</a>
</div></div>
{'<script src="/assets/tools.js"></script>' if 'data-tool=' in body else ''}
</body>
</html>
'''
    assert chr(0x2014) not in out, f'em-dash on {path}'
    dest = os.path.join(PUB, path.lstrip('/') + '.html')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w', encoding='utf-8').write(out)
    PAGES.append(path)

# ---------- shared pieces ----------
def rw_row(cid, door=None):
    return (f'<li class="ed-row ed-rw"><a href="{rw_href(cid, door)}"><span class="ed-ch-num">K-{cid}</span> '
            f'<span class="ed-row-t">{esc(RW[cid]["title"])}</span></a>'
            f'<span class="ed-row-m">Rewritten for this edition from Field Manual Ch {cid} · '
            f'<a class="ed-out" href="{E.fm_url(cid)}">the original</a></span></li>')

def fm_link(cid, door=None):
    """A Field Manual chapter the edition leans on: its Kindling rewrite where one exists, else the Library link and its note."""
    if cid in E.REWRITES:
        return rw_row(cid, door)
    title, note = E.FM[cid]
    return (f'<li class="ed-lean"><a class="ed-out" href="{E.fm_url(cid)}"><span class="ed-ch-num">{cid}</span> '
            f'<span class="ed-row-t">{esc(title)}</span></a>'
            f'<span class="ed-row-m">From the Field Manual, on solo.joshwolf.net</span>'
            f'<p class="ed-lean-note"><span class="eyebrow">For a Kindling reader</span> {inline(note, door)}</p></li>')

def k_row(kid, door):
    return (f'<li class="ed-row"><a href="{k_href(kid, door)}"><span class="ed-ch-num">{kid}</span> '
            f'<span class="ed-row-t">{esc(K[kid]["title"])}</span></a><span class="ed-row-m">Written for this edition</span></li>')

def read_row(cid, door):
    return k_row(cid, door) if cid.startswith('K.') else fm_link(cid, door)

def tool_row(key):
    t = E.TOOLS[key]
    return f'<li class="ed-row"><a href="{t["url"]}"><span class="ed-row-t">{esc(t["title"])}</span></a><span class="ed-row-m">Tool · works in your browser, stores nothing</span></li>'

# ---------- K chapter pages ----------
def chapter_order(door):
    seq = []
    for a in E.DOORS[door]['articles']:
        if a.get('k'):
            seq.append(('k', a['k']))
        elif a.get('tool'):
            seq.append(('tool', a['tool']))
    return seq

def chapter_nav(door, kid):
    seq = [x for x in chapter_order(door) if x[0] == 'k']
    ids = [x[1] for x in seq]
    i = ids.index(kid)
    parts = []
    if i:
        parts.append(f'<a class="k-btn k-btn-secondary" href="{k_href(ids[i - 1], door)}" rel="prev">Before: {ids[i - 1]} {esc(K[ids[i - 1]]["title"])}</a>')
    parts.append(f'<a class="k-btn k-btn-quiet" href="/{door}">The {"builder" if door == "builders" else "curator"}’s charter</a>')
    if i + 1 < len(ids):
        parts.append(f'<a class="k-btn k-btn-secondary" href="{k_href(ids[i + 1], door)}" rel="next">Next: {ids[i + 1]} {esc(K[ids[i + 1]]["title"])}</a>')
    return '<nav class="ed-chnav" aria-label="Chapters on this path">' + ''.join(parts) + '</nav>'

def k_page(kid, door):
    k = K[kid]
    d = E.DOORS[door]
    art = next(i for i, a in enumerate(d['articles'], 1) if a.get('k') == kid)
    leans = next(a.get('leans', []) for a in d['articles'] if a.get('k') == kid)
    h = render(k['md'])
    h = re.sub(r'<h3>(.*?)</h3>', lambda m: f'<h2 id="{heading_id(kid, re.sub("<[^>]+>", "", m.group(1)))}">{m.group(1)}</h2>', h)
    h = re.sub(r'<h4>(.*?)</h4>', lambda m: f'<h3>{m.group(1)}</h3>', h)
    h = stamp_tables(h)
    h = link_sections(h)
    h = link_chapters(h, door)
    if d['dress'] == 'c1':
        h = mark_keywords(h)
    lean_html = ''
    if leans:
        lean_html = (f'<section class="ed-leans" aria-labelledby="leans-t"><h2 id="leans-t">Where this chapter leans on the Field Manual</h2>'
                     f'<p class="ed-small">{E.LIBRARY_LINE}</p><ul class="ed-rows">{"".join(fm_link(c, door) for c in leans)}</ul></section>')
    body = f'''<article class="ed-chapter" data-chapter="{kid}">
<div class="wrap ed-measure">
<p class="eyebrow">{d["short"]} · Article {ROMAN[art - 1]} · Written for this edition</p>
<h1 class="ed-ch-title"><span class="ed-ch-num">{kid}</span> {esc(k["title"])}</h1>
<p class="chips">{chip("Spec " + E.SPEC_VERSION + " · Stable")}{chip("Examples invented and labeled")}</p>
<div class="ed-text">
{h}
</div>
{lean_html}
{chapter_nav(door, kid)}
</div>
</article>'''
    page(f'/{door}/{k["slug"]}', f'{kid} {k["title"]} · Kindling edition', body, dress=d['dress'], current=door)

# ---------- rewrite pages ----------
def rw_article(cid, door):
    for i, a in enumerate(E.DOORS[door]['articles'], 1):
        if cid in a.get('leans', []):
            return i, a
    raise KeyError((cid, door))

def rw_page(cid, door):
    r = RW[cid]
    d = E.DOORS[door]
    art, a = rw_article(cid, door)
    parent = r['parent'].get(door)
    h = render(r['md'])
    h = re.sub(r'<h3>(.*?)</h3>', lambda m: f'<h2 id="{heading_id("K-" + cid, re.sub("<[^>]+>", "", m.group(1)))}">{m.group(1)}</h2>', h)
    h = re.sub(r'<h4>(.*?)</h4>', lambda m: f'<h3>{m.group(1)}</h3>', h)
    h = stamp_tables(h)
    h = link_sections(h)
    h = link_chapters(h, door, self_src=cid)
    if d['dress'] == 'c1':
        h = mark_keywords(h)
    h = h.replace('(verify)', '<span class="ed-verify">(verify)</span>')
    # the provenance and license line after the rule: the original is reachable from here (xrefs.md, item 1)
    h, n = re.subn(r'<hr\s*/?>\s*<p>(Rewritten for the Kindling edition.*?)</p>',
                   lambda m: '<hr><p class="ed-provenance">' + m.group(1).replace(
                       'The full chapter is on solo.joshwolf.net.',
                       f'The full chapter is on <a class="ed-out" href="{E.fm_url(cid)}">solo.joshwolf.net</a>.') + '</p>', h, flags=re.S)
    assert n == 1, f'K-{cid}: provenance line not found'
    nav = []
    if parent:
        nav.append(f'<a class="k-btn k-btn-secondary" href="{k_href(parent, door)}">Back to {parent} {esc(K[parent]["title"])}</a>')
    nav.append(f'<a class="k-btn k-btn-quiet" href="/{door}">The {"builder" if door == "builders" else "curator"}\u2019s charter</a>')
    nav.append(f'<a class="k-btn k-btn-quiet ed-out" href="{E.fm_url(cid)}">Ch {cid}, the original, on solo.joshwolf.net</a>')
    with_k = f', with {parent}' if parent else ''
    body = f'''<article class="ed-chapter" data-chapter="K-{cid}">
<div class="wrap ed-measure">
<p class="eyebrow">{d["short"]} · Article {ROMAN[art - 1]}{with_k} · Rewritten from Field Manual Ch {cid}</p>
<h1 class="ed-ch-title"><span class="ed-ch-num">K-{cid}</span> {esc(r["title"])}</h1>
<p class="chips">{chip("Spec " + E.SPEC_VERSION + " · Stable")}{chip("Examples invented and labeled")}</p>
<div class="ed-text">
{h}
</div>
<nav class="ed-chnav" aria-label="From this chapter">{"".join(nav)}</nav>
</div>
</article>'''
    page(f'/{door}/{E.rw_slug(cid)}', f'K-{cid} {r["title"]} · Kindling edition', body, dress=d['dress'], current=door)

# ---------- charter pages (with Tool 1, the chooser) ----------
def chooser_builder():
    opts = ''.join(f'<label class="ed-opt"><input type="radio" name="cls" value="{c["key"]}" autocomplete="off"> {esc(c["label"])}</label>' for c in E.BUILDER_CHOICES)
    panels = ''
    for c in E.BUILDER_CHOICES:
        secs = ''.join(f'<li>{inline(s)}: “{mark_keywords(inline(q))}”</li>' for s, q in c['sections'])
        reads = ''.join(read_row(x, 'builders') for x in c['read'])
        aside = f'<p class="ed-small">{inline(c["aside"], "builders")}</p>' if c.get('aside') else ''
        panels += (f'<div class="ed-panel" data-for="{c["key"]}" hidden><h3>The sections that bind it</h3><ul class="ed-musts">{secs}</ul>{aside}'
                   f'<h3>Read, in this order</h3><ul class="ed-rows">{reads}</ul></div>')
    return f'''<section class="ed-chooser" data-tool="chooser" aria-labelledby="choose-t">
<h2 id="choose-t">What are you building?</h2>
<p class="ed-small">Pick one. The page shows the sections that bind it, each MUST quoted, and what to read. Nothing is stored, and coming back to this page starts from nothing chosen.</p>
<fieldset class="ed-opts"><legend class="vh">Conformance class, {inline("§11")}</legend>{opts}</fieldset>
{panels}
</section>'''

def chooser_curator():
    opts = ''.join(f'<label class="ed-opt"><input type="radio" name="cm" value="{c["key"]}" autocomplete="off"> {c["label"]}</label>' for c in E.CURATOR_CHOICES)
    reads = ''.join(read_row(x, 'curators') for x in E.CURATOR_READING)
    head = '<thead><tr><th>Model</th><th>What it adds before the handshake</th><th>When it fits</th><th>What it can never remove</th></tr></thead>'
    def row(c):
        return f'<tr><th scope="row">{c["label"]}</th><td>{esc(c["adds"])}</td><td>{esc(c["fits"])}</td><td>The owner’s yes, and the right to leave</td></tr>'
    real = [c for c in E.CURATOR_CHOICES if c['adds']]
    panels = ''
    for c in E.CURATOR_CHOICES:
        rows = ''.join(row(x) for x in (real if c['key'] == 'unsure' else [c]))
        extra = ('<p class="ed-small">K.4 asks six questions of a charter, and the fourth is “How do people come in? Name the consent model in words.” '
                 'Write the charter first and the model usually follows.</p>') if c['key'] == 'unsure' else ''
        panels += (f'<div class="ed-panel" data-for="{c["key"]}" hidden><h3>From K.4’s table</h3>'
                   f'<div class="ed-table"><table>{head}<tbody>{rows}</tbody></table></div>{extra}'
                   f'<p>The floor never moves. Stricter Pools “{inline(E.CURATOR_FLOOR)}” ({inline("§5.4")}) '
                   f'K.4 sets out <a href="/curators/k4#{heading_id("K.4", "The rules you enforce")}">the rules you enforce</a>, each with its section.</p>'
                   f'<h3>Read, in this order</h3><ul class="ed-rows">{reads}</ul></div>')
    return f'''<section class="ed-chooser" data-tool="chooser" aria-labelledby="choose-t">
<h2 id="choose-t">How will people come in?</h2>
<p class="ed-small">Pick the consent model your manifest will name (§3.2, §5.4). Nothing is stored, and coming back to this page starts from nothing chosen.</p>
<fieldset class="ed-opts"><legend class="vh">Consent model</legend>{opts}</fieldset>
{panels}
</section>'''

def charter_page(door):
    d = E.DOORS[door]
    arts = ''
    for i, a in enumerate(d['articles'], 1):
        rows = ''
        if a.get('k'):
            rows += k_row(a['k'], door)
        if a.get('tool'):
            rows += tool_row(a['tool'])
        for c in a.get('leans', []):
            rows += fm_link(c, door)
        note = f'<p class="ed-small">{a["note"]}</p>' if a.get('note') else ''
        arts += f'''<section class="ed-art" id="art-{i}" aria-labelledby="art-{i}-t">
<p class="ed-art-n">Art. {ROMAN[i - 1]}</p>
<div><h2 id="art-{i}-t">{esc(a["title"])}</h2><p class="ed-binds">{inline(a["binds"], door)}</p>{note}<ul class="ed-rows">{rows}</ul></div>
</section>'''
    body = f'''<section class="hm-hero ed-charter-hero"><div class="wrap">
<p class="eyebrow">The {"builder" if door == "builders" else "curator"}’s charter · in {"the protocol site’s" if d["dress"] == "c1" else "the Charter’s"} dress</p>
<h1>{d["h1"]}</h1>
<p class="chips">{chip("Planned · shown with invented examples", planned=True)}</p>
<dl class="ed-charter-dl">
<div><dt>What it’s for</dt><dd>{inline(d["for"])}</dd></div>
<div><dt>What it’s not for</dt><dd>{inline(d["not_for"])}</dd></div>
</dl>
</div></section>
<div class="wrap ed-measure-wide">
{link_sections(chooser_builder() if door == "builders" else chooser_curator())}
<h2 class="ed-arts-t">The articles</h2>
<p class="ed-small">Everything in this edition is open. {E.LIBRARY_LINE}</p>
{arts}
</div>'''
    page(f'/{door}', f'{d["name"]} · Kindling edition', body, dress=d['dress'], current=door)

# ---------- build ----------
def main():
    for sub in ('builders', 'curators', 'tools'):
        p = os.path.join(PUB, sub)
        if os.path.isdir(p):
            shutil.rmtree(p)
    for f in os.listdir(PUB):
        if f.endswith('.html'):
            os.remove(os.path.join(PUB, f))
    for door in E.DOORS:
        charter_page(door)
    for kid, meta in E.K_CHAPTERS.items():
        for door in meta['doors']:
            k_page(kid, door)
    for cid, meta in E.REWRITES.items():
        for door in meta['doors']:
            rw_page(cid, door)
    import pages
    pages.build(page, inline, chip, k_href, fm_link, K)
    json.dump({'pages': sorted(PAGES)}, open(os.path.join(ROOT, 'build', 'site_manifest.json'), 'w'), indent=1)
    print('pages', len(PAGES))

if __name__ == '__main__':
    main()

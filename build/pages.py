"""The edition's own pages: the two doors, the tools, and the handshake pages."""
import html, json
import edition as E

CARE = E.fm_url('10.9')

def esc(s):
    return html.escape(s, quote=True)

def build(page, inline, chip, k_href, fm_link, K):
    doors(page, inline, chip)
    tools_index(page, inline)
    quick_start(page, inline, chip)
    hollis(page, inline, chip)
    money_lines(page, inline, chip)
    manifest(page, inline, chip)
    not_found(page)

# ---------- the first screen ----------
def doors(page, inline, chip):
    b, c = E.DOORS['builders'], E.DOORS['curators']
    body = f'''<section class="hm-hero" aria-labelledby="top-t"><div class="wrap">
<h1 id="top-t">The manual should belong to <em>the people building on it.</em></h1>
<p class="hm-sub ed-hero-lede">Two readers, one specification. Pick the door; every chapter links the section that binds it.</p>
<p class="ed-status">{chip("Stable")}<span>Specification {E.SPEC_VERSION}, dated {E.SPEC_DATE}.</span>{chip("Nothing yet", planned=True)}<span>Nothing runs on Kindling at TranquilTech yet.</span></p>
</div></section>
<section class="ed-doors" aria-labelledby="doors-t"><div class="wrap">
<h2 class="vh" id="doors-t">Two doors</h2>
<ul class="ed-door-list">
<li class="ed-door ed-c1" id="builders">
<p class="eyebrow">Door one · in the protocol site’s dress</p>
<h2>{b["name"]}</h2>
<p class="chips">{chip("Planned · shown with invented examples", planned=True)}</p>
<dl><div><dt>What it’s for</dt><dd>{inline(b["for"])}</dd></div><div><dt>What it’s not for</dt><dd>{inline(b["not_for"])}</dd></div></dl>
<p class="ed-opens">Article I is K.1, the protocol as a reader meets it. Article II is K.2, licensing and governance. Then the quick start, the manifest walkthrough and Try it as Hollis.</p>
<p class="ed-go"><a class="k-btn k-btn-secondary" href="/builders">Open the builder’s charter</a></p>
</li>
<li class="ed-door" id="curators">
<p class="eyebrow">Door two · in the Charter’s dress</p>
<h2>{c["name"]}</h2>
<p class="chips">{chip("Planned · shown with invented examples", planned=True)}</p>
<dl><div><dt>What it’s for</dt><dd>{inline(c["for"])}</dd></div><div><dt>What it’s not for</dt><dd>{inline(c["not_for"])}</dd></div></dl>
<p class="ed-opens">Article I is K.4, curation as a craft. Article II is K.3, money beside the introduction. Then Try it as Hollis, the Money lines and the manifest walkthrough.</p>
<p class="ed-go"><a class="k-btn k-btn-primary" href="/curators">Open the curator’s charter</a></p>
</li>
</ul>
<p class="ed-under">A door is a link. Choosing one stores nothing, and everything behind both doors is open. Where a chapter leans on the Field Manual, the edition carries a Kindling rewrite of that chapter, numbered K- after its source, and the original stays on solo.joshwolf.net. Both doors end with Chapter 10.4, and <a href="{CARE}">Chapter 10.9, crisis and support,</a> is open to everyone.</p>
</div></section>'''
    page('/index', 'Kindling · The Field Manual edition', body, current='doors',
         desc='The Solo Operator’s Field Manual for two readers of one specification: people building on the Kindling protocol and people keeping Pools on it. Every protocol claim carries its section number.')

# ---------- tools ----------
def tools_index(page, inline):
    items = [
        ('/tools/quick-start', 'The quick start', 'Clone, validate a Pool, parse a profile, ask a Pool a question. Verbatim from the protocol site, with the warning it leaves out.', 'For builders'),
        ('/tools/hollis', 'Try it as Hollis', 'The consent handshake as the owner of a page meets it, on kindling.foundation. The pattern every Pool builds to (\u00a75.2).', 'Both doors'),
        ('/tools/money-lines', 'The Money lines', 'What pays for a Kindling business and what never does, from the library\u2019s invented organizations, with the chapter that prices each.', 'For curators'),
    ]
    more = [
        ('/tools/manifest', 'The Pool manifest walkthrough', 'Write a manifest one field at a time and see what each field promises (\u00a73.2, \u00a73.3).'),
        ('/builders#choose-t', 'The builder\u2019s chooser', 'Pick a conformance class (\u00a711) and see the sections that bind it.'),
        ('/curators#choose-t', 'The curator\u2019s chooser', 'Pick a consent model (\u00a73.2, \u00a75.4) and see what it can never remove.'),
    ]
    cards = ''.join(f'<li class="ed-door"><p class="eyebrow">{who}</p><h2><a href="{u}">{t}</a></h2><p>{inline(d)}</p></li>' for u, t, d, who in items)
    rest = ''.join(f'<li class="ed-row"><a href="{u}"><span class="ed-row-t">{t}</span></a><span class="ed-row-m">{inline(d)}</span></li>' for u, t, d in more)
    body = f'''<section class="hm-hero"><div class="wrap">
<p class="eyebrow">Tools</p>
<h1>Three tools, <em>and nothing stored.</em></h1>
<p class="hm-sub">Every tool here works in your browser. Nothing you type is sent anywhere, and no tool keeps a score.</p>
</div></section>
<div class="wrap ed-measure-wide">
<ul class="ed-door-list ed-three">{cards}</ul>
<h2 class="ed-arts-t">Also on the two paths</h2>
<ul class="ed-rows">{rest}</ul>
</div>'''
    page('/tools/index', 'Tools \u00b7 Kindling edition', body, current='tools')

QS_STEPS = [
    ('Clone and install', 'You need git, Node.js and npm.', '$ git clone https://github.com/IntelliBotique/kindling.git\n$ cd kindling\n$ npm install'),
    ('Validate a Pool manifest', '<code>kindling-validate</code> checks a Kindling document against its schema.', '$ npx kindling-validate https://example.com/pools/queer-creatives-la'),
    ('Parse a profile URL', '<code>kindling-parse</code> turns a profile page into a structured <code>parsed_profile</code> JSON document.', '$ npx kindling-parse https://noor.example.com'),
    ('Run the starter discovery agent', '<code>kindling-discover</code> asks one or more Pools a question in natural language. Only people who said yes to a Pool are in it to be asked.', '$ npx kindling-discover \\\n  --pool https://example.com/pools/queer-creatives-la \\\n  --query "who is up for a hike this weekend?"'),
    ('Deploy the registry to your own infrastructure', 'See <code>registry/README.md</code> in the repository. It is designed to run on a single VPS or a small container. A registry is one consumer of the well-known file, and anyone may run one (§8.5).', '# see registry/README.md in the repository\n# designed to run on a single VPS or a small container'),
]

def quick_start(page, inline, chip):
    steps = ''
    for i, (t, d, cmd) in enumerate(QS_STEPS, 1):
        steps += f'''<li class="ed-step"><p class="ed-step-n">Step {i} of 5</p><h2>{t}</h2><p>{inline(d)}</p><pre class="ed-pre"><code>{esc(cmd)}</code></pre></li>'''
    body = f'''<section class="hm-hero"><div class="wrap ed-measure">
<p class="eyebrow">Tool · for builders · KINDLING(7)</p>
<h1>The quick start, <em>inside a clone.</em></h1>
<p class="hm-sub">Five steps from a clone to a question, as the protocol site’s “Build on it” gives them, read on {E.RESEARCH_DATE}. The site says “If it takes longer, that is a bug.”</p>
</div></section>
<div class="wrap ed-measure">
<aside class="ed-warn" role="note">
<p class="eyebrow">Before step 2</p>
<p><b>Run every <code>npx</code> command inside the cloned folder, after <code>npm install</code>.</b> Nothing from this project is on npm. Outside the clone, <code>npx kindling-validate</code> returned a 404 from npm on {E.RESEARCH_DATE}.</p>
<p><b>The npm name “kindling” belongs to someone else.</b> It is an unrelated project (“Project bootstrapping with an emphasis on simplicity,” version 1.1.0). <code>npm install kindling</code> will not install this protocol’s tools.</p>
<p>The README still points at <code>kindling.tranquiltech.com</code>. The live sites are kindling.foundation and protocol.kindling.foundation. K.1 lists <a href="/builders/k1#k1-before-you-clone-5-things-the-repository-gets-wrong-today">five things the repository gets wrong today</a>.</p>
</aside>
<ol class="ed-steps">{steps}</ol>
<p class="ed-small">The commands and their descriptions are the protocol site’s, from protocol.kindling.foundation/build.html, read {E.RESEARCH_DATE}. The example hosts are the site’s own <code>.example</code> addresses, and Noor is the site’s invented example person. Write your own manifest with <a href="/tools/manifest">the manifest walkthrough</a>.</p>
</div>'''
    page('/tools/quick-start', 'The quick start · Kindling edition', body, dress='c1', current='tools')

def hollis(page, inline, chip):
    body = f'''<section class="hm-hero"><div class="wrap ed-measure">
<p class="eyebrow">Tool · both doors · §5.2</p>
<h1>Try it <em>as Hollis.</em></h1>
<p class="hm-sub">The consent handshake, clickable, on kindling.foundation. Hollis Grant is invented. Nothing is sent anywhere.</p>
<p class="chips">{chip("Invented")}{chip("Spec " + E.SPEC_VERSION + " · Stable")}</p>
<p class="ed-go"><a class="k-btn k-btn-primary" href="https://kindling.foundation/intro.html">Open the handshake as Hollis</a></p>
</div></section>
<div class="wrap ed-measure">
<h2>What to look for</h2>
<p>Nobody enters a Pool without saying yes. §5.1: “A Profile MUST NOT be added to a Pool without the owner’s explicit consent. Silent inclusion is forbidden. There is no exception.”</p>
<ol class="ed-look">
<li><b>The confirmation step.</b> “Each link MUST open a confirmation step that shows the Pool’s name, charter, curator and visibility and asks the owner to confirm.” (§5.2) The page Hollis sees shows all four, numbered.</li>
<li><b>Only the button counts.</b> “Only an explicit action on that step, such as a button that sends a POST request, records a decision. A GET request to either link alone MUST NOT record a decision.” (§5.2) The reason takes one line: “email security scanners open every link in a message.”</li>
<li><b>A no is remembered.</b> A decline “MUST be recorded as declined for that Pool and MUST NOT be re-submitted by the same Curator without owner permission.” (§5.2) Press “Ask again” after a no and watch it be refused.</li>
<li><b>Silence expires.</b> “A request’s <code>expires_at</code> MUST equal its <code>sent_at</code> plus the window,” and the window is literally 14 days unless the manifest sets <code>handshake_window_days</code> (§5.2). Press “Let the window pass.”</li>
<li><b>The log.</b> Every step shows the exact JSON message the protocol would send. Check each against <code>schemas/handshake_message.schema.json</code>.</li>
</ol>
<p class="ed-small">Builders: K.1 maps <a href="/builders/k1#k1-the-handshake-and-the-6-message-types">the handshake and the 6 message types</a>. Curators: K.4 lists <a href="/curators/k4#k4-the-rules-you-enforce">the rules you enforce</a>, and its Field exercise 3 runs an invented profile through the whole handshake.</p>
</div>'''
    page('/tools/hollis', 'Try it as Hollis · Kindling edition', body, current='tools')

def money_lines(page, inline, chip):
    rows = ''
    for r in E.MONEY_LINES:
        cats = [r['cat']] + ([r['also']] if r.get('also') else [])
        chapters = sorted({c for k in cats for c in E.MONEY_CATS[k][1]})
        ch_links = ', '.join((f'<a href="/{E.REWRITES[c]["doors"][0]}/{E.rw_slug(c)}">K-{c}</a>' if c in E.REWRITES
                              else f'<a class="ed-out" href="{E.fm_url(c)}">Ch {c}</a>') for c in chapters)
        if 'thanks' in cats:
            ch_links = (ch_links + '; ' if ch_links else '') + f'thanks: none, see <a href="/curators/k3">K.3</a> and {inline("§1.3")}. Status: Draft (v0.2), {E.RESEARCH_DATE}'
        tag = chip('Real app · Kindling version early 2027') if r.get('real') else chip('Invented')
        srcs = ' '.join(f'<a href="{u}">{esc(u.replace("https://", ""))}</a>' for u in r['src'])
        never = f'<td class="ed-never">{r["never"]}</td>' if r['never'] else '<td class="ed-never">Not stated on the page</td>'
        rows += (f'<tr data-cats="{" ".join(cats)}" data-chapters="{" ".join(chapters)}">'
                 f'<th scope="row">{esc(r["org"])} {tag}</th><td>{esc(r["kind"])}</td><td>{r["pays"]}</td>{never}'
                 f'<td class="ed-src">{srcs}<br>checked {E.RESEARCH_DATE}</td><td>{ch_links or "None"}</td></tr>')
    cat_btns = ''.join(f'<button type="button" class="fchip" data-cat="{k}" aria-pressed="false">{esc(v[0])}</button>' for k, v in E.MONEY_CATS.items())
    ch_opts = ''.join(f'<option value="{c}">{("K-" if c in E.REWRITES else "Ch ") + c}</option>' for c in sorted({c for v in E.MONEY_CATS.values() for c in v[1]}))
    body = f'''<section class="hm-hero"><div class="wrap">
<p class="eyebrow">Tool · for curators and founders · §1.3</p>
<h1>What pays, and <em>what never does.</em></h1>
<p class="hm-sub">The Kindling library’s Money lines in one table, with the chapter that prices the thing that pays. It is not a directory of real businesses; none exists yet.</p>
</div></section>
<div class="wrap" data-tool="money">
<div class="ed-filters" role="group" aria-label="Filter the Money lines">
<p class="ed-small">What pays:</p>
<div class="chips">{cat_btns}</div>
<label class="ed-small">Chapter <select data-ch><option value="">Any chapter</option>{ch_opts}</select></label>
<label class="ed-small ed-toggle"><input type="checkbox" data-never checked> Show what never pays</label>
<button type="button" class="k-btn k-btn-quiet" data-clear>Show every row</button>
</div>
<div class="ed-table ed-money"><table>
<thead><tr><th>Organization</th><th>Kind</th><th>What pays</th><th class="ed-never">What never pays</th><th>Source page</th><th>Chapter that prices it</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="ed-small" data-empty hidden>No row fits these filters. <button type="button" class="k-btn k-btn-quiet" data-clear>Show every row</button></p>
</div>
<div class="wrap"><p class="ed-money-foot" role="note">{inline(E.MONEY_FOOTER)}</p>
<p class="ed-small">Quotations are from the Kindling sites, quoted in K.3 and checked against each source page on {E.RESEARCH_DATE}. The rows are in K.3’s order and are not sorted by size, popularity or revenue. Read <a href="/curators/k3">K.3</a> for the three questions to ask of any price.</p></div>'''
    page('/tools/money-lines', 'The Money lines · Kindling edition', body, current='tools')

MANIFEST_FIELDS = [
    ('schema_version', 'Filled in', '§12.1', 'fixed', '"0.1"'),
    ('name', 'Name the Pool.', '§3.2', 'text', 'A plain name a member would say aloud'),
    ('curator', 'Who curates it, and how are you verified?', '§3.2, §4.5', 'curator', 'One entry with identity, display_name, verification_level (email or oauth), primary: true'),
    ('intent_tags', 'What is it for, in tags?', '§3.2', 'tags', '2 to 5 short tags'),
    ('visibility', 'Who can see the list?', '§3.2', 'visibility', ''),
    ('consent_model', 'How do people come in?', '§3.2, §5.4', 'consent', ''),
    ('curator_contact', 'Where does someone write to be removed?', '§3.2', 'text', 'An address you read'),
    ('charter', 'What is it for, and what is it not for?', '§3.2', 'charter', 'At least 20 characters'),
    ('entries', 'Shown empty', '§3.4', 'fixed', '[]'),
    ('handshake_window_days', 'Optional', '§5.2', 'int', 'Leave unset for the literal default of 14'),
    ('geographic_scope', 'Optional', '§3.3', 'geo', 'City, region, country, or online'),
    ('block_list_subscriptions', 'Optional', '§3.3, §7.3', 'urls', 'URLs of lists you have read'),
]
VIS_NOTES = {
    'public': 'Does not make anyone’s page more public than it already is (K.4).',
    'unlisted': 'It is not secret. RFC 0002: “An `unlisted` Pool isn’t secret: its URL is just not in the public registry.”',
    'invite-only': 'Auto-accept never applies (§5.5).',
}
CONSENT_NOTES = {
    'universal-opt-in': 'Adds nothing before the handshake; literally the default value in the schema.',
    'vouching-required': 'Adds a vouch from someone the curator trusts. The floor of §5.4 still holds.',
    'curator-only-adds': 'Only the curator may submit. The floor of §5.4 still holds.',
}
INVENTED_EXAMPLE = {
    'schema_version': '0.1',
    'name': 'Night Shift Neighbors (invented)',
    'curator': [{'identity': 'curator@night-shift-neighbors.example', 'display_name': 'The curator (invented)', 'verification_level': 'email', 'primary': True}],
    'intent_tags': ['friendship', 'night-shift', 'neighbors'],
    'visibility': 'unlisted',
    'consent_model': 'universal-opt-in',
    'curator_contact': 'curator@night-shift-neighbors.example',
    'charter': 'For people in and around an invented town who work nights and would like company at hours when most places are closed: a walk at 7 a.m., breakfast after a shift, someone to text on a long night. Not for dating, recruiting, selling or promotion. The curator asks each person by email before listing them; nobody is added without a yes. Leave any time from any message. The list is never sold, shared outside this Pool, or ranked.',
    'entries': [],
}

def manifest(page, inline, chip):
    rows = ''
    for key, prompt, sec, kind, hint in MANIFEST_FIELDS:
        fid = 'mf-' + key
        lab = f'<label for="{fid}"><code>{key}</code> <span class="ed-small">{inline(sec)}</span></label><p class="ed-prompt">{esc(prompt)}</p>'
        if kind == 'fixed':
            ctl = f'<output id="{fid}" class="ed-fixed">{esc(hint)}</output>'
            if key == 'entries':
                ctl += '<p class="ed-small">Entries stay empty until someone accepts (§5.1, §3.4).</p>'
        elif kind == 'text':
            ctl = f'<input id="{fid}" data-f="{key}" type="text" autocomplete="off" placeholder="{esc(hint)}">'
        elif kind == 'curator':
            ctl = (f'<input id="{fid}" data-f="curator.identity" type="text" autocomplete="off" placeholder="identity">'
                   f'<input data-f="curator.display_name" type="text" autocomplete="off" placeholder="display_name" aria-label="Curator display name">'
                   f'<select data-f="curator.verification_level" aria-label="Verification level"><option>email</option><option>oauth</option></select>'
                   f'<p class="ed-small">The level is shown to every owner (§4.5). <code>cryptographic</code> is reserved for v0.2.</p>')
        elif kind == 'tags':
            ctl = f'<input id="{fid}" data-f="intent_tags" type="text" autocomplete="off" placeholder="friendship, night-shift"><p class="ed-small">{esc(hint)}, separated by commas.</p>'
        elif kind == 'visibility':
            ctl = f'<select id="{fid}" data-f="visibility">' + ''.join(f'<option>{v}</option>' for v in VIS_NOTES) + '</select>' + \
                  ''.join(f'<p class="ed-small" data-note-for="visibility" data-v="{v}" hidden>{inline(n)}</p>' for v, n in VIS_NOTES.items())
        elif kind == 'consent':
            ctl = f'<select id="{fid}" data-f="consent_model">' + ''.join(f'<option>{v}</option>' for v in CONSENT_NOTES) + '</select>' + \
                  ''.join(f'<p class="ed-small" data-note-for="consent_model" data-v="{v}" hidden>{inline(n)}</p>' for v, n in CONSENT_NOTES.items()) + \
                  f'<p class="ed-small">Under every model: stricter Pools “{inline(E.CURATOR_FLOOR)}” ({inline("§5.4")})</p>'
        elif kind == 'charter':
            ctl = (f'<textarea id="{fid}" data-f="charter" rows="6" autocomplete="off"></textarea>'
                   '<p class="ed-small">K.4’s six questions: Who is it for? What is it for? What is it not for? How do people come in? '
                   'How does someone leave? What do you do with the list, and what do you never do with it? At least 20 characters.</p>')
        elif kind == 'int':
            ctl = f'<input id="{fid}" data-f="handshake_window_days" type="number" min="1" step="1" autocomplete="off" placeholder="14"><p class="ed-small">{esc(hint)}.</p>'
        elif kind == 'geo':
            ctl = (f'<input id="{fid}" data-f="geographic_scope.city" type="text" autocomplete="off" placeholder="city">'
                   '<input data-f="geographic_scope.region" type="text" autocomplete="off" placeholder="region" aria-label="Region">'
                   '<input data-f="geographic_scope.country" type="text" autocomplete="off" placeholder="country" aria-label="Country">'
                   '<label class="ed-small ed-toggle"><input data-f="geographic_scope.online" type="checkbox"> Online</label>')
        else:
            ctl = f'<textarea id="{fid}" data-f="messaging_preferences.block_list_subscriptions" rows="2" autocomplete="off" placeholder="https://protocol.kindling.foundation/blocklist.json"></textarea><p class="ed-small">One URL per line. Read each list first (K.4): the project’s own says its entries are illustrative until the registry opens.</p>'
        rows += f'<div class="ed-field" data-key="{key}">{lab}{ctl}</div>'
    body = f'''<section class="hm-hero"><div class="wrap">
<p class="eyebrow">Tool · both doors · §3.2</p>
<h1>A Pool is a file <em>before it is anything else.</em></h1>
<p class="hm-sub">Write a manifest one field at a time. The tool does not host a Pool, send a handshake, or add anyone to anything, and nothing you type leaves this page.</p>
</div></section>
<div class="wrap ed-manifest" data-tool="manifest">
<form class="ed-mf-form" autocomplete="off" onsubmit="return false">
<div class="ed-mf-bar"><p class="chips">{chip("Invented example")}</p>
<button type="button" class="k-btn k-btn-quiet" data-reset>Reset to the invented example</button>
<button type="button" class="k-btn k-btn-quiet" data-empty>Start empty</button></div>
{rows}
</form>
<div class="ed-mf-out">
<p class="eyebrow">The manifest · validates against <code>schemas/pool_manifest.schema.json</code></p>
<p class="ed-small" data-check role="status"></p>
<pre class="ed-pre"><code data-json></code></pre>
<p><button type="button" class="k-btn k-btn-secondary" data-download>Save as my-pool.json</button></p>
<aside class="ed-warn" role="note"><p>Run this inside a clone of the repository. Nothing from this project is on npm.</p>
<pre class="ed-pre"><code>npx kindling-validate ./my-pool.json</code></pre>
<p class="ed-small">The <a href="/tools/quick-start">quick start</a> has the clone. The tool checks the required fields and their shapes as the schema states them; the validator is the authority.</p></aside>
</div>
</div>
<script type="application/json" id="mf-example">{json.dumps(INVENTED_EXAMPLE)}</script>'''
    page('/tools/manifest', 'The Pool manifest walkthrough · Kindling edition', body, current='tools')

def not_found(page):
    body = f'''<section class="hm-hero"><div class="wrap ed-measure">
<h1>Nothing is <em>at this address.</em></h1>
<p class="hm-sub"><a href="/">Back to the two doors.</a> <a href="{CARE}">Chapter 10.9, crisis and support,</a> is open to everyone.</p>
</div></section>'''
    page('/404', 'Not found · Kindling edition', body)

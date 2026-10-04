"""What the Kindling edition carries: K.1 to K.4, the three tools, and the two charters that order them.

The edition carries no Field Manual chapters. Where a K chapter leans on one, the edition links to it on
solo.joshwolf.net and puts a Kindling note beside the link, written from the pointers list in
content/brief/xrefs.md. Every protocol claim carries its section number in spec v0.1.1. Every example is
labeled. No em-dashes anywhere.
"""

SPEC_VERSION = 'v0.1.1'
SPEC_DATE = '1 October 2026'
SPEC_URL = 'https://protocol.kindling.foundation/spec.html'
RESEARCH_DATE = 'October 4, 2026'
LIBRARY = 'https://solo.joshwolf.net'

def fm_url(cid):
    return LIBRARY + '/care' if cid == '10.9' else f'{LIBRARY}/read#ch-{cid}'

# The K chapters, and the doors that carry each one. K.2 is on both.
K_CHAPTERS = {
    'K.1': {'file': 'K1.md', 'slug': 'k1', 'doors': ['builders']},
    'K.2': {'file': 'K2.md', 'slug': 'k2', 'doors': ['builders', 'curators']},
    'K.3': {'file': 'K3.md', 'slug': 'k3', 'doors': ['curators']},
    'K.4': {'file': 'K4.md', 'slug': 'k4', 'doors': ['curators']},
}

TOOLS = {
    'quick-start': {'title': 'The quick start', 'url': '/tools/quick-start'},
    'hollis': {'title': 'Try it as Hollis', 'url': '/tools/hollis'},
    'money-lines': {'title': 'The Money lines', 'url': '/tools/money-lines'},
    'manifest': {'title': 'The Pool manifest walkthrough', 'url': '/tools/manifest'},
}

NON_GOAL_LINE = 'Kindling defines no chargeable surface between two people (§1.3, a stated non-goal).'

# Field Manual chapters the K chapters lean on: title (from the master), and the Kindling note beside the link.
# Notes for 3.5 to 8.5 and 10.4 come from the pointers list in xrefs.md; 5.3, 6.3 and 10.9 from its references list.
FM = {
    '3.5': ('Moats in the AI Era',
            'This chapter teaches the moat. ' + NON_GOAL_LINE + ' The project calls Pools a commons, and its Why page says: “When you can leave without losing anyone, streaks, paywalled likes and fake urgency lose their leverage.” See K.3.'),
    '3.6': ('Pricing Strategy',
            'On Kindling, the introduction has no price; price the thing beside it. See K.3. This chapter’s “Offer a lock-in” is a price lock on the thing sold, and it never applies to a Pool.'),
    '3.7': ('Outcome, Performance and Usage Pricing: The Mechanics',
            'Success fees and percentages are closed to anything an introduction produces. ' + NON_GOAL_LINE + ' Usage pricing fits a host’s own costs only. See K.3.'),
    '4.3': ('Contracts',
            'The terms-of-service section teaches clickwrap. A Kindling Pool’s consent record is the `consent_proof` of §3.4, set by a button that sends a POST on a confirmation page (§5.2). See K.4.'),
    '4.7': ('Privacy and AI Regulation',
            '§2.5 (no photo bytes), §2.7 (noindex) and §2.3 (recording what was inferred) are worked examples of this chapter’s principles. See K.1.'),
    '4.8': ('Risk: Insurance, Disputes and Lawyers',
            'K.4 has an invented risk register for a curator, on this chapter’s one-page form.'),
    '5.3': ('Invoicing, Payments and Collections',
            'For invoicing memberships, tickets and hosting. Kindling changes none of it, as long as no invoice line is for an introduction (K.3).'),
    '6.3': ('Grants and Non-Dilutive Money',
            'For grant-shaped and nonprofit Pools. The invented Midspan and The Board run on grants and public budgets (K.3).'),
    '7.1': ('Distribution Is the Scarce Asset',
            'For builders, the protocol’s distribution story is the registry and the well-known file (§8.3 to §8.5, §10). “Send the link and the registry lists it” had no live endpoint on October 4, 2026. See K.1.'),
    '8.5': ('Security and Reliability for a Tiny Company',
            'The v0.1.1 confirmation step is a clean case study: “email security scanners open every link in a message” (§5.2), so only a button that sends a POST records a decision. See K.1.'),
    '10.4': ('Loneliness and Identity',
             'Read it as it stands. This edition adds nothing to it.'),
    '10.9': ('Crisis and Support Directory',
             'The crisis and support directory, open to everyone without a link.'),
}

DOORS = {
    'builders': {
        'name': 'For builders of clients, hosts and tools',
        'short': 'For builders',
        'dress': 'c1',
        'h1': 'For builders of <em>clients, hosts and tools.</em>',
        'for': 'Building on Kindling: one of the four conformance classes in §11, or a registry, block list or agent that §11 does not name.',
        'not_for': 'A hosted consumer product, or a chargeable surface at the connection layer. §1.3 lists both as non-goals.',
        'articles': [
            {'title': 'The protocol as a reader meets it', 'k': 'K.1', 'binds': 'All twelve sections, read for what each asks of you.', 'leans': ['4.7', '8.5', '7.1']},
            {'title': 'Licensing and governance', 'k': 'K.2', 'binds': 'Code under Apache 2.0, specification text under CC BY 4.0, and how a section changes.'},
            {'title': 'What the protocol leaves out', 'binds': '§1.3 lists “a chargeable surface at the connection layer” among the non-goals, and K.1 shows which of the site’s ten lines rest on no MUST. The Field Manual’s moats chapter is the case the protocol answers.', 'leans': ['3.5'],
             'note': 'A builder who will sell something beside the protocol reads <a href="/curators/k3">K.3, money beside the introduction</a>.'},
            {'title': 'The quick start', 'tool': 'quick-start', 'binds': 'Clone, validate, parse, ask. Every command runs only inside the clone.'},
            {'title': 'The Pool manifest walkthrough', 'tool': 'manifest', 'binds': 'The 9 required fields of §3.2, one at a time.'},
            {'title': 'Try it as Hollis', 'tool': 'hollis', 'binds': 'The confirmation step of §5.2, as the owner of a page meets it.'},
            {'title': 'Before you go further', 'binds': 'Volume 10 of the Field Manual, on solo.joshwolf.net, with Chapter 10.4 first.', 'leans': ['10.4', '10.9']},
        ],
    },
    'curators': {
        'name': 'For curators and the organizations that keep Pools',
        'short': 'For curators',
        'dress': 'charter',
        'h1': 'For curators and the organizations that <em>keep Pools.</em>',
        'for': 'Keeping a Pool: writing its charter and choosing its consent model (§3.2), holding a consent proof for every entry (§3.4), and paying for the work with something sold beside the introduction.',
        'not_for': 'Adding anyone who has not said yes, which §5.1 forbids. Charging two people to meet, which §1.3 names as a non-goal.',
        'articles': [
            {'title': 'Curation as a craft', 'k': 'K.4', 'binds': '§3.2, §5.1 to §5.5, §7.3 and §9, read as what a curator does.', 'leans': ['4.3', '4.8', '4.7']},
            {'title': 'Money beside the introduction', 'k': 'K.3', 'binds': '§1.3 and Article VIII of the How page.', 'leans': ['3.6', '3.7', '5.3', '6.3']},
            {'title': 'Licensing and governance', 'k': 'K.2', 'binds': 'Who decides today, and how a section changes.'},
            {'title': 'Try it as Hollis', 'tool': 'hollis', 'binds': 'The confirmation step of §5.2 that every Pool builds to.'},
            {'title': 'The Money lines', 'tool': 'money-lines', 'binds': 'What pays and what never does, from the library’s invented organizations.'},
            {'title': 'The Pool manifest walkthrough', 'tool': 'manifest', 'binds': 'The 9 required fields of §3.2, one at a time.'},
            {'title': 'Before you go further', 'binds': 'Volume 10 of the Field Manual, on solo.joshwolf.net, with Chapter 10.4 first.', 'leans': ['10.4', '10.9']},
        ],
    },
}

LIBRARY_LINE = ('Field Manual chapters live on solo.joshwolf.net, the Library edition. Volume 1 and Chapter 10.9 are open there; '
                'the rest open free with an email. Each link here carries a note for a Kindling reader.')

# Tool 1, builder step 2: conformance class to the sections that bind it, MUSTs quoted from K.1.
BUILDER_CHOICES = [
    {'key': 'host', 'label': 'Pool host (§11.1)', 'sections': [
        ('§3.1', 'A Pool MUST be retrievable as a JSON document, either from a public Git repository or from a Pool API endpoint that returns the same shape.'),
        ('§5.1', 'A Profile MUST NOT be added to a Pool without the owner’s explicit consent.'),
        ('§5.3', 'Implementations MUST process withdrawal within 60 seconds of receipt.'),
        ('§9.1', 'the Pool MUST enter `dormant` status. Pool members MUST see a notice. The well-known file MUST reflect dormancy.'),
        ('§10.2', 'MUST list, for each discoverable Pool on the domain, its `manifest_url`, `visibility` and `status`'),
     ], 'read': ['K.1', 'K.2', '4.7', '8.5', '7.1']},
    {'key': 'ui', 'label': 'Pool UI (§11.2)', 'sections': [
        ('§4.5', 'a v1-conforming UI MUST render it alongside every Profile.'),
        ('§5.1', 'A Profile MUST NOT be added to a Pool without the owner’s explicit consent.'),
        ('§5.3', 'Implementations MUST process withdrawal within 60 seconds of receipt.'),
        ('§7', 'A v1-conforming implementation MUST support all three layers.'),
     ], 'read': ['K.1', 'K.2', '4.7', '8.5']},
    {'key': 'parser', 'label': 'Parser (§11.3)', 'sections': [
        ('§2.2', 'Parsers MUST read h-card fields where present and MUST NOT infer values that contradict explicit h-card markup.'),
        ('§2.3', 'Implementations MUST record which fields were h-card-derived and which were inferred.'),
        ('§2.5', 'Photos MUST be referenced by URL only. Kindling and Pools MUST NOT store photo bytes.'),
        ('§2.7', 'Compliant Pools and crawlers MUST NOT include such a Profile in any Pool, registry, or discovery surface.'),
     ], 'read': ['K.1', 'K.2', '4.7']},
    {'key': 'client', 'label': 'Messaging client (§11.4)', 'sections': [
        ('§6.2', 'MUST validate against `schemas/kindling_message.schema.json`'),
        ('§4.5', 'a v1-conforming UI MUST render it alongside every Profile.'),
        ('§7.1', 'Messages from unverified senders MUST be quarantined or rejected per the recipient’s per-profile preference.'),
     ], 'read': ['K.1', 'K.2', '8.5']},
    {'key': 'other', 'label': 'Something §11 does not name (registry, block list, agent)', 'sections': [
        ('§8.4', 'MUST NOT be the only way a Pool is discoverable'),
        ('§10.3', 'MUST respect `Cache-Control` headers'),
        ('§7.3', 'Implementations MUST be able to subscribe to one or more lists and filter accordingly.'),
        ('§5.1', 'A Profile MUST NOT be added to a Pool without the owner’s explicit consent.'),
     ], 'read': ['K.1', 'K.2', '7.1'], 'aside': 'Say “built on Kindling” for these; “Kindling-conformant” belongs to the 4 classes until a later version names more (K.1).'},
]

# Tool 1, curator step 2: consent model to K.4's row. The floor is §5.4.
CURATOR_CHOICES = [
    {'key': 'universal-opt-in', 'label': '<code>universal-opt-in</code>', 'adds': 'Nothing; literally the default value in the schema', 'fits': 'Open Pools where anyone with a page may be asked'},
    {'key': 'vouching-required', 'label': '<code>vouching-required</code>', 'adds': 'A vouch from someone the curator trusts', 'fits': 'Pools where trust is the point, such as the invented Drip Line’s belay check'},
    {'key': 'curator-only-adds', 'label': '<code>curator-only-adds</code>', 'adds': 'Only the curator may submit', 'fits': 'Small, invitation-shaped Pools; the project’s own Founding Curators Pool uses it'},
    {'key': 'unsure', 'label': 'Not sure yet', 'adds': None, 'fits': None},
]
CURATOR_FLOOR = 'MAY add pre-handshake steps but MUST NOT remove the owner’s ability to decline or withdraw.'
CURATOR_READING = ['K.4', 'K.3', '4.3', '4.8', '4.7']

# Tool 3: the Money lines, from K.3's table. Every organization but Mycelial is invented by the Kindling sites.
# 'quotes' are the exact strings checked on the source page on October 4, 2026, at kindling-sites 5afb487;
# test/test.mjs checks them again against a local clone. 'pays' and 'never' are K.3's cells as written.
MONEY_CATS = {
    'tickets': ('Classes, memberships, day passes, tickets', ['3.6', '5.3']),
    'services': ('Private services sold after an introduction, on request', ['3.6']),
    'grants': ('A grant, a public budget, donations, a nonprofit', ['6.3']),
    'hosting': ('Hosting, a shared desk, an organization paying for the service', ['3.6', '5.3']),
    'thanks': ('Thanks after an introduction worked', []),
}
Q = '“{}”'.format
MONEY_LINES = [
    {'org': 'Correo Lento', 'kind': 'Letter co-op', 'cat': 'tickets', 'quotes': ['Our teachers run paid language classes, and the fees pay for everything the letters need', 'Nobody pays to be introduced, nobody pays to write, and you never need a class to join a Pool.'], 'src': ['https://correolento.kindling.foundation/']},
    {'org': 'Drip Line', 'kind': 'Climbing gym', 'cat': 'tickets', 'quotes': ['Memberships and day passes pay for the gym.', 'Nobody pays to be in a Pool or to be introduced.'], 'src': ['https://dripline.kindling.foundation/']},
    {'org': 'Late Supper', 'kind': 'Matchmakers', 'cat': 'services', 'also': 'thanks', 'pays': 'Private dinners Nadia (invented) cooks, which “pays for Late Supper”; thanks “after an introduction has worked”', 'quotes': ['pays for Late Supper', 'after an introduction has worked', 'Nobody pays to join a table or to be introduced.'], 'src': ['https://latesupper.kindling.foundation/']},
    {'org': 'Seen Work', 'kind': 'Trades referral circle', 'cat': 'grants', 'quotes': ['the Harbor Trades Hall pays it from its education budget', 'Nobody pays a referral fee, on either side'], 'src': ['https://seenwork.kindling.foundation/']},
    {'org': 'Face Up', 'kind': 'App, “One card at a time”', 'cat': 'tickets', 'quotes': ['Ticketed evenings at a bar pay for it', 'nothing about who sees you is for sale'], 'src': ['https://kindling.foundation/apps.html']},
    {'org': 'Card Catalog', 'kind': 'App, “search-first”', 'cat': 'grants', 'pays': '“A nonprofit”; “members’ donations and a small grant”', 'quotes': ['A nonprofit', "members' donations and a small grant", 'nobody pays to see who said yes'], 'src': ['https://cardcatalog.kindling.foundation/about.html', 'https://cardcatalog.kindling.foundation/']},
    {'org': 'Heartwood', 'kind': 'Dating and friendship app', 'cat': 'grants', 'quotes': ['Member-supported: people chip in what they like, once a year', 'every feature is the same for everyone'], 'src': ['https://kindling.foundation/apps.html']},
    {'org': 'Familiar Faces', 'kind': 'Friendship app', 'cat': 'hosting', 'quotes': ['paid for by the libraries and clubs whose groups it reads', 'That money never buys a place in line.'], 'src': ['https://kindling.foundation/apps.html', 'https://familiarfaces.kindling.foundation/']},
    {'org': 'Threshold', 'kind': 'A desk for curators', 'cat': 'hosting', 'quotes': ['Organizations that keep many Pools may pay for a shared desk.', 'Free for volunteer curators.'], 'src': ['https://threshold.kindling.foundation/about.html']},
    {'org': 'Many Moons', 'kind': 'Community', 'cat': 'tickets', 'quotes': ['Tickets to the socials and workshops pay for the room.', 'No paid boosts, no paywall on who is interested'], 'src': ['https://manymoons.kindling.foundation/']},
    {'org': 'The Board, Port Ellery Free Library', 'kind': 'Public library', 'cat': 'grants', 'quotes': ["the library's public budget", 'Nobody pays to pin up a flyer, to be on one, or to be introduced to anyone.'], 'src': ['https://noticeboard.kindling.foundation/']},
    {'org': 'Midspan', 'kind': 'Mentorship program', 'cat': 'grants', 'quotes': ['a three-year grant from the Ellery Coast College Foundation', 'Nobody pays to be listed or introduced, before or after.'], 'src': ['https://midspan.kindling.foundation/']},
    {'org': 'Hearthhold', 'kind': 'Introductions for chosen family', 'cat': 'services', 'quotes': ['We charge only for help after two people decide to build something together, and only if they ask.', 'Nobody pays to be listed, met or introduced.'], 'src': ['https://hearthhold.kindling.foundation/']},
    {'org': 'Ferry Room Players', 'kind': 'Musicians’ collective', 'cat': 'tickets', 'quotes': ['Tickets and the bar keep the Ferry Room open.', "we don't take a cut of a gig"], 'src': ['https://ferryroom.kindling.foundation/']},
    {'org': 'Mycelial', 'kind': 'App, made by TranquilTech', 'cat': 'hosting', 'real': True, 'quotes': ['Communities that want hosting pay for it, and small groups without revenue can run it themselves for free.'], 'src': ['https://kindling.foundation/apps.html']},
]
for _r in MONEY_LINES:
    _q = [x.replace("'", '’') for x in _r['quotes']]
    if _r.get('real'):
        _r.setdefault('pays', Q(_q[0])); _r['never'] = None
    else:
        _r.setdefault('pays', Q(_q[0]))
        _r['never'] = Q(_q[-1])
MONEY_FOOTER = '§1.3: the protocol defines no chargeable surface at the connection layer. Every organization here except Mycelial is invented by the Kindling sites, to show what could be built.'

LICENSE_LINE = ('This edition’s text is © 2026 Josh Wolf, licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. '
                'Its code is licensed under <a href="https://www.apache.org/licenses/LICENSE-2.0">Apache 2.0</a>. '
                'Quotations from the Kindling Protocol Specification v0.1.1: © 2026 TranquilTech and Kindling spec contributors, CC BY 4.0, marked where shortened.')
CREDIT = 'Produced and edited by Josh Wolf. Research and writing support by Claude, from Anthropic.'
COOKIE_LINE = 'This site sets no cookies. Day, Night and Readable letters stay in this browser.'

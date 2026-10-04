# Supplementary tools for the Kindling edition: specifications

Three tools, specified for the build session (Session 9, kindling.foundation). These are specifications; the build session writes the code. Every protocol claim carries its section number in `spec/SPEC.md` v0.1.1 (commit `e4eb787`), and every example is invented and labeled so. Wrapper copy follows the site's register: a promise, then its section number; the negative before the positive; "you" as the owner of a page; roles, not demographics; no urgency and no exclamation marks.

Shared rules for all three:

1. Nothing a reader does is stored or sent. The protocol site says "this site sets no cookies," and these tools should do the same: state lives in the page and, at most, in the reader's own browser.
2. No scores, streaks, counters, timers or rankings, in keeping with the care sheet.
3. Every status carries one word and a date: Stable, Draft, Planned, Nothing yet.
4. Every chapter link goes to K.1 to K.4 or to a Field Manual chapter by number; every protocol link goes to the protocol site's section anchor.

## Tool 1: The two-door chooser

**What it is for.** A reader picks a door, builder or curator, then one narrower choice, and gets the reading list for that reader. **What it is not for.** It is not a quiz, it does not score anyone, and it does not sign anyone up.

**Flow.**

| Step | Builder door | Curator door |
|---|---|---|
| 1 | "For builders of clients, hosts and tools" | "For curators and the organizations that keep Pools" |
| 2 | Pick a conformance class (§11): Pool host (§11.1), Pool UI (§11.2), parser (§11.3), messaging client (§11.4), or "Something §11 does not name" (registry, block list, agent) | Pick a consent model (§3.2, §5.4): `universal-opt-in`, `vouching-required`, `curator-only-adds`, or "Not sure yet" |
| 3 | Show the sections that bind the choice, from K.1's build table, each with its MUST quoted | Show the K.4 consent-model row and the rules table, each with its section |
| 4 | Reading list (below) | Reading list (below) |

**Reading lists.** Builder: K.1, K.2, then Ch 4.7 and Ch 8.5 (privacy and security, with §2.5, §2.7 and the POST-only handshake of §5.2 as case studies), Ch 7.1 for distribution ("Send the link and the registry lists it," status Planned, no live endpoint on October 4, 2026; §8.4, §8.5, §10). A builder who will sell something beside the protocol adds K.3 and Ch 3.6. Curator: K.4, K.3, then Ch 4.3, Ch 4.8 and Ch 4.7; a curator inside a nonprofit adds Ch 6.3. Both doors end with Volume 10, Ch 10.4 first, and Ch 10.9, open without any gate.

**Copy for the first screen.** Heading: "Two readers, one specification." Line: "Pick a door. Every chapter links the section that binds it." Chip on both doors: "Planned · shown with invented examples," dated.

**Done when.** Each of the 9 step-2 choices produces a list that names at least one section and at least one chapter, and the back button returns to step 1 with nothing remembered.

## Tool 2: The Pool manifest walkthrough

**What it is for.** A curator or builder writes a valid manifest one field at a time and learns what each field promises. **What it is not for.** It does not host a Pool, send a handshake, or add anyone to anything.

**Fields, in order.** The 9 required fields of §3.2, then the optional ones from §3.3 a reader is most likely to need.

| Field | Prompt | A good value looks like | Validated by |
|---|---|---|---|
| `schema_version` | Filled in | `"0.1"` (§12.1) | `const "0.1"` |
| `name` | "Name the Pool." | A plain name a member would say aloud | `minLength 1` |
| `curator` | "Who curates it, and how are you verified?" | One entry with `identity`, `display_name`, `verification_level` (`email` or `oauth`), `primary: true` | `minItems 1` |
| `intent_tags` | "What is it for, in tags?" | 2 to 5 short tags | `minItems 1` |
| `visibility` | "Who can see the list?" | One of 3, with K.4's "what it does not do" line shown beside each | enum |
| `consent_model` | "How do people come in?" | One of 3; the floor of §5.4 shown under each | enum |
| `curator_contact` | "Where does someone write to be removed?" | An address you read | string |
| `charter` | "What is it for, and what is it not for?" | K.4's 6 questions as hints | `minLength 20` |
| `entries` | Shown empty | `[]`, with the note "Entries stay empty until someone accepts" | array |
| `handshake_window_days` | Optional | Leave unset for the literal default of 14 (§5.2) | integer, minimum 1 |
| `geographic_scope` | Optional | City, region, country, or online | object |
| `messaging_preferences.block_list_subscriptions` | Optional | URLs of lists you have read (K.4) | array of URIs |

**Example.** One worked example only, labeled "Invented example" at the top of the panel and in the JSON itself (a `name` ending "(invented)"), using reserved `.example` hosts as the repository's own examples do.

**Output.** A JSON panel that updates as the reader types, the schema file named (`schemas/pool_manifest.schema.json`), and the validator command with its warning: "Run this inside a clone of the repository. Nothing from this project is on npm." Command: `npx kindling-validate ./my-pool.json`.

**Done when.** The invented example, exported from the tool, passes `kindling-validate` inside a clone with no errors, and every field's prompt shows its section number.

## Tool 3: The Money-lines table, filterable

**What it is for.** A founder sees, in one place, what pays for a Kindling business and what never does, and which Field Manual chapter prices the thing that pays. **What it is not for.** It is not a directory of real businesses; none exists yet.

**Data.** One row per invented organization from K.3's table, plus Mycelial labeled "Real app · Kindling version early 2027." Columns: organization (with "Invented" chip), kind, what pays (quoted), what never pays (quoted), source page and date checked, Field Manual chapter.

**Chapter mapping.**

| What pays | Chapter |
|---|---|
| Classes, memberships, day passes, tickets | Ch 3.6 (price), Ch 5.3 (invoice and collect) |
| Private services sold after an introduction, on request | Ch 3.6, pricing for services |
| A grant, a public budget, donations, a nonprofit | Ch 6.3 |
| Hosting, a shared desk | Ch 3.6 (tiering by Pools hosted), Ch 5.3 |
| Thanks after an introduction worked | None; K.3 and §1.3. Status: Draft (v0.2), dated |

**Filters.** By "what pays" category, by chapter, and a toggle "show what never pays," switched on when the page opens. No sort by size, popularity or revenue.

**Footer, always visible.** "§1.3: the protocol defines no chargeable surface at the connection layer. Every organization here except Mycelial is invented by the Kindling sites, to show what could be built."

**Done when.** Every row's quotes agree with the source page on the date shown, every row carries "Invented" except Mycelial, and no filter state hides the §1.3 footer.

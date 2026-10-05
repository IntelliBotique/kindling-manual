# Check A: K-3.5, K-3.6, K-3.7, K-4.3, K-4.7

October 4, 2026. Checked against spec/SPEC.md at c3e24cd, K.1 to K.4 (gated, not .base), content/manual.md, and the live sites (fetched October 4, 2026). Every quotation in the five chapters (161) was matched by script against its source: all found. Site quotations were matched on the live pages, and their attributions checked in context. Arithmetic in K-3.6 and K-3.7 recomputed in Python: all correct. Originals of the five files before my edits are saved in my scratchpad (orig_A/).

Official texts opened for the law fixes:
- Cal. Civ. Code § 1798.105 and § 1798.140, from leginfo.legislature.ca.gov
- 16 CFR part 318, from ecfr.gov
- RCW 19.373, from app.leg.wa.gov
- Va. Code §§ 59.1-575 and 59.1-577, from law.lis.virginia.gov
- Colorado SB21-190 as signed, from leg.colorado.gov
- Connecticut Attorney General's CTDPA page, from portal.ct.gov. cga.ct.gov failed TLS from this container, so I did not read the statute text itself.

## K-3.5

| Finding | Severity | Fixed? | Old -> New (short) | Source |
|---|---|---|---|---|
| "leaving costs a person under a minute" is stronger than §5.3, which is a processing deadline after receipt ("within 60 seconds of receipt") | low | Yes | "leaving costs a person under a minute and takes nothing" -> "a Pool must process a person's leaving within 60 seconds of receipt (§5.3), and leaving takes nothing" | SPEC §5.3 |
| All other § claims (§2.1, §2.3, §2.5, §2.7, §4.1, §4.5, §5.1, §6.1, §6.4, §8.4, §11) checked for meaning and keyword strength: correct. §1.3 is described as a non-goal | none | n/a | n/a | SPEC |
| Quotations: 34 of 34 found (master 3.5, why.html, protocol site, GOVERNANCE.md at c3e24cd). "first of its twelve shifts" confirmed on why.html | none | n/a | n/a | sites |

## K-3.6

| Finding | Severity | Fixed? | Old -> New (short) | Source |
|---|---|---|---|---|
| The chapter says "Every organization named here is invented," but its table labels Mycelial "(real)". It contradicts itself, and the "every example is labeled invented" rule depends on this line being right | med | Yes | added "except Mycelial, which the sites label real" | K.3 line 46; K-3.6 table |
| "A member who can leave a Pool in under a minute (§5.3)" is the same overstatement as in K-3.5 | low | Yes | -> "A member whose withdrawal any Pool must process within 60 seconds (§5.3)" | SPEC §5.3 |
| Value table arithmetic (120 + 180 = 300; 90/300 = 30%; 210 left over) is correct. Inputs are labeled as assumptions | none | n/a | n/a | python |
| Subscription paragraph matches master line 3189 word for word | none | n/a | n/a | master Ch 3.6 |
| Quotations: 38 of 38 found. Site attributions checked: Drip Line has "No 'we miss you' emails"; Threshold about has "Free for volunteer curators"; Familiar Faces app has its own quote | none | n/a | n/a | sites |

## K-3.7

| Finding | Severity | Fixed? | Old -> New (short) | Source |
|---|---|---|---|---|
| "Each follows from §1.3" treats the §1.3 non-goal as a ban. K.3 says the three-questions test is "this chapter's own rule, built beside §1.3" | med | Yes | -> "Each fails K.3's three questions, the edition's rule built beside §1.3's non-goal." | K.3 line 60; SPEC §1.3 |
| The draft attributes "Designed to run on a single VPS or a small container" to the registry's README. The README (c3e24cd) actually says "small enough to run on a single VPS or container." The quoted words are on protocol.kindling.foundation/build.html, in lowercase | low | Yes | "the registry's README says it is \"Designed..." -> "the protocol site's build page says the registry is \"designed..." | registry/README.md line 17; build.html |
| Worked model recomputed: $22.67 (75.6%), $51.52 (85.9%), $119.95 (80.0%); the cap costs $90. All correct | none | n/a | n/a | python; master Ch 5.3 lines 4925, 4927; K.3 lines 83 and 84 |
| §3.1, §5.3, §6.3 and §9.1 claims are correct. The "thanks" row matches the protocol site ("Draft"; "v0.2 in draft") | none | n/a | n/a | SPEC; protocol site |

## K-4.3

| Finding | Severity | Fixed? | Old -> New (short) | Source |
|---|---|---|---|---|
| The handover table says consent proofs "move with the manifest." §3.4 defines `consent_proof` only as a "reference to the handshake response," so the response it points to can live outside the manifest and be lost in a handover | med | Yes | -> "The reference moves with the manifest; the spec does not say where the response itself is kept"; the contract column now adds "and the handshake responses the references point to" | SPEC §3.4 |
| "Most Kindling clients build on the reference tools" has no source | low | Yes | -> "A Kindling client may build on the reference tools" | none found |
| §5.1, §5.2, §9.1, §9.3, §9.4 claims and the `curator_contact` schema description are correct | none | n/a | n/a | SPEC; pool_manifest.schema.json |
| Clause table, contractor list and ESIGN line carry over from master Ch 4.3 without drift | none | n/a | n/a | work/src/4.3.md |
| Quotations: 29 of 29 found | none | n/a | n/a | n/a |

## K-4.7

| Finding | Severity | Fixed? | Old -> New (short) | Source |
|---|---|---|---|---|
| The state section says a small Pool sits below the volume thresholds, leaving three things to check. That misses Connecticut: as amended from July 1, 2026, its law reaches anyone who controls or processes sensitive data at any volume. A peer-support, faith or orientation Pool is exactly that case, and the master's own Volume 13 says so | high | Yes | added the Connecticut trigger and its nonprofit exemption (which does not cover consumer health data); "three things" -> "four things" | master line 15308; CT Attorney General page |
| (verify) 1: right to delete vs decline records | med | Yes, resolved as far as official texts go | -> Virginia's "record of the deletion request" rule, California's (d)(7) internal-use exception (none names a refusal record), and Washington's health-data deletion right with no such exception. The question for counsel stays | Va. Code § 59.1-577(B)(5); Civ. Code § 1798.105(d); RCW 19.373.040 |
| (verify) 2: health-data rules | med | Yes, partly resolved | -> Washington's law: no size threshold, "any legal entity", definition of consumer health data, separate consents. Connecticut's health-data rules apply regardless of size and to nonprofits. The FTC rule's definition of a personal health record. Whether a Pool UI is covered stays a question for counsel | RCW 19.373.010, .030; 16 CFR 318.2; CT Attorney General |
| (verify) 3: state sensitive-data definitions | med | Yes | -> Virginia's definition quoted; Colorado and Connecticut name the same kinds; California's sensitive personal information quoted | Va. Code § 59.1-575; Colo. SB21-190 § 6-1-1303(24); Civ. Code § 1798.140(ae); CT Attorney General |
| "A person can see which parts..." overstates §2.3, which only requires implementations to record provenance | low | Yes | -> "Your records then show which parts..." | SPEC §2.3 |
| "the sections a conformance claim rests on (§11.3)": §11.3 is the parser class only | low | Yes | -> "a parser's conformance claim" | SPEC §11.3 |
| "It covers the United States first, as the Field Manual does." is an announcement sentence with a dangling "It" | low | Yes | sentence removed | Rules |
| Master carry-overs checked: COPPA, HIPAA, HBNR/MHMDA mention, pixels, state thresholds, GDPR test, AI register, EU AI Act Article 50, eight-step program. No drift | none | n/a | n/a | master lines 4153 to 4270 |
| Data-map § citations (§3.2, §3.3, §3.4, §4.2, §5.2, §5.3, §6.1, §7.3, §2.6) are correct | none | n/a | n/a | SPEC |
| Quotations: 37 of 37 found, plus 15 new law quotations matched against the opened texts | none | n/a | n/a | n/a |

Rules, all five chapters: no em-dashes; no "user", "match" or "default" outside quotations; every Field exercise ends in *Done when*; license line present; a "Figures checked" line under each table with figures.

## For Josh

1. **The public-information exclusion.** California, Virginia, Colorado and Washington all leave out of "personal information" anything the business has a reasonable basis to believe the person "lawfully made available to the general public." California also says sensitive information that is publicly available "shall not be considered sensitive personal information or personal information" (Civ. Code § 1798.140(v)(2), (ae)(3)). A Kindling profile is a page the owner publishes, so this could shrink what these laws reach. Pool entries, decline records and member-only fields (Scattered Light: "Names are visible only to members") are not public. I did not add this to K-4.7; whether to add it is your call.
2. **The handshake as a Washington consent step.** RCW 19.373.030(1)(c) lists four disclosures a consent request must make, including the categories of data and how to withdraw. The §5.2 handshake shows the Pool name, charter, curator and visibility. Whether it should carry those four disclosures for a peer-support Pool is a question for a protocol RFC or for K.4, not for this chapter.
3. **Stale files.** README.md still lists five (verify) marks; three are now resolved in K-4.7. ledger.md has no rows for the 15 new law quotations or for the changed registry attribution in K-3.7.
4. **Connecticut statute not read.** cga.ct.gov failed TLS from this container, so the Connecticut lines rest on the Attorney General's page and on Volume 13. Someone should read chapter 743jj before publishing.
# Check B: K-4.8, K-5.3, K-6.3, K-7.1, K-8.5

Checked October 4, 2026, against: SPEC.md and schemas at c3e24cd (the live repository HEAD); the Field Manual master at /home/claude/sofm/content/manual.md and the work/src chapters; K.1 to K.4 (gated, not .base); the live sites, crawled the same day (187 pages across kindling.foundation, protocol.kindling.foundation and 29 library subdomains).

Quotations: every quotation in all five chapters was matched by an independent script against that corpus. That is 152 quotations after fixes (K-4.8 31, K-5.3 24, K-6.3 27, K-7.1 27, K-8.5 43), including every site quotation, and all were found. Spec quotations were read in context for meaning, keyword strength and scope. Arithmetic was recomputed in Python: 12 × 2.9% + $0.30 = $0.648 (5.4%), 90 × 2.9% + $0.30 = $2.91, 1/0.15 = 6.67 (about 7). Rules: 0 em-dashes; no "user" and no "match" used as a verb; no "default"; no "This chapter covers"; every Field exercise has a *Done when* test; license line present; a "Figures checked" line after every table.

## K-4.8

| Finding | Severity | Fixed? | Old -> New (short) | Source |
|---|---|---|---|---|
| Threshold called "a hosting desk," but the site says "It hosts no Pools itself." | med | Yes | "A hosting desk like the invented Threshold" -> "A shared curator desk like the invented Threshold" | threshold.kindling.foundation/about.html |
| "The Field Manual lists the predictable moments. Four of them fit." The fourth (a data request you cannot answer) is not on the master's list. | med | Yes | "Four of them fit a Kindling reader:" -> "Three of them fit a Kindling reader, and the edition adds a fourth:" | master 4.8, "Hire one for" |
| §5.3 withdrawal was called a "deletion." §5.3 is removal from a Pool. It does not require destroying records. | low | Yes | "one deletion is never routine and never stops" -> "one removal never stops" | SPEC §5.3 |
| "A host that stops hosting buys 'tail' coverage." The master says "buy 'tail' coverage if you close." | low | No (close enough) | None | master 4.8 |
| (verify) product liability for Late Supper's dinners | n/a | Mark kept: honest | The SBA's insurance page says product liability is for businesses that "manufacture, wholesale, distribute, and retail a product." It does not say whether a matchmaker's cooked dinners need it. A broker question. | sba.gov/business-guide/launch-your-business/get-business-insurance |
| (verify) litigation hold versus §5.3 | n/a | Mark kept: honest | No official source answers it. The spec text helps: §5.3 requires removal from the Pool, not erasure, so preserved copies and a 60-second removal need not conflict. That is a lawyer's call, so the mark stays. | SPEC §5.3 |

All other spec claims checked. §5.3 is quoted exactly. The `curator_contact` description is the schema's own words. §7.2 and §7.3 are used correctly. §3.4 `consent_proof` is a MUST on every entry. The block-list "2 illustrative entries" matches blocklist.json (version 3) and K.4.

## K-5.3

| Finding | Severity | Fixed? | Old -> New (short) | Source |
|---|---|---|---|---|
| The $90 hosting invoice is an invented input that was not labeled. | med | Yes | "On an organization's $90 hosting invoice" -> "On an invented $90 hosting invoice to an organization" | Brief rule 4 |
| The card-surcharging line dropped the master's card-network clause (a risk area). | low | Yes | Quote extended with "and the card networks add their own rules (caps, disclosure, registration)." | master 5.3 |
| The ACH advice quotes the master's "invoices over about $1,000" right after a $90 example. Not wrong, but it reads oddly. | low | No | None | master 5.3 |

These carry over accurately from the master: the 1099-NEC $2,000 threshold, the 1099-K threshold (more than $20,000 and more than 200 transactions), the Stripe, PayPal and ACH table, the FDCPA line, and the small-claims range. §5.3 and §9.1 are quoted at their correct strength.

## K-6.3

| Finding | Severity | Fixed? | Old -> New (short) | Source |
|---|---|---|---|---|
| "Most state programs fund businesses, so a Pool qualifies only as part of one" had no source, and is doubtful for public libraries. | med | Yes | Sentence deleted | No source in the master |
| "Real ones 'never charge application fees'" was attached to prizes. The master says it of private small-grant programs. | low | Yes | -> "Real private small-grant programs 'never charge application fees.'" | master 6.3 |
| The text said only the restrictions row was adapted, but the reporting and strategic-pull rows were rewritten too. | low | Yes | -> "with the restrictions, reporting and strategic-pull rows read against the protocol" | master 6.3 table |
| The GPA quotation cut the master's "(item 19)" without marking it. | low | Yes | -> `...based on grants" (item 19).` | master 3.7 |

Every site quotation was found live, including Card Catalog's "members' donations and a small grant" (about.html) and the Familiar Faces lines. The §1.3 non-goal framing matches K.1.

## K-7.1

| Finding | Severity | Fixed? | Old -> New (short) | Source |
|---|---|---|---|---|
| "Some Pools will never appear there" (the well-known file). The schema allows `unlisted` and `invite-only` entries, so leaving them out is the library's convention, not a protocol rule. | med | Yes | -> "Some Pools are left out of it." | schemas/well_known_pool.schema.json; registry.html |
| "can find every public Pool a host offers." §10.2 covers each "discoverable" Pool, and only where a host publishes the file (SHOULD). | low | Yes | -> "every Pool a host lists as discoverable" | SPEC §10.2, §8.3 |
| "ships validators, a parser and a reference handshake server." There is one validator, and the reference registry server (registry/server.js) was left out, though the chapter's own "A registry you run" needs it. | low | Yes | -> "a validator, a parser, a reference handshake server and a reference registry server" | package.json bin; registry/README.md |

Checked against §8, §10 and the live pages:

- The surfaces table matches §8.2 to §8.5 at their correct strength. §8.1 ends in a colon with no list. FRAMEWORK.md names the four surfaces, so reading the subsections as that list is sound.
- The registry status is correct. `registry-data/` holds only its README. registry.kindling.foundation returns 404. registry/README.md says the well-known crawler "is not in v0.1."
- kindling.foundation/.well-known/kindling-pool now has `"pools": []` (last-modified Oct 4, 21:09). The draft makes no claim about the project's own Pools, and K.4 already says the file lists none. No conflict.
- The `kindling-validate` exercise works. The CLI accepts `--type wellknown` or infers the type.

## K-8.5

| Finding | Severity | Fixed? | Old -> New (short) | Source |
|---|---|---|---|---|
| The Kindling incident scenario dropped the master runbook's ASSESS and GET HELP steps, including attorney first for breach-notification law. A compromised curator mailbox can expose personal data. | med | Yes | New step 5, "Assess and get help," quoting the master. Later steps renumbered. | master 8.5 runbook |
| "move hosts without losing its consent proofs or decline records (§9.3)." §9.3 is curator transition and says nothing about this. | low | Yes | (§9.3) -> (§3.4, §5.2) | SPEC |
| "never a page with the noindex directive (§2.7)." §2.7 forbids including such a page, not reading it, and parsers MUST record the directive. | low | Yes | -> "never surfaces a page with the noindex directive" | SPEC §2.7 |
| "Their decline links worked as designed" claimed too much for mail an attacker may have written. | low | Yes | -> "Links in any handshake your Pool sent worked as designed" | SPEC §5.2 |
| Exercise 5 allowed an agent to be named in the `curator` field. The chapter itself says an agent never adds anyone. | low | Yes | -> "every person with edit rights ... is named in its `curator` field, and no agent holds edit rights" | Chapter's own rule; SPEC §3.2 |

These match the spec: §5.2 step 3 (quoted exactly, with its MUST and MUST NOT kept), §5.3, §9.1, §6.1 and §6.4, and §3.1 and §3.4. The reference server's SMTP-by-environment quote and the discovery agent's header quote are verbatim from the repo.

## Totals

High 0. Medium 7, all fixed. Low 15: 13 fixed, 2 left as written. The two (verify) marks are kept as honest.

## For Josh

1. **The protocol site contradicts the live well-known file.** protocol.kindling.foundation/registry.html still lists the project's 5 planned Pools (Founding Curators, Client Builders and the rest) and says it is "built from each site's .well-known/kindling-pool file." kindling.foundation's file now has `"pools": []`. Either rebuild the registry view or change its wording. No draft depends on it.
2. **Spec erratum candidate.** §8.1 ends "through at least one of these surfaces ... :" with no list. FRAMEWORK.md has the list (four surfaces). A v0.1.2 erratum could add it.
3. **K-4.8, Late Supper's dinners.** Beyond product liability, selling cooked food may bring state food-permit rules (home-kitchen and cottage-food rules). I opened no source, so I added nothing. Decide whether the chapter should point at it.
4. **K-8.5's new step 5** adds about 40 words. Word counts in README.md are now stale. K-6.3 lost 15 words and stays above 900.

# The Kindling edition: lane statement

Session 9, October 4, 2026, run on Claude Opus 5.5. Read against spec v0.1.1 (Stable, 1 October 2026), IntelliBotique/kindling at `c3e24cd`, and kindling-sites at `5afb487`. Revised the same day for Josh's change of scope: the edition carries no Field Manual chapters. It is K.1 to K.4 and the three tools, and where they lean on the Field Manual it links to the Library edition on solo.joshwolf.net with a Kindling note beside each link.

## The eight points

1. **First screen.** The Charter dress, opening at Night. One h1 with the italic accent: "The manual should belong to *the people building on it.*" Then the brief's lede and two status chips, each one word: Stable (v0.1.1) and Nothing yet (nothing runs at TranquilTech). Then two doors, both chipped "Planned · shown with invented examples." The builder door wears the protocol site's greys and Archivo; the curator door wears Charter purple. The first screen shows both dresses before you choose.
2. **Order, and what sits behind doors.** Nothing sits behind any door; the whole edition is open. Each door is a charter: "What it's for," then "What it's not for," then a chooser, then numbered articles.
   - **Builder:** Art. I is K.1, then Art. II K.2, Art. III "What the protocol leaves out," Art. IV the quick start, Art. V the manifest walkthrough, Art. VI Try it as Hollis, Art. VII Volume 10 on the Library, with 10.4 first and 10.9 beside it.
   - **Curator:** Art. I is K.4, then Art. II K.3, Art. III K.2, Art. IV Try it as Hollis, Art. V the Money lines, Art. VI the manifest walkthrough, Art. VII the same Volume 10 links.
   - **Kindling rewrites** of 3.5, 3.6, 3.7, 4.3, 4.7, 4.8, 5.3, 6.3, 7.1 and 8.5, numbered K-3.5 to K-8.5 and listed with the K chapter each leans from. Each links its original on solo.joshwolf.net. 10.4 and 10.9 are linked there unchanged, with their notes.
3. **First ask.** Pick a door. A door is a link and stores nothing.
4. **Tools and examples.** Three tools are foregrounded:
   - the quick start, the protocol site's five steps verbatim, with K.1's clone-only and npm-name warnings;
   - "Try it as Hollis," linked to kindling.foundation/intro.html and read against §5.2;
   - the Money lines, filterable, with the §1.3 footer outside every filter.

   The return's other two tools ride inside: the chooser is on each charter (9 choices), and the manifest walkthrough stands on its own page. The sites' organizations, Hollis and the walkthrough's example are labeled invented.
5. **Register.** A promise, then its section number. The negative before the positive. Status in one word. "You" as the owner of a page. No "user," no "match" as a verb, no urgency, no exclamation marks, no em-dashes. §1.3 is called a non-goal, never a ban: "Kindling defines no chargeable surface between two people (§1.3, a stated non-goal)." The two site lines that K.1 shows resting on no MUST (§1.3 and §6.1) are never quoted as MUSTs.
6. **Dress.** `charter.css` is copied byte for byte from kindling-sites `5afb487`. The C1 tokens are copied from `spec.css` into `edition.css`, which adds only `ed-` classes and uses tokens only. RFC keywords on the builder path take the protocol site's weights. Day, Night and Readable letters are on every page and kept in the browser.
7. **Access.** Open. No signup, no list, no cookie, no handshake. "This site sets no cookies."
8. **Cuts and additions.** No Field Manual chapter is carried as written. The additions are the four finished chapters, the research return's three tools, and ten Kindling rewrites of the chapters those lean on, each gated by the Field Manual lane and wired as written. The gate's record is in `content/brief/rewrites_gate/`.

The care sheet holds on every page. 988 and 741741 are a pinned line at the foot of the screen, one tap, never behind a menu, with Chapter 10.9 linked on the Library rather than copied. No tool keeps a score, a streak, a counter or a timer. Every table with a figure carries its "Figures checked" line. The credit line and the license line are in the colophon.

## Settled by Josh, October 4

- Repo: `IntelliBotique/kindling-manual`, public, its own Vercel project at `manual.kindling.foundation`. Links in from the Kindling sites come to Josh as a pull request.
- §1.3 wording: the non-goal line above. The builder article is "What the protocol leaves out."
- License: the whole edition's text is © 2026 Josh Wolf under CC BY 4.0, its code under Apache 2.0. Spec quotations are credited "© 2026 TranquilTech and Kindling spec contributors, CC BY 4.0" and marked where shortened.

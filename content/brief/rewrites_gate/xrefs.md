# Cross-references, Kindling rewrites

Three lists: what each rewrite points to; which note in the edition each one replaces; and what the edition must change when the rewrites are wired.

## References each rewrite makes

| Rewrite | K chapters | Other rewrites | Field Manual chapters (on solo.joshwolf.net) | Field Manual volumes |
|---|---|---|---|---|
| K-3.5 | K.1 | K-7.1 | 3.5 | none |
| K-3.6 | K.3 | none | none | 5 |
| K-3.7 | K.3 | K-3.6, K-4.3 | 3.7, 5.2, 5.3 | none |
| K-4.3 | K.2, K.3, K.4 | K-3.6, K-4.7, K-5.3 | 4.3 | none |
| K-4.7 | K.3, K.4 | K-4.3, K-4.8, K-8.5 | 4.6, 4.7, 11.6 | 13 |
| K-4.8 | K.4 | K-4.3, K-4.7, K-5.3, K-8.5 | 4.8 | 13 |
| K-5.3 | K.3 | K-3.6, K-4.3 | none | 13 |
| K-6.3 | K.3, K.4 | none | 3.7, 6.3 | 13 |
| K-7.1 | K.1 | K-3.6 | 7.1 | none |
| K-8.5 | K.1, K.3 | K-4.7 | none | none |

A Field Manual chapter number inside a rewrite that names its own source (for example "Chapter 3.6" in K-3.6) refers to the original on solo.joshwolf.net. Every other Field Manual number refers to the Library too, except where a rewrite of that number exists, as listed below.

## Notes in the edition each rewrite replaces

The edition links twelve Field Manual chapters out with a note beside each link (`build/edition.py`, the `FM` dictionary, at kindling-manual 901777a). Ten of those links become links to the rewrite. The notes for 10.4 and 10.9 stay as they are.

| Rewrite | Replaces the `FM` note for | Where the link appears in the edition |
|---|---|---|
| K-3.5 | 3.5 | Builder's charter, Art. III "What the protocol leaves out" |
| K-3.6 | 3.6 | Curator's charter, with K.3; K.3 page; the Money lines tool |
| K-3.7 | 3.7 | Curator's charter, with K.3; K.3 page |
| K-4.3 | 4.3 | Curator's charter, with K.4, and its chooser; K.4 page |
| K-4.7 | 4.7 | Both charters and both choosers; K.1 and K.4 pages |
| K-4.8 | 4.8 | Curator's charter, with K.4, and its chooser; K.4 page |
| K-5.3 | 5.3 | Curator's charter, with K.3; K.3 page; the Money lines tool |
| K-6.3 | 6.3 | Curator's charter, with K.3; K.3 page; the Money lines tool |
| K-7.1 | 7.1 | Builder's charter, with K.1, and its chooser; K.1 page |
| K-8.5 | 8.5 | Builder's charter, with K.1, and its chooser; K.1 page |

## What wiring must change in the edition

1. Inline mentions such as "Ch 3.6" in K.1 to K.4 currently link to solo.joshwolf.net. After wiring, the ten rewritten numbers link to the rewrite, with the original reachable from each rewrite's footer ("The full chapter is on solo.joshwolf.net").
2. The edition's build adds a "Figures checked" line under every table with a digit. The drafts already carry the line. The wiring must not add a second one.
3. Each rewrite ends with its own license line. The page footer already carries the edition's license line; keep the rewrite's line in the body, since it names the source chapter.
4. The edition test suite should gain a check that every rewrite page carries its section links, its license line and no em-dashes, as it does for K.1 to K.4.
5. 10.4 and 10.9 are not rewritten. Their links and notes are unchanged.

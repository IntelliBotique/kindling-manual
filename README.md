# The Solo Operator's Field Manual: the Kindling edition

manual.kindling.foundation. Four chapters, ten Kindling rewrites of Field Manual chapters, and three tools, for two readers of one specification: people building on the [Kindling protocol](https://protocol.kindling.foundation/) and people keeping Pools on it. Every protocol claim carries its section number in spec v0.1.1, and every example is labeled invented.

The edition carries no Field Manual chapter as written. Ten of the chapters K.1 to K.4 lean on are rewritten for a Kindling reader (K-3.5 to K-8.5, each keeping its source number), gated by the Field Manual lane on October 4, 2026. Each rewrite links its original on [solo.joshwolf.net](https://solo.joshwolf.net), the Library edition. Chapters 10.4 and 10.9 are linked there unchanged.

## Layout

| Path | What it is |
|---|---|
| `content/kindling/` | K.1 to K.4, the finished chapters, as the Field Manual lane gated them. Never edited here; problems go to `FIELD_MANUAL_CORRECTIONS.md`. |
| `content/kindling/rewrites/` | K-3.5 to K-8.5, the ten Kindling rewrites, as gated. Never edited here either. |
| `content/brief/rewrites_gate/` | The gate's notes, check log and cross-references for the rewrites. |
| `content/brief/` | The tool specifications and the cross-reference list the chapters and notes are built from. |
| `build/edition.py` | The wrapper copy: the two charters, the rewrite table, the notes for 10.4 and 10.9, the chooser and the Money lines data. |
| `build/build.py`, `build/pages.py` | The generator. Writes every page into `public/`. |
| `public/` | The site, served as static files. `assets/charter.css` is kindling-sites' file, unchanged. |
| `test/test.mjs` | The checks: the care line, licensing, register, section links, quotation fidelity, the tools. |

## Build and test

```bash
python3 -m venv build/.venv && build/.venv/bin/pip install -r build/requirements.txt
npm run build
npm test
```

The test turns on two more checks when it finds local clones: `KINDLING_REPO` (IntelliBotique/kindling, with `npm install` run) validates the walkthrough's invented manifest with `kindling-validate`, and `KINDLING_SITES` (IntelliBotique/kindling-sites) checks every Money-lines quotation and every section anchor against the live sites' files.

## Deploy

Vercel project `kindling-manual`, no build step, output `public`. Pushes to `main` deploy.

## License

This edition's text is © 2026 Josh Wolf, licensed under CC BY 4.0 (`LICENSE-TEXT`, whose first line names the files it covers). Its code is licensed under Apache 2.0 (`LICENSE`). Quotations from the Kindling Protocol Specification v0.1.1 are © 2026 TranquilTech and Kindling spec contributors, CC BY 4.0, and are marked where shortened. The fonts are under the SIL Open Font License 1.1; their licenses are in `public/fonts/licenses/`.

Produced and edited by Josh Wolf. Research and writing support by Claude, from Anthropic.

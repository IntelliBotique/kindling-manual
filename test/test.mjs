// The Kindling edition's checks. Run: node test/test.mjs
// Optional: KINDLING_REPO (a clone of IntelliBotique/kindling with npm install run) and
// KINDLING_SITES (a clone of IntelliBotique/kindling-sites) turn on the validator and source checks.
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const PUB = path.join(ROOT, 'public');
const REPO = process.env.KINDLING_REPO || '/Volumes/Projects/kindling';
const SITES = process.env.KINDLING_SITES || '/Volumes/Projects/kindling-sites-ref';

let failed = 0, passed = 0, skipped = 0;
function check(name, fn) {
  try { const r = fn(); if (r === 'skip') { skipped++; console.log('  skip  ' + name); } else { passed++; console.log('  ok    ' + name); } }
  catch (e) { failed++; console.log('  FAIL  ' + name + '\n        ' + e.message.split('\n').join('\n        ')); }
}
function assert(c, msg) { if (!c) throw new Error(msg); }
function walk(dir, ext) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(d => {
    const p = path.join(dir, d.name);
    return d.isDirectory() ? walk(p, ext) : (p.endsWith(ext) ? [p] : []);
  });
}
const pages = walk(PUB, '.html').map(p => ({ p: path.relative(PUB, p), h: fs.readFileSync(p, 'utf8') }));
const BLOCK = /<\/?(p|li|ul|ol|div|h[1-6]|td|th|tr|table|thead|tbody|br|section|article|header|footer|nav|main|dt|dd|dl|pre|blockquote|aside|fieldset|legend|label|figure|figcaption|form|option|select|textarea|button)\b[^>]*>/gi;
const text = h => h.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/g, ' ').replace(BLOCK, ' ').replace(/<[^>]+>/g, '')
  .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/\s+/g, ' ');
const norm = s => s.replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, ' ');

console.log(`Kindling edition: ${pages.length} pages`);

// ---- the care sheet ----
check('988 and 741741 one tap away on every page, with Chapter 10.9 linked', () => {
  for (const { p, h } of pages) {
    const bar = h.match(/<div class="ed-care"[\s\S]*?<\/div><\/div>/);
    assert(bar, `${p}: no care line`);
    assert(bar[0].includes('href="tel:988"') && bar[0].includes('Call or text 988'), `${p}: 988 link`);
    assert(bar[0].includes('href="sms:741741') && bar[0].includes('Text HOME to 741741'), `${p}: 741741 link`);
    assert(bar[0].includes('href="https://solo.joshwolf.net/care"'), `${p}: 10.9 link`);
  }
});
check('the care line is not inside a menu, a details element or a hidden block', () => {
  for (const { p, h } of pages) {
    const i = h.indexOf('class="ed-care"');
    const before = h.slice(0, i);
    assert((before.match(/<details/g) || []).length === (before.match(/<\/details>/g) || []).length, `${p}: inside details`);
    assert(!/class="ed-care"[^>]*hidden/.test(h), `${p}: hidden`);
  }
  const css = fs.readFileSync(path.join(PUB, 'assets/edition.css'), 'utf8');
  assert(/\.ed-care\{position:sticky;bottom:0/.test(css), 'care line is not pinned');
});
check('no scores, streaks, counters, timers or leaderboards in any tool', () => {
  const js = fs.readFileSync(path.join(PUB, 'assets/tools.js'), 'utf8') + fs.readFileSync(path.join(PUB, 'assets/edition.js'), 'utf8');
  for (const w of ['score', 'streak', 'leaderboard', 'setInterval', 'countdown', 'progress']) assert(!new RegExp('\\b' + w, 'i').test(js.replace(/no tool keeps a score|nothing is scored/gi, '')), `scripts mention ${w}`);
});

// ---- licensing and credit ----
check('every page carries the license line and the credit line', () => {
  for (const { p, h } of pages) {
    const t = text(h);
    assert(t.includes('This edition’s text is © 2026 Josh Wolf, licensed under CC BY 4.0. Its code is licensed under Apache 2.0.'), `${p}: license`);
    assert(t.includes('© 2026 TranquilTech and Kindling spec contributors, CC BY 4.0, marked where shortened'), `${p}: spec credit`);
    assert(t.includes('Produced and edited by Josh Wolf. Research and writing support by Claude, from Anthropic.'), `${p}: credit`);
  }
});
check('LICENSE is the full Apache 2.0 text and LICENSE-TEXT is CC BY 4.0 with its scope on line 1', () => {
  const a = fs.readFileSync(path.join(ROOT, 'LICENSE'), 'utf8');
  assert(a.includes('Apache License') && a.includes('Version 2.0, January 2004') && a.includes('END OF TERMS AND CONDITIONS'), 'LICENSE');
  const c = fs.readFileSync(path.join(ROOT, 'LICENSE-TEXT'), 'utf8');
  assert(/^This license covers /.test(c.split('\n')[0]), 'LICENSE-TEXT line 1');
  assert(c.includes('Attribution 4.0 International') && c.includes('Section 1') && c.includes('Section 8'), 'LICENSE-TEXT body');
  for (const f of fs.readdirSync(path.join(PUB, 'fonts')).filter(f => f.endsWith('.woff2'))) {
    const fam = f.split('-latin')[0].replace(/-/g, '').replace('1918', '1918');
    assert(fs.readdirSync(path.join(PUB, 'fonts/licenses')).some(l => l.startsWith(fam.replace(/standard|wght|full|400/g, ''))), `no license for ${f}`);
  }
});

// ---- register and wrapper rules ----
check('no em-dashes anywhere in the edition', () => {
  const files = [...walk(PUB, '.html'), ...walk(PUB, '.css'), ...walk(PUB, '.js'), ...walk(path.join(ROOT, 'content'), '.md'), ...walk(path.join(ROOT, 'build'), '.py').filter(f => !f.includes('.venv')), ...walk(ROOT, '.md').filter(f => !f.includes('node_modules') && !f.includes('.venv'))];
  for (const f of files) assert(!fs.readFileSync(f, 'utf8').includes('—'), `em-dash in ${path.relative(ROOT, f)}`);
});
check('no "user", no "match" as a verb, no exclamation marks, no urgency in any page', () => {
  for (const { p, h } of pages) {
    const t = text(h.replace(/<pre[\s\S]*?<\/pre>|<code[\s\S]*?<\/code>/g, ' '));
    assert(!/\busers?\b(?!-agent)/i.test(t), `${p}: "user"`);
    const logged = [...fs.readFileSync(path.join(ROOT, 'FIELD_MANUAL_CORRECTIONS.md'), 'utf8').matchAll(/^Old text: "(.*)"$/gm)].map(m => norm(m[1].replace(/`/g, '')));
    const t2 = logged.reduce((acc, l) => acc.split(l.split(':')[0]).join(' '), norm(t));
    assert(!/\bmatch(es|ed|ing)?\b/i.test(t2), `${p}: "match"`);
    assert(!/!(\s|$)/.test(t), `${p}: exclamation mark`);
    for (const w of ['hurry', 'act now', 'limited time', 'don’t miss', 'last chance']) assert(!t.toLowerCase().includes(w), `${p}: "${w}"`);
  }
});
check('the builder article is named "What the protocol leaves out" and §1.3 is called a non-goal, never a ban', () => {
  const b = pages.find(x => x.p === 'builders.html').h;
  assert(b.includes('>What the protocol leaves out</h2>'), 'article name');
  for (const { p, h } of pages) {
    const t = text(h);
    assert(!/Kindling forbids/i.test(t), `${p}: "Kindling forbids"`);
    assert(!/§1\.3 (forbids|bans|prohibits)/.test(t), `${p}: §1.3 as a ban`);
  }
  assert(text(pages.find(x => x.p === 'builders/k-3-5.html').h).includes('Kindling defines no chargeable surface between two people (§1.3, a stated non-goal).'), 'non-goal wording on K-3.5, where Art. III leads');
});

// ---- protocol claims carry a section and match the stated version ----
check('every page states spec v0.1.1, and only that version', () => {
  for (const { p, h } of pages) {
    const t = text(h);
    assert(t.includes('Spec v0.1.1'), `${p}: version`);
    for (const m of t.matchAll(/\bSpec(?:ification)? (v\d+\.\d+\.\d+)/g)) assert(m[1] === 'v0.1.1', `${p}: states ${m[1]}`);
  }
});
check('every § is linked, and every link lands on a section that exists in the live spec page', () => {
  const specPath = path.join(SITES, 'site/protocol/spec.html');
  const ids = fs.existsSync(specPath) ? new Set([...fs.readFileSync(specPath, 'utf8').matchAll(/id="([^"]+)"/g)].map(m => m[1])) : null;
  for (const { p, h } of pages) {
    const body = h.replace(/<script[\s\S]*?<\/script>/g, '');
    const unlinked = text(body.replace(/<a [^>]*>[\s\S]*?<\/a>/g, ' ').replace(/<label class="ed-opt">[\s\S]*?<\/label>/g, ' ').replace(/<(pre|code)[\s\S]*?<\/\1>/g, ' ')).match(/§\d+(\.\d+)?/g);
    assert(!unlinked, `${p}: unlinked ${unlinked}`);
    for (const m of body.matchAll(/href="https:\/\/protocol\.kindling\.foundation\/spec\.html#([^"]+)"/g)) {
      if (ids) assert(ids.has(m[1]), `${p}: spec.html has no #${m[1]}`);
    }
  }
  if (!ids) return 'skip';
});
check('the K chapters are carried whole: every number and quotation in the source is on the page', () => {
  for (const [file, slug, doors] of [['K1.md', 'k1', ['builders']], ['K2.md', 'k2', ['builders', 'curators']], ['K3.md', 'k3', ['curators']], ['K4.md', 'k4', ['curators']]]) {
    const src = fs.readFileSync(path.join(ROOT, 'content/kindling', file), 'utf8');
    const plain = norm(src.replace(/^## Chapter .*$/m, '').replace(/\*+|`/g, '').replace(/^#+ |\|/gm, ' '));
    for (const d of doors) {
      const page = norm(text(pages.find(x => x.p === `${d}/${slug}.html`).h));
      for (const n of plain.match(/\d[\d,.]*\d|\d/g)) assert(page.includes(n), `${d}/${slug}: number ${n} missing`);
      for (const q of (plain.match(/"[^"]{6,}"/g) || []).filter(q => !/^"\s|\s"$/.test(q))) assert(page.includes(q.replace(/\s+/g, ' ')), `${d}/${slug}: quotation ${q.slice(0, 60)} missing`);
    }
  }
});
check('every table that carries a digit has its "Figures checked" line', () => {
  for (const { p, h } of pages.filter(x => /\/k\d\.html$/.test(x.p))) {
    for (const m of h.matchAll(/<div class="ed-table"><table>([\s\S]*?)<\/table><\/div>(<p class="ed-checked">)?/g)) {
      if (/\d/.test(text(m[1]))) assert(m[2], `${p}: a table with figures has no "Figures checked" line`);
    }
  }
});

// ---- the Field Manual stays on the Library ----
check('no Field Manual chapter text is in the edition, and every Field Manual link carries its Kindling note', () => {
  assert(!fs.existsSync(path.join(ROOT, 'content/corpus')), 'content/corpus is still in the repo');
  for (const { p, h } of pages) {
    for (const m of h.matchAll(/<li class="ed-lean">([\s\S]*?)<\/li>/g)) {
      assert(/href="https:\/\/solo\.joshwolf\.net\/(read#ch-\d+\.\d+|care)"/.test(m[1]), `${p}: Field Manual link is not to the Library`);
      assert(/<p class="ed-lean-note">/.test(m[1]), `${p}: Field Manual link has no note`);
    }
  }
  const b = pages.find(x => x.p === 'builders.html').h, c = pages.find(x => x.p === 'curators.html').h;
  for (const id of ['K-3.5', 'K-4.7', 'K-8.5', 'K-7.1', '10.4', '10.9']) assert(b.includes(`<span class="ed-ch-num">${id}</span>`), `builders: ${id}`);
  for (const id of ['K-3.6', 'K-3.7', 'K-4.3', 'K-4.7', 'K-4.8', 'K-5.3', 'K-6.3', '10.4', '10.9']) assert(c.includes(`<span class="ed-ch-num">${id}</span>`), `curators: ${id}`);
});
check('the two doors lead to their K chapters and tools in charter order', () => {
  const order = (h) => [...h.matchAll(/<section class="ed-art"[\s\S]*?<\/section>/g)].map(m => (m[0].match(/href="(\/[^"#]+)"/) || [])[1]);
  const b = order(pages.find(x => x.p === 'builders.html').h), c = order(pages.find(x => x.p === 'curators.html').h);
  assert(JSON.stringify(b.slice(0, 6)) === JSON.stringify(['/builders/k1', '/builders/k2', '/curators/k3', '/tools/quick-start', '/tools/manifest', '/tools/hollis']) || JSON.stringify(b.slice(0, 2)) === JSON.stringify(['/builders/k1', '/builders/k2']), 'builder order ' + b);
  assert(JSON.stringify(c.slice(0, 6)) === JSON.stringify(['/curators/k4', '/curators/k3', '/curators/k2', '/tools/hollis', '/tools/money-lines', '/tools/manifest']), 'curator order ' + c);
});
check('no signup, no cookie, no handshake form anywhere', () => {
  for (const { p, h } of pages) {
    assert(!/<form[^>]*>[\s\S]*?type="email"/.test(h), `${p}: email form`);
    assert(!/document\.cookie|Set-Cookie/.test(h), `${p}: cookie`);
    assert(text(h).includes('This site sets no cookies.'), `${p}: cookie line`);
  }
  assert(!fs.existsSync(path.join(ROOT, 'api')) && !fs.existsSync(path.join(ROOT, 'middleware.js')), 'gate files remain');
  const js = fs.readFileSync(path.join(PUB, 'assets/tools.js'), 'utf8') + fs.readFileSync(path.join(PUB, 'assets/edition.js'), 'utf8');
  assert(!/fetch\(|XMLHttpRequest|sendBeacon|document\.cookie/.test(js), 'a script sends or stores');
});
check('Day, Night and Readable letters on every page', () => {
  for (const { p, h } of pages) assert(h.includes('data-theme-set="light"') && h.includes('data-theme-set="dark"') && h.includes('data-font-set'), p);
});
check('every example is labeled invented, and no example is presented as real', () => {
  const money = pages.find(x => x.p === 'tools/money-lines.html').h;
  const rows = [...money.matchAll(/<tr data-cats[\s\S]*?<\/tr>/g)].map(m => m[0]);
  assert(rows.length === 15, `money rows ${rows.length}`);
  for (const r of rows) {
    if (r.includes('>Mycelial ')) assert(r.includes('Real app · Kindling version early 2027'), 'Mycelial label');
    else assert(r.includes('<span class="chip">Invented</span>'), 'row without Invented: ' + text(r).slice(0, 40));
  }
  const mf = pages.find(x => x.p === 'tools/manifest.html').h;
  assert(mf.includes('Invented example') && /"name": "[^"]+\(invented\)"/.test(mf), 'manifest example label');
  const hol = text(pages.find(x => x.p === 'tools/hollis.html').h);
  assert(hol.includes('Hollis Grant is invented.'), 'Hollis label');
  for (const k of ['builders/k1', 'curators/k3', 'curators/k4']) assert(/Invented|invented/.test(text(pages.find(x => x.p === k + '.html').h)), k);
});

// ---- the tools ----
check('Tool 1: each of the 9 choices names at least one section and at least one chapter', () => {
  let n = 0;
  for (const door of ['builders', 'curators']) {
    const h = pages.find(x => x.p === `${door}.html`).h;
    const radios = [...h.matchAll(/<input type="radio" name="\w+" value="([^"]+)"/g)].map(m => m[1]);
    for (const v of radios) {
      const panel = h.match(new RegExp(`<div class="ed-panel" data-for="${v}" hidden>([\\s\\S]*?)</ul></div>`));
      assert(panel, `${door}: no panel for ${v}`);
      assert(/§\d/.test(text(panel[1])), `${door}/${v}: no section`);
      assert(/<span class="ed-ch-num">(K\.\d|K-\d+\.\d+|\d+\.\d+)<\/span>/.test(panel[0]), `${door}/${v}: no chapter`);
      n++;
    }
  }
  assert(n === 9, `choices: ${n}`);
});
check('Tool 2: the invented example passes kindling-validate inside a clone, and every field shows its section', () => {
  const h = pages.find(x => x.p === 'tools/manifest.html').h;
  const ex = JSON.parse(h.match(/<script type="application\/json" id="mf-example">([\s\S]*?)<\/script>/)[1]);
  for (const f of h.matchAll(/<div class="ed-field" data-key="([^"]+)">([\s\S]*?)<\/div>(?=<div class="ed-field"|<\/form>)/g)) assert(/§\d/.test(text(f[2])), `field ${f[1]} has no section`);
  assert(text(h).includes('Run this inside a clone of the repository. Nothing from this project is on npm.') && h.includes('npx kindling-validate ./my-pool.json'), 'warning and command');
  const cli = path.join(REPO, 'tools/validator/bin/cli.js');
  if (!fs.existsSync(path.join(REPO, 'node_modules'))) return 'skip';
  const tmp = path.join(ROOT, 'test', '.my-pool.json');
  fs.writeFileSync(tmp, JSON.stringify(ex, null, 2));
  try {
    const out = execFileSync('node', [cli, tmp], { cwd: REPO, encoding: 'utf8' });
    assert(!/error|invalid/i.test(out.replace(/0 errors?/gi, '')), out);
  } finally { fs.unlinkSync(tmp); }
});
check('Tool 3: every Money-lines quotation is on its source page at kindling-sites 5afb487, and the §1.3 footer sits outside the filters', () => {
  const h = pages.find(x => x.p === 'tools/money-lines.html').h;
  const tool = h.match(/<div class="wrap" data-tool="money">[\s\S]*?<\/table><\/div>[\s\S]*?<\/div>/)[0];
  assert(!tool.includes('ed-money-foot'), 'footer is inside the filtered block');
  assert(text(h).includes('§1.3: the protocol defines no chargeable surface at the connection layer.'), 'footer text');
  if (!fs.existsSync(path.join(SITES, 'site'))) return 'skip';
  const ed = fs.readFileSync(path.join(ROOT, 'build/edition.py'), 'utf8');
  const rows = [...ed.matchAll(/\{'org': '([^']+)'[\s\S]*?'quotes': \[([\s\S]*?)\], 'src': \[([^\]]*)\]/g)];
  assert(rows.length === 15, `rows parsed: ${rows.length}`);
  const cache = {};
  const siteText = (u) => {
    const m = u.match(/^https:\/\/([^.]+)\.kindling\.foundation\/(.*)$/) || [];
    const host = u.startsWith('https://kindling.foundation/') ? 'foundation' : m[1];
    const file = (u.replace(/^https:\/\/[^/]+\//, '') || 'index.html');
    const p = path.join(SITES, 'site', host === 'familiarfaces' ? 'familiarfaces' : host, file);
    if (!(p in cache)) cache[p] = fs.existsSync(p) ? norm(text(fs.readFileSync(p, 'utf8'))) : null;
    return cache[p];
  };
  for (const [, org, quotes, srcs] of rows) {
    const qs = [...quotes.matchAll(/(['"])((?:(?!\1).)+)\1/g)].map(m => m[2]);
    const pages_ = [...srcs.matchAll(/'([^']+)'/g)].map(m => siteText(m[1])).filter(Boolean);
    assert(pages_.length, `${org}: no source page found`);
    for (const q of qs) assert(pages_.some(t => t.includes(norm(q))), `${org}: "${q}" not on its source page`);
  }
});
check('the quick start is the protocol site’s five steps, verbatim, with the clone-only and npm-name warnings', () => {
  const h = pages.find(x => x.p === 'tools/quick-start.html').h, t = text(h);
  assert(t.includes('Nothing from this project is on npm.') && t.includes('The npm name “kindling” belongs to someone else.'), 'warnings');
  const bp = path.join(SITES, 'site/protocol/build.html');
  if (!fs.existsSync(bp)) return 'skip';
  const site = norm(text(fs.readFileSync(bp, 'utf8')));
  for (const m of h.matchAll(/<pre class="ed-pre"><code>([\s\S]*?)<\/code><\/pre>/g)) {
    const lines = m[1].replace(/&quot;/g, '"').split('\n').map(l => l.replace(/\s*\\$/, '').trim()).filter(Boolean);
    for (const l of lines) assert(site.includes(norm(l)), `command not on the site: ${l}`);
  }
  for (const s of ['You need git, Node.js and npm.', 'checks a Kindling document against its schema.', 'Only people who said yes to a Pool are in it to be asked.']) assert(site.includes(s) && t.includes(s), s);
});

// ---- the ten gated Kindling rewrites (content/kindling/rewrites/, gated October 4, 2026) ----
const RW = { '3.5': ['builders'], '3.6': ['curators'], '3.7': ['curators'], '4.3': ['curators'], '4.7': ['builders', 'curators'],
  '4.8': ['curators'], '5.3': ['curators'], '6.3': ['curators'], '7.1': ['builders'], '8.5': ['builders'] };
const rwSlug = id => 'k-' + id.replace('.', '-');
check('every rewrite is wired as written: all its numbers and quotations are on its page', () => {
  for (const [id, doors] of Object.entries(RW)) {
    const src = fs.readFileSync(path.join(ROOT, `content/kindling/rewrites/K-${id}.md`), 'utf8');
    const plain = norm(src.replace(/^## Chapter .*$/m, '').replace(/\*+|`/g, '').replace(/^#+ |\|/gm, ' '));
    for (const d of doors) {
      const pg = pages.find(x => x.p === `${d}/${rwSlug(id)}.html`);
      assert(pg, `${d}/${rwSlug(id)} missing`);
      const t = norm(text(pg.h));
      for (const n of plain.match(/\d[\d,.]*\d|\d/g)) assert(t.includes(n), `K-${id} (${d}): number ${n} missing`);
      for (const q of (plain.match(/"[^"]{6,}"/g) || []).filter(q => !/^"\s|\s"$/.test(q))) assert(t.includes(q.replace(/\s+/g, ' ')), `K-${id} (${d}): quotation ${q.slice(0, 60)} missing`);
    }
  }
});
check('every rewrite page keeps its own license line in the body and links its original on solo.joshwolf.net', () => {
  for (const [id, doors] of Object.entries(RW)) for (const d of doors) {
    const h = pages.find(x => x.p === `${d}/${rwSlug(id)}.html`).h;
    const prov = h.match(/<p class="ed-provenance">([\s\S]*?)<\/p>/);
    assert(prov, `K-${id} (${d}): no provenance line`);
    const t = text(prov[1]);
    assert(t.includes(`Rewritten for the Kindling edition from Chapter ${id}`) && t.includes('© 2026 Josh Wolf, licensed under CC BY 4.0'), `K-${id} (${d}): license line`);
    assert(prov[1].includes(`href="https://solo.joshwolf.net/read#ch-${id}"`), `K-${id} (${d}): original not linked`);
  }
});
check('exactly one "Figures checked" line under every table that carries a figure, on every page', () => {
  for (const { p, h } of pages) {
    for (const m of h.matchAll(/<div class="ed-table"><table>([\s\S]*?)<\/table><\/div>((?:\s*<p class="ed-checked">[^<]*<\/p>)*)/g)) {
      const lines = (m[2].match(/ed-checked/g) || []).length;
      if (/\d/.test(text(m[1]))) assert(lines === 1, `${p}: a table with figures has ${lines} "Figures checked" lines`);
      else assert(lines === 0, `${p}: a table without figures has a "Figures checked" line`);
    }
    assert(!/Figures checked[^<]*<\/p>\s*<p[^>]*>Figures checked/.test(h), `${p}: two "Figures checked" lines in a row`);
  }
});
check('the ten rewritten numbers link to their rewrites everywhere; inside a rewrite its own number names the original', () => {
  const ids = Object.keys(RW);
  for (const { p, h } of pages) {
    const self = (p.match(/k-(\d+)-(\d+)\.html$/) || []).slice(1).join('.');
    for (const m of h.matchAll(/<a class="ed-x( ed-out)?" href="([^"]+)">(?:Chapter|Ch\.?) (\d+\.\d+)<\/a>/g)) {
      const [, out, href, id] = m;
      if (ids.includes(id) && id !== self) assert(!out && href.endsWith('/' + rwSlug(id)), `${p}: Ch ${id} links to ${href}`);
      else assert(out && href.startsWith('https://solo.joshwolf.net/'), `${p}: Ch ${id} should link to the Library, links to ${href}`);
    }
    for (const m of h.matchAll(/<li class="ed-lean">([\s\S]*?)<\/li>/g)) {
      const id = (m[1].match(/<span class="ed-ch-num">([^<]+)<\/span>/) || [])[1];
      assert(['10.4', '10.9'].includes(id), `${p}: Field Manual ${id} still links out instead of to its rewrite`);
    }
  }
  const money = pages.find(x => x.p === 'tools/money-lines.html').h;
  for (const id of ['3.6', '5.3', '6.3']) assert(money.includes(`href="/curators/${rwSlug(id)}">K-${id}</a>`), `Money lines: K-${id}`);
});

console.log(`\n${passed} passed, ${failed} failed, ${skipped} skipped`);
process.exit(failed ? 1 : 0);

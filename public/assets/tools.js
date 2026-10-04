/* The edition's tools. Everything happens in the page. Nothing is sent, nothing is stored, nothing is scored. */
(function () {
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }

  /* Tool 1: the chooser. Coming back to the page starts from nothing chosen. */
  function chooser(root) {
    function show() {
      var picked = $('input[type=radio]:checked', root);
      $$('.ed-panel', root).forEach(function (p) { p.hidden = !picked || p.getAttribute('data-for') !== picked.value; });
    }
    function reset() { $$('input[type=radio]', root).forEach(function (i) { i.checked = false; }); show(); }
    root.addEventListener('change', show);
    window.addEventListener('pageshow', reset);
    reset();
  }

  /* Tool 3: the Money lines. Filters hide rows; the §1.3 footer sits outside the filtered area. */
  function money(root) {
    var cats = [], ch = $('[data-ch]', root), never = $('[data-never]', root), empty = $('[data-empty]', root);
    function apply() {
      var shown = 0;
      $$('tbody tr', root).forEach(function (tr) {
        var rc = (tr.getAttribute('data-cats') || '').split(' ');
        var rch = (tr.getAttribute('data-chapters') || '').split(' ');
        var ok = (!cats.length || cats.some(function (c) { return rc.indexOf(c) >= 0; })) && (!ch.value || rch.indexOf(ch.value) >= 0);
        tr.hidden = !ok; if (ok) shown++;
      });
      root.classList.toggle('ed-money-hide', !never.checked);
      empty.hidden = shown > 0;
    }
    $$('[data-cat]', root).forEach(function (b) {
      b.addEventListener('click', function () {
        var c = b.getAttribute('data-cat'), i = cats.indexOf(c);
        if (i >= 0) cats.splice(i, 1); else cats.push(c);
        b.setAttribute('aria-pressed', String(i < 0));
        apply();
      });
    });
    $$('[data-clear]', root).forEach(function (b) {
      b.addEventListener('click', function () {
        cats = []; ch.value = ''; never.checked = true;
        $$('[data-cat]', root).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        apply();
      });
    });
    ch.addEventListener('change', apply);
    never.addEventListener('change', apply);
    window.addEventListener('pageshow', function () { never.checked = true; apply(); });
    apply();
  }

  /* Tool 2: the manifest walkthrough. Builds the JSON as you type and checks the shapes the schema states. */
  function manifest(root) {
    var form = $('form', root), out = $('[data-json]', root), check = $('[data-check]', root);
    var example = JSON.parse(document.getElementById('mf-example').textContent);
    function field(path) { return $('[data-f="' + path + '"]', form); }
    function val(path) { var el = field(path); if (!el) return ''; return el.type === 'checkbox' ? el.checked : el.value.trim(); }
    function load(m) {
      $$('[data-f]', form).forEach(function (el) { if (el.type === 'checkbox') el.checked = false; else el.value = el.tagName === 'SELECT' ? el.options[0].value : ''; });
      if (!m) return update();
      field('name').value = m.name || '';
      var c = (m.curator || [])[0] || {};
      field('curator.identity').value = c.identity || '';
      field('curator.display_name').value = c.display_name || '';
      field('curator.verification_level').value = c.verification_level || 'email';
      field('intent_tags').value = (m.intent_tags || []).join(', ');
      field('visibility').value = m.visibility || 'public';
      field('consent_model').value = m.consent_model || 'universal-opt-in';
      field('curator_contact').value = m.curator_contact || '';
      field('charter').value = m.charter || '';
      update();
    }
    function build() {
      var m = { schema_version: '0.1' };
      m.name = val('name');
      var cur = { identity: val('curator.identity'), verification_level: val('curator.verification_level'), primary: true };
      if (val('curator.display_name')) cur.display_name = val('curator.display_name');
      m.curator = [cur];
      m.intent_tags = val('intent_tags').split(',').map(function (s) { return s.trim(); }).filter(Boolean);
      m.visibility = val('visibility');
      m.consent_model = val('consent_model');
      m.curator_contact = val('curator_contact');
      m.charter = val('charter');
      var w = val('handshake_window_days');
      if (w !== '') m.handshake_window_days = parseInt(w, 10);
      var g = {};
      ['city', 'region', 'country'].forEach(function (k) { if (val('geographic_scope.' + k)) g[k] = val('geographic_scope.' + k); });
      if (val('geographic_scope.online')) g.online = true;
      if (Object.keys(g).length) m.geographic_scope = g;
      var bl = val('messaging_preferences.block_list_subscriptions').split(/\s+/).filter(Boolean);
      if (bl.length) m.messaging_preferences = { block_list_subscriptions: bl };
      m.entries = [];
      return m;
    }
    function problems(m) {
      var p = [];
      if (!m.name) p.push('name needs at least 1 character (§3.2)');
      if (!m.curator[0].identity) p.push('curator needs an identity (§3.2)');
      if (!m.intent_tags.length) p.push('intent_tags needs at least 1 tag (§3.2)');
      if (!m.curator_contact) p.push('curator_contact is required (§3.2)');
      if (m.charter.length < 20) p.push('charter needs at least 20 characters (§3.2)');
      if ('handshake_window_days' in m && !(m.handshake_window_days >= 1)) p.push('handshake_window_days must be a whole number of at least 1 (§5.2)');
      if (m.messaging_preferences && m.messaging_preferences.block_list_subscriptions.some(function (u) { return !/^https?:\/\//.test(u); })) p.push('block list subscriptions must be URLs (§3.3)');
      return p;
    }
    function update() {
      var m = build();
      out.textContent = JSON.stringify(m, null, 2);
      var p = problems(m);
      check.textContent = p.length ? 'Not yet valid: ' + p.join('; ') + '.' : 'The required fields are filled in the shapes the schema states. Run the validator to be sure.';
      check.classList.toggle('ed-bad', p.length > 0);
      ['visibility', 'consent_model'].forEach(function (k) {
        $$('[data-note-for="' + k + '"]', form).forEach(function (n) { n.hidden = n.getAttribute('data-v') !== val(k); });
      });
    }
    form.addEventListener('input', update);
    form.addEventListener('change', update);
    $('[data-reset]', root).addEventListener('click', function () { load(example); });
    $('[data-empty]', root).addEventListener('click', function () { load(null); });
    $('[data-download]', root).addEventListener('click', function () {
      var blob = new Blob([out.textContent + '\n'], { type: 'application/json' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = 'my-pool.json';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    });
    load(example);
    window.KindlingManifest = { build: build, problems: problems };
  }

  document.addEventListener('DOMContentLoaded', function () {
    $$('[data-tool="chooser"]').forEach(chooser);
    $$('[data-tool="money"]').forEach(money);
    $$('[data-tool="manifest"]').forEach(manifest);
  });
})();

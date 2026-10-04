/* Day, Night and Readable letters. Kept in this browser only; nothing is sent and no cookie is set.
   Same keys and attributes as the Kindling sites (tt-theme, data-theme, data-font). */
(function () {
  var root = document.documentElement;
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function put(k, v) { try { if (v == null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} }

  var t = get('tt-theme');
  if (t === 'light' || t === 'dark') root.setAttribute('data-theme', t);
  if (get('tt-font') === 'readable') root.setAttribute('data-font', 'readable');
  root.classList.add('js');

  function sync() {
    var theme = root.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
    document.querySelectorAll('[data-theme-set]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-theme-set') === theme));
    });
    document.querySelectorAll('[data-font-set]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(root.getAttribute('data-font') === 'readable'));
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', theme === 'light' ? '#E9E8EF' : '#16121F');
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-theme-set]').forEach(function (b) {
      b.addEventListener('click', function () {
        var v = b.getAttribute('data-theme-set');
        root.setAttribute('data-theme', v);
        put('tt-theme', v);
        sync();
      });
    });
    document.querySelectorAll('[data-font-set]').forEach(function (b) {
      b.addEventListener('click', function () {
        var on = root.getAttribute('data-font') !== 'readable';
        if (on) root.setAttribute('data-font', 'readable'); else root.removeAttribute('data-font');
        put('tt-font', on ? 'readable' : null);
        sync();
      });
    });
    var mb = document.querySelector('.menu-btn');
    if (mb) mb.addEventListener('click', function () {
      var open = mb.getAttribute('aria-expanded') !== 'true';
      mb.setAttribute('aria-expanded', String(open));
      var h = mb.closest('header.site'); if (h) h.classList.toggle('open', open);
    });
    sync();
  });
})();

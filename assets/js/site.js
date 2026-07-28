/* combinatorics.in — theme toggle, KaTeX, and the lozenge-flip hero.
   Everything here is an enhancement: the site is fully readable without it. */
(function () {
  'use strict';

  /* ---------------------------------------------------------- theme ---- */
  var root = document.documentElement;
  var btn = document.getElementById('theme');
  var label = document.getElementById('themelabel');

  function syncTheme() {
    var dark = root.dataset.theme === 'dark';
    if (label) label.textContent = dark ? 'Light' : 'Dark';
    if (btn) btn.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
    if (window.__drawTiling) window.__drawTiling();
  }

  if (btn) {
    btn.addEventListener('click', function () {
      root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('theme', root.dataset.theme); } catch (e) { /* private mode */ }
      syncTheme();
    });
  }

  /* ---------------------------------------------------------- KaTeX ---- */
  /* Write inline maths as \( ... \) and display maths as \[ ... \].
     Kramdown leaves both alone, so nothing needs escaping in Markdown. */
  window.addEventListener('load', function () {
    if (typeof renderMathInElement !== 'function') return;
    renderMathInElement(document.body, {
      delimiters: [
        { left: '\\[', right: '\\]', display: true },
        { left: '\\(', right: '\\)', display: false }
      ],
      ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
      throwOnError: false
    });
  });

  /* ------------------------------------------------- plane partition ---- */
  /* The hero SVG ships with a static first frame, so it is visible before
     this runs. From here we walk the lozenge-flip Markov chain on plane
     partitions in a 5x5x5 box, redrawing after each pair of flips. */
  var svg = document.getElementById('tiling');
  if (!svg) return;

  var NS = 'http://www.w3.org/2000/svg';
  var N = 5, C = 5, S = 22, OX = 110, OY = 126;
  var U = [Math.sqrt(3) / 2 * S, S / 2];
  var V = [-Math.sqrt(3) / 2 * S, S / 2];
  var W = [0, -S];

  function P(a, b, c) {
    return [OX + a * V[0] + b * U[0] + c * W[0],
            OY + a * V[1] + b * U[1] + c * W[1]];
  }

  var h = [];
  for (var i = 0; i < N; i++) {
    h.push([]);
    for (var j = 0; j < N; j++) h[i].push(Math.max(0, C - i - j));
  }

  var ceil = function (i, j) {
    return Math.min(i > 0 ? h[i - 1][j] : C, j > 0 ? h[i][j - 1] : C);
  };
  var floor = function (i, j) {
    return Math.max(i < N - 1 ? h[i + 1][j] : 0, j < N - 1 ? h[i][j + 1] : 0);
  };

  function flip() {
    for (var t = 0; t < 40; t++) {
      var a = Math.random() * N | 0, b = Math.random() * N | 0;
      var canAdd = h[a][b] + 1 <= ceil(a, b);
      var canRemove = h[a][b] - 1 >= floor(a, b);
      if (canAdd && canRemove) { h[a][b] += Math.random() < 0.5 ? 1 : -1; return; }
      if (canAdd) { h[a][b]++; return; }
      if (canRemove) { h[a][b]--; return; }
    }
  }

  window.__drawTiling = function () {
    var cs = getComputedStyle(root);
    var col = function (n) { return cs.getPropertyValue(n).trim(); };
    var stroke = col('--ground');

    function quad(pts, fill) {
      var e = document.createElementNS(NS, 'polygon');
      e.setAttribute('points', pts.map(function (p) {
        return p[0].toFixed(2) + ',' + p[1].toFixed(2);
      }).join(' '));
      e.setAttribute('fill', fill);
      e.setAttribute('stroke', stroke);
      e.setAttribute('stroke-width', '0.7');
      e.setAttribute('stroke-linejoin', 'round');
      svg.appendChild(e);
    }

    svg.textContent = '';
    quad([P(0, 0, 0), P(0, N, 0), P(N, N, 0), P(N, 0, 0)], col('--box-floor'));
    quad([P(0, 0, 0), P(N, 0, 0), P(N, 0, C), P(0, 0, C)], col('--box-right'));
    quad([P(0, 0, 0), P(0, N, 0), P(0, N, C), P(0, 0, C)], col('--box-left'));

    var cells = [];
    for (var a = 0; a < N; a++) for (var b = 0; b < N; b++) cells.push([a, b]);
    cells.sort(function (p, q) { return (p[0] + p[1]) - (q[0] + q[1]); });

    cells.forEach(function (cell) {
      var a = cell[0], b = cell[1], k = h[a][b];
      if (k === 0) return;
      var A = P(a, b, k), B = P(a, b + 1, k), Cc = P(a + 1, b + 1, k), D = P(a + 1, b, k);
      var drop = k * S;
      quad([D, Cc, [Cc[0], Cc[1] + drop], [D[0], D[1] + drop]], col('--facet-left'));
      quad([B, Cc, [Cc[0], Cc[1] + drop], [B[0], B[1] + drop]], col('--facet-right'));
      quad([A, B, Cc, D], col('--facet-top'));
    });
  };

  syncTheme();

  if (!window.matchMedia || !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    setInterval(function () { flip(); flip(); window.__drawTiling(); }, 1100);
  }
})();

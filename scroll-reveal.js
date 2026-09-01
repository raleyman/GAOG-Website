/* GAOG — scroll-reveal entrance motion.
   Load with <script src="/scroll-reveal.js" defer></script>, after the one
   inline <script>document.documentElement.classList.add('js');</script>
   that must be the first thing inside <head> on any page using this.

   Mark any container with class="reveal-group"; its direct children
   animate in the first time they scroll into view, once each, staggered
   left-to-right within their own visual row. */
(function () {
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('.reveal-group').forEach(function (group) {
    var kids = Array.prototype.slice.call(group.children);
    kids.forEach(function (el) { el.classList.add('reveal'); });

    // Stagger by VISUAL ROW so the sweep restarts left-to-right on each
    // row instead of continuing (or wrapping) across the whole grid.
    // Grouped by proximity rather than an exact offsetTop match — on this
    // site's own team strip, sub-pixel flex-basis math (calc(16.6667% -
    // 17px)) lands same-row items a pixel apart (measured: four items at
    // 405px, one at 404px), so an exact-equality grouping would wrongly
    // split that row into two and reveal two people at once instead of
    // sweeping cleanly across five.
    var ROW_TOLERANCE = 4; // px
    var rowTops = [];
    var rows = [];
    kids.forEach(function (el) {
      var top = el.offsetTop;
      var rowIndex = -1;
      for (var i = 0; i < rowTops.length; i++) {
        if (Math.abs(rowTops[i] - top) <= ROW_TOLERANCE) { rowIndex = i; break; }
      }
      if (rowIndex === -1) {
        rowTops.push(top);
        rows.push([el]);
      } else {
        rows[rowIndex].push(el);
      }
    });
    rows.forEach(function (row) {
      row.forEach(function (el, i) {
        el.style.setProperty('--reveal-i', Math.min(i, 7)); // cap so a long row doesn't crawl in for seconds
      });
    });
  });

  if (reduced || !('IntersectionObserver' in window)) {
    // Reduced motion, or a very old browser with no observer support:
    // reveal everything immediately rather than leaving it to a scroll
    // that may never trigger an observer.
    document.querySelectorAll('.reveal').forEach(function (el) {
      el.classList.add('is-visible');
    });
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target); // reveal once — re-triggering on every scroll up/down reads as busy, not polished
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
})();

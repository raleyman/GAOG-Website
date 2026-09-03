/* GAOG — scroll-reveal entrance motion.
   Load with <script src="/scroll-reveal.js" defer></script>, after the one
   inline <script>document.documentElement.classList.add('js');</script>
   that must be the first thing inside <head> on any page using this.

   Mark any container with class="reveal-group"; its direct children
   animate in the first time they scroll into view, once each, staggered
   left-to-right within their own visual row. */
(() => {
  var reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('.reveal-group').forEach((group) => {
    var kids = Array.prototype.slice.call(group.children);
    kids.forEach((el) => { el.classList.add('reveal'); });

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
    kids.forEach((el) => {
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
    rows.forEach((row) => {
      row.forEach((el, i) => {
        el.style.setProperty('--reveal-i', Math.min(i, 7)); // cap so a long row doesn't crawl in for seconds
      });
    });
  });

  if (reduced || !('IntersectionObserver' in window)) {
    // Reduced motion, or a very old browser with no observer support:
    // reveal everything immediately rather than leaving it to a scroll
    // that may never trigger an observer.
    document.querySelectorAll('.reveal').forEach((el) => {
      el.classList.add('is-visible');
    });
    return;
  }

  // Trigger right as the card starts crossing into the real viewport — no
  // advance lead. Round 3 gave it a 30%-of-viewport head start on the
  // theory that a fast flick would otherwise skip past a small margin
  // before the animation had time to play. Measured against actual scroll
  // speed, that assumption only held for a hard flick: at a normal,
  // deliberate scroll (the pace someone reviewing their own site
  // actually uses) the card was already ~93% revealed by the time it was
  // genuinely on screen, and ~60% done even at a moderate scroll — the
  // 30% lead gave the animation so much of a head start that it finished
  // before most visitors ever saw it move. Only a hard flick benefited,
  // and that's the least common case, not the one to optimize for.
  //
  // rootMargin 0 / a small threshold means the reveal starts the instant
  // the card is genuinely entering the viewport, so the motion plays out
  // ON SCREEN at any normal scroll pace. The one tradeoff: an extremely
  // fast flick can still outrun it and land with the card already
  // mostly revealed — acceptable, since that's true of any on-scroll
  // animation and it's a rare way to scroll anyway (Sept 2026, fourth
  // pass — measured across slow/moderate/fast scroll speeds before
  // shipping this time, not just reasoned about).
  var io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target); // reveal once — re-triggering on every scroll up/down reads as busy, not polished
      }
    });
  }, { threshold: 0.01, rootMargin: '0px' });

  document.querySelectorAll('.reveal').forEach((el) => { io.observe(el); });
})();

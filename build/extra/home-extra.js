
/* Industries: accessible tabs with keyboard support and deep links (#industries-<slug>). */
(() => {
  'use strict';
  const tabs = Array.from(document.querySelectorAll('.sector-tab'));
  if (!tabs.length) return;
  const panels = tabs.map((t) => document.getElementById(t.getAttribute('aria-controls')));
  const select = (i, focus) => {
    tabs.forEach((t, k) => {
      const on = k === i;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      panels[k].hidden = !on;
      panels[k].classList.toggle('is-on', on);
    });
    const t = tabs[i];
    const bar = t.parentElement;
    const left = t.offsetLeft - (bar.clientWidth - t.offsetWidth) / 2;
    try { bar.scrollTo({ left, behavior: 'smooth' }); } catch (e) { bar.scrollLeft = left; }
    if (focus) t.focus();
    if (window.ScrollTrigger) window.ScrollTrigger.refresh();
  };
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => select(i, false));
    t.addEventListener('keydown', (ev) => {
      const k = ev.key;
      let n = null;
      if (k === 'ArrowRight') n = (i + 1) % tabs.length;
      else if (k === 'ArrowLeft') n = (i - 1 + tabs.length) % tabs.length;
      else if (k === 'Home') n = 0;
      else if (k === 'End') n = tabs.length - 1;
      if (n !== null) { ev.preventDefault(); select(n, true); }
    });
  });
  const m = location.hash.match(/^#industries-(.+)$/);
  if (m) { const i = tabs.findIndex((t) => t.id === 'st-' + m[1]); if (i > -1) select(i, false); }
})();

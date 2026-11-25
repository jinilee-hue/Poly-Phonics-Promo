/* 시안 A · 클레이 월드 — extra UI on top of site.js: try-zone tabs, lesson-flow dials, chant → songs tab.
   Loaded (not deferred) before site.js, so the capture listener below runs before site.js's chant handler. */
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const showIn = el => $$('.reveal', el).forEach(r => r.classList.add('is-in'));

  /* ---------- 체험존 tabs ---------- */
  const tabs = $$('.tab[data-tab]');
  function openTab(name, focus) {
    tabs.forEach(t => {
      const on = t.dataset.tab === name;
      t.classList.toggle('is-on', on);
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      if (on && focus) t.focus();
    });
    $$('.panel[data-panel]').forEach(p => {
      const on = p.dataset.panel === name;
      p.hidden = !on;
      p.classList.toggle('is-on', on);
      if (on) showIn(p);
    });
    if (name !== 'songs') { const v = $('#video'); if (v && !v.paused) v.pause(); }
  }
  tabs.forEach(t => t.addEventListener('click', () => openTab(t.dataset.tab)));
  $('.tabs')?.addEventListener('keydown', e => {
    if (!['ArrowLeft', 'ArrowRight'].includes(e.key)) return;
    const i = tabs.findIndex(t => t.classList.contains('is-on'));
    const n = (i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length;
    openTab(tabs[n].dataset.tab, true);
  });
  // "챈트로 들어 보기" — show the songs panel before site.js scrolls to #songs and loads the chant
  document.addEventListener('click', e => { if (e.target.closest('[data-chant]')) openTab('songs'); }, true);

  /* ---------- lesson-flow dials ---------- */
  const dials = $$('.dial[data-step]');
  function openStep(n, focus) {
    dials.forEach(d => {
      const on = d.dataset.step === String(n);
      d.classList.toggle('is-on', on);
      d.setAttribute('aria-selected', String(on));
      d.tabIndex = on ? 0 : -1;
      if (on && focus) d.focus();
    });
    $$('.board[data-board]').forEach(b => {
      const on = b.dataset.board === String(n);
      b.hidden = !on;
      b.classList.toggle('is-on', on);
    });
  }
  dials.forEach(d => d.addEventListener('click', () => openStep(d.dataset.step)));
  $('.dials')?.addEventListener('keydown', e => {
    if (!['ArrowLeft', 'ArrowRight'].includes(e.key)) return;
    const i = dials.findIndex(d => d.classList.contains('is-on'));
    const n = (i + (e.key === 'ArrowRight' ? 1 : dials.length - 1)) % dials.length;
    openStep(dials[n].dataset.step, true);
  });

  /* ---------- print: every panel and board ---------- */
  addEventListener('beforeprint', () => $$('.panel, .board').forEach(showIn));

  if (reduce) document.documentElement.classList.add('reduce');
})();

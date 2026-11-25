/* 시안 D — showcase extras on top of site.js: hero tablet video, sticky lesson screens, unit carousel. */
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* hero tablet: muted ABC Song loop, only while on screen */
  const hv = $('.hero-video');
  if (hv) {
    if (reduce) { hv.removeAttribute('autoplay'); hv.pause(); }
    else {
      new IntersectionObserver(([e]) => {
        if (e.isIntersecting) hv.play().catch(() => {}); else hv.pause();
      }, { threshold: 0.15 }).observe(hv);
    }
  }

  /* lesson flow: the step in the middle of the viewport drives the sticky tablet */
  const steps = $$('.fstep');
  const screens = $$('.fscreen');
  const names = ['Picture Match', 'Sound Chant 1', 'Sound Chant 3', 'Trace and Write', 'G-Learning 게임', 'Fluency Check'];
  const fcNo = $('#fcNo'), fcT = $('#fcT'), fcBar = $('#fcBar');
  function setStep(i) {
    steps.forEach(s => s.classList.toggle('is-on', +s.dataset.i === i));
    screens.forEach(s => s.classList.toggle('is-on', +s.dataset.i === i));
    if (fcNo) fcNo.textContent = String(i + 1).padStart(2, '0');
    if (fcT) fcT.textContent = names[i] || '';
    if (fcBar) fcBar.style.transform = `scaleX(${(i + 1) / steps.length})`;
  }
  const stepObs = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) setStep(+e.target.dataset.i); }),
    { rootMargin: '-45% 0px -45% 0px' });
  steps.forEach(s => stepObs.observe(s));

  /* mobile: step 06 gets its own copy of the Fluency Check screen */
  const flu = $('#fluency'), slot = $('.fshot-m[data-clone="fluency"]');
  if (flu && slot) { const c = flu.cloneNode(true); c.removeAttribute('id'); slot.appendChild(c); }

  /* unit carousel arrows */
  const units = $('#units');
  if (units) {
    const cards = $$('.unit', units);
    const prev = $('.car-btn[data-dir="-1"]'), next = $('.car-btn[data-dir="1"]');
    const step = () => (cards[1] ? cards[1].offsetLeft - cards[0].offsetLeft : 360);
    $$('.car-btn').forEach(b => b.addEventListener('click', () => units.scrollBy({ left: step() * +b.dataset.dir, behavior: reduce ? 'auto' : 'smooth' })));
    const edge = new IntersectionObserver(es => es.forEach(e => {
      if (e.target === cards[0]) prev.disabled = e.isIntersecting;
      if (e.target === cards[cards.length - 1]) next.disabled = e.isIntersecting;
    }), { root: units, threshold: 0.9 });
    edge.observe(cards[0]); edge.observe(cards[cards.length - 1]);
  }

  /* print: hero video → poster image (handled in CSS); pause it */
  addEventListener('beforeprint', () => { if (hv) hv.pause(); });
})();

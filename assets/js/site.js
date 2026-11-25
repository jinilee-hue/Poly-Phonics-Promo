/* POLY Phonics parent page — sounds, Lesson 1 sound sort, video playlist, game filter, share. No build. */
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- official lesson-pack audio ---------- */
  const cache = {};
  let current = null;
  function say(name, el) {
    const a = cache[name] || (cache[name] = new Audio(`assets/audio/${name}.mp3`));
    if (current && current !== a) { current.pause(); current.currentTime = 0; }
    pauseVideo();
    a.currentTime = 0;
    a.play().catch(() => {});
    current = a;
    if (el) { el.classList.remove('is-playing'); void el.offsetWidth; el.classList.add('is-playing'); setTimeout(() => el.classList.remove('is-playing'), 1400); }
    return a;
  }
  $$('[data-say]').forEach(b => b.addEventListener('click', () => {
    say(b.dataset.say, b);
    if (b.classList.contains('sound-chip')) bopFriends();
  }));
  function bopFriends() {
    const f = $('.friends'); if (!f || reduce) return;
    f.classList.remove('bop'); void f.offsetWidth; f.classList.add('bop');
  }

  /* ---------- nav: glass state + mobile sheet ---------- */
  const nav = $('#nav');
  const hero = $('.hero');
  new IntersectionObserver(([e]) => nav.classList.toggle('is-scrolled', !e.isIntersecting), { rootMargin: '-80px 0px 0px 0px' }).observe(hero);
  const sheet = $('#sheet'), menuBtn = $('.nav-menu');
  const openSheet = on => { sheet.hidden = !on; menuBtn.setAttribute('aria-expanded', String(on)); document.body.style.overflow = on ? 'hidden' : ''; };
  menuBtn.addEventListener('click', () => openSheet(true));
  $('.sheet-close').addEventListener('click', () => openSheet(false));
  $$('#sheet a').forEach(a => a.addEventListener('click', () => openSheet(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape' && !sheet.hidden) openSheet(false); });
  // current section highlight
  const links = $$('.nav-links a');
  const secObs = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    links.forEach(a => a.classList.toggle('is-on', a.getAttribute('href') === '#' + e.target.id));
  }), { rootMargin: '-45% 0px -50% 0px' });
  ['why', 'curriculum', 'flow', 'try', 'faq'].forEach(id => { const s = document.getElementById(id); if (s) secObs.observe(s); });

  /* ---------- reveal on scroll ---------- */
  const rev = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('is-in'); rev.unobserve(e.target); }
  }), { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  $$('.reveal').forEach(el => rev.observe(el));
  // print: show everything
  addEventListener('beforeprint', () => {
    $$('.reveal').forEach(el => el.classList.add('is-in'));
    $$('.qa').forEach(d => { d.dataset.wasOpen = d.open ? '1' : ''; d.open = true; });   // FAQ answers print open
  });
  addEventListener('afterprint', () => $$('.qa').forEach(d => { d.open = !!d.dataset.wasOpen; }));

  /* ---------- curriculum level chips ---------- */
  const notes = {
    k: '지금 보고 있는 과정 · <b>5세 Level K</b> — 입학 첫 레슨은 <b>Lesson 1 · Mm</b>입니다.',
    a: '<b>6세 Level A</b> — K에서 익힌 소리로 단어와 문장, 이야기를 읽어요. 아래는 5세 Level K 과정입니다.',
    b: '<b>7세 Level B</b> — A 다음 단계로 읽기를 넓혀 가요. 아래는 5세 Level K 과정입니다.'
  };
  $$('.level').forEach(btn => btn.addEventListener('click', () => {
    $$('.level').forEach(b => { b.classList.toggle('is-on', b === btn); b.setAttribute('aria-selected', String(b === btn)); });
    $('#levelNote').innerHTML = notes[btn.dataset.level];
    $('.units').classList.toggle('dim', btn.dataset.level !== 'k');
  }));

  /* ---------- Lesson 1 sound sort (SB p14 Say It: mop man doll heart moon mitt) ---------- */
  const SORT = [
    { w: 'mop', m: true, str: 'mmm…mop' },
    { w: 'man', m: true, str: 'mmm…man' },
    { w: 'doll', m: false, str: 'd-d-doll', first: '/d/' },
    { w: 'heart', m: false, str: 'h-h-heart', first: '/h/' },
    { w: 'moon', m: true, str: 'mmm…moon' },
    { w: 'mitt', m: true, str: 'mmm…mitt' }
  ];
  const box = $('#sortCards'), msg = $('#sortMsg'), count = $('#sortCount b');
  const found = new Set();
  SORT.forEach((it, i) => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'scard';
    b.setAttribute('aria-label', `${it.w} 듣기`);
    b.innerHTML = `<span class="num">${i + 1}</span><img src="assets/img/words/${it.w}.webp" alt="" loading="lazy" decoding="async">`
      + `<span class="w" lang="en">${it.m ? '<b>m</b>' + it.w.slice(1) : it.w}</span><span class="ok" aria-hidden="true"><svg class="ic"><use href="#i-check"/></svg></span>`;
    b.addEventListener('click', () => {
      say(it.w);
      if (it.m) {
        const first = !found.has(it.w);
        found.add(it.w); b.classList.add('is-found');
        count.textContent = found.size;
        if (found.size === 4) {
          msg.className = 'sort-msg win';
          msg.innerHTML = '잘했어요! <span class="en">mop · man · moon · mitt</span> 모두 /m/로 시작해요';
          if (first) { const r = b.getBoundingClientRect(); confetti(r.left + r.width / 2, r.top + r.height / 2); }
        } else {
          msg.className = 'sort-msg';
          msg.innerHTML = `<span class="en">${it.str}</span> — /m/로 시작해요!`;
        }
      } else {
        b.classList.remove('is-no'); void b.offsetWidth; b.classList.add('is-no');
        msg.className = 'sort-msg';
        msg.innerHTML = `<span class="en">${it.str}</span> — ${it.first} 소리로 시작해요. 다시 들어 볼까요?`;
      }
    });
    box.appendChild(b);
  });
  function confetti(x, y) {
    if (reduce) return;
    const colors = ['var(--c-blue)', 'var(--c-orange)', 'var(--c-yellow)', 'var(--c-teal)'];
    for (let i = 0; i < 28; i++) {
      const p = document.createElement('i');
      p.className = 'burst';
      const ang = Math.random() * Math.PI * 2, dist = 80 + Math.random() * 140;
      p.style.cssText = `left:${x}px;top:${y}px;background:${colors[i % 4]};--dx:${Math.cos(ang) * dist}px;--dy:${Math.sin(ang) * dist - 60}px;--rot:${Math.random() * 540}deg`;
      document.body.appendChild(p);
      setTimeout(() => p.remove(), 1100);
    }
  }

  /* ---------- video playlist ---------- */
  const video = $('#video'), screen = $('.screen'), playBtn = $('#screenPlay'), titleEl = $('#screenTitle');
  function pauseVideo() { if (video && !video.paused) video.pause(); }
  function load(btn, autoplay) {
    $$('.pl').forEach(b => b.classList.toggle('is-on', b === btn));
    const src = btn.dataset.src;
    video.poster = `assets/video/${src}.jpg`;
    video.src = `assets/video/${src}.mp4`;
    titleEl.textContent = btn.dataset.title;
    screen.classList.remove('is-playing');
    if (autoplay) { if (current) current.pause(); video.play().catch(() => {}); }
  }
  $$('.pl').forEach(b => b.addEventListener('click', () => load(b, true)));
  playBtn.addEventListener('click', () => { if (current) current.pause(); video.play().catch(() => {}); });
  video.addEventListener('play', () => { video.controls = true; screen.classList.add('is-playing'); });
  video.addEventListener('ended', () => {
    const list = $$('.pl'), i = list.findIndex(b => b.classList.contains('is-on'));
    if (i > 0 && i < list.length - 1) load(list[i + 1], true);   // chants 1→4 run on, like "All together"
    else screen.classList.remove('is-playing');
  });
  $$('[data-chant]').forEach(b => b.addEventListener('click', () => {
    const target = $(`.pl[data-src="l1-chant-${b.dataset.chant}"]`);
    $('#songs').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    load(target, true);
  }));

  /* ---------- game filter ---------- */
  $$('.filter').forEach(f => f.addEventListener('click', () => {
    $$('.filter').forEach(x => x.classList.toggle('is-on', x === f));
    $$('#gameCards .card').forEach(c => c.classList.toggle('is-hidden', f.dataset.f !== 'all' && c.dataset.kind !== f.dataset.f));
  }));

  /* ---------- share ---------- */
  const toast = $('#toast');
  function showToast(t) { toast.textContent = t; toast.classList.add('is-on'); clearTimeout(showToast.t); showToast.t = setTimeout(() => toast.classList.remove('is-on'), 2200); }
  $('#shareBtn').addEventListener('click', async () => {
    const data = { title: 'POLY Phonics · 5세 파닉스', text: '노래·정규 수업·G-Learning 게임을 아이와 먼저 체험해 보세요.', url: location.href };
    try {
      if (navigator.share) { await navigator.share(data); return; }
      await navigator.clipboard.writeText(location.href);
      showToast('링크를 복사했어요');
    } catch (e) { if (e && e.name !== 'AbortError') showToast('주소창의 링크를 복사해 공유해 주세요'); }
  });
})();

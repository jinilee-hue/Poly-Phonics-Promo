/* Concept C extras: turn the hero letter tiles into rounded 3D dice (the logo is a rendered sprite).
   Each element keeps its own colours (read before conversion) and gets six faces;
   data-dice lists the letters, front face first. Runs after site.js. */
(() => {
  const FACES = ['front', 'right', 'back', 'left', 'top', 'bottom'];
  const FILLS = [1, 2, 3, 4, 5, 6].map(i => `<span class="dc-fill dc-f${i}"></span>`).join('');
  document.querySelectorAll('[data-dice]').forEach(el => {
    const cs = getComputedStyle(el);
    el.style.setProperty('--dc', cs.backgroundColor);
    el.style.setProperty('--di', cs.color);
    const letters = el.dataset.dice.split(' ');
    const faces = FACES.map((f, i) => `<span class="dc-face dc-${f}">${letters[i] || ''}</span>`).join('');
    el.innerHTML = `<span class="dice-cube"><span class="dc-core dc-cx"></span><span class="dc-core dc-cy"></span><span class="dc-core dc-cz"></span>${FILLS}${faces}</span>`;
    el.classList.add('dice');
    // stale stylesheet (no dice rules yet): put the plain letter back instead of showing six letters in a row
    if (getComputedStyle(el.firstElementChild).transformStyle !== 'preserve-3d') {
      el.classList.remove('dice'); el.textContent = letters[0]; return;
    }
    // tap/click on a hero die rolls it again (hover does it on desktop)
    if (!el.closest('a')) {
      el.style.pointerEvents = 'auto';
      el.addEventListener('click', () => {
        el.classList.remove('is-rolling'); void el.offsetWidth; el.classList.add('is-rolling');
      });
      el.addEventListener('animationend', e => { if (e.animationName === 'diceRoll') el.classList.remove('is-rolling'); });
    }
  });
})();

/* Word strips: the markup holds the word set twice and the strip slid by 50%, so on screens wider than one set
   (1920px+) a blank gap showed after "mitt". Clone the set until it covers the screen and slide by exactly one copy:
   -100%/copies of the strip's own width, so late-loading fonts can't throw the seam off. */
(() => {
  const SPEED = 31;   // px per second, same pace as before
  document.querySelectorAll('.mq-track').forEach(track => {
    const set = [...track.children].slice(0, track.children.length / 2);
    const fill = () => {
      while (track.children.length > set.length) track.lastElementChild.remove();
      const setW = track.scrollWidth;
      const copies = Math.max(2, Math.ceil(innerWidth / setW) + 2);
      for (let c = 1; c < copies; c++) set.forEach(n => track.appendChild(n.cloneNode(true)));
      track.style.setProperty('--shift', (100 / copies) + '%');
      track.style.animationDuration = (setW / SPEED).toFixed(1) + 's';
    };
    fill();
    document.fonts && document.fonts.ready.then(fill);
    let t; addEventListener('resize', () => { clearTimeout(t); t = setTimeout(fill, 200); });
  });
})();

/* Curriculum level chips: show that level's six units (site.js only dims the K units and rewrites the note). */
(() => {
  const panels = document.querySelectorAll('.units[data-level]');
  const k = document.querySelector('.units[data-level="k"]');
  const note = document.getElementById('levelNote');
  const NOTES = {
    k: '지금 보고 있는 과정 · <b>5세 Level K</b> — 입학 첫 레슨은 <b>Lesson 1 · Mm</b>입니다.',
    a: '지금 보고 있는 과정 · <b>6세 Level A</b> — 카드 아래 따옴표는 그 Unit에서 읽는 글이에요.',
    b: '지금 보고 있는 과정 · <b>7세 Level B</b> — 카드 아래 따옴표는 그 Unit에서 읽는 글이에요.'
  };
  // heading + intro follow the level (texts from the FPR K / A / B lesson topics)
  const HEAD = {
    k: ['5세 1년,', '소리를 하나씩 차근차근', 'Level K는 6개 Unit, 30개 레슨입니다.<br>Unit마다 다섯 소리를 배우고, 단모음으로 묶어 단어 읽기의 기초를 다집니다.'],
    a: ['6세 1년,', '소리에서 글 읽기로', 'Level A는 6개 Unit, 30개 레슨입니다.<br>짧은 모음에서 긴 모음, r 모음까지 넓히고, 레슨마다 짧은 글을 읽어요.'],
    b: ['7세 1년,', '긴 단어도 술술', 'Level B는 6개 Unit, 30개 레슨입니다.<br>긴 단어를 음절로 나눠 읽고, 레슨마다 글 두 편을 읽어요.']
  };
  const $id = id => document.getElementById(id);
  document.querySelectorAll('.level[data-level]').forEach(btn => btn.addEventListener('click', () => {
    const lv = btn.dataset.level;
    panels.forEach(p => { p.hidden = p.dataset.level !== lv; });
    if (k) k.classList.remove('dim');
    if (note) note.innerHTML = NOTES[lv];
    if ($id('curYear')) { $id('curYear').textContent = HEAD[lv][0]; $id('curHead').textContent = HEAD[lv][1]; $id('curLead').innerHTML = HEAD[lv][2]; }
    const shown = document.querySelector(`.units[data-level="${lv}"]`);
    if (shown) { shown.classList.remove('pop'); void shown.offsetWidth; shown.classList.add('pop'); shown.closest('.units-scroll')?.scrollTo({ left: 0 }); }
  }));
})();

/* G-Learning filter chips also filter the locked "more games" strip (site.js only handles the playable cards). */
(() => {
  document.querySelectorAll('.filter[data-f]').forEach(f => f.addEventListener('click', () => {
    document.querySelectorAll('.mg').forEach(m => m.classList.toggle('is-hidden', f.dataset.f !== 'all' && m.dataset.kind !== f.dataset.f));
  }));
})();

/* Lesson flow board: a dotted road through the numbered tokens in step order, a U-turn between rows,
   START before 01 and a goal flag after 06. Redrawn from the token positions on resize. */
(() => {
  const ol = document.querySelector('.flow .steps'); if (!ol) return;
  const NS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(NS, 'svg'); svg.setAttribute('class', 'flow-path'); svg.setAttribute('aria-hidden', 'true');
  ol.prepend(svg);
  const top = svg.cloneNode(); top.classList.add('flow-top'); ol.append(top);   // flag above the cards
  const draw = () => {
    const box = ol.getBoundingClientRect();
    const t = [...ol.querySelectorAll('.token')].map(el => {
      const r = el.getBoundingClientRect();
      return { cx: r.left - box.left + r.width / 2, cy: r.top - box.top + r.height / 2, r: r.width / 2 };
    });
    if (t.length < 2) return;
    let d = `M${t[0].cx} ${t[0].cy}`;
    for (let i = 1; i < t.length; i++) {
      const a = t[i - 1], b = t[i];
      if (Math.abs(b.cx - a.cx) < 4 && Math.abs(b.cy - a.cy) > 4 && t.some(o => Math.abs(o.cy - a.cy) < 4 && o !== a)) {
        // same column, next row (desktop U-turn on the outside edge)
        const right = a.cx > box.width / 2, out = (right ? 1 : -1) * Math.max(a.r + 34, 70);
        d += ` C${a.cx + out} ${a.cy} ${b.cx + out} ${b.cy} ${b.cx} ${b.cy}`;
      } else d += ` L${b.cx} ${b.cy}`;
    }
    const f = t[t.length - 1], s0 = t[0];
    const vertical = Math.abs(t[1].cx - s0.cx) < 4;
    // finish: a chunky checkered goal flag (sticker style) where the road ends
    const lastLi = [...ol.children].filter(n => n.tagName === 'LI').pop().getBoundingClientRect();
    const flag = vertical ? { x: f.cx, y: lastLi.bottom - box.top + 96 } : { x: f.cx - f.r - 54, y: f.cy + 22 };
    const dir = vertical ? 1 : -1;                                // desktop: flag points left, away from the cards
    d += ` L${flag.x} ${flag.y}`;
    // start: a START sticker badge with an arrow pointing down the road
    const start = vertical ? { x: Math.max(s0.cx, 50), y: s0.cy - s0.r - 34 } : { x: s0.cx - s0.r - 120, y: s0.cy };
    const pad = 90;
    svg.setAttribute('viewBox', `0 ${-pad} ${box.width} ${box.height + pad * 2}`);
    svg.style.top = (-pad) + 'px'; svg.style.height = (box.height + pad * 2) + 'px';
    const road = `M${s0.cx} ${s0.cy}` + d.replace(/^M[^LC]*/, ' ');   // dotted road starts at 01; START→01 is a solid arrow
    const P = vertical ? 62 : 40, W = 72, H = 48, sq = 12;      // pole height, flag size, checker size
    const fx = dir > 0 ? flag.x + 2 : flag.x - 2 - W, fy = flag.y - P - 40;
    let checks = '';
    for (let r = 0; r < H / sq; r++) for (let c = 0; c < W / sq; c++) if ((r + c) % 2)
      checks += `<rect x="${fx + c * sq}" y="${fy + r * sq}" width="${sq}" height="${sq}"/>`;
    const cloth = dir > 0 ? `M${fx} ${fy} h${W} c-6 ${H / 2} -6 ${H / 2} 0 ${H} h-${W}Z` : `M${fx + W} ${fy} h-${W} c6 ${H / 2} 6 ${H / 2} 0 ${H} h${W}Z`;
    const tagX = vertical ? flag.x - 12 : flag.x - 42, tagY = vertical ? flag.y + 14 : flag.y + 8;
    const flagSvg = `<g class="fp-goal">
        <ellipse class="fp-goal-shadow" cx="${flag.x}" cy="${flag.y + 4}" rx="28" ry="8"/>
        <path class="fp-flag-pole" d="M${flag.x} ${flag.y} V${fy - 4}"/>
        <circle class="fp-pole-cap" cx="${flag.x}" cy="${fy - 6}" r="6"/>
        <g class="fp-flag-wave" style="transform-origin: ${dir > 0 ? '0' : '100%'} 50%"><path class="fp-flag" d="${cloth}"/>
          <g class="fp-checks">${checks}</g><path class="fp-flag-line" d="${cloth}"/></g>
        <g class="fp-goal-tag"><rect x="${tagX}" y="${tagY}" width="84" height="32" rx="16"/><text x="${tagX + 42}" y="${tagY + 22}" text-anchor="middle">GOAL!</text></g>
      </g>`;
    const bx = start.x - 46, by = vertical ? start.y - 46 : start.y - 19;
    // solid arrow from the START badge to the 01 token
    const l0 = vertical ? { x: start.x, y: by + 38 + 6 } : { x: bx + 92 + 6, y: start.y };
    const l1 = vertical ? { x: s0.cx, y: s0.cy - s0.r - 8 } : { x: s0.cx - s0.r - 8, y: s0.cy };
    const head = vertical ? `M${l1.x - 9} ${l1.y - 11} L${l1.x} ${l1.y} L${l1.x + 9} ${l1.y - 11}` : `M${l1.x - 11} ${l1.y - 9} L${l1.x} ${l1.y} L${l1.x - 11} ${l1.y + 9}`;
    const arrow = `M${l0.x} ${l0.y} L${l1.x} ${l1.y} ${head}`;
    const startSvg = `<g class="fp-start"><rect class="fp-start-badge" x="${bx}" y="${by}" width="92" height="38" rx="19"/>
        <text x="${bx + 46}" y="${by + 26}" text-anchor="middle">START</text>
        <path class="fp-arrow" d="${arrow}"/></g>`;
    svg.innerHTML = `<path class="road" d="${road}"/>` + startSvg;
    top.setAttribute('viewBox', svg.getAttribute('viewBox')); top.style.top = svg.style.top; top.style.height = svg.style.height;
    top.innerHTML = flagSvg;
  };
  draw();
  addEventListener('resize', draw);
  document.fonts && document.fonts.ready.then(draw);
  new ResizeObserver(draw).observe(ol);
})();

/* Hero friends: lean toward the pointer (desktop) and cheer when tapped (site.js plays the word). */
(() => {
  const art = document.querySelector('.hero-art'); if (!art) return;
  const chars = [...art.querySelectorAll('.stk-char.char')];
  if (matchMedia('(hover: hover)').matches && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    let raf = 0;
    addEventListener('pointermove', e => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => chars.forEach(c => {
        const r = c.getBoundingClientRect(), cx = r.left + r.width / 2;
        const dx = Math.max(-1, Math.min(1, (e.clientX - cx) / (innerWidth * .5)));
        c.style.transform = `skewX(${(-dx * 3).toFixed(2)}deg) rotate(${(dx * 4).toFixed(2)}deg)`;
      }));
    });
  }
  chars.forEach(c => {
    const hit = c.querySelector('.char-hit'); if (!hit) return;
    hit.addEventListener('click', () => {
      c.classList.remove('is-cheer'); void c.offsetWidth; c.classList.add('is-cheer');
      clearTimeout(c._t); c._t = setTimeout(() => c.classList.remove('is-cheer'), 1400);
    });
  });
})();

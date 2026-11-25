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

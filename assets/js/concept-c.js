/* Concept C extras: turn the logo mark and the hero letter tiles into rounded 3D dice.
   Each element keeps its own colours (read before conversion) and gets six faces;
   data-dice lists the letters, front face first. Runs after site.js. */
(() => {
  const FACES = ['front', 'right', 'back', 'left', 'top', 'bottom'];
  document.querySelectorAll('[data-dice]').forEach(el => {
    const cs = getComputedStyle(el);
    el.style.setProperty('--dc', cs.backgroundColor);
    el.style.setProperty('--di', cs.color);
    const letters = el.dataset.dice.split(' ');
    const faces = FACES.map((f, i) => `<span class="dc-face dc-${f}">${letters[i] || ''}</span>`).join('');
    el.innerHTML = `<span class="dice-cube"><span class="dc-core dc-cx"></span><span class="dc-core dc-cy"></span><span class="dc-core dc-cz"></span>${faces}</span>`;
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

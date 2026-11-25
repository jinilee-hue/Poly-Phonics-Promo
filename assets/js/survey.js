/* After every game or video, a short survey pops up — one per item, the same form for all (user 2026-11-25).
   Games open in a new tab: the survey shows when the parent comes back to this page.
   Videos: the survey shows when a video ends (each chant separately; the next one waits until the survey closes).
   Faces are Tata expressions with eyelid / heart overlays (tools/survey_faces.py); survey.css moves the whole figure from its base (a head
   turning on its own opened gaps at the collar — user 2026-11-25).
   Answers are NOT sent anywhere yet ("화면만 먼저"): they stay in this browser (localStorage 'polySurvey.v1').
   Loaded after site.js on every concept page. */
(() => {
  const KEY = 'polySurvey.v1';
  const PAGE = (location.pathname.match(/concept-([a-d])/) || [, '?'])[1].toUpperCase();
  const ADMISSION = 'https://www.poly-english.com/admission/info.do';
  const save = rec => { try { const a = JSON.parse(localStorage.getItem(KEY) || '[]'); a.push(rec); localStorage.setItem(KEY, JSON.stringify(a)); } catch (e) {} };

  /* ---------- dialog (built once) ---------- */
  const dlg = document.createElement('dialog');
  dlg.className = 'sv';
  dlg.setAttribute('aria-labelledby', 'svTitle');
  dlg.innerHTML = `
    <form class="sv-card" method="dialog" novalidate>
      <button class="sv-x" type="button" value="close" aria-label="닫기">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
      <div class="sv-head">
        <span class="sv-kind" id="svKind">게임</span>
        <h2 id="svTitle"><b id="svItem">Toy Catch</b> 체험, 어떠셨어요?</h2>
        <p>30초면 끝나요. 더 좋은 수업을 만드는 데 참고할게요.</p>
      </div>
      <fieldset class="sv-q">
        <legend>아이가 재미있어 했나요?</legend>
        <div class="sv-faces" role="radiogroup">
          ${[['1', '전혀요'], ['2', '별로'], ['3', '보통'], ['4', '좋아했어요'], ['5', '아주 좋아했어요']]
            .map(([v, t]) => `<label class="f${v}"><input type="radio" name="fun" value="${v}" required><span class="sv-face" aria-hidden="true"><img src="assets/img/emoji3d/face-${v}.webp?v=plain1" alt="">${v === '2' ? `<img class="sv-bead" src="assets/img/emoji3d/face-2-sweat.webp?v=body2" alt="">` : ''}${v === '3' ? `<img class="sv-smile" src="assets/img/emoji3d/face-3-smile.webp?v=plain1" alt="">` : ''}${v === '4' ? `<img class="sv-thumb" src="assets/img/emoji3d/face-4-thumb.webp?v=body2" alt="">` : ''}${v === '4' ? `<img class="sv-lid" src="assets/img/emoji3d/face-${v}-lid.webp?v=body2" alt="">` : ''}${v === '5' ? `<img class="sv-heart hl" src="assets/img/emoji3d/face-5-heartL.webp?v=body2" alt=""><img class="sv-heart hr" src="assets/img/emoji3d/face-5-heartR.webp?v=body2" alt="">` : ''}</span><span class="sv-t">${t}</span></label>`).join('')}
        </div>
      </fieldset>
      <fieldset class="sv-q">
        <legend>난이도는 어땠나요?</legend>
        <!-- difficulty: drag Bobo up the hill — flat 쉬웠어요, halfway 적당했어요, the top 어려웠어요 (no flag, user 2026-11-25); the climbed part colours in (user 2026-11-25) -->
        <div class="sv-slide">
          <div class="sv-hill" aria-hidden="true">
            <svg class="sv-ground" viewBox="0 0 100 100" preserveAspectRatio="none"><path class="g-base" d="M0 100 L0.0 92.0 L5.0 91.06 L10.0 89.34 L15.0 87.12 L20.0 84.49 L25.0 81.5 L30.0 78.2 L35.0 74.61 L40.0 70.75 L45.0 66.64 L50.0 62.3 L55.0 57.74 L60.0 52.96 L65.0 47.98 L70.0 42.8 L75.0 37.44 L80.0 31.89 L85.0 26.17 L90.0 20.28 L95.0 14.22 L100.0 8.0 L100 100 Z"/><path class="g-line" d="M0.0 92.0 L5.0 91.06 L10.0 89.34 L15.0 87.12 L20.0 84.49 L25.0 81.5 L30.0 78.2 L35.0 74.61 L40.0 70.75 L45.0 66.64 L50.0 62.3 L55.0 57.74 L60.0 52.96 L65.0 47.98 L70.0 42.8 L75.0 37.44 L80.0 31.89 L85.0 26.17 L90.0 20.28 L95.0 14.22 L100.0 8.0" vector-effect="non-scaling-stroke"/></svg>
            <div class="sv-climb"><svg viewBox="0 0 100 100" preserveAspectRatio="none"><defs><linearGradient id="svHillGrad" x1="0" x2="1" y1="0" y2="0"><stop offset="0" class="hg1"/><stop offset=".5" class="hg2"/><stop offset="1" class="hg3"/></linearGradient></defs><path d="M0 100 L0.0 92.0 L5.0 91.06 L10.0 89.34 L15.0 87.12 L20.0 84.49 L25.0 81.5 L30.0 78.2 L35.0 74.61 L40.0 70.75 L45.0 66.64 L50.0 62.3 L55.0 57.74 L60.0 52.96 L65.0 47.98 L70.0 42.8 L75.0 37.44 L80.0 31.89 L85.0 26.17 L90.0 20.28 L95.0 14.22 L100.0 8.0 L100 100 Z" fill="url(#svHillGrad)"/><path class="g-line" d="M0.0 92.0 L5.0 91.06 L10.0 89.34 L15.0 87.12 L20.0 84.49 L25.0 81.5 L30.0 78.2 L35.0 74.61 L40.0 70.75 L45.0 66.64 L50.0 62.3 L55.0 57.74 L60.0 52.96 L65.0 47.98 L70.0 42.8 L75.0 37.44 L80.0 31.89 L85.0 26.17 L90.0 20.28 L95.0 14.22 L100.0 8.0" vector-effect="non-scaling-stroke"/></svg></div>
            <i class="sv-stop s1"></i><i class="sv-stop s2"></i><i class="sv-stop s3"></i>
            <span class="sv-knob"><img src="assets/img/concept-c/bobo.webp" alt=""><i class="sv-sweat"></i></span>
            <b class="sv-hint">끌어서 올려 보세요</b>
          </div>
          <div class="sv-stops" role="radiogroup">
            ${['쉬웠어요', '적당했어요', '어려웠어요'].map((t, i) => `<label class="lv${i + 1}"><input type="radio" name="level" value="${t}"><span>${t}</span></label>`).join('')}
          </div>
        </div>
      </fieldset>
      <label class="sv-q sv-note">
        <span class="sv-legend">한 줄 의견 <small>(선택)</small></span>
        <textarea name="note" rows="2" maxlength="200" placeholder="좋았던 점이나 아쉬운 점을 적어 주세요. 이름·연락처는 적지 말아 주세요."></textarea>
      </label>
      <p class="sv-err" id="svErr" role="alert"></p>
      <div class="sv-actions">
        <button class="sv-later" type="button" value="later">다음에 할게요</button>
        <button class="sv-send" type="submit">의견 보내기<span class="sv-go" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></button>
      </div>
    </form>
    <div class="sv-card sv-thanks" hidden>
      <img class="sv-big" src="assets/img/emoji3d/party.webp" width="96" height="96" alt="" aria-hidden="true">
      <h2>고마워요!</h2>
      <p>남겨 주신 의견은 수업을 다듬는 데 참고할게요.</p>
      <div class="sv-actions">
        <button class="sv-later" type="button" value="done">닫기</button>
        <a class="sv-send" href="${ADMISSION}" target="_blank" rel="noopener">입학 문의하기</a>
      </div>
    </div>`;
  document.body.appendChild(dlg);
  const form = dlg.querySelector('form'), thanks = dlg.querySelector('.sv-thanks');
  /* difficulty slider: drag or tap anywhere on the track; it snaps to 쉬웠어요 / 적당했어요 / 어려웠어요 */
  const slide = dlg.querySelector('.sv-slide'), track = slide.querySelector('.sv-hill');
  const levels = [...slide.querySelectorAll('input[name=level]')];
  const ratio = e => { const r = track.getBoundingClientRect(); return Math.min(1, Math.max(0, (e.clientX - r.left) / r.width)); };
  let dragging = false;
  const follow = e => { const r = ratio(e); slide.style.setProperty('--drag', r); slide.style.setProperty('--dragy', 8 + 84 * Math.pow(r, 1.5)); };   // Bobo rides the hill surface
  track.addEventListener('pointerdown', e => { dragging = true; track.setPointerCapture(e.pointerId); slide.classList.add('is-drag'); follow(e); });
  track.addEventListener('pointermove', e => { if (dragging) follow(e); });
  const drop = e => {
    if (!dragging) return; dragging = false; slide.classList.remove('is-drag'); slide.style.removeProperty('--drag'); slide.style.removeProperty('--dragy');
    const k = Math.round(ratio(e) * 2); levels[k].checked = true; levels[k].dispatchEvent(new Event('change', { bubbles: true }));
  };
  track.addEventListener('pointerup', drop); track.addEventListener('pointercancel', drop);
  const err = dlg.querySelector('#svErr');
  let current = null, onClose = null;
  const queue = [];

  function open(item, after) {
    if (dlg.open) { queue.push([item, after]); return; }
    current = item; onClose = after || null;
    form.reset(); err.textContent = ''; slide.classList.remove('is-drag'); slide.style.removeProperty('--drag'); slide.style.removeProperty('--dragy');
    form.hidden = false; thanks.hidden = true;
    dlg.querySelector('#svItem').textContent = item.title;
    dlg.querySelector('#svKind').textContent = item.type === 'video' ? '노래 · 영상' : '게임';
    dlg.showModal();
    dlg.classList.remove('is-in'); void dlg.offsetWidth; dlg.classList.add('is-in');
  }
  function close() {
    dlg.close();
  }
  dlg.addEventListener('close', () => {
    const f = onClose; current = null; onClose = null;
    if (f) f();
    const next = queue.shift(); if (next) setTimeout(() => open(...next), 250);
  });
  dlg.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (b && (b.value === 'close' || b.value === 'later' || b.value === 'done')) { e.preventDefault(); close(); }
    else if (e.target === dlg) close();                       // click on the backdrop
  });
  form.addEventListener('submit', e => {
    e.preventDefault();
    const fd = new FormData(form);
    if (!fd.get('fun')) { err.textContent = '아이가 재미있어 했는지 하나만 골라 주세요.'; dlg.querySelector('.sv-faces input').focus(); return; }
    save({ page: PAGE, id: current.id, title: current.title, type: current.type, fun: +fd.get('fun'),
      level: fd.get('level') || '', note: (fd.get('note') || '').trim(), at: new Date().toISOString() });
    form.hidden = true; thanks.hidden = false;
    thanks.querySelector('.sv-later').focus();
  });
  window.PolySurvey = { open, responses: () => { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; } } };

  /* ---------- games: links that open a game (or a Constella lesson) in a new tab ---------- */
  const GAME = /jinilee-hue\.github\.io\/([^/]+)|devconstella\.polarislabs\.ai\.kr\/(?:play|learn)\/([^/]+)/;
  let pending = null;
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]'); if (!a) return;
    const m = a.href.match(GAME); if (!m) return;
    const card = a.closest('article, .card, .ccard, .dpanel, li') || a;
    const h = card.querySelector('h4, h3, b');
    const title = (h ? (h.firstChild && h.firstChild.nodeType === 3 ? h.firstChild.textContent : h.textContent) : '').trim() || (m[1] || m[2]);
    pending = { id: (m[1] || m[2]).toLowerCase(), title, type: 'game', at: Date.now() };
  }, true);
  const back = () => {
    if (!pending || document.visibilityState !== 'visible') return;
    if (Date.now() - pending.at < 1500) return;                // still on the way out
    const item = pending; pending = null;
    setTimeout(() => open(item), 400);
  };
  document.addEventListener('visibilitychange', back);
  addEventListener('focus', back);

  /* ---------- videos: the main player (#video) ---------- */
  const video = document.getElementById('video');
  if (video) {
    let playing = null, hold = false;
    video.addEventListener('playing', () => {
      if (hold) return;
      const on = document.querySelector('.pl.is-on');
      playing = { id: (on && on.dataset.src) || 'video', title: (on && on.dataset.title) || '노래 영상', type: 'video' };
    });
    video.addEventListener('play', () => { if (hold) video.pause(); });   // the next chant waits for the survey
    video.addEventListener('ended', () => {
      const item = playing; if (!item) return;
      hold = true;
      setTimeout(() => {                                          // after site.js has queued the next chant (or not)
        video.pause();
        const on = document.querySelector('.pl.is-on');
        const queued = on && on.dataset.src !== item.id;
        open(item, () => { hold = false; if (queued) video.play().catch(() => {}); });
      }, 0);
    });
  }
})();

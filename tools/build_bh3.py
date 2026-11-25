import json, re
ROOT = '/Users/jini/Documents/Jini/2026/Phonics/Poly-Phonics-Promo'
src = open(f'{ROOT}/concept-b.html', encoding='utf-8').read()
roads = json.load(open('/Users/jini/.cache/agent-scratch/promo/bh3/roads.json'))
VILLAGE = '''<svg class="h3-village {cls}" viewBox="0 0 260 120" aria-hidden="true">
      <ellipse class="yard" cx="146" cy="101" rx="116" ry="14"/>
      <ellipse class="yard yard-in" cx="146" cy="99" rx="98" ry="9"/>
      <g class="tree"><rect x="18" y="66" width="6" height="26" rx="3"/><circle cx="21" cy="58" r="18"/></g>
      <g class="house h1"><rect class="wall" x="46" y="58" width="52" height="40" rx="6"/><path class="roof" d="M40 62 L72 30 L104 62Z"/><rect class="door" x="64" y="74" width="16" height="24" rx="8"/></g>
      <g class="house h2"><rect class="wall" x="112" y="48" width="64" height="50" rx="6"/><path class="roof" d="M104 54 L144 16 L184 54Z"/><rect class="win" x="119" y="58" width="13" height="13" rx="4"/><rect class="win" x="156" y="58" width="13" height="13" rx="4"/><rect class="door" x="136" y="74" width="16" height="24" rx="8"/><path class="flag" d="M144 16 V2 l14 5 -14 5"/></g>
      <g class="house h3"><rect class="wall" x="190" y="66" width="46" height="32" rx="6"/><path class="roof" d="M184 70 L213 42 L242 70Z"/><rect class="door" x="206" y="80" width="14" height="18" rx="7"/></g>
      <g class="tree"><rect x="243" y="74" width="5" height="22" rx="2.5"/><circle cx="245.5" cy="68" r="13"/></g>
    </svg>'''
HERO = f'''<section class="hero h3" aria-labelledby="hero-title">
  <!-- sky -->
  <div class="sky" aria-hidden="true">
    <span class="sun"><i class="rays"></i></span>
    <svg class="cloud h3-cl1" viewBox="0 0 120 56"><use href="#cloud"/></svg>
    <svg class="cloud h3-cl2" viewBox="0 0 120 56"><use href="#cloud"/></svg>
    <svg class="cloud h3-cl3" viewBox="0 0 120 56"><use href="#cloud"/></svg>
    <svg class="birds h3-birds" viewBox="0 0 80 30"><path d="M4 14q7-8 14 0q7-8 14 0M44 8q5-6 10 0q5-6 10 0"/></svg>
  </div>

  <!-- world, far to near (far layers softened = depth of field) -->
  <div class="h3-world w-desk" aria-hidden="true">
    <svg class="h3-far" viewBox="0 0 1440 900" preserveAspectRatio="none">
      <path class="mtn-1" d="M0 600 C 70 548, 150 520, 236 548 S 380 512, 470 536 S 610 486, 736 520 S 960 470, 1090 506 S 1320 462, 1440 500 V900 H0Z"/>
      <path class="mtn-2" d="M0 622 C 110 590, 220 580, 330 600 S 520 600, 640 584 S 900 560, 1060 578 S 1320 572, 1440 566 V900 H0Z"/>
      <path class="h-far" d="M0 640 C 120 612, 250 600, 372 612 S 590 634, 760 618 S 1040 596, 1210 610 S 1390 614, 1440 610 V900 H0Z"/>
    </svg>
    {VILLAGE.format(cls='v-desk')}
    <svg class="h3-mid" viewBox="0 0 1440 900" preserveAspectRatio="none">
      <path class="h-mid" d="M0 704 C 150 668, 300 660, 440 682 S 740 722, 930 694 S 1230 656, 1440 672 V900 H0Z"/>
    </svg>
    <span class="h3-haze"></span>
    <svg class="h3-near" viewBox="0 0 1440 900" preserveAspectRatio="none">
      <path class="h-near" d="M0 792 C 210 760, 430 752, 640 772 S 1060 802, 1250 778 S 1410 772, 1440 776 V900 H0Z"/>
      <path class="road" d="{roads['desk']}"/>
      <g class="tufts">
        <path d="M18 900 q10 -46 22 -60 q-2 30 6 60Z"/><path d="M40 900 q14 -60 34 -78 q-10 40 -6 78Z"/><path d="M76 900 q6 -34 18 -44 q-2 24 2 44Z"/>
        <path d="M1352 900 q10 -40 24 -54 q-4 30 2 54Z"/><path d="M1380 900 q14 -56 32 -72 q-8 38 -4 72Z"/><path d="M1414 900 q6 -30 16 -40 q-2 22 2 40Z"/>
      </g>
    </svg>
  </div>
  <div class="h3-world w-mob" aria-hidden="true">
    <svg class="h3-far" viewBox="0 0 390 844" preserveAspectRatio="none">
      <path class="mtn-1" d="M0 470 C 40 440, 92 428, 146 448 S 242 420, 300 436 S 362 428, 390 432 V844 H0Z"/>
      <path class="h-far" d="M0 514 C 70 496, 150 492, 230 500 S 350 510, 390 504 V844 H0Z"/>
    </svg>
    {VILLAGE.format(cls='v-mob')}
    <svg class="h3-mid" viewBox="0 0 390 844" preserveAspectRatio="none">
      <path class="h-mid" d="M0 584 C 80 564, 170 560, 250 572 S 360 584, 390 578 V844 H0Z"/>
    </svg>
    <span class="h3-haze"></span>
    <svg class="h3-near" viewBox="0 0 390 844" preserveAspectRatio="none">
      <path class="h-near" d="M0 690 C 90 672, 200 666, 290 680 S 370 692, 390 688 V844 H0Z"/>
      <path class="road" d="{roads['mob']}"/>
    </svg>
  </div>
  <svg width="0" height="0" class="sr-only" aria-hidden="true"><defs><linearGradient id="roadFill3" x1="0" y1="0" x2="0" y2="1"><stop class="road-g0" offset="0"/><stop class="road-g1" offset=".5"/><stop class="road-g2" offset="1"/></linearGradient>
    <radialGradient id="h3shadow"><stop offset="0" class="sh-0"/><stop offset="1" class="sh-1"/></radialGradient></defs></svg>

  <!-- glow that lifts the cast off the background -->
  <span class="h3-glow" aria-hidden="true"></span>

  <!-- the cast: Tata front centre, Bobo and Nunu a step behind -->
  <div class="h3-cast friends">
    <span class="bub b-t" aria-hidden="true">t</span>
    <span class="bub b-s" aria-hidden="true">s</span>
    <figure class="ch ch-bobo"><span class="ch-shadow"></span><img src="assets/img/bobo.webp" width="363" height="556" alt=""></figure>
    <figure class="ch ch-nunu"><span class="ch-shadow"></span><img src="assets/img/nunu.webp" width="440" height="604" alt=""></figure>
    <figure class="ch ch-tata"><span class="ch-shadow"></span><img src="assets/img/tata.webp" width="338" height="580" alt="Phonics Land의 친구들 보보, 타타, 누누"></figure>
    <span class="bub b-a" aria-hidden="true">a</span>
  </div>
  <span class="bub b-p" aria-hidden="true">p</span>

  <button class="stone h3-m sound-chip" type="button" data-say="m" aria-label="/m/ 소리 듣기">M<i>m</i>
    <span class="stone-tip">눌러 보세요 · /m/</span>
  </button>

  <div class="h3-copy">
    <p class="eyebrow reveal"><span class="dot"></span>5세 유치부 입학을 준비하는 부모님께</p>
    <h1 id="hero-title" class="hero-title reveal" style="--i:1">영어 첫걸음은<br><span class="hl">소리</span>부터,<br>Phonics Land로 떠나요</h1>
    <p class="hero-lead reveal" style="--i:2">POLY Phonics는 『From Phonics to Reading K』로 알파벳 글자의 소리를 노래와 그림, 게임으로 익히는 5세 과정입니다. 입학 전에 실제 수업 콘텐츠를 아이와 먼저 체험해 보세요.</p>
    <div class="hero-cta reveal" style="--i:3">
      <a class="btn btn-primary" href="#try">지금 체험하기 <span class="ic-wrap"><svg class="ic"><use href="#i-arrow"/></svg></span></a>
      <a class="btn btn-glass" href="#curriculum">모험 지도 보기</a>
    </div>
  </div>
  <svg class="wave wave-bottom" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true"><path d="M0 50 C 240 10, 420 90, 720 52 S 1200 8, 1440 46 V90 H0Z"/></svg>
</section>'''
s, n = re.subn(r'<section class="hero" aria-labelledby="hero-title">.*?</section>', lambda m: HERO, src, count=1, flags=re.S)
assert n == 1
a = '<link rel="stylesheet" href="assets/css/concept-b.css">'
assert a in s
s = s.replace(a, a + '\n<link rel="stylesheet" href="assets/css/b-hero-3.css">', 1)
s = s.replace('<title>', '<title>H3 · ', 1)
open(f'{ROOT}/b-hero-3.html', 'w', encoding='utf-8').write(s)
print('ok', len(s))

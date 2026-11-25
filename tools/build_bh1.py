"""Assemble b-hero-1.html: concept-b.html with only the hero <section> swapped for variant H1 (land from tools/hero_bh1.py)."""
import math, re
src = open('concept-b.html', encoding='utf-8').read()
land = open('assets/img/b-hero-1/land.svg.txt', encoding='utf-8').read()

# bunting flags along the balloon's trailing string (cubic from basket to the left)
p0, p1, p2, p3 = (52, 196), (24, 218), (-44, 232), (-122, 214)
def bez(t):
    return tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * c + t ** 3 * d for a, b, c, d in zip(p0, p1, p2, p3))
flags = []
for t, ch, cls in [(.16, 't', 'fg-c'), (.4, 's', 'fg-t'), (.64, 'a', 'fg-o'), (.88, 'M', 'fg-b')]:   # reads M a s t left to right
    x, y = bez(t); x2, y2 = bez(t + .1)
    ang = math.degrees(math.atan2(y2 - y, x2 - x)) + 180
    flags.append(f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f})"><path class="{cls}" d="M-13 0 L13 0 L0 30Z"/>'
                 f'<text x="0" y="15" text-anchor="middle">{ch}</text></g>')
gores = []
bounds = [-16, -9, -3, 3, 9, 16]
fills = ['gore-y', 'gore-b', 'gore-w', 'gore-b', 'gore-y']
for i in range(5):
    a, b = bounds[i], bounds[i + 1]
    gores.append(f'<path class="{fills[i]}" d="M70 6 Q{70 + a * 5.2:.1f} 80 {70 + a} 158 L{70 + b} 158 Q{70 + b * 5.2:.1f} 80 70 6Z"/>')

balloon = f'''<svg class="balloon" viewBox="-132 0 274 250" aria-hidden="true">
      <defs><clipPath id="h1Env"><path d="M70 6 C28 6 4 40 4 80 C4 118 40 140 54 158 L86 158 C100 140 136 118 136 80 C136 40 112 6 70 6Z"/></clipPath></defs>
      <path class="bunting" d="M{p0[0]} {p0[1]} C{p1[0]} {p1[1]} {p2[0]} {p2[1]} {p3[0]} {p3[1]}"/>
      {''.join(flags)}
      <g clip-path="url(#h1Env)"><rect class="gore-o" x="0" y="0" width="140" height="170"/>{''.join(gores)}
        <ellipse class="env-hi" cx="40" cy="58" rx="11" ry="30" transform="rotate(14 40 58)"/></g>
      <rect class="skirt" x="53" y="154" width="34" height="9" rx="4"/>
      <path class="rope" d="M57 162 L60 186 M83 162 L80 186"/>
      <rect class="basket" x="50" y="184" width="40" height="26" rx="7"/>
      <path class="weave" d="M50 194 H90 M60 186 V210 M70 186 V210 M80 186 V210"/>
    </svg>'''

kite = '''<svg class="kite" viewBox="0 0 140 300" aria-hidden="true">
      <path class="kite-string" d="M70 128 C96 190 54 236 138 300"/>
      <path class="kite-tail" d="M70 128 C54 150 86 170 66 194 C48 214 72 228 52 250"/>
      <path class="bow bow-y" d="M60 160 l-9 -6 v12Z M60 160 l9 -6 v12Z"/><path class="bow bow-c" d="M68 202 l-9 -6 v12Z M68 202 l9 -6 v12Z"/><path class="bow bow-b" d="M56 240 l-9 -6 v12Z M56 240 l9 -6 v12Z"/>
      <path class="kq-b" d="M70 10 L28 64 L70 64Z"/><path class="kq-y" d="M70 10 L112 64 L70 64Z"/>
      <path class="kq-o" d="M112 64 L70 128 L70 64Z"/><path class="kq-t" d="M28 64 L70 128 L70 64Z"/>
      <path class="kite-stick" d="M70 10 V128 M28 64 H112"/>
    </svg>'''

tuft = '''<svg class="tuft {cls}" viewBox="0 0 260 130" aria-hidden="true">
      <path class="bl2" d="M10 130 Q18 70 4 40 Q30 78 34 130Z M60 130 Q70 60 58 18 Q90 70 84 130Z M150 130 Q156 84 144 56 Q174 88 170 130Z M214 130 Q226 80 216 46 Q244 86 236 130Z"/>
      <path class="bl1" d="M26 130 Q40 76 30 30 Q58 80 52 130Z M96 130 Q100 70 92 34 Q128 78 120 130Z M120 130 Q136 92 132 66 Q156 96 146 130Z M180 130 Q196 74 192 28 Q218 82 206 130Z"/>
      <g class="tf"><circle cx="74" cy="44" r="7"/><circle cx="202" cy="40" r="6"/></g>
    </svg>'''

village = '''<svg class="village" viewBox="0 0 300 170" aria-hidden="true">
      <g class="rainbow"><path class="rb1" d="M45 150 A120 120 0 0 1 285 150"/><path class="rb2" d="M57 150 A108 108 0 0 1 273 150"/><path class="rb3" d="M69 150 A96 96 0 0 1 261 150"/><path class="rb4" d="M81 150 A84 84 0 0 1 249 150"/><path class="rb5" d="M93 150 A72 72 0 0 1 237 150"/></g>
      <g transform="translate(20 52)">
      <ellipse class="yard" cx="146" cy="101" rx="122" ry="15"/>
      <ellipse class="yard yard-in" cx="146" cy="99" rx="102" ry="9"/>
      <g class="tree"><rect x="18" y="66" width="6" height="26" rx="3"/><circle cx="21" cy="58" r="18"/></g>
      <g class="house h1"><rect class="wall" x="46" y="58" width="52" height="40" rx="6"/><path class="roof" d="M40 62 L72 30 L104 62Z"/><rect class="door" x="64" y="74" width="16" height="24" rx="8"/></g>
      <g class="house h2"><rect class="wall" x="112" y="48" width="64" height="50" rx="6"/><path class="roof" d="M104 54 L144 16 L184 54Z"/><rect class="win" x="119" y="58" width="13" height="13" rx="4"/><rect class="win" x="156" y="58" width="13" height="13" rx="4"/><rect class="door" x="136" y="74" width="16" height="24" rx="8"/><path class="flag" d="M144 16 V2 l14 5 -14 5"/></g>
      <g class="house h3"><rect class="wall" x="190" y="66" width="46" height="32" rx="6"/><path class="roof" d="M184 70 L213 42 L242 70Z"/><rect class="door" x="206" y="80" width="14" height="18" rx="7"/></g>
      <g class="tree"><rect x="243" y="74" width="5" height="22" rx="2.5"/><circle cx="245.5" cy="68" r="13"/></g>
      </g>
    </svg>'''

hero = f'''<section class="hero h1v" aria-labelledby="hero-title">
  <div class="sky" aria-hidden="true">
    <span class="sun"><i class="rays"></i></span>
    <svg class="cloud cl1" viewBox="0 0 120 56"><use href="#cloud"/></svg>
    <svg class="cloud cl2" viewBox="0 0 120 56"><use href="#cloud"/></svg>
    <svg class="birds" viewBox="0 0 80 30"><path d="M4 14q7-8 14 0q7-8 14 0M44 8q5-6 10 0q5-6 10 0"/></svg>
    <svg class="birds birds-2" viewBox="0 0 80 30"><path d="M4 14q7-8 14 0q7-8 14 0M44 8q5-6 10 0q5-6 10 0"/></svg>
    {balloon}
    {kite}
  </div>

  <div class="hero-copy">
    <p class="eyebrow reveal"><span class="dot"></span>5세 유치부 입학을 준비하는 부모님께</p>
    <h1 id="hero-title" class="hero-title reveal" style="--i:1">영어 첫걸음은 <span class="hl">소리</span>부터,<br>Phonics Land로 떠나요</h1>
    <p class="hero-lead reveal" style="--i:2">POLY Phonics는 『From Phonics to Reading K』로 알파벳 글자의 소리를 노래와 그림, 게임으로 익히는 5세 과정입니다. 입학 전에 실제 수업 콘텐츠를 아이와 먼저 체험해 보세요.</p>
    <div class="hero-cta reveal" style="--i:3">
      <a class="btn btn-primary" href="#try">지금 체험하기 <span class="ic-wrap"><svg class="ic"><use href="#i-arrow"/></svg></span></a>
      <a class="btn btn-glass" href="#curriculum">모험 지도 보기</a>
    </div>
  </div>

  <div class="land">
    <svg class="hills" viewBox="0 0 1440 520" preserveAspectRatio="none" aria-hidden="true">
{land}
    </svg>
    {village}
    <span class="stone s-p" aria-hidden="true">p</span>
    <span class="stone s-t" aria-hidden="true">t</span>
    <span class="stone s-s" aria-hidden="true">s</span>
    <span class="stone s-a" aria-hidden="true">a</span>
    <button class="stone s-m sound-chip" type="button" data-say="m" aria-label="/m/ 소리 듣기">M<i>m</i>
      <span class="stone-tip">눌러 보세요 · /m/</span>
    </button>
    <img class="friends" src="assets/img/friends.webp" width="1400" height="803" alt="Phonics Land의 친구들 보보, 타타, 누누">
    {tuft.format(cls="tuft-l")}
    {tuft.format(cls="tuft-r")}
  </div>
  <svg class="wave wave-bottom" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true"><path d="M0 50 C 240 10, 420 90, 720 52 S 1200 8, 1440 46 V90 H0Z"/></svg>
</section>'''

out, n = re.subn(r'<section class="hero".*?</section>', lambda m: hero, src, count=1, flags=re.S)
assert n == 1
out = out.replace('<link rel="stylesheet" href="assets/css/concept-b.css">',
                  '<link rel="stylesheet" href="assets/css/concept-b.css">\n<link rel="stylesheet" href="assets/css/b-hero-1.css">', 1)
out = out.replace('<title>POLY Phonics · 모험 지도</title>', '<title>POLY Phonics · 모험 지도 · 히어로 H1</title>', 1)
open('b-hero-1.html', 'w', encoding='utf-8').write(out)
print('ok', len(out))

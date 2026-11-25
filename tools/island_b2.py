"""B hero H2 'floating island': builds the island SVG (viewBox 0 0 800 780) for b-hero-2.html.
Prints the <svg> markup to stdout and, on stderr, where the HTML overlays (letter stones, friends) sit
in % of the island box. Colours come from CSS classes (b-hero-2.css), no hex in the markup.
usage: python3 tools/island_b2.py > /tmp/island.svg"""
import math, sys

W, H = 800, 780
CX, CY, RX, RY = 400, 292, 352, 122          # top face (perspective ellipse)
RIM = 30                                     # grass side thickness


def blob(cx, cy, rx, ry, n=72, wob=((3, .018, 0), (5, .012, 1.3), (7, .008, .4))):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        r = 1 + sum(a * math.sin(k * t + ph) for k, a, ph in wob)
        pts.append((cx + rx * r * math.cos(t), cy + ry * r * math.sin(t)))
    return pts


def smooth_closed(pts):
    """closed Catmull-Rom → cubic Bezier path"""
    n = len(pts); d = f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return d + 'Z'


def smooth_open(pts):
    n = len(pts); d = f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
    for i in range(n - 1):
        p0, p1, p2 = pts[max(0, i - 1)], pts[i], pts[i + 1]
        p3 = pts[min(n - 1, i + 2)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return d


top = blob(CX, CY, RX, RY)
rim = [(x, y + RIM) for x, y in top]
# the visible front edge of the rim: blob angles 0..π (the lower half), walked left → right
n_top = len(top)
front = [rim[i] for i in range(n_top) if 0 <= i <= n_top // 2][::-1]
L, R = front[0], front[-1]

# underside: rim front edge, then down both sides to a tip
tip = (432, 752)
right_side = [R, (R[0] + 4, R[1] + 70), (R[0] - 60, R[1] + 170), (R[0] - 150, R[1] + 270), (tip[0] + 60, tip[1] - 70), tip]
left_side = [tip, (tip[0] - 70, tip[1] - 80), (L[0] + 150, L[1] + 250), (L[0] + 60, L[1] + 150), (L[0] - 2, L[1] + 60), L]
under_pts = front[::-1]          # right → left along the front edge … reversed below
under_d = smooth_open(front) + ' ' + smooth_open(right_side).replace('M', 'L', 1) + ' ' + smooth_open(left_side).replace('M', 'L', 1) + 'Z'


def band(dy, wob):
    """strata boundary: the front edge pushed down by dy, closed to the bottom of the box"""
    pts = []
    for x, y in front:
        pts.append((x, y + dy + wob * math.sin(x / 37) + wob * .6 * math.sin(x / 13 + 1)))
    d = smooth_open(pts)
    return d + f' L{W + 40} {pts[-1][1]:.1f} L{W + 40} {H + 40} L-40 {H + 40} L-40 {pts[0][1]:.1f}Z'


# grass scallops hanging over the rim front edge
scallops = []
for i, (x, y) in enumerate(front[::2]):
    if 0 < i < len(front[::2]) - 1:
        r = 9 + (i * 7 % 5)
        scallops.append(f'<circle cx="{x:.1f}" cy="{y - 2:.1f}" r="{r}"/>')

# hanging roots + vines
roots = [
    'M168 432 C 160 470 176 500 162 540 C 154 560 166 576 160 590',
    'M262 452 C 258 500 274 520 266 566',
    'M598 440 C 606 480 590 512 600 552 C 604 570 596 584 600 596',
    'M676 418 C 690 450 676 476 686 506',
    'M380 462 C 384 520 372 560 384 610 C 388 630 380 644 386 660',
]
vines = [
    ('M118 404 C 112 440 128 470 118 506 C 112 530 124 548 118 566', [(118, 440), (124, 478), (116, 520), (121, 552)]),
    ('M520 440 C 528 486 512 520 522 566 C 526 586 518 600 524 616', [(524, 470), (516, 512), (523, 552), (520, 596)]),
    ('M722 380 C 736 410 724 440 734 468', [(728, 404), (730, 446)]),
]

# rocks embedded in the strata
rocks = [(205, 500, 22, 12), (330, 560, 18, 10), (470, 520, 26, 13), (560, 600, 16, 9), (290, 640, 14, 8),
         (420, 680, 15, 8), (640, 500, 17, 9), (150, 470, 12, 7), (505, 650, 12, 7)]

# road on the top face: from the yard under the houses to the front lip, perspective width
road_c = [(442, 232), (452, 252), (480, 278), (506, 306), (524, 338), (542, 372), (556, 404), (562, 428)]


def catmull(pts, n=24):
    ext = [pts[0]] + pts + [pts[-1]]; out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                  + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    return out + [pts[-1]]


c = catmull(road_c)
Lr, Rr = [], []
for i, (x, y) in enumerate(c):
    a, b = c[max(0, i - 3)], c[min(len(c) - 1, i + 3)]
    dx, dy = b[0] - a[0], b[1] - a[1]; m = math.hypot(dx, dy) or 1
    nx, ny = -dy / m, dx / m
    f = max(0.0, min(1.0, (y - 232) / 196))
    w = (20 + 92 * f ** 1.1) / 2
    Lr.append((x + nx * w, y + ny * w)); Rr.append((x - nx * w, y - ny * w))
road_d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in Lr + Rr[::-1]) + 'Z'


def at(y):
    return min(c, key=lambda p: abs(p[1] - y))


stones = {'p': at(256), 't': at(285), 's': at(316), 'a': at(349), 'm': at(414)}
for k, (x, y) in stones.items():
    print(f'stone {k}: left {x / W * 100:.1f}%  top {y / H * 100:.1f}%', file=sys.stderr)

# trees (back of the island), flowers (top face), pond + stream feeding the waterfall
trees = [(96, 262, 30), (150, 236, 24), (650, 222, 24), (704, 250, 30), (252, 214, 20), (290, 236, 16)]
flowers = [(190, 330), (232, 318), (300, 352), (612, 344), (650, 368), (700, 322), (120, 318), (360, 380), (470, 222), (338, 236)]

base = [(726, 0, 54), (738, 48, 96), (748, 110, 170), (733, 140, 196), (756, 30, 80), (744, 168, 200)]
streaks = ' '.join(f'M{x} {y0 + off} V {y1 + off}' for off in (100, 300, 500) for x, y0, y1 in base)
svg = f'''<svg class="isle-svg" viewBox="0 0 {W} {H}" aria-hidden="true">
  <defs>
    <linearGradient id="i2Top" x1="0" y1="0" x2="0" y2="1"><stop class="g-top-0" offset="0"/><stop class="g-top-1" offset="1"/></linearGradient>
    <linearGradient id="i2Road" x1="0" y1="0" x2="0" y2="1"><stop class="road-g0" offset="0"/><stop class="road-g2" offset="1"/></linearGradient>
    <linearGradient id="i2Fall" x1="0" y1="0" x2="0" y2="1"><stop class="g-fall-0" offset="0"/><stop class="g-fall-1" offset="1"/></linearGradient>
    <linearGradient id="i2Shade" x1="0" y1="0" x2="1" y2="0"><stop class="g-shade-0" offset="0"/><stop class="g-shade-1" offset=".55"/><stop class="g-shade-2" offset="1"/></linearGradient>
    <clipPath id="i2Under"><path d="{under_d}"/></clipPath>
    <clipPath id="i2TopClip"><path d="{smooth_closed(top)}"/></clipPath>
    <clipPath id="i2FallClip"><path d="M716 318 C 722 380 720 470 728 560 L 770 560 C 764 470 762 380 752 318Z"/></clipPath>
  </defs>
  <g class="under">
    <path class="earth-1" d="{under_d}"/>
    <g clip-path="url(#i2Under)">
      <path class="earth-2" d="{band(62, 9)}"/>
      <path class="earth-3" d="{band(150, 12)}"/>
      <path class="earth-4" d="{band(250, 10)}"/>
      {''.join(f'<ellipse class="rock" cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"/>' for x, y, rx, ry in rocks)}
      <path class="under-shade" d="{under_d}"/>
    </g>
    <g class="roots">{''.join(f'<path d="{d}"/>' for d in roots)}</g>
    <g class="vines">{''.join(f'<path d="{d}"/>' + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="7" ry="4.5" transform="rotate({-35 if j % 2 else 35} {x} {y})"/>' for j, (x, y) in enumerate(lv)) for d, lv in vines)}</g>
  </g>
  <path class="rim" d="{smooth_closed(rim)}"/>
  <g class="scallops">{''.join(scallops)}</g>
  <path class="top" d="{smooth_closed(top)}"/>
  <ellipse class="top-glow" cx="{CX - 40}" cy="{CY - 24}" rx="{RX * .72:.0f}" ry="{RY * .58:.0f}"/>
  <g class="fall">
    <path class="fall-body" d="M716 318 C 722 380 720 470 728 560 L 770 560 C 764 470 762 380 752 318Z"/>
    <g clip-path="url(#i2FallClip)"><g class="fall-streaks">
      <path d="{streaks}"/>
    </g></g>
    <g class="mist"><circle cx="724" cy="566" r="22"/><circle cx="754" cy="560" r="26"/><circle cx="782" cy="572" r="18"/><circle cx="740" cy="586" r="20"/><circle cx="706" cy="580" r="14"/></g>
  </g>
  <g class="pond"><ellipse class="pond-water" cx="676" cy="300" rx="56" ry="20"/><ellipse class="pond-hi" cx="664" cy="296" rx="24" ry="6"/>
    <path class="stream" d="M712 304 C 724 310 730 316 738 322 L 752 320 C 742 312 732 304 722 296Z"/></g>
  <g clip-path="url(#i2TopClip)"><path class="isle-road" d="{road_d}"/></g>
  <g class="flowers">{''.join(f'<g transform="translate({x} {y})"><circle class="fl-{i % 3}" r="5.5"/><circle class="fl-c" r="2.2"/></g>' for i, (x, y) in enumerate(flowers))}</g>
  <g class="trees">{''.join(f'<g class="tree"><rect x="{x - 3}" y="{y - 6}" width="6" height="{r + 8}" rx="3"/><circle cx="{x}" cy="{y - r * .55:.0f}" r="{r}"/><circle class="tree-hi" cx="{x - r * .3:.0f}" cy="{y - r * .85:.0f}" r="{r * .38:.0f}"/></g>' for x, y, r in trees)}</g>
  <g class="village" transform="translate(298 124) scale(1.08)">
    <ellipse class="yard" cx="146" cy="101" rx="118" ry="15"/>
    <ellipse class="yard yard-in" cx="146" cy="99" rx="98" ry="9"/>
    <g class="house h1"><rect class="wall" x="46" y="58" width="52" height="40" rx="6"/><path class="roof" d="M40 62 L72 30 L104 62Z"/><rect class="door" x="64" y="74" width="16" height="24" rx="8"/></g>
    <g class="house h2"><rect class="wall" x="112" y="48" width="64" height="50" rx="6"/><path class="roof" d="M104 54 L144 16 L184 54Z"/><rect class="win" x="119" y="58" width="13" height="13" rx="4"/><rect class="win" x="156" y="58" width="13" height="13" rx="4"/><rect class="door" x="136" y="74" width="16" height="24" rx="8"/><path class="flag" d="M144 16 V2 l14 5 -14 5"/></g>
    <g class="house h3"><rect class="wall" x="190" y="66" width="46" height="32" rx="6"/><path class="roof" d="M184 70 L213 42 L242 70Z"/><rect class="door" x="206" y="80" width="14" height="18" rx="7"/></g>
  </g>
</svg>'''
print(svg)

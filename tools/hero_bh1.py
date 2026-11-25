"""B hero variant H1 ("풍성한 마을") — generates the land SVG body (viewBox 0 0 1440 520, stretched to the .land box):
mountains, far hill with the village mound and tiny trees, mid hill with bushes, near meadow, the road
(one smooth borderless outline from the village yard down to the bottom edge), fence posts and flowers.
Writes assets/img/b-hero-1/land.svg.txt (inner markup) and prints the stone spots (% of .land).
usage: python3 tools/hero_bh1.py"""
import math, random, os, sys

W, H = 1440, 520
YARD = (1228, 146)                     # village yard centre in land units (see b-hero-1.css .village)

def poly(pts):
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)

def band(fn, step=8):
    pts = [(x, fn(x)) for x in range(0, W + step, step)]
    return poly(pts) + f' L{W} {H + 60} L0 {H + 60}Z'

def gauss(x, c, w):
    return math.exp(-((x - c) / w) ** 2)

# ---- hill functions (y grows downward) ----
def y_mtn_back(x):
    peaks = [(60, 58, 150), (300, 22, 170), (560, 70, 140), (820, 38, 190), (1090, 30, 170), (1360, 64, 160)]
    return 205 - max((205 - py) * gauss(x, px, w) for px, py, w in peaks)
def y_mtn_front(x):
    peaks = [(170, 92, 130), (450, 78, 150), (700, 104, 120), (960, 84, 160), (1250, 96, 150)]
    return 215 - max((215 - py) * gauss(x, px, w) for px, py, w in peaks)
def y_far(x):
    return 182 + 9 * math.sin(x / 120) + 6 * math.sin(x / 47 + 1) - 34 * gauss(x, YARD[0], 210)
def y_mid(x):
    return 262 + 13 * math.sin(x / 150 + 2) + 7 * math.sin(x / 61)
def y_near(x):
    return 338 + 15 * math.sin(x / 170 + 4) + 7 * math.sin(x / 70 + 1)

# ---- road (same method as tools/road_b.py) ----
P = [(1228, 138), (1222, 156), (1188, 178), (1128, 202), (1062, 230), (1006, 262), (962, 300), (900, 342),
     (812, 386), (700, 430), (566, 480), (440, 540), (360, 600)]
def catmull(pts, n=40):
    ext = [pts[0]] + pts + [pts[-1]]; out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                  + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    return out + [pts[-1]]
def resample(pts, step=3.0):
    out = [pts[0]]; carry = 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        seg = math.hypot(x2 - x1, y2 - y1); d = step - carry
        while d <= seg:
            t = d / seg; out.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * t)); d += step
        carry = seg - (d - step)
    return out + [pts[-1]]
def smooth(pts, k=9, passes=4):
    for _ in range(passes):
        n = len(pts); q = []
        for i in range(n):
            r = min(k, i, n - 1 - i); lo, hi = i - r, i + r + 1
            q.append((sum(p[0] for p in pts[lo:hi]) / (hi - lo), sum(p[1] for p in pts[lo:hi]) / (hi - lo)))
        pts = q
    return pts
C = smooth(resample(catmull(P)))
def width(y):
    f = max(0.0, min(1.0, (y - 138) / 420))
    return 24 + 410 * f ** 1.15
L, R, N = [], [], []
for i, (x, y) in enumerate(C):
    a, b = C[max(0, i - 6)], C[min(len(C) - 1, i + 6)]
    dx, dy = b[0] - a[0], b[1] - a[1]; m = math.hypot(dx, dy) or 1
    nx, ny = -dy / m, dx / m; w = width(y) / 2
    N.append((nx, ny))
    L.append((x + nx * w, y + ny * w)); R.append((x - nx * w, y - ny * w))
road = poly([(C[0][0], C[0][1] - 3)] + L + R[::-1]) + 'Z'
def at_y(ty):
    i = min(range(len(C)), key=lambda k: abs(C[k][1] - ty)); return i, C[i]
def on_road(x, y, pad=0):
    i, (cx, cy) = at_y(y)
    if y < C[0][1] - 10: return False
    return abs(x - cx) < width(y) / 2 + pad

# ---- fence posts beside the road ----
def fence(side, y0, y1, n):
    posts = []
    for k in range(n):
        ty = y0 + (y1 - y0) * (k / (n - 1)) ** 1.25
        i, (cx, cy) = at_y(ty)
        f = max(0.0, (cy - 138) / 420)
        off = width(cy) / 2 + 10 + 26 * f
        nx, ny = N[i]
        s = -1 if side == 'R' else 1
        px, py = cx + s * nx * off, cy + s * ny * off
        h = 9 + 34 * f; w = 2.4 + 5 * f
        posts.append((px, py, h, w))
    g = []
    for k in range(len(posts) - 1):
        (x1, y1, h1, w1), (x2, y2, h2, w2) = posts[k], posts[k + 1]
        for fr in (.78, .42):
            g.append(f'<path class="rail" d="M{x1:.1f} {y1 - h1 * fr:.1f} L{x2:.1f} {y2 - h2 * fr:.1f}" style="stroke-width:{(w1 + w2) / 3.2:.1f}"/>')
    for x, y, h, w in posts:
        g.append(f'<rect class="post" x="{x - w / 2:.1f}" y="{y - h:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{w / 2:.1f}"/>')
    return '\n'.join(g)

# ---- little things ----
rnd = random.Random(7)
def tree(x, y, r):
    return (f'<rect class="trunk" x="{x - r * .16:.1f}" y="{y - r * 1.5:.1f}" width="{r * .32:.1f}" height="{r * 1.5:.1f}" rx="{r * .16:.1f}"/>'
            f'<circle class="crown" cx="{x:.1f}" cy="{y - r * 1.7:.1f}" r="{r:.1f}"/>'
            f'<circle class="crown-hi" cx="{x - r * .3:.1f}" cy="{y - r * 2:.1f}" r="{r * .42:.1f}"/>')
def bush(x, y, r):
    return (f'<g class="bush"><circle cx="{x - r * .8:.1f}" cy="{y - r * .55:.1f}" r="{r * .7:.1f}"/>'
            f'<circle cx="{x:.1f}" cy="{y - r * .8:.1f}" r="{r:.1f}"/><circle cx="{x + r * .85:.1f}" cy="{y - r * .5:.1f}" r="{r * .65:.1f}"/></g>')
def flower(x, y, r, cls):
    petals = ''.join(f'<circle cx="{x + math.cos(a) * r:.1f}" cy="{y + math.sin(a) * r * .8:.1f}" r="{r * .62:.1f}"/>'
                     for a in [k * 2 * math.pi / 5 - math.pi / 2 for k in range(5)])
    return f'<g class="fl {cls}">{petals}<circle class="fc" cx="{x:.1f}" cy="{y:.1f}" r="{r * .5:.1f}"/></g>'

trees_far = [(90, 9), (190, 7), (262, 10), (430, 8), (520, 6), (930, 8), (1010, 6), (1390, 9)]   # none under the CTA buttons
far_trees = ''.join(tree(x, y_far(x) + 2, r) for x, r in trees_far)
mid_bushes = ''.join(bush(x, y_mid(x) + 8, r) for x, r in [(70, 16), (300, 13), (520, 18), (1180, 15), (1330, 19)])
mid_trees = ''.join(tree(x, y_mid(x) + 6, r) for x, r in [(170, 15), (1260, 13), (1405, 16)])

flowers = []
cls = ['f-w', 'f-c', 'f-y', 'f-b']
tries = 0
while len(flowers) < 90 and tries < 4000:
    tries += 1
    x = rnd.uniform(10, 1430); y = rnd.uniform(300, 515)
    if y < y_near(x) + 8: continue
    if on_road(x, y, pad=24): continue
    if 150 < x < 660 and y > 300: continue           # under the friends (covered anyway)
    f = (y - 300) / 220
    flowers.append(flower(x, y, 3.2 + 4.5 * f, rnd.choice(cls)))
for x in [(40), (110), (1330), (1410)]:             # a few on the mid hill too
    flowers.append(flower(x, y_mid(x) + 22, 3.2, rnd.choice(cls)))

out = f'''<defs><linearGradient id="h1Road" x1="0" y1="0" x2="0" y2="1"><stop class="road-g0" offset="0"/><stop class="road-g1" offset=".5"/><stop class="road-g2" offset="1"/></linearGradient>
<linearGradient id="h1Mtn" x1="0" y1="0" x2="0" y2="1"><stop class="mtn-g0" offset="0"/><stop class="mtn-g1" offset="1"/></linearGradient></defs>
<path class="mtn-back" d="{band(y_mtn_back)}"/>
<path class="mtn-front" d="{band(y_mtn_front)}"/>
<path class="hill-far" d="{band(y_far)}"/>
<g class="trees-far">{far_trees}</g>
<path class="hill-mid" d="{band(y_mid)}"/>
<g class="bushes">{mid_bushes}{mid_trees}</g>
<path class="hill-near" d="{band(y_near)}"/>
<path class="road" d="{road}"/>
<g class="fence">{fence('R', 176, 440, 11)}{fence('L', 176, 318, 7)}</g>
<g class="flowers">{''.join(flowers)}</g>'''
os.makedirs('assets/img/b-hero-1', exist_ok=True)
open('assets/img/b-hero-1/land.svg.txt', 'w').write(out)
print('far hill under the yard:', round(y_far(YARD[0]), 1), file=sys.stderr)
for name, ty in [('p', 186), ('t', 236), ('s', 290), ('a', 352), ('m', 420)]:
    i, (x, y) = at_y(ty)
    print(f'stone {name}: left {x / W * 100:.1f}%  top {y / H * 100:.1f}%  road {width(y):.0f}', file=sys.stderr)
print(len(out), 'chars', file=sys.stderr)

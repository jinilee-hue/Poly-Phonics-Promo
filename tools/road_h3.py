"""H3 hero roads: smooth centreline -> perspective-widened borderless outline (same method as tools/road_b.py).
Prints desktop (viewBox 1440x900) and mobile (390x844) path d strings."""
import math, json
def catmull(pts, n=40):
    ext = [pts[0]] + pts + [pts[-1]]; out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                  + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    return out + [pts[-1]]
def resample(pts, step=2.5):
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
def road(P, w0, w1, y0, y1, gamma=1.2):
    c = smooth(resample(catmull(P)))
    def width(y):
        f = max(0.0, min(1.0, (y - y0) / (y1 - y0))); return w0 + (w1 - w0) * f ** gamma
    L, R = [], []
    for i, (x, y) in enumerate(c):
        a, b = c[max(0, i - 6)], c[min(len(c) - 1, i + 6)]
        dx, dy = b[0] - a[0], b[1] - a[1]; m = math.hypot(dx, dy) or 1
        nx, ny = -dy / m, dx / m; w = width(y) / 2
        L.append((x + nx * w, y + ny * w)); R.append((x - nx * w, y - ny * w))
    x0, yy = c[0]
    return f'M{x0:.1f} {yy - 2:.1f} ' + ' '.join(f'L{x:.1f} {y:.1f}' for x, y in L) + ' ' + ' '.join(f'L{x:.1f} {y:.1f}' for x, y in R[::-1]) + 'Z'
desk = road([(585, 610), (566, 624), (530, 642), (504, 666), (508, 698), (536, 734), (562, 770), (650, 815), (780, 862), (930, 930)],
            12, 330, 610, 930)
mob = road([(300, 504), (276, 516), (246, 530), (218, 550), (204, 578), (210, 610), (200, 660), (196, 760), (200, 870)],
           8, 210, 504, 870)
json.dump({'desk': desk, 'mob': mob}, open('/Users/jini/.cache/agent-scratch/promo/bh3/roads.json', 'w'))
print(len(desk), len(mob))

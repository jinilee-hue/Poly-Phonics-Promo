"""Concept B hero road (viewBox 0 0 1440 420, .land coords): one smooth centreline from the village
down to the bottom edge, widened with perspective, closed as a single borderless filled outline.
Also prints where each letter stone should sit (% of .land) so the stones stay on the centreline."""
import math
P = [(1257, 30), (1252, 50), (1214, 72), (1152, 100), (1098, 132), (1070, 170), (1050, 208), (1000, 248), (920, 292), (820, 346), (720, 412), (620, 494), (530, 580)]
def catmull(pts, n=40):
    ext = [pts[0]] + pts + [pts[-1]]; out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                  + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    return out + [pts[-1]]
c = catmull(P)
# even spacing + moving-average smoothing so the outline has no kinks where catmull segments meet
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
            r = min(k, i, n - 1 - i)          # shrink the window at the ends: continuous, ends stay put
            lo, hi = i - r, i + r + 1
            q.append((sum(p[0] for p in pts[lo:hi]) / (hi - lo), sum(p[1] for p in pts[lo:hi]) / (hi - lo)))
        pts = q
    return pts
c = smooth(resample(c))
def width(y):
    f = max(0.0, min(1.0, (y - 34) / 410))
    return 24 + 254 * f ** 1.12   # monotonic: no shoulder where it leaves the yard
L, R = [], []
for i, (x, y) in enumerate(c):
    a, b = c[max(0, i - 6)], c[min(len(c) - 1, i + 6)]
    dx, dy = b[0] - a[0], b[1] - a[1]; m = math.hypot(dx, dy) or 1
    nx, ny = -dy / m, dx / m; w = width(y) / 2
    L.append((x + nx * w, y + ny * w)); R.append((x - nx * w, y - ny * w))
x0, y0 = c[0]
d = f'M{x0:.1f} {y0 - 3:.1f} ' + ' '.join(f'L{x:.1f} {y:.1f}' for x, y in L) + ' ' + ' '.join(f'L{x:.1f} {y:.1f}' for x, y in R[::-1]) + 'Z'
print(d)
# stone spots: nearest centreline point to these target y values
import sys
for name, ty in [('p', 74), ('t', 128), ('s', 190), ('a', 246), ('m', 312)]:
    x, y = min(c, key=lambda q: abs(q[1] - ty))
    print(f'#stone {name}: left {x / 1440 * 100:.1f}%  top {y / 420 * 100:.1f}%  road width {width(y):.0f}', file=sys.stderr)

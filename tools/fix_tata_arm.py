"""Tata-book: the pointing hand floated with no arm (AI artefact). Paint a clay forearm from the
hanging arm's elbow across the belly to the wrist. usage: fix_tata_arm.py SRC DST [ax ay bx by r]"""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, dst = sys.argv[1], sys.argv[2]
ax, ay, bx, by, r = map(float, sys.argv[3:8]) if len(sys.argv) > 7 else (466, 768, 576, 772, 34)
ra, rb = r - 4, r + 2          # taper: thinner at the wrist, chunkier at the elbow
im = np.array(Image.open(src).convert('RGBA')).astype(float)
H, W = im.shape[:2]
yy, xx = np.mgrid[0:H, 0:W].astype(float)

def capsule(ax, ay, bx, by, r):
    vx, vy = bx - ax, by - ay
    t = np.clip(((xx - ax) * vx + (yy - ay) * vy) / (vx * vx + vy * vy), 0, 1)
    cx, cy = ax + t * vx, ay + t * vy
    dx, dy = xx - cx, yy - cy
    d = np.sqrt(dx * dx + dy * dy)
    return d, dx, dy, t

orig = im.copy()
# hand pixels to keep in front (fingers/palm left of the wrist)
R, G, B, A = [orig[..., i] for i in range(4)]
hand = (xx >= 300) & (xx < ax - 2) & (yy >= 660) & (yy <= 808) & (R > 150) & (G > 50) & (G < 175) & (B < 90) & (A > 200)

# soft contact shadow on the vest
d, _, _, t = capsule(ax, ay + 9, bx, by + 9, r)
rt = ra + (rb - ra) * t + 5
sh = np.clip((rt - d) / 6, 0, 1)
sh = np.array(Image.fromarray((sh * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(7))).astype(float) / 255
im[..., :3] *= (1 - .42 * sh)[..., None]

# the forearm, clay-shaded (light from the upper left, like the rest of the character)
d, dx, dy, t = capsule(ax, ay, bx, by, r)
rt = ra + (rb - ra) * t
inside = np.clip(rt - d + .5, 0, 1)
nx, ny = dx / rt, dy / rt
nz = np.sqrt(np.clip(1 - nx * nx - ny * ny, 0, 1))
L = np.array([-.35, -.75, .56]); L /= np.linalg.norm(L)
lam = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
dark, mid, lite = np.array([196, 84, 8.]), np.array([250, 120, 16.]), np.array([255, 146, 42.])
k = lam[..., None]
col = np.where(k < .55, dark + (mid - dark) * (k / .55), mid + (lite - mid) * ((k - .55) / .45))
col += (np.clip(lam - .9, 0, 1) * 160)[..., None] * np.array([1, .55, .3])   # soft sheen
a = inside[..., None]
im[..., :3] = im[..., :3] * (1 - a) + col * a
im[..., 3] = np.maximum(im[..., 3], inside * 255)

# fingers back on top, fading into the forearm over the wrist (no seam)
fade = np.clip((ax - 4 - xx) / 26, 0, 1)
fade = fade * fade * (3 - 2 * fade)
w = (hand * fade)[..., None]
im = im * (1 - w) + orig * w
Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)).save(dst, 'WEBP', quality=92, method=6)
print('ok', dst)

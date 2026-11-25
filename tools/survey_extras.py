"""Extra survey-face layers (all on the source canvas of each face, coordinates on a 1000 px basis):
  별로  fun-2-base.webp  the face with its two sweat drops painted out (fitted skin)
        fun-2-sweat.webp the two drops alone — CSS runs them down the temple over and over
  보통  fun-3-plain.webp the face with a short flat mouth (its smile painted out)
        fun-3-smile.webp the source's own smile — CSS turns plain → smile
usage: uv run --with numpy --with pillow --with opencv-python-headless python tools/survey_extras.py"""
import os
import numpy as np, cv2
from PIL import Image
D = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img', 'emoji3d')

def load(n):
    im = Image.open(f'{D}/fun-{n}.webp').convert('RGBA'); return np.asarray(im).astype(float), im.size[0] / 1000

def skin_fit(rgb, ring, fill):
    ys, xs = np.where(ring)
    A = np.stack([np.ones(len(xs)), xs, ys, xs * xs, xs * ys, ys * ys], 1).astype(float)
    fy, fx = np.where(fill)
    F = np.stack([np.ones(len(fx)), fx, fy, fx * fx, fx * fy, fy * fy], 1).astype(float)
    out = rgb.copy()
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A, rgb[ys, xs, c], rcond=None); out[fy, fx, c] = np.clip(F @ coef, 0, 255)
    return out

# ---- 별로: sweat drops ----
a, s = load(2); H, W = a.shape[:2]; rgb = a[..., :3]; al = a[..., 3]
R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
box = np.zeros((H, W), bool); box[int(280 * s):int(455 * s), int(690 * s):int(800 * s)] = True
drop = box & (al > 0) & (B > 150) & (B - R > 30)
drop = cv2.dilate(drop.astype(np.uint8), np.ones((5, 5), np.uint8), iterations=max(1, int(2 * s))).astype(bool) & box
ring = cv2.dilate(drop.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=int(10 * s)).astype(bool) & ~drop & (al > 250) & (R > 180) & (B < 120)
wide = cv2.dilate(drop.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=int(9 * s)).astype(bool)   # the drops' soft shadow and rim too
base = a.copy(); base[..., :3] = cv2.inpaint(rgb.astype(np.uint8), wide.astype(np.uint8) * 255, int(16 * s), cv2.INPAINT_TELEA)
soft = cv2.GaussianBlur(drop.astype(np.float32), (0, 0), 1.2)
sw = cv2.GaussianBlur(wide.astype(np.float32), (0, 0), 3 * s)
base[..., :3] = rgb * (1 - sw[..., None]) + base[..., :3] * sw[..., None]
sweat = np.zeros_like(a); sweat[..., :3] = rgb; sweat[..., 3] = np.where(drop, al, 0) * np.clip(soft * 1.4, 0, 1)
Image.fromarray(base.astype(np.uint8)).save(f'{D}/fun-2-base.webp', 'WEBP', quality=90, method=6)
Image.fromarray(sweat.astype(np.uint8)).save(f'{D}/fun-2-sweat.webp', 'WEBP', quality=90, method=6)

# ---- 보통: plain → smile (user 2026-11-25: the source already smiles, so start from a plain face) ----
a, s = load(3); H, W = a.shape[:2]; rgb = a[..., :3]; al = a[..., 3]
R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
mbox = np.zeros((H, W), bool); mbox[int(512 * s):int(600 * s), int(390 * s):int(605 * s)] = True
line = mbox & (R < 190) & (G < 95) & (al > 200)                     # the smile line on the source
line = cv2.dilate(line.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=max(2, int(6 * s))).astype(bool)
plain_rgb = cv2.inpaint(rgb.astype(np.uint8), line.astype(np.uint8) * 255, int(14 * s) or 3, cv2.INPAINT_TELEA).astype(float)
S4 = 4; big = np.zeros((H * S4, W * S4), np.uint8)
P = lambda x, y: (int(x * s * S4), int(y * s * S4))
cv2.line(big, P(450, 566), P(550, 566), 255, max(2, int(7 * s * S4)), cv2.LINE_AA)   # a short, flat mouth
ink = cv2.resize(big, (W, H), interpolation=cv2.INTER_AREA).astype(float) / 255
plain = a.copy(); plain[..., :3] = plain_rgb * (1 - ink[..., None]) + np.array([92, 34, 12]) * ink[..., None]
Image.fromarray(np.clip(plain, 0, 255).astype(np.uint8)).save(f'{D}/fun-3-plain.webp', 'WEBP', quality=92, method=6)
# the smile overlay: the source's own mouth area, feathered, so it lands exactly where the plain mouth was
patch = np.zeros((H, W), np.float32); patch[int(505 * s):int(605 * s), int(380 * s):int(620 * s)] = 1
patch = cv2.GaussianBlur(patch, (0, 0), 7 * s)
smile = a.copy(); smile[..., 3] = al * np.clip(patch * 1.25, 0, 1)
Image.fromarray(np.clip(smile, 0, 255).astype(np.uint8)).save(f'{D}/fun-3-smile.webp', 'WEBP', quality=92, method=6)
print('ok')

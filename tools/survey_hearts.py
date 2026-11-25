"""아주 좋아했어요 heart eyes (assets/img/emoji3d/fun-5.webp) as clean layers that can grow without showing a ragged rim:
  - the mask is the heart only (no orange skin ring), smoothed at 4x so the rim never looks stair-stepped
  - hearts are recoloured to C's yellow (user 2026-11-25), keeping their 3D shading
Writes fun-5-heartL.webp / fun-5-heartR.webp and prints each heart's centre (% of the canvas) for survey.css.
usage: uv run --with numpy --with scipy --with pillow python tools/survey_hearts.py"""
import os, colorsys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd
D = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img', 'emoji3d')
im = Image.open(f'{D}/fun-5.webp').convert('RGBA'); a = np.asarray(im).astype(float); H, W = a.shape[:2]
R, G, B, A = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
hsv = np.stack(np.vectorize(colorsys.rgb_to_hsv, otypes=[float, float, float])(R / 255, G / 255, B / 255), -1)
h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
# heart = red/pink hue (not the orange skin, hue ≈ .05-.1), upper half of the face
red = (A > 200) & ((h > .9) | (h < .025)) & (s > .35) & (v > .35)
red[int(H * .6):] = False
red = nd.binary_closing(red, iterations=3); red = nd.binary_fill_holes(red)
lab, k = nd.label(red); sizes = nd.sum(red, lab, range(1, k + 1))
idx = (np.argsort(sizes)[::-1][:2] + 1)
idx = sorted(idx, key=lambda i: np.where(lab == i)[1].mean())
out = []
for side, i in zip('LR', idx):
    m = lab == i
    ys, xs = np.where(m); cx, cy = xs.mean() / W * 100, ys.mean() / H * 100
    # recolour to C's yellow, keep the light/shade (value) of the original heart
    hh = np.full_like(h, .125); ss = np.clip(s * .95, 0, .85); vv = np.clip(v * 1.12 + .06, 0, 1)
    yel = np.stack(np.vectorize(colorsys.hsv_to_rgb, otypes=[float, float, float])(hh, ss, vv), -1) * 255
    # smooth masks: work at 4x, blur, threshold, then shrink — no stair-stepped rim
    def smooth(mask, grow):
        big = Image.fromarray((mask * 255).astype(np.uint8)).resize((W * 4, H * 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(6))
        arr = np.asarray(big).astype(float) / 255
        cut = .5 if grow == 0 else .5 * np.exp(-grow / 3.2)
        hard = (arr > cut).astype(np.uint8) * 255
        return np.asarray(Image.fromarray(hard).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.LANCZOS)).astype(float) / 255
    core = smooth(m, 0)
    outer = smooth(m, 7)                       # white sticker rim ≈ 3 px at 1 px = 1/340 of the face
    layer = np.zeros_like(a)
    layer[..., :3] = yel * core[..., None] + 255 * (1 - core[..., None])
    layer[..., 3] = core * 255             # no white rim (user 2026-11-25); the heart only ever grows, so the base heart stays hidden
    Image.fromarray(np.clip(layer, 0, 255).astype(np.uint8)).save(f'{D}/fun-5-heart{side}.webp', 'WEBP', quality=92, method=6)
    out.append((side, round(cx, 1), round(cy, 1)))
print(out)

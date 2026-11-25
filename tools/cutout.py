"""White-background character sheets -> transparent cutouts (colour-to-alpha on the border-connected light area).
usage: cutout.py SRC OUTDIR NAME [pick ...]   pick = index of component sorted left->right, top->bottom; 'all' = whole image"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as nd
src, outdir, name, *picks = sys.argv[1:]
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
H, W, _ = im.shape
mn = im.min(2); mx = im.max(2)
light = (mn > 150) & ((mx - mn) < 28)              # whites + soft grey shadows
lab, n = nd.label(light)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(border))
# enclosed pure-white holes (gap between legs) also go; the cream collars and the grey-white P logo stay
for i in set(range(1, n + 1)) - border:
    m = lab == i
    if m.sum() > 150 and (mx[m] - mn[m]).mean() < 6 and mn[m].mean() >= 247: bg |= m
band = nd.binary_dilation(bg, iterations=2) & ~bg  # anti-aliased rim just outside the bg area
zone = bg | band
# colour-to-alpha against white
a = np.clip((255 - mn) / 255.0, 0, 1)
a = np.where(zone, a, 1.0)
a = np.where(bg, np.clip(a * 1.6, 0, 1) ** 1.15, a)   # shadows a bit stronger, pure white -> 0
safe = np.maximum(a, 1e-3)[..., None]
col = np.where(zone[..., None], (im - 255 * (1 - safe)) / safe, im)
col = np.clip(col, 0, 255)
rgba = np.dstack([col, a * 255]).astype(np.uint8)
fg = a > 0.5
fl, fn = nd.label(nd.binary_closing(fg, iterations=3))
objs = nd.find_objects(fl)
comps = []
for i, sl in enumerate(objs):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if h * w > (H * W) * 0.01: comps.append(sl)
comps.sort(key=lambda s: (round(s[0].start / (H / 3)), s[1].start))
print(name, 'components:', [(s[1].start, s[0].start, s[1].stop - s[1].start, s[0].stop - s[0].start) for s in comps])
for p in (picks or ['all']):
    if p == 'all':
        ys, xs = np.where(a > 0.02); sl = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1))
    else:
        sl = comps[int(p)]
    pad = 8
    y0, y1 = max(0, sl[0].start - pad), min(H, sl[0].stop + pad + 30)   # keep the contact shadow under feet
    x0, x1 = max(0, sl[1].start - pad), min(W, sl[1].stop + pad)
    crop = rgba[y0:y1, x0:x1].copy()
    if p != 'all':  # drop pixels that belong to other components
        own = (fl[y0:y1, x0:x1] == (objs.index(sl) + 1)) | ~fg[y0:y1, x0:x1]
        crop[..., 3] = np.where(own, crop[..., 3], 0)
    out = f"{outdir}/{name}{'' if p == 'all' else '-' + p}.png"
    Image.fromarray(crop).save(out); print('->', out, crop.shape[1], 'x', crop.shape[0])

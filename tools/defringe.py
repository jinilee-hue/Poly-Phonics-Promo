"""Clean cut-out edges: drop the light matte fringe, pull edge colours from the inside, re-antialias the alpha.
usage: uv run --with numpy --with scipy --with pillow python tools/defringe.py IN.webp [OUT.webp] [--clear x0,y0,x1,y1 ...]
--clear: a box where light, cool pixels are leftover background sealed off by the character (Bobo's ear gap)."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd
args = sys.argv[1:]
boxes = [tuple(int(v) for v in args[i + 1].split(',')) for i, a in enumerate(args) if a == '--clear']
pos = [a for i, a in enumerate(args) if a != '--clear' and (i == 0 or args[i - 1] != '--clear')]
src = pos[0]; dst = pos[1] if len(pos) > 1 else src
im = np.asarray(Image.open(src).convert('RGBA')).astype(np.float32)
rgb, al = im[..., :3], im[..., 3]
solid = al > 128
# white background trapped in gaps (e.g. between Bobo's ear and head): grow the outside through light, cool/neutral
# pixels. Warm creams (collars, r > b) and enclosed whites (eyes, logo) are never reached.
mn0, mx0 = rgb.min(-1), rgb.max(-1)
light_cool = solid & (mn0 > 185) & ((rgb[..., 2] - rgb[..., 0]) >= -6) & (mx0 - mn0 < 60)
lab0, _ = nd.label(~solid | light_cool)
bg_ids = np.unique(lab0[~solid]); bg_ids = bg_ids[bg_ids > 0]
trapped = np.isin(lab0, bg_ids) & solid
solid = solid & ~nd.binary_dilation(trapped, iterations=1)
for x0, y0, x1, y1 in boxes:
    box = np.zeros_like(solid); box[y0:y1, x0:x1] = True
    sealed = box & solid & (mn0 > 150) & ((rgb[..., 2] - rgb[..., 0]) >= -6)
    solid = solid & ~nd.binary_dilation(sealed, iterations=1)
# light, low-saturation pixels on the outer rim = leftover white matte
rim = solid & ~nd.binary_erosion(solid, iterations=3)
mn, mx = rgb.min(-1), rgb.max(-1)
matte = rim & (mn > 185) & (mx - mn < 40)
mask = solid & ~matte
mask = nd.binary_opening(mask, iterations=1)          # nibble single-pixel spurs
mask = nd.binary_erosion(mask, iterations=1)          # 1px inset so no fringe survives
lab, n = nd.label(mask)                               # keep the character, drop crumbs
if n > 1:
    sizes = nd.sum(mask, lab, range(1, n + 1)); mask = lab == (int(np.argmax(sizes)) + 1)
# colours: every pixel near/outside the edge takes the nearest well-inside colour
inner = nd.binary_erosion(mask, iterations=3)
_, (iy, ix) = nd.distance_transform_edt(~inner, return_indices=True)
fixed = rgb[iy, ix]
keep = inner[..., None]
rgb2 = np.where(keep, rgb, fixed)
# antialiased alpha from the binary mask (supersampled feel via blur + contrast)
soft = nd.gaussian_filter(mask.astype(np.float32), sigma=1.0)
alpha = np.clip((soft - .5) * 2.4 + .5, 0, 1) * 255
out = np.dstack([rgb2, alpha]).clip(0, 255).astype(np.uint8)
img = Image.fromarray(out, 'RGBA')   # keep the canvas so width/height in the HTML stay true
img.save(dst, 'WEBP', quality=90, method=6)
print(dst, img.size, 'matte px removed', int(matte.sum()), 'trapped bg px', int(trapped.sum()))

"""Per-concept character casts from the Phonics Land sheets (cutouts made with tools/cutout.py into FAM).
A = Sound Seed Explorers, D = Little Big House (fur texture); B and C keep Classmate Friends (user 2026-11-25).
Pocket Friends (cast-pocket) was tried on B and dropped; it stays in CAST so it can be rebuilt.
Roles keep the old file roles so layouts stay: blue (was Bobo), orange (was Tata), yellow (was Nunu), *-face, group.
usage: uv run --with numpy --with scipy --with pillow python tools/cast_build.py FAM_DIR"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd
FAM = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img')
CAST = {
  'cast-seed':   {'group': 'seedgroup-0', 'blue': 'collv-1', 'orange': 'loopv-1', 'yellow': 'beadv-1',
                  'blue-face': 'colle-1', 'orange-face': 'loope-1', 'yellow-face': 'beade-1'},
  'cast-pocket': {'group': 'pocketgroup-0', 'blue': 'popov-1', 'orange': 'duduv-1', 'yellow': 'momov-0',
                  'orange-face': 'dudue-1'},
  'cast-lbh':    {'group': 'lbhgroup-0', 'blue': 'partyv-1', 'orange': 'feetv-1', 'yellow': 'bigv-1',
                  'blue-face': 'partye-1', 'orange-face': 'feete-1', 'yellow-face': 'bige-1'},
}
def clean(im, keep_frac=.02):
    """drop stray bits (contact-shadow arcs, neighbour crumbs): keep components >= keep_frac of the largest"""
    arr = np.asarray(im).copy(); a = arr[..., 3]
    lab, n = nd.label(a > 40)
    if n > 1:
        sizes = nd.sum(np.ones_like(a), lab, range(1, n + 1)); big = sizes.max()
        keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= big * keep_frac])
        arr[..., 3] = np.where(keep | (a <= 40) & nd.binary_dilation(keep, iterations=2), a, 0)
    out = Image.fromarray(arr); bb = out.getbbox(); return out.crop(bb)
def fit(im, box):
    im = im.copy(); im.thumbnail(box, Image.LANCZOS); return im
def sticker(im, frac=.034):
    a = np.asarray(im.getchannel('A')) > 90
    r = max(6, int(max(im.size) * frac))
    pad = r + 4
    big = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); big.alpha_composite(im, (pad, pad))
    m = np.zeros((big.height, big.width), bool); m[pad:pad + im.height, pad:pad + im.width] = a
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]; disk = xx * xx + yy * yy <= r * r
    m = nd.binary_dilation(m, structure=disk)
    rim = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    white = Image.new('RGBA', big.size, (255, 255, 255, 255)); white.putalpha(rim)
    white.alpha_composite(big)
    bb = white.getbbox(); return white.crop(bb)
STICKER = set()
for folder, roles in CAST.items():
    os.makedirs(os.path.join(OUT, folder), exist_ok=True)
    for role, src in roles.items():
        im = clean(Image.open(os.path.join(FAM, src + '.png')).convert('RGBA'), .02 if role == 'group' else .2)
        box = (1400, 900) if role == 'group' else ((360, 420) if role.endswith('face') else (520, 640))
        im = fit(im, box)
        if folder in STICKER: im = sticker(im)   # white die-cut outline (tried on C's sticker look; user kept C's own cast)
        im.save(os.path.join(OUT, folder, role + '.webp'), 'WEBP', quality=88, method=6)
        print(folder, role, im.size)

"""좋아했어요 face (assets/img/emoji3d/fun-4.webp): split the thumbs-up hand off so CSS can wag it up and down.
  fun-4-thumb.webp  the raised forearm + hand (same canvas)
  fun-4-base.webp   the face without the hand; a stub of the forearm stays by the shoulder so the wag never opens a gap
Polygon traced on the 1013 px image (hand sits apart from the head except where the arm meets it, x≈700-778, y≈600-640).
usage: uv run --with numpy --with scipy --with pillow python tools/survey_thumb.py"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
D = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img', 'emoji3d')
im = Image.open(f'{D}/fun-4.webp').convert('RGBA'); W, H = im.size
s = W / 1013
poly = [(778, 430), (1013, 430), (1013, 1013), (700, 1013), (700, 642), (770, 602), (778, 560)]
stub = [(690, 600), (775, 600), (775, 840), (690, 840)]          # forearm kept on the base near the shoulder
def mask(pts):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([(x * s, y * s) for x, y in pts], fill=255); return m
region = np.asarray(mask(poly)) > 0
keep = np.asarray(mask(stub)) > 0
a = np.asarray(im).copy()
R, G, B, A = [a[..., i].astype(int) for i in range(4)]
navy = B > R
cream = (R > 200) & (G > 180) & (B > 150) & (R - B < 80)
skin = region & (A > 0) & ~navy & ~cream
# only the hand: the skin blob that holds the palm (the head's rim inside the box is a separate blob)
from scipy import ndimage as nd
lab, _ = nd.label(skin)
seed = lab[int(620 * s), int(860 * s)]
hand = lab == seed
# take the hand's soft outline too (light anti-aliased rim), but never the shirt
hand = nd.binary_dilation(hand, iterations=max(2, int(4 * s))) & region & (A > 0) & ~navy
thumb = a.copy(); thumb[~hand, 3] = 0
base = a.copy(); base[hand & ~keep, 3] = 0
# soften the stub's cut edge so it never shows as a hard line under the moving hand
Image.fromarray(thumb).save(f'{D}/fun-4-thumb.webp', 'WEBP', quality=90, method=6)
Image.fromarray(base).save(f'{D}/fun-4-base.webp', 'WEBP', quality=90, method=6)
print('ok', W, H)

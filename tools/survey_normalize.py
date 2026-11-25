"""Make the five survey faces the same size: every face and its overlays get one affine so the head is 660/1000 wide
at eye level, centred, eyes at y = 450/1000. Sources stay as fun-*.webp; outputs are face-*.webp (600 px) for survey.js.
Head measurements (1000 px basis, eye-row width / centre x / eye y) come from the current fun-*.webp files.
usage: uv run --with pillow python tools/survey_normalize.py"""
import os
from PIL import Image
D = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img', 'emoji3d')
OUT = 600; TW, TY = 660, 450
FACES = {  # n: (width, centre, eye_y, base, overlays)
    1: (610, 500, 419, 'fun-1', []),
    2: (686, 479, 405, 'fun-2-base', ['fun-2-sweat']),
    3: (792, 495, 469, 'fun-3', ['fun-3-lid', 'fun-3-grin']),
    4: (637, 449, 388, 'fun-4-base', ['fun-4-lid', 'fun-4-thumb']),
    5: (649, 499, 396, 'fun-5', ['fun-5-heartL', 'fun-5-heartR']),
}
def params(w, c, ey):
    k = TW / w; dx = -(c - 500) * k; dy = TY - (500 + (ey - 500) * k); return k, dx, dy
def place(x, y, k, dx, dy):  # 1000-basis point → % of the output
    return round((500 + (x - 500) * k + dx) / 10, 1), round((500 + (y - 500) * k + dy) / 10, 1)
for n, (w, c, ey, base, ovs) in FACES.items():
    k, dx, dy = params(w, c, ey)
    for f in [base] + ovs:
        im = Image.open(f'{D}/{f}.webp').convert('RGBA'); s = im.size[0] / 1000
        q = 1000 / OUT
        data = (s * q / k, 0, s * (500 - (500 + dx) / k), 0, s * q / k, s * (500 - (500 + dy) / k))
        out = im.transform((OUT, OUT), Image.AFFINE, data, resample=Image.BICUBIC)
        name = f'face-{n}' if f == base else 'face-' + f.split('-', 1)[1]
        out.save(f'{D}/{name}.webp', 'WEBP', quality=90, method=6)
    print(n, 'k', round(k, 3))
k, dx, dy = params(*FACES[5][:3]); print('hearts', place(377, 396, k, dx, dy), place(627, 396, k, dx, dy))
k, dx, dy = params(*FACES[4][:3]); print('thumb pivot', place(710.8, 730.5, k, dx, dy))

"""Survey faces (Tata expressions, assets/img/emoji3d/fun-1..5.webp) split into layers so CSS can move them like a real face:
  fun-N-body.webp  everything except the head (collar in front)
  fun-N-head.webp  the head (+ a band below the collar line, hidden under the body, so a tilt never opens a gap)
  fun-N-lid.webp   closed eyelids for a blink (faces with open eyes: 2, 3, 4)
  fun-5-heartL/R.webp  each heart eye on its own, to pulse around its own centre
Prints the neck pivot and heart centres (% of the canvas) for survey.css.
usage: uv run --with numpy --with scipy --with pillow --with opencv-python-headless python tools/survey_faces.py"""
import os, json
import numpy as np, cv2
from PIL import Image
from scipy import ndimage as nd
D = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img', 'emoji3d')
S = 256
def save(arr, name):
    Image.fromarray(arr.astype(np.uint8), 'RGBA').save(f'{D}/{name}', 'WEBP', quality=90, method=6)
info = {}
for n in range(1, 6):
    a = np.asarray(Image.open(f'{D}/fun-{n}.webp').convert('RGBA').resize((S, S), Image.LANCZOS)).astype(float)
    rgb, al = a[..., :3], a[..., 3]; H, W = al.shape
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    cream = (al > 200) & (R > 215) & (G > 195) & (B > 160) & (R - B < 75)
    cream[: int(H * .58)] = False; cream[:, : int(W * .2)] = False; cream[:, int(W * .8):] = False
    split = int(np.where(cream.any(1))[0].min()) + 2                       # top of the collar
    above = (al > 8); above[split:] = False
    lab, k = nd.label(above); sizes = nd.sum(above, lab, range(1, k + 1))
    head = lab == (int(np.argmax(sizes)) + 1)
    head = nd.binary_dilation(head, iterations=1) & (al > 0)
    xs = np.where(head.any(0))[0]; x0, x1 = xs.min(), xs.max()
    band = np.zeros_like(head); band[split: split + int(H * .07), x0 + 6: x1 - 6] = True
    hmask = (head | (band & (al > 0)))
    headA = a.copy(); headA[~hmask, 3] = 0
    bodyA = a.copy(); bodyA[head, 3] = 0
    save(headA, f'fun-{n}-head.webp'); save(bodyA, f'fun-{n}-body.webp')
    cx = (x0 + x1) / 2
    info[n] = {'neck': [round(cx / W * 100, 1), round(split / H * 100, 1)]}
    # blink: open eyes = white blobs in the face (not the collar), fill with fitted skin, draw a soft lash curve
    mn, mx = rgb.min(-1), rgb.max(-1)
    white = head & (mn > 200) & (mx - mn < 45); white[split - int(H * .05):] = False
    lab, k = nd.label(white); eyes = []
    for i in range(1, k + 1):
        ys, xs2 = np.where(lab == i)
        if len(ys) > 40: eyes.append((xs2.min(), xs2.max(), ys.min(), ys.max()))
    if n in (2, 3, 4) and len(eyes) >= 2:
        eyes = sorted(eyes, key=lambda e: -(e[1] - e[0]) * (e[3] - e[2]))[:2]
        lid = np.zeros_like(a)
        for (ex0, ex1, ey0, ey1) in eyes:
            pad = 3
            box = np.zeros(al.shape, bool); box[ey0 - pad: ey1 + pad + 1, ex0 - pad: ex1 + pad + 1] = True
            eyeblob = box & head
            ring = nd.binary_dilation(eyeblob, iterations=6) & ~nd.binary_dilation(eyeblob, iterations=2) & head
            skin = ring & (R > 180) & (G > 70) & (G < 170) & (B < 90)
            ys, xs2 = np.where(skin)
            if len(ys) < 20: continue
            A = np.stack([np.ones(len(xs2)), xs2, ys, xs2 * xs2, xs2 * ys, ys * ys], 1).astype(float)
            fy, fx = np.where(eyeblob)
            F = np.stack([np.ones(len(fx)), fx, fy, fx * fx, fx * fy, fy * fy], 1).astype(float)
            for c in range(3):
                coef, *_ = np.linalg.lstsq(A, rgb[ys, xs2, c], rcond=None)
                lid[fy, fx, c] = np.clip(F @ coef, 0, 255)
            # soft-edged lid: full inside the eye box, feathered 1-2 px outside (per eye, kept with max)
            soft = cv2.GaussianBlur(eyeblob.astype(np.float32), (0, 0), 1.2)
            ring2 = (soft > .02) & ~eyeblob
            ry, rx = np.where(ring2)
            if len(ry):
                G2 = np.stack([np.ones(len(rx)), rx, ry, rx * rx, rx * ry, ry * ry], 1).astype(float)
                for c in range(3):
                    coef, *_ = np.linalg.lstsq(A, rgb[ys, xs2, c], rcond=None)
                    lid[ry, rx, c] = np.clip(G2 @ coef, 0, 255)
            lid[..., 3] = np.maximum(lid[..., 3], np.where(eyeblob, 255, soft * 255))
            # lash: a gentle arc across the middle of the eye
            canvas = np.zeros((H * 4, W * 4), np.uint8)
            mx0, mx1, my = ex0 * 4, ex1 * 4, int((ey0 + ey1) / 2 * 4 + (ey1 - ey0) * .5)
            my = int((ey0 + ey1) / 2 * 4)
            pts = np.array([[mx0 + t * (mx1 - mx0), my + np.sin(t * np.pi) * (ey1 - ey0) * 4 * .2] for t in np.linspace(0, 1, 24)], np.int32)   # closed lid ︶
            cv2.polylines(canvas, [pts], False, 255, thickness=max(4, int((ey1 - ey0) * .7)), lineType=cv2.LINE_AA)
            lash = cv2.resize(canvas, (W, H), interpolation=cv2.INTER_AREA).astype(float) / 255
            for c, v in enumerate((70, 38, 22)): lid[..., c] = lid[..., c] * (1 - lash) + v * lash
            lid[..., 3] = np.maximum(lid[..., 3], lash * 255)
        save(lid, f'fun-{n}-lid.webp'); info[n]['lid'] = True
    if n == 5:   # heart eyes: red-pink blobs, one layer each
        heart = head & (R > 190) & (G < 130) & (B > 60) & (B < 170)
        heart = nd.binary_closing(heart, iterations=2)
        lab, k = nd.label(heart); sizes = nd.sum(heart, lab, range(1, k + 1))
        idx = np.argsort(sizes)[::-1][:2] + 1
        cents = []
        for side, i in zip('LR', sorted(idx, key=lambda i: np.where(lab == i)[1].mean())):
            m = nd.binary_dilation(lab == i, iterations=2)
            hA = a.copy(); hA[~m, 3] = 0
            save(hA, f'fun-5-heart{side}.webp')
            ys, xs2 = np.where(lab == i); cents.append([round(xs2.mean() / W * 100, 1), round(ys.mean() / H * 100, 1)])
        info[n]['hearts'] = cents
print(json.dumps(info))

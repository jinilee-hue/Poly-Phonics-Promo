"""Closed-eye overlays for concept C hero characters.
For each *-jump.webp: find each eye (white + pupil + dark rim), fill it with a smooth skin surface fitted to the skin
around it (quadratic fit — the nose and eyebrows are ignored, so no colour bleeds in), then draw a soft lash curve:
'closed' = gentle ︶, 'happy' = ^ ^ arc. Writes assets/img/concept-c/<name>-eyes-closed.webp / -eyes-happy.webp
(same canvas as the character, transparent except over the eyes) for CSS to fade in during a blink.
usage: uv run --with numpy --with scipy --with pillow --with opencv-python-headless python tools/eyes_closed.py"""
import os
import numpy as np, cv2
from PIL import Image, ImageDraw
from scipy import ndimage as nd
D = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img', 'concept-c')
SS = 4
def fit_fill(rgb, samples_mask, fill_mask):
    ys, xs = np.where(samples_mask); H, W = samples_mask.shape
    def feats(x, y):
        x = x / W; y = y / H
        return np.stack([np.ones_like(x), x, y, x * x, x * y, y * y], 1)
    A = feats(xs.astype(float), ys.astype(float))
    out = rgb.astype(float).copy()
    fy, fx = np.where(fill_mask); F = feats(fx.astype(float), fy.astype(float))
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A, rgb[ys, xs, c].astype(float), rcond=None)
        out[fy, fx, c] = F @ coef
    return np.clip(out, 0, 255)
for name in ['bobo', 'tata', 'nunu']:
    im = Image.open(f'{D}/{name}-jump.webp').convert('RGBA'); a = np.asarray(im).copy()
    rgb = a[..., :3].astype(int); al = a[..., 3]; H, W = al.shape
    mn, mx = rgb.min(-1), rgb.max(-1)
    white = (al > 200) & (mn > 205) & (mx - mn < 40); white[int(H * .48):] = False
    lab, k = nd.label(white)
    sizes = sorted([((lab == i + 1).sum(), i + 1) for i in range(k)], reverse=True)[:2]
    eye_masks = []; boxes = []
    for _, i in sizes:
        ys, xs = np.where(lab == i); cx, cy = xs.mean(), ys.mean(); w = xs.max() - xs.min(); h = ys.max() - ys.min()
        # gather white + dark (pupil/rim) pixels near this eye, take the convex hull
        x0, x1 = int(max(0, cx - w * 1.0)), int(min(W, cx + w * 1.0)); y0, y1 = int(max(0, cy - h * 1.0)), int(min(H, cy + h * 1.0))
        sub = rgb[y0:y1, x0:x1]; smn = sub.min(-1); smx = sub.max(-1)
        cand = ((smn > 160) & (smx - smn < 48)) | (smx < 80)   # whites incl. their grey shading, pupils, dark rim
        cl, ck = nd.label(cand)
        # keep the component(s) touching the eye white
        seed = (lab[y0:y1, x0:x1] == i)
        keep = np.isin(cl, np.unique(cl[seed & (cl > 0)]))
        pts = np.column_stack(np.where(keep))[:, ::-1].astype(np.int32)
        hull = cv2.convexHull(pts); m = np.zeros((H, W), np.uint8)
        cv2.fillConvexPoly(m, hull + np.array([x0, y0]), 255)
        m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)))   # cover the rim, its highlight and AA edge
        eye_masks.append(m > 0)
        yy, xx = np.where(m > 0); boxes.append((xx.min(), yy.min(), xx.max(), yy.max()))
    boxes, eye_masks = zip(*sorted(zip(boxes, eye_masks), key=lambda t: t[0][0]))
    eye = np.logical_or.reduce(eye_masks)
    # skin samples: ring around the eyes, close to the ring's median colour (drops nose, brows, rim)
    ring = cv2.dilate(eye.astype(np.uint8), np.ones((45, 45), np.uint8)).astype(bool) & ~cv2.dilate(eye.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool) & (al > 250)
    med = np.median(rgb[ring], 0)
    skin = ring & (np.abs(rgb - med).sum(-1) < 70)
    # never paint over the nose: a big blob of bright, non-skin, non-white colour that reaches outside the eyes
    dist = np.abs(rgb - med).sum(-1)
    nose_like = (al > 200) & (dist > 120) & (mx > 110) & ~((mn > 160) & (mx - mn < 48))
    nl, nk = nd.label(nose_like)
    nose = np.zeros_like(eye)
    for j in range(1, nk + 1):
        comp = nl == j
        if (comp & ~eye).sum() > 400 and (comp & eye).any(): nose |= comp
    paint = eye & ~nose
    filled = fit_fill(rgb, skin, paint)
    soft = cv2.GaussianBlur(paint.astype(np.float32), (0, 0), 2.5)
    alpha = np.where(nose, 0, np.clip(soft * 1.6, 0, 1)) * 255   # fade out at the cheeks, hard stop at the nose
    x0, y0, x1, y1 = boxes[0]
    band = rgb[max(0, y0 - (y1 - y0)):y0, x0:x1].reshape(-1, 3); s = band.sum(1)
    lash = tuple(int(v) for v in np.median(band[s < np.percentile(s, 5)], 0))
    for mode in ('closed', 'happy'):
        big = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); dr = ImageDraw.Draw(big)
        for (bx0, by0, bx1, by1) in boxes:
            w, h = bx1 - bx0, by1 - by0; cx = (bx0 + bx1) / 2; lw = int(max(5, h * .085) * SS)
            if mode == 'closed':
                cy = by0 + h * .56; box = [(cx - w * .33) * SS, (cy - h * .26) * SS, (cx + w * .33) * SS, (cy + h * .14) * SS]
                dr.arc(box, 18, 162, fill=lash + (255,), width=lw)
            else:
                cy = by0 + h * .60; box = [(cx - w * .28) * SS, (cy - h * .24) * SS, (cx + w * .28) * SS, (cy + h * .30) * SS]
                dr.arc(box, 205, 335, fill=lash + (255,), width=lw)
        strokes = big.resize((W, H), Image.LANCZOS)
        base = Image.fromarray(np.dstack([filled, alpha]).astype(np.uint8), 'RGBA')
        base.alpha_composite(strokes)
        base.save(f'{D}/{name}-eyes-{mode}.webp', 'WEBP', quality=90, method=6)
    print(name, 'boxes', boxes, 'lash', lash, 'skin samples', int(skin.sum()), 'nose px kept out', int(nose.sum()))

/* 시안 B extras (site.js stays as is): the map road through the Unit pins, and the bunting over the song stage. */
(() => {
  const map = document.getElementById('map');
  if (map) {
    const svg = map.querySelector('.map-path');
    const bed = svg.querySelector('.road-bed'), dash = svg.querySelector('.road-dash');
    const pins = [...map.querySelectorAll('.stop .pin')];
    // smooth curve through the pin centres (Catmull-Rom → cubic Bézier)
    function draw() {
      const box = map.getBoundingClientRect();
      if (!box.width) return;
      svg.setAttribute('viewBox', `0 0 ${box.width} ${box.height}`);
      const raw = pins.map(p => { const r = p.getBoundingClientRect(); return [r.left - box.left + r.width / 2, r.top - box.top + r.height / 2]; });
      // where the road turns down a row (same column, big drop) it goes round the outside edge, not under the card
      const pts = [];
      raw.forEach((p, i) => {
        pts.push(p);
        const q = raw[i + 1];
        if (q && box.width > 760 && Math.abs(q[0] - p[0]) < 60 && q[1] - p[1] > 160) {
          const right = p[0] > box.width / 2;
          const x = right ? box.width - 14 : 14;
          pts.push([x, p[1] + (q[1] - p[1]) * 0.28], [x, p[1] + (q[1] - p[1]) * 0.72]);
        }
      });
      let d = `M${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)}`;
      for (let i = 0; i < pts.length - 1; i++) {
        const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
        const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
        const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
        d += ` C${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
      }
      bed.setAttribute('d', d); dash.setAttribute('d', d);
    }
    new ResizeObserver(draw).observe(map);
    addEventListener('load', draw);
    // the reveal motion shifts the pins for ~1s; redraw once they settle
    map.querySelectorAll('.stop').forEach(s => s.addEventListener('transitionend', e => { if (e.propertyName === 'transform') draw(); }));
    draw();
  }

  const flags = document.querySelector('.bunting .flags');
  if (flags) {
    const n = 22, cls = ['f1', 'f2', 'f3', 'f4'];
    let g = '';
    for (let i = 0; i < n; i++) {
      const x = 20 + i * (960 / (n - 1));
      const t = x / 1000, y = 6 + 80 * t * (1 - t);   // on the curve M0 6 Q500 46 1000 6
      g += `<path class="${cls[i % 4]}" d="M${(x - 14).toFixed(1)} ${(y - 1).toFixed(1)} L${(x + 14).toFixed(1)} ${(y - 1).toFixed(1)} L${x.toFixed(1)} ${(y + 24).toFixed(1)}Z"/>`;
    }
    flags.innerHTML = g;
  }
})();

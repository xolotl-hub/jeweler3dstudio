"""
generate_gem_icons.py
Genera 17 SVG con estilos matemáticos/gráficos únicos por talla de gema
y los convierte a PNG de alta resolución usando Inkscape CLI.
"""

import math
import os
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
SVG_DIR = ROOT / "assets" / "gems" / "svg"
PNG_DIR = ROOT / "assets" / "gems" / "png"
SVG_DIR.mkdir(parents=True, exist_ok=True)
PNG_DIR.mkdir(parents=True, exist_ok=True)

S = 256  # canvas size
cx = S / 2
cy = S / 2
R = S * 0.42

def polar(px, py, r, deg):
    a = math.radians(deg)
    return (px + r * math.cos(a), py + r * math.sin(a))

def ring(px, py, r, n, off=0):
    return [polar(px, py, r, 360 * i / n + off) for i in range(n)]

def pts(ps):
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in ps)

def poly(ps, **kw):
    a = " ".join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items())
    return f'<polygon points="{pts(ps)}" {a}/>'

def ln(x1, y1, x2, y2, **kw):
    a = " ".join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items())
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" {a}/>'

def circ(px, py, r, **kw):
    a = " ".join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items())
    return f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{r:.2f}" {a}/>'

def wrap_svg(body, defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">\n<defs>{defs}</defs>\n{body}\n</svg>'

# ══════════════════════════════════════════════════════════════════════════════
# 17 GENERADORES CON ESTILOS GRÁFICOS ÚNICOS
# ══════════════════════════════════════════════════════════════════════════════

def gen_round():
    """1. ROUND: Línea fina elegante / luxury sobre fondo azul marino profundo."""
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#0d1b3e"/>']
    b.append(circ(cx, cy, R, fill="none", stroke="#dde4f5", stroke_width="1.2"))
    tbl = ring(cx, cy, R * 0.38, 8, 22.5)
    b.append(poly(tbl, fill="none", stroke="#dde4f5", stroke_width="1"))
    star = ring(cx, cy, R * 0.72, 8, 0)
    grd = ring(cx, cy, R, 16, 11.25)
    for i in range(8):
        t = tbl[i]; s = star[i]; g1 = grd[i * 2]; g2 = grd[i * 2 + 1]; nt = tbl[(i + 1) % 8]
        for a, b2 in [(t, s), (s, g1), (s, g2), (t, nt)]:
            b.append(ln(a[0], a[1], b2[0], b2[1], stroke="#dde4f5", stroke_width="0.8"))
    return wrap_svg("\n".join(b))

def gen_oval():
    """2. OVAL: Vitral artístico / Stained glass degradado con marco de plomo oscuro."""
    d = '''<linearGradient id="og" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1a6b4a"/>
      <stop offset="45%" stop-color="#0d4f8c"/>
      <stop offset="100%" stop-color="#6b1a6b"/>
    </linearGradient>'''
    ow, oh = R, R * 1.28
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#111111"/>']
    b.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{ow:.1f}" ry="{oh:.1f}" fill="url(#og)" stroke="#111111" stroke-width="3"/>')
    for frac in [0.33, 0.67]:
        y = cy - oh + oh * 2 * frac
        hw = math.sqrt(max(0, ow**2 * (1 - ((y - cy) / oh)**2)))
        b.append(ln(cx - hw, y, cx + hw, y, stroke="#111111", stroke_width="3"))
    for frac in [0.28, 0.72]:
        x = cx - ow + ow * 2 * frac
        hh = math.sqrt(max(0, oh**2 * (1 - ((x - cx) / ow)**2)))
        b.append(ln(x, cy - hh, x, cy + hh, stroke="#111111", stroke_width="3"))
    b.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{ow:.1f}" ry="{oh:.1f}" fill="none" stroke="#111111" stroke-width="4"/>')
    b.append(f'<ellipse cx="{cx-ow*0.2:.1f}" cy="{cy-oh*0.3:.1f}" rx="{ow*0.14:.1f}" ry="{oh*0.07:.1f}" fill="white" opacity="0.2"/>')
    return wrap_svg("\n".join(b), d)

def gen_cushion():
    """3. CUSHION: Grabado clásico / Vintage etching con tramado y papel marfil."""
    pad = S * 0.13; cr = S * 0.13; w = S - 2 * pad
    x0, y0, x1, y1 = pad, pad, pad + w, pad + w
    path = f"M{x0+cr},{y0} Q{x0},{y0} {x0},{y0+cr} L{x0},{y1-cr} Q{x0},{y1} {x0+cr},{y1} L{x1-cr},{y1} Q{x1},{y1} {x1},{y1-cr} L{x1},{y0+cr} Q{x1},{y0} {x1-cr},{y0} Z"
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#f4f0e6"/>',
         f'<clipPath id="cc"><path d="{path}"/></clipPath>',
         f'<g clip-path="url(#cc)">']
    step = 7
    for i in range(-int(S // step), int(S // step) + 2):
        o = i * step
        b.append(ln(o, 0, o + S, S, stroke="#2a1f0e", stroke_width="0.5", opacity="0.4"))
        b.append(ln(o, 0, o - S, S, stroke="#2a1f0e", stroke_width="0.5", opacity="0.25"))
    b.append('</g>')
    b.append(f'<path d="{path}" fill="none" stroke="#2a1f0e" stroke_width="2.5"/>')
    ip = S * 0.27; wi = S - 2 * ip; cr2 = S * 0.07; xi, yi = ip, ip; xi1, yi1 = ip + wi, ip + wi
    p2 = f"M{xi+cr2},{yi} Q{xi},{yi} {xi},{yi+cr2} L{xi},{yi1-cr2} Q{xi},{yi1} {xi+cr2},{yi1} L{xi1-cr2},{yi1} Q{xi1},{yi1} {xi1},{yi1-cr2} L{xi1},{yi+cr2} Q{xi1},{yi} {xi1-cr2},{yi} Z"
    b.append(f'<path d="{p2}" fill="none" stroke="#2a1f0e" stroke_width="1.2"/>')
    for px, py, ex, ey in [(x0, y0, xi, yi), (x1, y0, xi1, yi), (x0, y1, xi, yi1), (x1, y1, xi1, yi1)]:
        b.append(ln(px, py, ex, ey, stroke="#2a1f0e", stroke_width="1.0"))
    return wrap_svg("\n".join(b))

def gen_pear():
    """4. PEAR: Kawaii pastel — degradado lila/menta con destellos y trazo suave."""
    d = '''<linearGradient id="pg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#b8f0d8"/>
      <stop offset="100%" stop-color="#d8b4fe"/>
    </linearGradient>'''
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#fdf4ff"/>']
    pear = (f"M{cx},{cy+R*1.0} "
            f"C{cx-R*0.72},{cy+R*0.38} {cx-R*0.98},{cy-R*0.22} {cx-R*0.52},{cy-R*0.72} "
            f"A{R*0.58},{R*0.58} 0 1,1 {cx+R*0.52},{cy-R*0.72} "
            f"C{cx+R*0.98},{cy-R*0.22} {cx+R*0.72},{cy+R*0.38} {cx},{cy+R*1.0} Z")
    b.append(f'<path d="{pear}" fill="url(#pg)" stroke="#7c3aed" stroke-width="3.5" stroke-linejoin="round"/>')
    b.append(ln(cx, cy - R * 0.52, cx, cy + R * 1.0, stroke="#7c3aed", stroke_width="1.2", opacity="0.35"))
    b.append(ln(cx - R * 0.48, cy - R * 0.05, cx + R * 0.48, cy - R * 0.05, stroke="#7c3aed", stroke_width="1.2", opacity="0.35"))
    b.append(ln(cx - R * 0.3, cy + R * 0.42, cx + R * 0.3, cy + R * 0.42, stroke="#7c3aed", stroke_width="1.2", opacity="0.35"))
    for sx, sy, ss, sc in [(cx - R * 0.78, cy - R * 0.68, 18, "#a855f7"), (cx + R * 0.82, cy - R * 0.48, 12, "#6d28d9"), (cx + R * 0.62, cy + R * 0.52, 10, "#c4b5fd")]:
        b.append(f'<text x="{sx:.1f}" y="{sy:.1f}" font-size="{ss}" fill="{sc}" text-anchor="middle" dominant-baseline="central" font-family="serif">✦</text>')
    b.append(circ(cx - R * 0.18, cy - R * 0.28, R * 0.055, fill="white", opacity="0.8"))
    return wrap_svg("\n".join(b), d)

def gen_marquise():
    """5. MARQUISE: Art Deco dorado de 1920 sobre fondo negro azabache."""
    gold = "#c9a84c"
    d = '''<linearGradient id="mg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0d060"/>
      <stop offset="50%" stop-color="#c9a84c"/>
      <stop offset="100%" stop-color="#8a6820"/>
    </linearGradient>'''
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#080808"/>']
    for scale, sw in [(1.0, "1.8"), (0.88, "0.7")]:
        sq = [(S * 0.08 * scale + (1 - scale) * cx, cy), (cx, S * 0.08 * scale + (1 - scale) * cy),
              (S * (1 - 0.08 * scale) + (scale - 1) * cx + cx * (1 - scale), cy), (cx, S * (1 - 0.08 * scale) + (scale - 1) * cy + cy * (1 - scale))]
        b.append(poly(sq, fill="none", stroke="url(#mg)", stroke_width=sw))
    marq = (f"M{cx},{cy-R*1.0} C{cx+R*0.8},{cy-R*0.4} {cx+R*0.8},{cy+R*0.4} {cx},{cy+R*1.0} "
            f"C{cx-R*0.8},{cy+R*0.4} {cx-R*0.8},{cy-R*0.4} {cx},{cy-R*1.0} Z")
    b.append(f'<path d="{marq}" fill="none" stroke="url(#mg)" stroke-width="2.5"/>')
    inner = (f"M{cx},{cy-R*0.55} C{cx+R*0.45},{cy-R*0.22} {cx+R*0.45},{cy+R*0.22} {cx},{cy+R*0.55} "
             f"C{cx-R*0.45},{cy+R*0.22} {cx-R*0.45},{cy-R*0.22} {cx},{cy-R*0.55} Z")
    b.append(f'<path d="{inner}" fill="none" stroke="{gold}" stroke_width="1.4"/>')
    b.append(ln(cx - R * 1.0, cy, cx + R * 1.0, cy, stroke=gold, stroke_width="0.7", opacity="0.55"))
    for px, py in [(S * 0.08, cy), (S * 0.92, cy), (cx, S * 0.08), (cx, S * 0.92)]:
        b.append(circ(px, py, 3.2, fill=gold))
    return wrap_svg("\n".join(b), d)

def gen_princess():
    """6. PRINCESS: Technical Blueprint de ingeniería con cuadrícula y cotas."""
    bg = "#1a2d5a"; grid = "#243d72"; ink = "#c8d8f8"
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="{bg}"/>']
    for i in range(0, S + 1, 16):
        b.append(ln(i, 0, i, S, stroke=grid, stroke_width="0.4"))
        b.append(ln(0, i, S, i, stroke=grid, stroke_width="0.4"))
    pad = S * 0.16; w = S - 2 * pad; x0, y0, x1, y1 = pad, pad, pad + w, pad + w
    b.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{w:.1f}" fill="none" stroke="{ink}" stroke-width="2"/>')
    ip = S * 0.28; wi = S - 2 * ip; xi, yi = ip, ip
    b.append(f'<rect x="{xi:.1f}" y="{yi:.1f}" width="{wi:.1f}" height="{wi:.1f}" fill="none" stroke="{ink}" stroke-width="1.5"/>')
    for px, py, ex, ey in [(x0, y0, xi, yi), (x1, y0, xi + wi, yi), (x0, y1, xi, yi + wi), (x1, y1, xi + wi, yi + wi)]:
        b.append(ln(px, py, ex, ey, stroke=ink, stroke_width="0.9"))
    b.append(ln(x0, y0 - 12, x1, y0 - 12, stroke=ink, stroke_width="0.8", stroke_dasharray="4,3"))
    b.append(f'<text x="{cx:.0f}" y="{y0-15:.0f}" fill="{ink}" font-size="9" font-family="monospace" text-anchor="middle">5.00mm</text>')
    b.append(ln(cx, y0, cx, y1, stroke=ink, stroke_width="0.5", opacity="0.4", stroke_dasharray="2,4"))
    b.append(ln(x0, cy, x1, cy, stroke=ink, stroke_width="0.5", opacity="0.4", stroke_dasharray="2,4"))
    return wrap_svg("\n".join(b))

def gen_baguette():
    """7. BAGUETTE: Estilo Bauhaus — colores constructivistas primarios y forma pura."""
    bw = R * 0.68; bh = R * 1.48
    x0, y0, x1, y1 = cx - bw, cy - bh, cx + bw, cy + bh
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#f0ece4"/>',
         f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{bw*2:.1f}" height="{bh*2:.1f}" fill="#1a1a1a"/>']
    for frac in [0.28, 0.56]:
        sw, sh = bw * frac, bh * frac
        b.append(f'<rect x="{cx-sw:.1f}" y="{cy-sh:.1f}" width="{sw*2:.1f}" height="{sh*2:.1f}" fill="none" stroke="#f0ece4" stroke-width="1.4"/>')
    b.append(f'<rect x="{x0:.1f}" y="{cy-4}" width="{bw*2:.1f}" height="8" fill="#cc2200"/>')
    b.append(circ(cx + bw + 16, cy - bh + 16, 9, fill="#f0c000"))
    return wrap_svg("\n".join(b))

def gen_square():
    """8. SQUARE: Pixel Art retro 16-bit arcade gem."""
    px = 14
    grid = [
        "000011110000000",
        "001122221100000",
        "011233332110000",
        "012334443210000",
        "012344544321000",
        "012345554321000",
        "012345554321000",
        "012345554321000",
        "012345554321000",
        "012344544321000",
        "012334443210000",
        "011233332110000",
        "001122221100000",
        "000011110000000",
    ]
    colors = {"0": None, "1": "#3a4f9a", "2": "#5570d0", "3": "#7898f8", "4": "#a0b8ff", "5": "#d0dcff"}
    rows = len(grid); cols = len(grid[0])
    ox = cx - cols * px / 2; oy = cy - rows * px / 2
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#12083a"/>']
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            col = colors.get(ch)
            if col:
                x, y = ox + c * px, oy + r * px
                b.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{px}" height="{px}" fill="{col}"/>')
                b.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{px}" height="{px}" fill="none" stroke="#12083a" stroke-width="1"/>')
    return wrap_svg("\n".join(b))

def gen_emerald():
    """9. EMERALD: Esmeralda profunda de catedral con reflejos y cortes ortogonales."""
    d = '''<linearGradient id="eg1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d5c2e"/>
      <stop offset="50%" stop-color="#1a9c50"/>
      <stop offset="100%" stop-color="#083d1e"/>
    </linearGradient>
    <linearGradient id="eg2" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#12784c"/>
      <stop offset="100%" stop-color="#051508"/>
    </linearGradient>'''
    pad = S * 0.11; ew = S - 2 * pad; eh = ew * 0.72; ex0 = pad; ey0 = cy - eh / 2
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#060606"/>',
         f'<rect x="{ex0:.1f}" y="{ey0:.1f}" width="{ew:.1f}" height="{eh:.1f}" fill="url(#eg1)"/>']
    for s in [0.22, 0.43]:
        sw, sh = ew * (1 - 2 * s), eh * (1 - 2 * s)
        b.append(f'<rect x="{ex0+ew*s:.1f}" y="{ey0+eh*s:.1f}" width="{sw:.1f}" height="{sh:.1f}" fill="url(#eg2)" stroke="#060606" stroke-width="3.2"/>')
    for frac in [0.3, 0.7]:
        x = ex0 + ew * frac
        b.append(ln(x, ey0, x, ey0 + eh, stroke="#060606", stroke_width="3.2"))
    for frac in [0.28, 0.72]:
        y = ey0 + eh * frac
        b.append(ln(ex0, y, ex0 + ew, y, stroke="#060606", stroke_width="3.2"))
    b.append(f'<rect x="{ex0:.1f}" y="{ey0:.1f}" width="{ew:.1f}" height="{eh:.1f}" fill="none" stroke="#060606" stroke-width="4.5"/>')
    b.append(f'<rect x="{ex0+8:.1f}" y="{ey0+8:.1f}" width="{ew*0.14:.1f}" height="{eh*0.07:.1f}" fill="white" opacity="0.18" rx="2"/>')
    return wrap_svg("\n".join(b), d)

def gen_asscher():
    """10. ASSCHER: Geometría sagrada / Mandala concéntrico."""
    gold = "#8b6914"
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#faf6ee"/>']
    for scale in [1.0, 0.78, 0.58, 0.38, 0.2]:
        r = R * scale * math.sqrt(2)
        sq = ring(cx, cy, r, 4, 45)
        sw = "2.2" if scale == 1.0 else "1.2"
        b.append(poly(sq, fill="none", stroke=gold, stroke_width=sw))
    for a in range(0, 360, 45):
        x1, y1 = polar(cx, cy, R * 0.2, a); x2, y2 = polar(cx, cy, R, a)
        b.append(ln(x1, y1, x2, y2, stroke=gold, stroke_width="0.6", opacity="0.45"))
    for scale in [1.0, 0.78, 0.58]:
        r = R * scale * math.sqrt(2)
        for a in range(0, 360, 90):
            px2, py2 = polar(cx, cy, r, a + 45)
            b.append(circ(px2, py2, 3.2, fill=gold))
    for a in range(0, 360, 60):
        px2, py2 = polar(cx, cy, R * 0.13, a)
        b.append(circ(px2, py2, R * 0.1, fill="none", stroke=gold, stroke_width="1"))
    b.append(circ(cx, cy, 4.5, fill=gold))
    return wrap_svg("\n".join(b))

def gen_radiant():
    """11. RADIANT: Cyberpunk neón glow cyan/magenta."""
    d = '''<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="cb"/>
      <feMerge><feMergeNode in="cb"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow2" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="9" result="cb2"/>
      <feMerge><feMergeNode in="cb2"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>'''
    pad = S * 0.14; co = S * 0.07; x0, y0, x1, y1 = pad, pad, S - pad, S - pad
    path = (f"M{x0+co},{y0} L{x1-co},{y0} L{x1},{y0+co} L{x1},{y1-co} "
            f"L{x1-co},{y1} L{x0+co},{y1} L{x0},{y1-co} L{x0},{y0+co} Z")
    pad2 = S * 0.27; co2 = S * 0.04; x0b, y0b, x1b, y1b = pad2, pad2, S - pad2, S - pad2
    path2 = (f"M{x0b+co2},{y0b} L{x1b-co2},{y0b} L{x1b},{y0b+co2} L{x1b},{y1b-co2} "
             f"L{x1b-co2},{y1b} L{x0b+co2},{y1b} L{x0b},{y1b-co2} L{x0b},{y0b+co2} Z")
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#030008"/>',
         f'<path d="{path}" fill="none" stroke="#00ffee" stroke-width="3" filter="url(#glow2)"/>',
         f'<path d="{path}" fill="none" stroke="#00ffee" stroke-width="1.5"/>',
         f'<path d="{path2}" fill="none" stroke="#ff00cc" stroke-width="2" filter="url(#glow)"/>']
    corners = [((x0+co,y0),(x0b+co2,y0b)),((x1-co,y0),(x1b-co2,y0b)),
               ((x0,y0+co),(x0b,y0b+co2)),((x1,y0+co),(x1b,y0b+co2)),
               ((x0+co,y1),(x0b+co2,y1b)),((x1-co,y1),(x1b-co2,y1b)),
               ((x0,y1-co),(x0b,y1b-co2)),((x1,y1-co),(x1b,y1b-co2))]
    for p1, p2 in corners:
        b.append(ln(p1[0], p1[1], p2[0], p2[1], stroke="#8800ff", stroke_width="1", opacity="0.7", filter="url(#glow)"))
    b.append(circ(cx, cy, 5.5, fill="#ff00cc", filter="url(#glow2)"))
    return wrap_svg("\n".join(b), d)

def gen_flanders():
    """12. FLANDERS: Botánico orgánico — talla rodeada de ramas y hojas."""
    green = "#4a7c59"; gem = "#8b5cf6"
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#fafaf5"/>']
    sq = ring(cx, cy, R * 0.5, 4, 45)
    b.append(poly(sq, fill="#e8d8ff", stroke=gem, stroke_width="2.2"))
    sqi = ring(cx, cy, R * 0.3, 4, 45)
    b.append(poly(sqi, fill="none", stroke=gem, stroke_width="1.2"))
    for i in range(4):
        b.append(ln(sq[i][0], sq[i][1], sqi[i][0], sqi[i][1], stroke=gem, stroke_width="0.8", opacity="0.55"))
    for a in range(0, 360, 45):
        bx, by = polar(cx, cy, R * 0.5, a)
        ex, ey = polar(bx, by, R * 0.42, a)
        b.append(ln(bx, by, ex, ey, stroke=green, stroke_width="1.4", stroke_linecap="round"))
        mx, my = (bx + ex) / 2, (by + ey) / 2
        for side in [-1, 1]:
            lx, ly = polar(mx, my, R * 0.12, a + side * 90)
            b.append(f'<ellipse cx="{lx:.1f}" cy="{ly:.1f}" rx="9" ry="4" fill="{green}" opacity="0.65" transform="rotate({a},{lx:.1f},{ly:.1f})"/>')
    return wrap_svg("\n".join(b))

def gen_octagon():
    """13. OCTAGON: Moneda antigua / Medallón en relieve de bronce."""
    d = '''<radialGradient id="br" cx="35%" cy="30%">
      <stop offset="0%" stop-color="#d4956a"/>
      <stop offset="40%" stop-color="#a0632a"/>
      <stop offset="100%" stop-color="#5c3010"/>
    </radialGradient>
    <radialGradient id="br2" cx="40%" cy="35%">
      <stop offset="0%" stop-color="#b07840"/>
      <stop offset="100%" stop-color="#3d1e08"/>
    </radialGradient>'''
    oct_out = ring(cx, cy, R, 8, 22.5)
    oct_in = ring(cx, cy, R * 0.76, 8, 22.5)
    oct_t = ring(cx, cy, R * 0.48, 8, 22.5)
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#1e0e04"/>',
         poly(oct_out, fill="url(#br)", stroke="#1e0e04", stroke_width="3"),
         poly(oct_in, fill="url(#br2)"),
         poly(oct_t, fill="#2e1008", stroke="#c08040", stroke_width="1")]
    for i in range(8):
        p1, p2 = oct_out[i], oct_in[i]
        b.append(ln(p1[0], p1[1], p2[0], p2[1], stroke="#3e1808", stroke_width="1.5"))
    b.append(f'<path d="M{cx-R*0.62},{cy-R*0.28} Q{cx-R*0.18},{cy-R*0.72} {cx+R*0.38},{cy-R*0.52}" fill="none" stroke="#e8b870" stroke_width="2" opacity="0.38" stroke-linecap="round"/>')
    return wrap_svg("\n".join(b), d)

def gen_heart():
    """14. HEART: Estilo moderno ruby flat con facetas limpias."""
    d = '''<linearGradient id="hg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff6b9d"/>
      <stop offset="100%" stop-color="#c0392b"/>
    </linearGradient>'''
    s = R * 1.02; hx, hy = cx, cy + s * 0.08
    heart = (f"M{hx},{hy+s*0.32} "
             f"C{hx-s*1.0},{hy+s*0.08} {hx-s*1.0},{hy-s*0.62} {hx-s*0.5},{hy-s*0.62} "
             f"C{hx-s*0.25},{hy-s*0.62} {hx},{hy-s*0.36} {hx},{hy-s*0.36} "
             f"C{hx},{hy-s*0.36} {hx+s*0.25},{hy-s*0.62} {hx+s*0.5},{hy-s*0.62} "
             f"C{hx+s*1.0},{hy-s*0.62} {hx+s*1.0},{hy+s*0.08} {hx},{hy+s*0.32} Z")
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#fff0f5"/>',
         f'<path d="{heart}" fill="url(#hg)" stroke="#7a0a18" stroke-width="2.5"/>',
         ln(hx, hy - s * 0.36, hx, hy + s * 0.32, stroke="white", stroke_width="1.1", opacity="0.38"),
         ln(hx - s * 0.48, hy, hx + s * 0.48, hy, stroke="white", stroke_width="1.1", opacity="0.38"),
         f'<ellipse cx="{hx-s*0.3:.1f}" cy="{hy-s*0.2:.1f}" rx="{s*0.17:.1f}" ry="{s*0.09:.1f}" fill="white" opacity="0.35" transform="rotate(-30,{hx-s*0.3:.1f},{hy-s*0.2:.1f})"/>']
    return wrap_svg("\n".join(b), d)

def gen_trillion():
    """15. TRILLION: Runas nórdicas ancestrales grabadas."""
    ink = "#d4c5a0"
    oy = R * 0.12
    tri = [polar(cx, cy - oy, R * 1.02, a) for a in [-90, 150, 30]]
    tri2 = [polar(cx, cy - oy, R * 0.55, a) for a in [-90, 150, 30]]
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#1c1410"/>',
         poly(tri, fill="none", stroke=ink, stroke_width="2.8"),
         poly(tri2, fill="none", stroke=ink, stroke_width="1.6")]
    for i in range(3):
        mid = ((tri[i][0] + tri[(i + 1) % 3][0]) / 2, (tri[i][1] + tri[(i + 1) % 3][1]) / 2)
        opp = tri[(i + 2) % 3]
        b.append(ln(mid[0], mid[1], opp[0], opp[1], stroke=ink, stroke_width="1.1", opacity="0.45"))
    for i in range(3):
        a = tri[i]; bb = tri[(i + 1) % 3]
        for frac in [0.28, 0.5, 0.72]:
            mx, my = a[0] + (bb[0] - a[0]) * frac, a[1] + (bb[1] - a[1]) * frac
            dx, dy = -(bb[1] - a[1]), (bb[0] - a[0])
            nrm = math.sqrt(dx * dx + dy * dy) or 1
            dx, dy = dx / nrm * 9, dy / nrm * 9
            b.append(ln(mx - dx, my - dy, mx + dx, my + dy, stroke=ink, stroke_width="1.8"))
    for p in tri:
        b.append(circ(p[0], p[1], 4.8, fill=ink))
    return wrap_svg("\n".join(b))

def gen_trilliant():
    """16. TRILLIANT: Foil holográfico iridiscente prisma."""
    d = '''<linearGradient id="hl1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff0080"/>
      <stop offset="16%" stop-color="#ff8800"/>
      <stop offset="33%" stop-color="#ffff00"/>
      <stop offset="50%" stop-color="#00ff88"/>
      <stop offset="66%" stop-color="#0088ff"/>
      <stop offset="83%" stop-color="#8800ff"/>
      <stop offset="100%" stop-color="#ff0080"/>
    </linearGradient>
    <linearGradient id="hl2" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#00ffee" stop-opacity="0.55"/>
      <stop offset="50%" stop-color="#ff00cc" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#ffee00" stop-opacity="0.55"/>
    </linearGradient>'''
    tri = [polar(cx, cy, R, a) for a in [-90, 150, 30]]
    path = f"M{tri[0][0]:.1f},{tri[0][1]:.1f} L{tri[1][0]:.1f},{tri[1][1]:.1f} L{tri[2][0]:.1f},{tri[2][1]:.1f} Z"
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#f4f0ff"/>',
         f'<path d="{path}" fill="url(#hl1)" opacity="0.82"/>',
         f'<path d="{path}" fill="url(#hl2)"/>']
    mc = (cx, cy + R * 0.1)
    for p in tri:
        b.append(ln(mc[0], mc[1], p[0], p[1], stroke="white", stroke_width="1.8", opacity="0.48"))
    b.append(f'<path d="{path}" fill="none" stroke="white" stroke-width="2"/>')
    for gx2, gy2, gr in [(cx - R * 0.2, cy - R * 0.28, 4), (cx + R * 0.38, cy + 0.02 * R, 2.5), (cx - R * 0.4, cy + R * 0.48, 2)]:
        b.append(circ(gx2, gy2, gr, fill="white", opacity="0.92"))
    return wrap_svg("\n".join(b), d)

def gen_triangle():
    """17. TRIANGLE: Diseño Suizo vanguardista — contraste puro y corte diagonal rojo."""
    oy = R * 0.06
    tri = [polar(cx, cy + oy, R * 0.95, a) for a in [-90, 150, 30]]
    path = f"M{tri[0][0]:.1f},{tri[0][1]:.1f} L{tri[1][0]:.1f},{tri[1][1]:.1f} L{tri[2][0]:.1f},{tri[2][1]:.1f} Z"
    tri2 = [polar(cx, cy + oy, R * 0.44, a) for a in [-90, 150, 30]]
    path2 = f"M{tri2[0][0]:.1f},{tri2[0][1]:.1f} L{tri2[1][0]:.1f},{tri2[1][1]:.1f} L{tri2[2][0]:.1f},{tri2[2][1]:.1f} Z"
    b = [f'<rect width="{S}" height="{S}" rx="28" fill="#f2f2f0"/>',
         f'<path d="{path}" fill="#1a1a1a"/>',
         f'<path d="{path2}" fill="#f2f2f0"/>',
         ln(S * 0.08, tri[1][1], S * 0.92, tri[1][1], stroke="#cc1100", stroke_width="3.5")]
    return wrap_svg("\n".join(b))


GENERATORS = {
    "ROUND":     gen_round,
    "OVAL":      gen_oval,
    "CUSHION":   gen_cushion,
    "PEAR":      gen_pear,
    "MARQUISE":  gen_marquise,
    "PRINCESS":  gen_princess,
    "BAGUETTE":  gen_baguette,
    "SQUARE":    gen_square,
    "EMERALD":   gen_emerald,
    "ASSCHER":   gen_asscher,
    "RADIANT":   gen_radiant,
    "FLANDERS":  gen_flanders,
    "OCTAGON":   gen_octagon,
    "HEART":     gen_heart,
    "TRILLION":  gen_trillion,
    "TRILLIANT": gen_trilliant,
    "TRIANGLE":  gen_triangle,
}

def find_inkscape(override=None):
    candidates = [
        override,
        r"C:\Program Files\Inkscape\bin\inkscape.exe",
        r"C:\Program Files (x86)\Inkscape\bin\inkscape.exe",
    ]
    for p in candidates:
        if p and os.path.isfile(p):
            return p
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inkscape", default=r"C:\Program Files\Inkscape\bin\inkscape.exe")
    parser.add_argument("--size", type=int, default=256)
    args = parser.parse_args()

    inkscape_exe = find_inkscape(args.inkscape)
    print(f"Inkscape: {inkscape_exe}")

    for name, fn in GENERATORS.items():
        svg_path = SVG_DIR / f"{name.lower()}.svg"
        png_path = PNG_DIR / f"{name.lower()}.png"

        # 1. Guardar SVG
        svg_data = fn()
        svg_path.write_text(svg_data, encoding="utf-8")
        print(f"[SVG]  {name:<10} -> {svg_path.name}")

        # 2. Convertir a PNG con Inkscape CLI
        if inkscape_exe:
            cmd = [
                inkscape_exe,
                str(svg_path),
                "--export-type=png",
                f"--export-filename={png_path}",
                f"--export-width={args.size}",
                f"--export-height={args.size}",
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"[PNG]  {name:<10} -> {png_path.name} ({args.size}x{args.size})")
            else:
                print(f"[ERR]  {name:<10} -> {res.stderr[:80]}")

    print("\n¡Proceso completado exitosamente!")

if __name__ == "__main__":
    main()

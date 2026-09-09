"""
gen_round_blueprint.py
Genera el SVG y PNG exacto del Round Brilliant (58 facetas - vista superior).

Topología exacta de la corona (GIA Standard Round Brilliant):
  - 8 Vértices de Tabla (T_i) en radio R_T, ángulos theta_i = i * 45°
  - 8 Vértices de Estrella (S_i) en radio R_S, ángulos beta_i = i * 45° + 22.5°
  - 16 Vértices de Filetín/Girdle (G_k) en radio R_G:
      * G_2i (puntas de cometas/kites) en ángulos theta_i = i * 45°
      * G_{2i+1} (divisores de medias facetas) en ángulos beta_i = i * 45° + 22.5°

Facetas resultantes:
  1. Tabla: 1 octágono central (T_0..T_7)
  2. 8 Facetas Estrella (Star facets): triángulos (T_i, T_{i+1}, S_i)
  3. 8 Facetas Cometa/Bisel (Kite/Bezel facets): cuadriláteros (T_i, S_i, G_{2i}, S_{i-1})
  4. 16 Facetas de Filetín Superior (Upper Girdle Halves):
      - Triángulo izquierdo: (S_i, G_{2i}, G_{2i+1})
      - Triángulo derecho:   (S_i, G_{2i+1}, G_{2i+2})
"""

import math
import subprocess
from pathlib import Path

S = 256
W = 320  # canvas más ancho para preview del visor
cx = W / 2
cy = S / 2
INKSCAPE = r"C:\Program Files\Inkscape\bin\inkscape.exe"

ROOT = Path(__file__).parent.parent
SVG_OUT = ROOT / "assets" / "gems" / "svg" / "round.svg"
PNG_OUT = ROOT / "assets" / "gems" / "png" / "round.png"

# Colores y estilo Blueprint Luxury
BG = "#0D1B3E"        # Navy profundo elegante
STROKE = "#DDE4F5"    # Blanco marfil nítido

# Radios según proporciones clásicas Tolkowsky / GIA
# Diámetro = 100% -> Radio = 1.0
# Diámetro de tabla = ~55% -> Radio de tabla = 0.55 * R_G
# Estrella = ~50% de la distancia entre tabla y girdle -> ~0.775 * R_G
R_G = 106.0           # Radio de girdle en canvas 256x256
R_T = R_G * 0.54      # Radio de tabla
R_S = R_G * 0.77      # Radio de puntas de estrella

# Offset de rotación para alinear con la vista estándar (tabla con lados horizontales/verticales)
# En JewelCraft, a 90° (arriba) hay un vértice del girdle G_2i
ROT_OFFSET = -90.0

def pt(r, deg):
    rad = math.radians(deg + ROT_OFFSET)
    return (cx + r * math.cos(rad), cy + r * math.sin(rad))

# Puntos clave
T = [pt(R_T, i * 45.0) for i in range(8)]
S_pts = [pt(R_S, i * 45.0 + 22.5) for i in range(8)]
G_even = [pt(R_G, i * 45.0) for i in range(8)]          # Alineados con T_i
G_odd  = [pt(R_G, i * 45.0 + 22.5) for i in range(8)]   # Alineados con S_i

lines = []

def add_line(p1, p2, sw="1.0"):
    lines.append(
        f'<line x1="{p1[0]:.2f}" y1="{p1[1]:.2f}" '
        f'x2="{p2[0]:.2f}" y2="{p2[1]:.2f}" '
        f'stroke="{STROKE}" stroke-width="{sw}" stroke-linecap="round"/>'
    )

def add_poly(pts, sw="1.0", fill="none"):
    pts_str = " ".join(f"{p[0]:.2f},{p[1]:.2f}" for p in pts)
    lines.append(
        f'<polygon points="{pts_str}" fill="{fill}" '
        f'stroke="{STROKE}" stroke-width="{sw}" stroke-linejoin="round"/>'
    )

# 1. Fondo contenedor con esquinas redondeadas
body = [f'<rect width="{W}" height="{S}" rx="20" fill="{BG}"/>']

# 2. Círculo exterior (Girdle)
body.append(
    f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R_G:.2f}" '
    f'fill="none" stroke="{STROKE}" stroke-width="1.4"/>'
)

# 3. Octágono de Tabla
add_poly(T, sw="1.3")

# 4. Aristas de Facetas Estrella (Star Facets):
# Conectan T[i] -> S[i] y T[(i+1)%8] -> S[i]
for i in range(8):
    add_line(T[i], S_pts[i], sw="0.95")
    add_line(T[(i + 1) % 8], S_pts[i], sw="0.95")

# 5. Aristas de Facetas Cometa (Kite Facets):
# Conectan S[(i-1)%8] -> G_even[i] y S[i] -> G_even[i]
for i in range(8):
    prev_s = S_pts[(i - 1) % 8]
    curr_s = S_pts[i]
    g_k = G_even[i]
    add_line(prev_s, g_k, sw="0.95")
    add_line(curr_s, g_k, sw="0.95")

# 6. Aristas divisorias de Halves (Upper Girdle):
# Conectan S[i] -> G_odd[i]
for i in range(8):
    add_line(S_pts[i], G_odd[i], sw="0.85")

body.extend(lines)

svg_content = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {S}" width="{W}" height="{S}">\n'
    f'{chr(10).join(body)}\n'
    f'</svg>'
)

SVG_OUT.write_text(svg_content, encoding="utf-8")
print(f"SVG generado: {SVG_OUT}")

# Compilar PNG con Inkscape
res = subprocess.run([
    INKSCAPE,
    str(SVG_OUT),
    "--export-type=png",
    f"--export-filename={PNG_OUT}",
    f"--export-width={W}",
    f"--export-height={S}",
], capture_output=True, text=True)

if res.returncode == 0:
    print(f"PNG generado exitosamente: {PNG_OUT}")
else:
    print(f"Error exportando PNG: {res.stderr}")

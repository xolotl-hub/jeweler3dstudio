"""Renderiza Round Brilliant fiel al motor de gemas en estilo Marquise Art Déco."""

import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).parent.parent
OUTPUT_DIR = ROOT / "assets" / "gems" / "styles" / "marquise"
SVG_OUTPUT = OUTPUT_DIR / "round.svg"
PNG_OUTPUT = OUTPUT_DIR / "round.png"
INKSCAPE = Path(r"C:\Program Files\Inkscape\bin\inkscape.exe")

HEIGHT = 256
WIDTH = round(HEIGHT * 1.30 * 1.30)
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
GIRDLE_RADIUS = 96.0
TABLE_RADIUS = GIRDLE_RADIUS * 0.56
STAR_RADIUS = GIRDLE_RADIUS * 0.77
GOLD = "#C9A84C"
GOLD_MUTED = "#806722"
BACKGROUND = "#0A0A0A"


def point(radius: float, degrees: float) -> tuple[float, float]:
    angle = math.radians(degrees - 90.0)
    return CENTER_X + radius * math.cos(angle), CENTER_Y + radius * math.sin(angle)


def line(start: tuple[float, float], end: tuple[float, float], width: float) -> str:
    return (
        f'<line x1="{start[0]:.2f}" y1="{start[1]:.2f}" '
        f'x2="{end[0]:.2f}" y2="{end[1]:.2f}" '
        f'stroke="{GOLD}" stroke-width="{width}" stroke-linecap="round"/>'
    )


def polygon(points: list[tuple[float, float]], width: float) -> str:
    joined = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polygon points="{joined}" fill="none" stroke="{GOLD}" stroke-width="{width}" stroke-linejoin="round"/>'


def render_svg() -> str:
    # Coincide con create_round_brilliant_mesh(): tabla (8), estrella (8),
    # filetín superior (16), mismas proporciones radiales y desfase angular.
    table = [point(TABLE_RADIUS, i * 45.0 + 22.5) for i in range(8)]
    star = [point(STAR_RADIUS, i * 45.0) for i in range(8)]
    upper_girdle = [point(GIRDLE_RADIUS, i * 22.5) for i in range(16)]

    facets = [polygon(table, 1.35)]
    for i in range(8):
        previous = (i - 1) % 8
        next_star = (i + 1) % 8
        middle = (2 * i + 1) % 16
        center = (2 * i) % 16
        prior = (2 * i - 1) % 16

        # 8 star facets, 8 kite facets y 16 upper-girdle halves del motor.
        facets.append(line(table[previous], star[i], 0.95))
        facets.append(line(table[i], star[i], 0.95))
        facets.append(polygon([table[i], star[next_star], upper_girdle[middle], star[i]], 0.82))
        facets.append(polygon([star[i], upper_girdle[middle], upper_girdle[center]], 0.72))
        facets.append(polygon([star[i], upper_girdle[center], upper_girdle[prior]], 0.72))

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}">',
            f'<rect width="{WIDTH}" height="{HEIGHT}" rx="28" fill="{BACKGROUND}"/>',
            f'<circle cx="{CENTER_X}" cy="{CENTER_Y}" r="{GIRDLE_RADIUS}" fill="none" stroke="{GOLD}" stroke-width="1.5"/>',
            f'<circle cx="{CENTER_X}" cy="{CENTER_Y}" r="{GIRDLE_RADIUS - 4}" fill="none" stroke="{GOLD_MUTED}" stroke-width="0.5"/>',
            *facets,
            "</svg>",
        ]
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SVG_OUTPUT.write_text(render_svg(), encoding="utf-8")
    subprocess.run(
        [
            str(INKSCAPE), str(SVG_OUTPUT), "--export-type=png",
            f"--export-filename={PNG_OUTPUT}", f"--export-width={WIDTH}", f"--export-height={HEIGHT}",
        ],
        check=True,
    )


if __name__ == "__main__":
    main()

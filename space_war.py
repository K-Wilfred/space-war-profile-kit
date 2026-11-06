"""Generate an animated dotted 'space war' SVG for a GitHub profile README.

Usage:  python space_war.py            -> writes war.svg
Install: pip install numpy global-land-mask
Tweak the settings below (marker city, colours, number of ships, seed).
"""
import math, random
import numpy as np
from global_land_mask import globe

# ---------- settings you can change ----------
SEED = 8
W, H = 900, 200
TITLE = "SPACE WAR"
MARKER_LAT, MARKER_LON = 9.9, 76.3        # your city (red pulsing dot on the globe)
EARTH_X, EARTH_Y, EARTH_R = W // 2, 100, 34
FLEET, ENEMIES = 3, 3                      # fighters per side
OUT = "war.svg"
# ---------------------------------------------
random.seed(SEED)

def dots(rows, s, cols):
    return "".join(
        f'<circle cx="{x*s+s/2:.1f}" cy="{y*s+s/2:.1f}" r="{s*0.46:.2f}" fill="{cols[c]}"/>'
        for y, r in enumerate(rows) for x, c in enumerate(r) if c in cols)

SHIP = ["X.........","XX........","XXXX..XX..","XXXXXXXXXX","XXXXXXXXXX","XXXX..XX..","XX........","X........."]
FOE  = ["..........XX","......XXXXXX","X.XXXXXXXXXX","XXXXXXRRXXXX","XXXXXXXXXXXX","X.XXXXXXXXXX","......XXXXXX","..........XX"]
UFO  = ["......XXXXXX......",".....XXXXXXXX.....",".....XX.XX.XX.....","..XXXXXXXXXXXXXX..",
        ".XXXXXXXXXXXXXXXX.","XXXXXXXXXXXXXXXXXX",".XXLXXLXXLXXLXXLX.","...XX........XX..."]

def roam(x0, y0, xr, yr, dur, n=7):
    """Smooth looping flight path through random waypoints."""
    pts = [(x0, y0)] + [(random.randint(*xr), random.randint(*yr)) for _ in range(n - 2)] + [(x0, y0)]
    seg = len(pts) - 1
    vals = ";".join(f"{x} {y}" for x, y in pts)
    kt = ";".join(f"{i/seg:.3f}" for i in range(seg + 1))
    ks = ";".join("0.42 0 0.58 1" for _ in range(seg))
    return (f'<animateTransform attributeName="transform" type="translate" values="{vals}" '
            f'keyTimes="{kt}" calcMode="spline" keySplines="{ks}" dur="{dur}s" repeatCount="indefinite"/>')

def flame(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ff9f0a"><animate attributeName="r" '
            f'values="{r*.6:.1f};{r*1.5:.1f};{r*.6:.1f}" dur=".25s" repeatCount="indefinite"/></circle>')

def fleet_ship(x, y, sc, dur):
    return f'<g>{roam(x, y, (20, 300), (22, H-35), dur)}{flame(-sc, 3.5*sc, sc*.7)}{dots(SHIP, sc, {"X": "#fff"})}</g>'

def enemy_ship(x, y, sc, dur):
    return (f'<g>{roam(x, y, (440, 700), (25, H-35), dur)}{flame(12.5*sc, 4*sc, sc*.8)}'
            f'{dots(FOE, sc, {"X": "#a8a8a8", "R": "#ff3b30"})}</g>')

def laser(color, x0, x1, y, dur, begin):
    segs = "".join(f'<circle cx="{i*5}" cy="0" r="1.6" fill="{color}"/>' for i in range(4))
    return (f'<g opacity="0"><g transform="translate(0 {y})">{segs}</g>'
            f'<animateTransform attributeName="transform" type="translate" values="{x0} 0;{x1} 0;{x1} 0" keyTimes="0;.7;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.69;.7;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></g>')

def explosion(x, y, per, begin):
    a = f'dur="{per}s" begin="{begin}s" repeatCount="indefinite"'
    return (f'<g transform="translate({x} {y})"><circle r="0" fill="#fff"><animate attributeName="r" values="0;0;6;16;0" keyTimes="0;.3;.35;.45;.55" {a}/>'
            f'<animate attributeName="opacity" values="0;0;1;.5;0" keyTimes="0;.3;.35;.45;.55" {a}/></circle>'
            f'<circle r="0" fill="none" stroke="#ff9f0a" stroke-width="2" stroke-dasharray="2 4"><animate attributeName="r" values="0;0;10;24;0" keyTimes="0;.3;.38;.5;.6" {a}/>'
            f'<animate attributeName="opacity" values="0;0;1;.4;0" keyTimes="0;.3;.38;.5;.6" {a}/></circle></g>')

def earth():
    N, step, lat0 = 10, 4.2, math.radians(18)
    kl = math.radians(MARKER_LAT); kn = math.radians(MARKER_LON)
    R = EARTH_R; frames = []
    for f in range(N):
        lon0 = math.radians(f * 360 / N + 20); land, sea = [], []
        for gy in np.arange(-R, R + 1, step):
            for gx in np.arange(-R, R + 1, step):
                x, y = gx / R, -gy / R
                if x*x + y*y > 1: continue
                z = math.sqrt(1 - x*x - y*y)
                lat = math.asin(z*math.sin(lat0) + y*math.cos(lat0))
                lon = lon0 + math.atan2(x, z*math.cos(lat0) - y*math.sin(lat0))
                (land if globe.is_land(math.degrees(lat), (math.degrees(lon)+180) % 360 - 180) else sea).append((gx, gy))
        cosc = math.sin(lat0)*math.sin(kl) + math.cos(lat0)*math.cos(kl)*math.cos(kn-lon0)
        mk = ""
        if cosc > 0.05:
            mx = R*math.cos(kl)*math.sin(kn-lon0)
            my = -R*(math.cos(lat0)*math.sin(kl) - math.sin(lat0)*math.cos(kl)*math.cos(kn-lon0))
            mk = (f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="3" fill="#ff3b30"><animate attributeName="r" '
                  f'values="2.2;4.4;2.2" dur="1.2s" repeatCount="indefinite"/></circle>')
        c = lambda pts, r: "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>' for x, y in pts)
        show = "none;"*f + "inline" + ";none"*(N-1-f)
        frames.append(f'<g display="none"><g fill="#3a3a3a">{c(sea,.9)}</g><g fill="#fff">{c(land,1.9)}</g>{mk}'
                      f'<animate attributeName="display" values="{show}" dur="{N*2.4}s" calcMode="discrete" repeatCount="indefinite"/></g>')
    return f'<g transform="translate({EARTH_X} {EARTH_Y})"><circle r="{R+3}" fill="#000"/>{"".join(frames)}</g>'

stars = "".join(
    f'<circle cx="{random.randint(5,W-5)}" cy="{random.randint(4,H-4)}" r="{random.choice([.8,1,1.2])}" fill="#fff" opacity=".7">'
    f'<animate attributeName="opacity" values=".8;.15;.8" dur="{random.randint(3,6)}s" begin="{random.random()*3:.1f}s" repeatCount="indefinite"/></circle>'
    for _ in range(45))
lanes = [H*0.26, H*0.5, H*0.74]
lasers = "".join(laser("#5aa0ff", 110, 640, y, 2.4, i*.8) for i, y in enumerate(lanes)) + \
         "".join(laser("#ff3b30", 640, 110, y+24, 2.4, .4+i*.8) for i, y in enumerate(lanes))
fleet = "".join(fleet_ship(30, 40 + i*52, 4, 8 + i*1.5) for i in range(FLEET))
foes  = "".join(enemy_ship(560, 45 + i*52, 3, 9 + i*1.7) for i in range(ENEMIES))
mother = (f'<g><animateTransform attributeName="transform" type="translate" values="{W-135} 60;{W-140} 68;{W-135} 60" '
          f'dur="5s" repeatCount="indefinite"/>{dots(UFO, 7, {"X": "#d8d8d8", "L": "#ff3b30"})}</g>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{TITLE}">
<rect width="{W}" height="{H}" fill="#000"/>
{stars}
<text x="{W/2+6}" y="22" text-anchor="middle" font-family="Courier New, monospace" font-size="13" letter-spacing="12" fill="#8a8a8a">{TITLE}</text>
{earth()}
{lasers}
{mother}{foes}{fleet}
{explosion(590, 80, 7, 1.0)}{explosion(560, 150, 9, 4.5)}
</svg>'''
open(OUT, "w").write(svg)
print(f"wrote {OUT} ({len(svg)//1024} KB)")

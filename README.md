# Space War Profile Kit

An animated, dotted **space war** strip for your GitHub profile README, plus a tool that turns any photo into a chunky dithered picture. No design skills needed, just Python.

<p align="center"><img src="./war.svg" alt="Space war example" width="100%" /></p>

Fighters roam the sky, a UFO mothership hovers, lasers fly, explosions pop, and a **spinning dotted Earth** shows a red pulsing dot on your city.

## What's inside

| File | What it does |
| --- | --- |
| `space_war.py` | Generates `war.svg`, the animated strip |
| `dither.py` | Turns a photo into a black and white dithered PNG |
| `war.svg` | Example output |
| `example-dither.png` | Example of the dithered look |

## How to use it

1. Create a public repo named **exactly your GitHub username** with a README. It shows on your profile.
2. Install Python 3, then: `pip install numpy pillow global-land-mask`
3. Open `space_war.py` and edit the settings at the top:
   - `TITLE`: the small text at the top of the strip
   - `MARKER_LAT`, `MARKER_LON`: your city (the red dot on the globe)
   - `FLEET`, `ENEMIES`: ships per side (fewer looks cleaner)
   - `SEED`: any number, changes flight paths and stars
4. Run `python space_war.py`. It writes `war.svg`. Open it in a browser to preview.
5. Optional: `python dither.py photo.jpg me.png 110` makes a dithered picture. Plain backgrounds work best. The last number is the width in dots.
6. Upload `war.svg` (and `me.png`) to your profile repo.
7. Add to your profile `README.md`:

```html
<p align="center"><img src="./war.svg" alt="Space war" width="100%" /></p>
<p align="center"><img src="./me.png" alt="Portrait" width="260" /></p>
```

## Troubleshooting

- **GitHub still shows the old image after an update:** GitHub caches images. Rename the file (for example `war2.svg`), update the README, and hard refresh with Ctrl+Shift+R.
- **Too busy:** lower `FLEET` and `ENEMIES`, or lower `H` for a slimmer strip.

Made by [@K-Wilfred](https://github.com/K-Wilfred).

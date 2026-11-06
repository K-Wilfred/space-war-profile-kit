"""Turn any photo into a chunky black-and-white dithered image (the 'dot pic' look).

Usage:  python dither.py photo.jpg out.png [width_in_dots]
Install: pip install pillow numpy
Tip: use a photo with a plain background; raise/lower width (default 110) for finer/chunkier dots.
"""
import sys
import numpy as np
from PIL import Image, ImageOps

src, out = sys.argv[1], sys.argv[2]
W = int(sys.argv[3]) if len(sys.argv) > 3 else 110
im = ImageOps.autocontrast(Image.open(src).convert("L"))
H = round(W * im.height / im.width)
v = np.array(im.resize((W, H), Image.LANCZOS)) / 255
bayer = np.array([[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],[12,44,4,36,14,46,6,38],[60,28,52,20,62,30,54,22],
                  [3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],[15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]]) / 64
th = np.tile(bayer, (H // 8 + 1, W // 8 + 1))[:H, :W]
Image.fromarray(((v > th) * 255).astype(np.uint8)).resize((W * 4, H * 4), Image.NEAREST).save(out)
print("wrote", out)

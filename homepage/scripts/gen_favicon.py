# Rasterize the project's real logo SVG into favicon + apple-touch-icon
# (issue #639). Requires: pip install resvg-py pillow
import io
import os
from PIL import Image
import resvg_py

SVG = "C:/Software/mine/Workday_Wake/resources/workday-wake.svg"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists(SVG):
    SVG = os.path.join(BASE, "workday-wake.svg")

with open(SVG, "rb") as f:
    svg_bytes = f.read()


def rasterize(size, out):
    png = resvg_py.svg_to_bytes(svg_string=svg_bytes.decode("utf-8"),
                                 width=size, height=size)
    Image.open(io.BytesIO(bytes(png))).convert("RGBA").save(out)


rasterize(16,  os.path.join(BASE, "fav16.png"))
rasterize(32,  os.path.join(BASE, "fav32.png"))
rasterize(48,  os.path.join(BASE, "fav48.png"))
rasterize(180, os.path.join(BASE, "apple-touch-icon.png"))

imgs = [Image.open(os.path.join(BASE, f"fav{s}.png")).convert("RGBA")
        for s in (16, 32, 48)]
imgs[2].save(os.path.join(BASE, "favicon.ico"), format="ICO",
             append_images=[imgs[0], imgs[1]],
             sizes=[(16, 16), (32, 32), (48, 48)])

for s in (16, 32, 48):
    os.remove(os.path.join(BASE, f"fav{s}.png"))

rasterize(640, os.path.join(BASE, "_logo640.png"))
print("favicon.ico + apple-touch-icon.png built from workday-wake.svg via resvg")

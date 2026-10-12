# Generate og-image.png (1200x630) for the Workday Wake homepage, embedding
# the real project logo SVG (rasterized via resvg) plus the site wordmark.
# Requires: pip install resvg-py pillow
import io
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import resvg_py

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1200, 630

BG = (13, 37, 49)         # deep petrol derived from --primary #185776
ACCENT = (37, 166, 215)   # --primary-light #25a6d7
FRAME = (24, 87, 118)     # --primary #185776
CLOCK = (255, 255, 255)
MUTED = (95, 130, 150)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Subtle rounded-corner frame in brand petrol
d.rounded_rectangle([24, 24, W - 24, H - 24], radius=48, outline=FRAME, width=3)

# --- Real logo (left side), soft accent glow behind it ---
svg_path = "C:/Software/mine/Workday_Wake/resources/workday-wake.svg"
if not os.path.exists(svg_path):
    svg_path = os.path.join(BASE, "workday-wake.svg")
with open(svg_path, "rb") as f:
    png = resvg_py.svg_to_bytes(svg_string=f.read().decode("utf-8"), width=440, height=440)
logo = Image.open(io.BytesIO(bytes(png))).convert("RGBA")

glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([90, 95, 530, 535], fill=ACCENT + (70,))
glow = glow.filter(ImageFilter.GaussianBlur(60))
img.paste(glow, (0, 0), glow)
img.paste(logo, (90, 95), logo)

# --- Wordmark (right side) ---
try:
    font_big = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 96)
    font_med = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 34)
    font_small = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 24)
except OSError:
    font_big = font_med = font_small = ImageFont.load_default()

tx = 610
d.text((tx, 215), "Workday Wake", font=font_big, fill=CLOCK)
d.text((tx + 4, 350), "The smart alarm that knows", font=font_med, fill=MUTED)
d.text((tx + 4, 396), "your work schedule", font=font_med, fill=MUTED)
d.text((tx + 4, 520), "free - no ads - no analytics - no location permission", font=font_small, fill=ACCENT)

img.save(os.path.join(BASE, "og-image.png"), optimize=True)
print("og-image.png written:", img.size, "(real logo embedded)")

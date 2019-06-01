import argparse
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import text_fill_image.fill_text.random_fill as f



def fill(text: str, canvas, mask):
    font = ImageFont.truetype("C:/Users/alist/OneDrive/Documents/Memes/cm-unicode-0.7.0/cmunrm.ttf", 600)



    draw = ImageDraw.Draw(canvas)
    draw.text((0, 0), text, (0, 0, 0), font=font)
    draw = ImageDraw.Draw(canvas)


    return canvas, mask



ap = argparse.ArgumentParser()
ap.add_argument("--font_dir", "-fd", help="Paths(s) to font directories", nargs='+')
ap.add_argument("--output_h_cm", type=float)
ap.add_argument("--output_w_cm", type=float)
ap.add_argument("--dpi", default=300, type=int)
args = ap.parse_args()

h_px = int((args.output_h_cm * args.dpi) / 2.54)
w_px = int((args.output_w_cm * args.dpi) / 2.54)


img = Image.new("RGBA", (w_px, h_px), (255, 255, 255, 0))
mask = Image.new("L", (w_px, h_px),(255))
text = "βΛΣ"

img, mask = f.fill(text, img, mask)
img.save("a_test.png")
mask.save("a_mask.png")
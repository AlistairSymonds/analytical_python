import argparse
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import text_fill_image.fill_text.random_fill as f
from pathlib import Path
from fontTools.ttLib import TTFont

def char_in_font(unicode_char, font):
    for cmap in font['cmap'].tables:
        if cmap.isUnicode():
            if ord(unicode_char) in cmap.cmap:
                return True
    return False

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

font_files = []
for font_dir in args.font_dir:
    for ff in Path(font_dir).glob("*.ttf"):
        print(ff)
        has_all_chars = True
        for test_char in text:
            test_font = TTFont(str(ff))
            if(char_in_font(test_char, test_font)) == False:
                has_all_chars= False
            if has_all_chars:
                font_files.append(ff)




font = ImageFont.truetype("C:/Users/alist/OneDrive/Documents/Memes/cm-unicode-0.7.0/cmunrm.ttf", 1200)
img = f.fill(text, (1000,2000), img, font_files, text_iters=50)
img = f.fill(text, (500,1000), img, font_files, text_iters=50)
img = f.fill(text, (250, 500), img, font_files, text_iters=150)
img = f.fill(text, (100,250), img, font_files, text_iters=150)
img = f.fill(text, (50,125), img, font_files, text_iters=150)
img.save("fill_text_out.png")
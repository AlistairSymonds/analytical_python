import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import random

def fill(text: str, canvas, mask):



    for i in range (0,10):
        font_size = random.randrange(400, 600)
        font = ImageFont.truetype("C:/Users/alist/OneDrive/Documents/Memes/cm-unicode-0.7.0/cmunrm.ttf", font_size)

        temp_mask = font.getmask(text)
        temp_canvas = Image.new("RGBA", (1000, 1000), (255, 255, 255, 0))
        text_h, text_y = temp_mask.size
        temp_mask_canvas = Image.new("RGBA", (text_h, text_y),(255,255,255,0))

        temp_mask_draw = ImageDraw.Draw(temp_mask_canvas)
        temp_mask_draw.rectangle([(0, 0), (text_h, text_y)], fill=0)

        temp_canvas_draw = ImageDraw.Draw(temp_canvas)
        temp_canvas_draw.text((0, 0), text, (0, 0, 0), font=font)


        canvas_h, canvas_w = canvas.size
        paste_x = random.randrange(0,canvas_w)
        paste_y = random.randrange(0, canvas_h)

        canvas.paste(temp_canvas,(paste_x,paste_y))





    return canvas, mask
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import random
import numpy as np
import matplotlib.pyplot as plt
def fill(text: str, font_range: (int, int), canvas, font_files, attempts_per_text=5, text_iters=100):

    random.seed(42)
    font_idx = 0
    random.shuffle(font_files)

    for i in range (0,text_iters):
        #text = str(i)
        print("== Pasting number: "+ str(i)+" ==")
        font_size = random.randrange(font_range[0], font_range[1])
        font = ImageFont.truetype(str(font_files[font_idx]), font_size)
        font_idx = font_idx + 1
        if font_idx % len(font_files) == 0:
            font_idx = 0
            random.shuffle(font_files)

        text_mask = font.getmask(text)
        text_w, text_h = text_mask.size
        text_h = int(text_h*1.6)
        temp_canvas = Image.new("RGBA", (text_w, text_h), (255, 255, 255, 0))


        temp_canvas_draw = ImageDraw.Draw(temp_canvas)
        temp_canvas_draw.text((0, 0), text, (0, 0, 0), font=font)
        rotation_amount = random.randrange(0, 359)
        temp_canvas = temp_canvas.rotate(rotation_amount, expand=True)
        text_w, text_h = temp_canvas.size
        canvas_w, canvas_h = canvas.size

        #canvas_w = 4000
        #canvas_h = 4000

        paste_x_max = canvas_w - text_w
        paste_y_max = canvas_h - text_h
        for j in range(0,attempts_per_text):

            if(paste_x_max < 0):
                paste_x_max = 1
            if ( paste_y_max < 0):
                paste_y_max = 1
            paste_x = random.randrange(0, paste_x_max)
            paste_y = random.randrange(0, paste_y_max)
            print("Gonna paste at: " + str(paste_x)+", "+str(paste_y))

            canvas_np = np.array(canvas)
            paste_dest = np.logical_not(canvas_np[paste_y:paste_y+text_h, paste_x:paste_x+text_w,0:3].astype(bool))
            text_bool = np.logical_not(np.array(temp_canvas).astype(bool)[:,:,0:3])
            intersect_points = np.logical_and(paste_dest, text_bool)


            intersect_detected = np.any(np.any(np.any(intersect_points)))
            if intersect_detected:
                print("overlap, attempting again")
            else:
                canvas.paste(temp_canvas,(paste_x,paste_y),temp_canvas)
                break






    return canvas
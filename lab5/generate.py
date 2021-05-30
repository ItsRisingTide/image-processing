from math import ceil

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

# from work_1.binarization.simple_binarization import simple_binarization
# from work_4.generate import FontUtil

SENTENCE = "O MARE CLAUSUM DOS DESCOBRIMENTOS"

def semitone(old_image):
    return (0.3 * old_image[:, :, 0] + 0.59 * old_image[:, :, 1] + 0.11 * old_image[:, :, 2]).astype(np.uint8)

def simple_binarization(old_image, threshold, semitone_needed=True):
    if semitone_needed:
        semi = semitone(old_image)
    else:
        semi = old_image
    new_image = np.zeros(shape=semi.shape)

    new_image[semi > threshold] = 255

    return new_image.astype(np.uint8)

class FontUtil:
    def __init__(self, font_path):
        self.font = TTFont(font_path)
        self.cmap = self.font['cmap']
        self.t = self.cmap.getcmap(3, 1).cmap
        self.s = self.font.getGlyphSet()
        self.units_per_em = self.font['head'].unitsPerEm

    def get_text_width(self, text, point_size):
        total = 0
        for c in text:
            if ord(c) in self.t and self.t[ord(c)] in self.s:
                total += self.s[self.t[ord(c)]].width
            else:
                total += self.s['.notdef'].width
        total = total * float(point_size)/self.units_per_em
        return total



def tt():
    util = FontUtil(font_path="fonts/times_kz.ttf")
    font = ImageFont.truetype("fonts/times_kz.ttf", 40)

    width = util.get_text_width(SENTENCE, 40) + 20

    img = Image.new(mode="RGB", size=(ceil(width), 56), color="white")

    draw = ImageDraw.Draw(img)

    draw.text((10, 2), SENTENCE, (0, 0, 0), font=font)

    Image.fromarray(simple_binarization(np.array(img), 120),
                    'L').save(f"out_sentence_2.png")

tt();
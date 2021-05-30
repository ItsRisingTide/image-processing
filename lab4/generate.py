# from lab1.simple_binarization import simple_binarization
# from lab4.static import KZ_LETTERS
import numpy as np
from math import ceil
from fontTools.ttLib import TTFont
from PIL import Image, ImageFont, ImageDraw

KZ_LETTERS = [
    'A', 'B', 'C', 'D', 'E',
    'F','G', 'H', 'I', 'J', 'K',
    'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X','Y', 'Z'
]

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
    font = ImageFont.truetype("fonts/times_kz.ttf", 52)

    for i, letter in enumerate(KZ_LETTERS):
        width = util.get_text_width(letter, 52)

        img = Image.new(mode="RGB", size=(ceil(width), 52), color="white")

        draw = ImageDraw.Draw(img)

        draw.text((0, 0), letter, (0, 0, 0), font=font)

        Image.fromarray(simple_binarization(np.array(img), 75),
                        'L').save(f"{i+1}.png")

tt()
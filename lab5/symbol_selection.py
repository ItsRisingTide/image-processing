# from work_5.text_selection import calculate_profiles
from PIL import Image
from PIL.ImageOps import invert
import numpy as np


def calculate_profiles(img):
    profile_x = np.sum(img, axis=0)
    profile_y = np.sum(img, axis=1)

    return {
        'x': profile_x,
        'y': profile_y
    }

def get_symbol_boxes(img):
    profiles = calculate_profiles(img)
    borders = []

    i = 0
    while i < profiles['x'].shape[0]:
        current = profiles['x'][i]
        if current != 0:
            x1, x2 = None, None
            x1 = i
            count = 0
            while profiles['x'][i + count] != 0:
                count += 1
            i += count
            x2 = i
            borders.append((x1, x2))
        i += 1

    return borders


def tt():
    img_src = Image.open(f'out_sentence_2.png').convert('L')
    img_src_arr = np.array(img_src)

    img_arr = np.zeros(shape=img_src_arr.shape)
    img_arr[img_src_arr == 0] = 1
    img_arr[img_src_arr == 255] = 0

    for i, (x1, x2) in enumerate(get_symbol_boxes(img_arr)):
        invert(Image.fromarray(img_src_arr[:, x1:x2])).save(
            f"symbols_{i+1}.png")

tt()
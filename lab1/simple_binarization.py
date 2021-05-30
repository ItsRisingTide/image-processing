from PIL import Image, ImageDraw
from lab1.semitone import semitone
import numpy as np


def simple_binarization(old_image, threshold, semitone_needed=True):
    if semitone_needed:
        semi = semitone(old_image)
    else:
        semi = old_image
    new_image = np.zeros(shape=semi.shape)

    new_image[semi > threshold] = 255

    return new_image.astype(np.uint8)


if __name__ == '__main__':
    image_name = 'random_text.jpg'
    method_prefix = 'Simple_binarization'
    img_src = Image.open('pictures_src/' + image_name).convert('RGB')
    img_src_arr = np.array(img_src)

    Image.fromarray(simple_binarization(
        img_src_arr, 128), 'L').show()
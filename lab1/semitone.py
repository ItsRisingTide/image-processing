from PIL import Image
import numpy as np


def semitone(old_image):
    return (0.3 * old_image[:, :, 0] + 0.59 * old_image[:, :, 1] + 0.11 * old_image[:, :, 2]).astype(np.uint8)

img1 = Image.open("cactus1.jpg")
img1Arr = np.array(img1)

Image.fromarray(semitone(img1Arr).astype(np.uint8), 'L').save("cactus_semitone_photoshop.jpg")
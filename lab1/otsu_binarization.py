from PIL import Image
import numpy as np


def semitone(old_image):
    return (0.3 * old_image[:, :, 0] + 0.59 * old_image[:, :, 1] + 0.11 * old_image[:, :, 2]).astype(np.uint8)

def calculate_threshold(image):
    bins = np.arange(image.min() - 1, image.max() + 1)
    hist, base = np.histogram(image, bins=bins, density=True)
    base = base[1:].astype(np.uint8)

    w0_raw = np.cumsum(hist)
    w1_raw = np.ones(shape=w0_raw.shape) - w0_raw
    t_rank = 0
    i_max = 0
    for i, (w0, w1) in enumerate(zip(w0_raw, w1_raw)):
        m0 = np.sum(base[:i] * hist[:i] / w0)
        m1 = np.sum(base[i + 1:] * hist[i + 1:] / w1)
        d0 = np.sum(hist[:i] * (base[:i] - m0)**2)
        d1 = np.sum(hist[i + 1:] * (base[i + 1:] - m1)**2)
        d_all = w0 * d0 + w1 * d1
        d_class = w0 * w1 * (m0 - m1)**2
        if d_all == 0:
            i_max = i
            break
        if d_class / d_all > t_rank:
            t_rank = d_class / d_all
            i_max = i

    return base[i_max]


def Otsu_binarization(old_image, semitone_needed=True):
    if semitone_needed:
        semi = semitone(old_image)
    else:
        semi = old_image

    new_image = np.zeros(shape=semi.shape)

    t = calculate_threshold(semi)

    new_image[semi > t] = 255

    return new_image.astype(np.uint8)

img1 = Image.open("book.jpg").convert('RGB')
img1Arr = np.array(img1)
Image.fromarray(Otsu_binarization(img1Arr), 'L').save("book_otsu.jpg")
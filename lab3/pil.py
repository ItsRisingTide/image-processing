import numpy as np
from PIL import Image

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

def __sharr_operator_helper(img, new_image, x, y, type):
    z = img[y - 3 // 2:y + 3 // 2 + 1,
            x - 3 // 2:x + 3 // 2 + 1]

    if type == 'x':
        new_image[y, x] = (3*z[0, 0] + 10*z[1, 0] + 3*z[2, 0]) - \
                          (3*z[0, 2] + 10*z[1, 2] + 3*z[2, 2])
    elif type == 'y':
        new_image[y, x] = (3*z[0, 0] + 10*z[0, 1] + 3*z[0, 2]) - \
            (3*z[2, 0] + 10*z[2, 1] + 3*z[2, 2])
    elif type == 'xy':
        new_image[y, x] = abs((3*z[0, 0] + 10*z[1, 0] + 3*z[2, 0]) -
                              (3*z[0, 2] + 10*z[1, 2] + 3*z[2, 2])) + \
            abs((3*z[0, 0] + 10*z[0, 1] + 3*z[0, 2]) -
                (3*z[2, 0] + 10*z[2, 1] + 3*z[2, 2]))
    else:
        raise Exception("Unsupported type")


def sharr_operator(img, type):
    semi = semitone(img)
    new_img = np.zeros(shape=semi.shape)

    x, y = 1, 1
    while y < semi.shape[0] - 1:
        if y % 2 == 0:
            while x + 1 < semi.shape[1] - 1:
                __sharr_operator_helper(semi, new_img, x, y, type)
                x += 1
        else:
            while x - 1 > 1:
                __sharr_operator_helper(semi, new_img, x, y, type)
                x -= 1
        y += 1

    new_img = new_img * 255 / new_img.max()

    if type == 'xy':
        return Otsu_binarization(new_img, semitone_needed=False)
    elif type == 'x' or type == 'y':
        return new_img.astype(np.uint8)
    else:
        raise Exception("Unsupported type")

# img1 = Image.open('text1.jpg').convert('RGB')
# img1Arr = np.array(img1)

# Image.fromarray(semitone(img1Arr).astype(np.uint8), 'L').save("text1_semitone.jpg")

img = Image.open('text1_semitone.jpg').convert('RGB')
imgArr = np.array(img)

type = 'y'

imgRes = Image.fromarray(
        sharr_operator(
            img=imgArr,
            type=type
        ),
        'L'
    )
imgRes.save('text1_shar_y.jpg')


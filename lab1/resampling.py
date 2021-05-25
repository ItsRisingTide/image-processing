from PIL import Image
import numpy as np

def NNResampling(old_image, scale):
    width = old_image.shape[1]
    height = old_image.shape[0]

    new_width = round(scale * width)
    new_height = round(scale * height)

    new_image = np.zeros(shape=(new_height, new_width, old_image.shape[2]))

    for x in range(new_width):
        for y in range(new_height):
            src_x = min(
                int(round(float(x) / float(new_width) * float(width))), width - 1)
            src_y = min(
                int(round(float(y) / float(new_height) * float(height))), height - 1)

            new_image[y, x] = old_image[src_y, src_x]

    return new_image

def bilinear_interpolate(im, x, y):
    Ia = im[y0, x0]
    Ib = im[y1, x0]
    Ic = im[y0, x1]
    Id = im[y1, x1]

    wa = (x1-x) * (y1-y)
    wb = (x1-x) * (y-y0)
    wc = (x-x0) * (y1-y)
    wd = (x-x0) * (y-y0)

    return wa*Ia + wb*Ib + wc*Ic + wd*Id


img1 = Image.open("cactus1_resampled_1-4.jpg")
print(img1)
img1Arr = np.array(img1)
newImgArr = NNResampling(img1Arr, 9)

Image.fromarray(newImgArr.astype(np.uint8), 'RGB').save("cactus_twoWays.jpg")
# print(np.shape(img1))

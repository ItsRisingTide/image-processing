import numpy as np
from PIL import Image, ImageChops
from tqdm import tqdm

def median(original: Image.Image, core: list) -> Image.Image:
    width = original.size[0]
    height = original.size[1]
    core = np.array(core)
    # print(core)
    b = len(core)  # размер окна
    pix = np.array(original)
    new_image = np.copy(pix)

    for x in tqdm(range(int(b / 2), width - int(b / 2)), ascii=True, desc="median_filtering"):
        for y in range(int(b / 2), height - int(b / 2)):
            # индексы окна
            x1 = x - int(b / 2) if x - int(b / 2) > 0 else 0
            x2 = x + int(b / 2) if x + int(b / 2) < width - 1 else width - 1
            y1 = y - int(b / 2) if y - int(b / 2) > 0 else 0
            y2 = y + int(b / 2) if y + int(b / 2) < height - 1 else height - 1

            local_window: np.ndarray = pix[y1:y2 + 1, x1:x2 + 1, 0]
            local_window = local_window * core  # окно после умножения на коэф. ядра
            local_window[local_window > 255] = 255
            med = np.median(local_window)
            med = int(med)
            new_image[y, x] = med

    return Image.fromarray(new_image.astype(np.uint8)).convert("RGB")


def add_salt_and_pepper(image : Image.Image, amount: float = 0.005, s_vs_p: float = 0.5) -> Image.Image:
    image = np.array(image)
    row, col, ch = image.shape
    out = np.copy(image)
    # Salt mode
    num_salt = np.ceil(amount * image.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt))
              for i in image.shape]
    out[coords] = 1

    # Pepper mode
    num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper))
              for i in image.shape]
    out[coords] = 0

    return Image.fromarray(out.astype(np.uint8)).convert("L").convert("RGB")

def gauss_noise(image: Image.Image) -> Image.Image:
    image = np.array(image)
    row, col, ch = image.shape
    mean = 0
    var = 0.5
    sigma = var ** 0.9
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(row, col, ch)
    out = image + gauss
    return Image.fromarray(out.astype(np.uint8)).convert("RGB")


hill_core = \
    [[1, 2, 1],
     [2, 4, 2],
     [1, 2, 1]]

depression_core = \
    [[4, 2, 4],
     [3, 1, 3],
     [4, 2, 4]]

print('ffffff')

s_vs_p = 0.5
amount = 0.05

img = Image.open('dasha_otsu.jpg').convert("RGB")
print(np.array(img))
original_with_salt = add_salt_and_pepper(img, amount, s_vs_p)
original_with_salt.save(f"dasha_otsu_salt_{s_vs_p}_{amount}.jpg")

# original_with_salt = Image.open('dasha_otsu_salt_0.5_0.05.jpg').convert("RGB")
median_depression = median(original_with_salt, depression_core)
median_depression.save(f"median_depression_{s_vs_p}_{amount}_dasha_otsu_salt.jpg")

xor_depression = ImageChops.logical_xor(original_with_salt.convert("1"), median_depression.convert("1"))
xor_depression.save(f"xor_depression_{s_vs_p}_{amount}_dasha_otsu_salt.jpg")

median_hill = median(original_with_salt, hill_core)
median_hill.save(f"median_hill_{s_vs_p}_{amount}_dasha_otsu.jpg")

xor_hill = ImageChops.logical_xor(original_with_salt.convert("1"), median_hill.convert("1"))
xor_hill.save(f"xor_hill_{s_vs_p}_{amount}_dasha_otsu.jpg")

xor = ImageChops.logical_xor(median_depression.convert("1"), median_hill.convert("1"))
xor.save(f"xor_hill_depression_{s_vs_p}_{amount}_dasha_otsu.jpg")

### Другие виды изображений

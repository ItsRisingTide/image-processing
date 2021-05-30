from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from PIL.ImageOps import invert


def calculate_profiles(img):
    profile_x = np.sum(img, axis=0)
    profile_y = np.sum(img, axis=1)

    return {
        'x': profile_x,
        'y': profile_y
    }


def show_profile(img, type='x'):
    if type == 'x':
        profile_y = calculate_profiles(img)[type]
        profile_x = np.arange(
            start=1, stop=img.shape[1] + 1).astype(int)

        plt.bar(x=profile_x, height=profile_y, width=0.9)

        plt.ylim(0, img.shape[0])

    elif type == 'y':
        profile_y = calculate_profiles(img)[type]
        profile_x = np.arange(
            start=1, stop=img.shape[0] + 1).astype(int)

        plt.barh(y=profile_x, width=profile_y, height=0.9)

        plt.ylim(52, 0)

    else:
        raise Exception('Unsupported profile')

    plt.xlim(0, img.shape[1])

    plt.show()


def get_text_box(img, h_gap, v_gap):
    profiles = calculate_profiles(img)

    x1, x2, y1, y2 = None, None, None, None
    i = 0
    while i < profiles['x'].shape[0]:
        current = profiles['x'][i]
        if current != 0 and x1 == None:
            x1 = i
        elif current == 0:
            if x1 == None:
                pass
            else:
                count = 0
                while profiles['x'][i + count] == 0:
                    if count == h_gap:
                        x2 = i
                        i = profiles['x'].shape[0]
                        break
                    if i + count >= profiles['x'].shape[0] - 1:
                        x2 = i
                        i = profiles['x'].shape[0]
                        break
                    count += 1
                i += count
                continue
        i += 1
    if x2 == None:
        x2 = i

    i = 0
    while i < profiles['y'].shape[0]:
        current = profiles['y'][i]
        if current != 0 and y1 == None:
            y1 = i
        elif current == 0:
            if y1 == None:
                pass
            else:
                count = 0
                while profiles['y'][i + count] == 0:
                    if count == v_gap:
                        y2 = i
                        count += 1
                        break
                    if i + count >= profiles['y'].shape[0] - 1:
                        y2 = i
                        count += 1
                        break
                    count += 1
                i += count
                continue
        i += 1
    if y2 == None:
        y2 = i

    return (x1, y1), (x2, y2)

def tt():
    img_src = Image.open(f'out_sentence_2.png').convert('L')
    invert(img_src).save("lab5_1_inverted.png")
    img_src_arr = np.array(img_src)

    img_arr = np.zeros(shape=img_src_arr.shape)
    img_arr[img_src_arr == 0] = 1
    img_arr[img_src_arr == 255] = 0

    (x1, y1), (x2, y2) = get_text_box(img_arr, h_gap=17, v_gap=52)

    invert(Image.fromarray(img_src_arr[y1:y2, x1:x2])).save(
        "lab5_1_cutted.png")

    print((x1, x2), (y1, y2))

tt()
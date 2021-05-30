# from lab4.calculate_profiles import get_profiles
from PIL import Image
import numpy as np
import csv

KZ_LETTERS = [
    'A', 'B', 'C', 'D', 'E',
    'F','G', 'H', 'I', 'J', 'K',
    'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X','Y', 'Z'
]

def get_profiles(img):
    return {
        'x': {
            'y': np.sum(img, axis=0),
            'x': np.arange(
                start=1, stop=img.shape[1] + 1).astype(int)
        },
        'y': {
            'y': np.arange(
                start=1, stop=img.shape[0] + 1).astype(int),
            'x': np.sum(img, axis=1)
        }
    }

def first_nonzero(arr, axis, invalid_val=-1):
    mask = arr != 0
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)


def last_nonzero(arr, axis, invalid_val=-1):
    mask = arr != 0
    val = arr.shape[axis] - np.flip(mask, axis=axis).argmax(axis=axis) - 1
    return np.where(mask.any(axis=axis), val, invalid_val)


def calculate_features(img):
    img_b = np.zeros(shape=img.shape)
    img_b[img != 255] = 1

    profiles = get_profiles(img_b)

    img_b = img_b[first_nonzero(profiles['y']['x'], 0): last_nonzero(
        profiles['y']['x'], 0) + 1, first_nonzero(profiles['x']['y'], 0): last_nonzero(profiles['x']['y'], 0) + 1]

    weight = img_b.sum()
    rel_weight = weight / (img_b.shape[0] * img_b.shape[1])

    x_avg = 0
    for x, column in enumerate(img_b.T):
        x_avg += sum((x + 1) * column)
    x_avg = x_avg/weight
    rel_x_avg = (x_avg-1)/(img_b.shape[1]-1)

    y_avg = 0
    for y, row in enumerate(img_b):
        y_avg += sum((y + 1) * row)
    y_avg = y_avg/weight
    rel_y_avg = (y_avg-1)/(img_b.shape[0]-1)

    iner_x = 0
    for y, row in enumerate(img_b):
        iner_x += sum((y + 1 - y_avg)**2 * row)
    rel_iner_x = iner_x/(img_b.shape[0]**2 + img_b.shape[1]**2)

    iner_y = 0
    for x, column in enumerate(img_b.T):
        iner_y += sum((x + 1 - x_avg)**2 * column)
    rel_iner_y = iner_y/(img_b.shape[0]**2 + img_b.shape[1]**2)

    return {
        'weight': weight,
        'rel_weight': rel_weight,
        'center': (x_avg, y_avg),
        'rel_center': (rel_x_avg, rel_y_avg),
        'inertia': (iner_x, iner_y),
        'rel_inertia': (rel_iner_x, rel_iner_y)
    }


def tt():
    method_prefix = 'Image_Features'

    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['letter', 'weight', 'rel_weight', 'center',
                                                     'rel_center', 'inertia', 'rel_inertia'])
        writer.writeheader()

        for i, letter in enumerate(KZ_LETTERS):
            img_src = Image.open(
                f'{i+1}.png').convert('L')
            img_src_arr = np.array(img_src)

            features = calculate_features(img_src_arr)
            features['letter'] = letter

            writer.writerow(features)

tt();
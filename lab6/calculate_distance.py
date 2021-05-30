# from work_5.symbol_selection import get_symbol_boxes
from PIL import Image
# from work_4.calculate_features import calculate_features
import csv
import numpy as np
from math import sqrt

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


def load_features():
    with open('data.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        result = {}
        for row in reader:
            result[row['letter']] = {
                'rel_weight': float(row['rel_weight']),
                'rel_center': tuple(map(float, row['rel_center'][1:len(row['rel_center'])-1].split(', '))),
                'rel_inertia': tuple(map(float, row['rel_inertia'][1:len(row['rel_inertia'])-1].split(', ')))
            }

        return result


def feature_distance(features_1, features_2):
    return sqrt(
        (features_1['rel_weight'] - features_2['rel_weight'])**2 +
        (features_1['rel_center'][0] - features_2['rel_center'][0])**2 +
        (features_1['rel_center'][1] - features_2['rel_center'][1])**2 +
        (features_1['rel_inertia'][0] - features_2['rel_inertia'][0])**2 +
        (features_1['rel_inertia'][1] - features_2['rel_inertia'][1])**2
    )


def calculate_distance(features_global, features_local):
    result = {}
    for letter, features in features_global.items():
        result[letter] = feature_distance(features_local, features)

    _max = max(result.values())

    new_result = {}
    for letter, distance in result.items():
        new_result[letter] = (_max - distance) / _max

    return new_result

def tt():
    img_src = Image.open(f'out_sentence_2.png').convert('L')
    img_src_arr = np.array(img_src)

    img_arr = np.zeros(shape=img_src_arr.shape)
    img_arr[img_src_arr != 255] = 1

    symbols = get_symbol_boxes(img_arr)
    features_global = load_features()

    file = open("out_data_2.txt", "w+")

    check = False
    for i, (left, right) in enumerate(symbols):
        symbol = img_src_arr[:, left:right]

        features_local = calculate_features(symbol)

        grades = calculate_distance(features_global, features_local)

        file.write(
            f"{i+1}: {dict(sorted(grades.items(), key=lambda item: item[1], reverse=True))}\n")

        letter = max(grades, key=grades.get)

        if letter == 'Ь':
            check = True
            continue

        if check:
            if letter == 'І':
                print('Ы', end=' ')
            else:
                print('Ь ', max(grades, key=grades.get), end=' ')
            check = False
            continue

        print(letter, end=' ')
    print()

    file.close()

tt()
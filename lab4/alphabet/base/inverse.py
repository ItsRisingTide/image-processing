from PIL import Image
from PIL.ImageOps import invert

KZ_LETTERS = [
    'A', 'B', 'C', 'D', 'E',
    'F','G', 'H', 'I', 'J', 'K',
    'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X','Y', 'Z'
]

def tt():
    for i, _ in enumerate(KZ_LETTERS):
        img = Image.open(f"{i+1}.png").convert('L')
        img = invert(img)
        img.save(f"inverse_{i+1}.png")

tt()
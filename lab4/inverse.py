from PIL import Image
from PIL.ImageOps import invert
from lab4.static import KZ_LETTERS

if __name__ == '__main__':
    for i, _ in enumerate(KZ_LETTERS):
        img = Image.open(f"work_4/alphabet/base/{i+1}.png").convert('L')
        img = invert(img)
        img.save(f"work_4/alphabet/inverse/{i+1}.png")
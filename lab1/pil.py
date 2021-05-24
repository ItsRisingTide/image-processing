from PIL import Image
import os

for f in os.listdir("."):
    if f.endswith(".jpg"):
        print(f)
img1 = Image.open("dasha.jpg")
img1.save("dasha.png")
print(img1)
# print("ddddd")
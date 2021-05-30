import os

def tt():
    with open('README.md', 'a+') as file:
        for i in sorted(os.listdir("symbols"), key=lambda x: int(x.split('.')[0])):
            file.write(f"![imgOut](symbols_{i}) ")

tt()
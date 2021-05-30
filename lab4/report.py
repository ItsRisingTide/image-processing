import csv

KZ_LETTERS = [
    'A', 'B', 'C', 'D', 'E',
    'F','G', 'H', 'I', 'J', 'K',
    'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X','Y', 'Z'
]


def tt():
    with open('data.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        with open('README.md', 'a+') as file:
            next(reader)
            for (i, letter), row in zip(enumerate(KZ_LETTERS), reader):
                file.write(
                    f"""
### Буква {letter}
<img src="{i+1}.png" width="150"> <img src="profile_x_{i+1}.png" width="300"> <img src="profile_y_{i+1}.png" width="300">
"""
                )

                file.write(
                    f"""
Признаки:
- Вес чёрного = {row[1]}
- Нормированный вес чёрного = {row[2]}
- Центр масс = {row[3]}
- Нормированный центр масс = {row[4]}
- Моменты инерции = {row[5]}
- Нормированные моменты инерции = {row[6]}
"""
                )

tt()
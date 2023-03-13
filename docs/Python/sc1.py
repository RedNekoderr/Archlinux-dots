from math import sqrt

number = 1
for i in range(1, 7):
    number = (1 / sqrt(5)) * ((((1 + sqrt(5)) / 2) ** i) -
                              (((1 - sqrt(5)) / 2) ** i))
    print(number)

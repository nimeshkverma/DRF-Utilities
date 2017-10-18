import math


def positive_ceil(number, places):
    positive_ceiled_number = number
    number = float(number)
    if number == round(number):
        return round(number, places)
    else:
        adjuster = 0.5 / (10**places)
        return round(number + adjuster, places)


def ceil(number):
    return int(math.ceil(number))


def floor(number):
    return int(math.floor(number))

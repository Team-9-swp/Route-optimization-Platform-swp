import math


def round_mathematically(value, decimals=2):
    if decimals == 0:
        return math.floor(value + 0.5)
    factor = 10**decimals
    return math.floor(value * factor + 0.5 * (1 if value >= 0 else -1)) / factor

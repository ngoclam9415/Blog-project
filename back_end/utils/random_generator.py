import random

def generate_random_hexcode():
    hash = random.getrandbits(128)
    hash = "%032x" % hash
    return hash
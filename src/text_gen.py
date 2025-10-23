from lorem_text import lorem
import random as rand


def generate_text():
    return lorem.words(rand.randint(5, 10))

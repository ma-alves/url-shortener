import string
import random

base62_chars = string.digits + string.ascii_letters

def generate_short_code():
    length = random.randint(2, 9)
    return ''.join(random.choice(base62_chars) for _ in range(length))

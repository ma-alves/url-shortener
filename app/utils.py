import string
import random

base62_chars = string.digits + string.ascii_letters


def generate_short_code():
    length = random.randint(2, 9)
    return "".join(random.choice(base62_chars) for _ in range(length))


# Alternativa para criação do short code
# porém o int(uuid4()) é muito longo e pybase62 não encoda

# import base62
# import uuid


# def generate_short_code(id_url):
#     return base62.encode(id_url)

# def decode_short_code(code: str):
#     return base62.decode(code)

# uid = int(uuid.uuid4())
# print(uid)
# print(generate_short_code(uid))

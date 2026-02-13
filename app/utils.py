# antiga implementação, incoerente com a proposta mas útil para outros casos

# import random
# import string

# base62_chars = string.digits + string.ascii_letters

# def generate_short_code():
#     length = random.randint(2, 9)
#     return "".join(random.choice(base62_chars) for _ in range(length))

from uuid import UUID
import base62

def generate_short_code(url_uuid: UUID):
    uuid_to_int = int(url_uuid)
    short_code = base62.encode(uuid_to_int)
    return short_code[:7]

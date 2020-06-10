from random import choices
from string import ascii_uppercase, digits


def generate_id(length):
    return "".join(choices(ascii_uppercase + digits, k=length))

from random import sample
from time import sleep

from .constants import ASCII_LETTERS_DIGITS, AUTO_SHORT_LENGTH
from .models import URLMap


def check_custom_id(custom_id):
    for symbol in custom_id:
        if symbol not in ASCII_LETTERS_DIGITS:
            return False
    return True


def get_unique_short_id():
    while True:
        for _ in range(5):
            short = ''.join(sample(ASCII_LETTERS_DIGITS, AUTO_SHORT_LENGTH))
            if URLMap.query.filter_by(short=short).first() is None:
                return short
        sleep(1)

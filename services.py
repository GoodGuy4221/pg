from collections import Counter
from timeit import timeit
import random
import string

CHARS = f'{string.digits}{string.ascii_letters}{string.punctuation}'


def get_random_string(length=12):
    list_chars = [random.choice(CHARS) for _ in range(length)]
    return ''.join(list_chars)


def character_count_converter_1(string: str) -> str:
    if not isinstance(string, str):
        raise ValueError('Получена не строка!')
    cnt = Counter(string)
    return ''.join(f'{k}{v}' for k, v in cnt.items())


def character_count_converter_2(string: str) -> str:
    if not isinstance(string, str):
        raise ValueError('Получена не строка!')
    count_chars = {}
    for char in string:
        if char in count_chars:
            count_chars[char] += 1
        else:
            count_chars[char] = 1
    return ''.join(f'{k}{v}' for k, v in count_chars.items())


def character_count_converter_3(string: str) -> str:
    if not isinstance(string, str):
        raise ValueError('Получена не строка!')
    count_chars = {}
    for char in string:
        if char in string:
            count_chars[char] = string.count(char)
    return ''.join(f'char: {k} count: {v} ' for k, v in count_chars.items())


if __name__ == '__main__':
    print(
        timeit(stmt='character_count_converter_1(s)', setup='s = get_random_string(1200)', globals=globals(),
               number=1000))

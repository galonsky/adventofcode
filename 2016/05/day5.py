import hashlib
from typing import List, Optional


def hash(value: str) -> str:
    m = hashlib.md5()
    m.update(value.encode('utf-8'))
    return m.hexdigest()


def find_password(door_id: str) -> str:
    password = ''
    i = 0
    while len(password) < 8:
        value = door_id + str(i)
        hashed = hash(value)
        if hashed.startswith('00000'):
            password += hashed[5]
        i += 1
    return password


def find_password_v2(door_id: str) -> str:
    password: List[Optional[str]] = [None] * 8
    i = 0
    while any((v is None for v in password)):
        value = door_id + str(i)
        hashed = hash(value)
        if hashed.startswith('00000'):
            index = int(hashed[5], 16)
            char = hashed[6]
            if index < 0 or index >= 8 or password[index] is not None:
                pass
            else:
                password[index] = char
        i += 1
    return ''.join(password)


if __name__ == '__main__':
    print(find_password_v2('uqwqemis'))

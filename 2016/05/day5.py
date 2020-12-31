import hashlib


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


if __name__ == '__main__':
    print(find_password('uqwqemis'))

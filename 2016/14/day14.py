import hashlib
from typing import Optional


def generate_hash(salt: str, index: int) -> str:
    corpus = salt + str(index)
    return hashlib.md5(corpus.encode("utf-8")).hexdigest()


def find_repetition(string: str, num: int, ch: str = None) -> Optional[str]:
    if ch:
        return ch if ch * num in string else None
    for i in range(len(string) - num + 1):
        substr = string[i:i+num]
        if len(set(substr)) == 1:
            return substr[0]
    return None


def find_index_for_keys(salt: str, num_keys: int = 64) -> int:
    i = 0
    keys = 0
    while keys < num_keys:
        hsh = generate_hash(salt, i)
        repeated = find_repetition(hsh, 3)
        if repeated and find_quintuple(i, repeated, salt):
            keys += 1
        i += 1
    return i - 1


def find_quintuple(i: int, ch: str, salt: str) -> bool:
    for j in range(i + 1, i + 1 + 1000):
        hsh2 = generate_hash(salt, j)
        if find_repetition(hsh2, 5, ch):
            return True
    return False


if __name__ == "__main__":
    # print(generate_hash("abc", 18))
    print(find_index_for_keys("abc"))

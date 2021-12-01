import hashlib
from functools import partial
from typing import Optional, Callable


def generate_hash(salt: str, index: int) -> str:
    corpus = salt + str(index)
    return hashlib.md5(corpus.encode("utf-8")).hexdigest()


class StretchedHash:
    def __init__(self, salt: str):
        self.salt = salt
        self.cache: dict[int, str] = {}

    def generate_stretched_hash(self, index: int) -> str:
        if index in self.cache:
            return self.cache[index]
        corpus = self.salt + str(index)
        for _ in range(2017):
            corpus = hashlib.md5(corpus.encode("utf-8")).hexdigest()
        self.cache[index] = corpus
        return corpus


def find_repetition(string: str, num: int, ch: str = None) -> Optional[str]:
    if ch:
        return ch if ch * num in string else None
    for i in range(len(string) - num + 1):
        substr = string[i:i+num]
        if len(set(substr)) == 1:
            return substr[0]
    return None


def find_index_for_keys(hash_fn: Callable[[int], str], num_keys: int = 64) -> int:
    i = 0
    keys = 0
    while keys < num_keys:
        hsh = hash_fn(i)
        repeated = find_repetition(hsh, 3)
        if repeated and find_quintuple(i, repeated, hash_fn):
            keys += 1
        i += 1
    return i - 1


def find_quintuple(i: int, ch: str, hash_fn: Callable[[int], str]) -> bool:
    for j in range(i + 1, i + 1 + 1000):
        hsh2 = hash_fn(j)
        if find_repetition(hsh2, 5, ch):
            return True
    return False


if __name__ == "__main__":
    # print(generate_hash("abc", 18))
    # print(find_index_for_keys(partial(generate_hash, "abc")))
    s_hash = StretchedHash("yjdafjpo")
    print(find_index_for_keys(s_hash.generate_stretched_hash))
    # print(s_hash.generate_stretched_hash(0))

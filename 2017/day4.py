def num_passphrases():
    passphrases = 0
    with open('day4_input.txt') as file:
        for line in file:
            words = line.rstrip('\n').split()
            if len(words) == len(set(words)):
                passphrases += 1
    return passphrases


def num_passphrases_anagrams():
    passphrases = 0
    with open('day4_input.txt') as file:
        for line in file:
            words = line.rstrip('\n').split()
            if len(words) == len(set([''.join(sorted(word)) for word in words])):
                passphrases += 1
    return passphrases


print(num_passphrases_anagrams())

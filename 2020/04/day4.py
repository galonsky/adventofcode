from typing import List


def get_passports(filename: str) -> List[dict]:
    with open(filename, 'r') as file:
        content = file.read()
        pass_dicts = []
        passports = content.split('\n\n')
        for passport in passports:
            pairs = passport.split()
            pass_dict = {}
            for pair in pairs:
                sides = pair.split(':')
                pass_dict[sides[0]] = sides[1]
            pass_dicts.append(pass_dict)
        return pass_dicts


if __name__ == '__main__':
    passports = get_passports('input.txt')
    required_keys = {
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid',
    }
    count = 0
    for passport in passports:
        if required_keys <= passport.keys():
            count += 1
    print(count)